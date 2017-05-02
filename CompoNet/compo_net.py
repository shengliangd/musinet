import tensorflow as tf
import numpy as np
from tensorflow.contrib import rnn
from tensorflow.contrib import legacy_seq2seq
import os.path
import random


class Config:
    def __init__(self, num_layers=2, rnn_size=128,
                 seq_length=32,
                 training=True, batch_size=4,
                 grad_clip=5,
                 save_dir='save/',
                 log_dir='log/',
                 output_dir='output/',
                 data_path='data/train.pkl',
                 learning_rate=0.001,
                 input_keep_prob=1,
                 output_keep_prob=1,
                 encoders=None,
                 vec_lengths=None,

                 restore=True):
        self.num_layers = num_layers
        self.rnn_size = rnn_size
        self.seq_length = seq_length
        self.training = training
        self.batch_size = batch_size
        self.grad_clip = grad_clip
        self.save_dir = save_dir
        self.log_dir = log_dir
        self.restore = restore
        self.output_dir = output_dir
        self.data_path = data_path
        self.learning_rate = learning_rate
        self.encoders = encoders
        self.vec_lengths = vec_lengths
        self.input_keep_prob = input_keep_prob
        self.output_keep_prob = output_keep_prob

        if not training:
            self.batch_size = 1
            self.seq_length = 1
            self.restore = True


def _sample(weights):
    threshold_high = 1.2
    threshold_low = 1/len(weights)

    total = 0
    for i in range(len(weights)):
        if threshold_high > weights[i] and weights[i] > threshold_low:
            total += weights[i]

    rand = random.random()*total
    summation = 0
    for i in range(len(weights)):
        if threshold_high > weights[i] and weights[i] > threshold_low:
            summation += weights[i]
            if summation >= rand:
                return i

    return len(weights)-1


class Model:
    # build the computing graph
    def __init__(self, config=Config()):
        self.config = config
        self.vec_len = sum(config.vec_lengths)

        # input placeholder
        with tf.name_scope('inputs'):
            self.inputs = tf.placeholder(tf.float32,
                                         [config.batch_size,
                                          config.seq_length,
                                          self.vec_len])

            inputs = tf.split(self.inputs, config.seq_length, 1)  # [batch_size, 1, vec_len]*seq_length
            inputs = [tf.squeeze(_input, [1]) for _input in inputs]  # [batch_size, vec_len]*seq_length

        with tf.name_scope('targets'):
            self.targets = tf.placeholder(tf.float32,
                                          [config.batch_size,
                                           config.seq_length,
                                           self.vec_len])
            targets = tf.split(self.targets, config.seq_length, 1)
            targets = [tf.squeeze(_target, [1]) for _target in targets]

        # create rnn cells and stack them together
        with tf.name_scope('lstm_cells'):
            cells = []
            for _ in range(config.num_layers):
                cell = rnn.BasicLSTMCell(config.rnn_size)  # don't dropout for now
                cell = rnn.DropoutWrapper(cell,
                                          config.input_keep_prob,
                                          config.output_keep_prob)
                cells.append(cell)
            self.cell = rnn.MultiRNNCell(cells, state_is_tuple=True)

            w_output = tf.Variable(tf.truncated_normal([config.rnn_size, self.vec_len],
                                                       stddev=1/(config.rnn_size**0.5)),
                                   trainable=True)
            b_output = tf.Variable(tf.truncated_normal([self.vec_len], stddev=1),
                                   trainable=True)

            # state and output
            self.init_state = self.cell.zero_state(config.batch_size, tf.float32)
            outputs, self.final_state = legacy_seq2seq.rnn_decoder(inputs,
                                                                   self.init_state,
                                                                   self.cell,
                                                                   loop_function=None)

            # [batch_size, rnn_size]*seq_length -> [batch_size, vec_length]*seq_length
            outputs = [tf.matmul(_output, w_output)+b_output for _output in outputs]

        with tf.name_scope('outputs'):
            self.probs = []
            for elem in outputs:
                slices = []
                for i in range(4):
                    _slice = tf.slice(elem, [0, sum(config.vec_lengths[:i])], [-1, config.vec_lengths[i]])
                    _slice = tf.nn.softmax(_slice)
                    slices.append(_slice)
                self.probs.append(tf.concat(slices, 1))

        if config.training:
            with tf.name_scope('loss'):
                loss = 0

                # loss will be weighted
                '''
                weights = tf.reshape(tf.constant([[0.333]*config.vec_lengths[0] +
                                               [0.333]*config.vec_lengths[1] +
                                               [1]*config.vec_lengths[2] +
                                               [1]*config.vec_lengths[3]]), [-1, 1])
                '''
                for i in range(config.seq_length):
                    for j in range(config.batch_size):
                        loss += targets[i][j]*tf.log(self.probs[i][j])
                    self.cost = -tf.reduce_sum(loss) / config.seq_length / config.batch_size / self.vec_len

            # optimizer
            with tf.name_scope('optimizer'):
                self.learning_rate = tf.placeholder(tf.float32, [])
                tvars = tf.trainable_variables()
                grads, _ = tf.clip_by_global_norm(tf.gradients(self.cost, tvars),
                                                  config.grad_clip)
                optimizer = tf.train.AdamOptimizer(learning_rate= self.learning_rate)
                self.train = optimizer.apply_gradients(zip(grads, tvars))

        # saver
        self.saver = tf.train.Saver(tf.global_variables())

    def sample(self, sess, init_seq, final_len=1024):
        state = sess.run(self.cell.zero_state(1, tf.float32))

        ret = []
        for note in init_seq[:-1]:
            x = np.zeros((1, 1, self.vec_len))
            x[0][0] = note
            feed = {self.inputs: x, self.init_state: state}
            [state] = sess.run([self.final_state], feed)

            indices = []
            output = x[0][0].tolist()
            for i in range(4):
                tmp = output[sum(self.config.vec_lengths[:i]):
                             sum(self.config.vec_lengths[:i+1])]
                indices.append(tmp.index(max(tmp)))
            note = [self.config.encoders[i].active_features_[indices[i]] for i in range(4)]
            ret.append(note)

        note = init_seq[-1]
        for _ in range(final_len-len(init_seq)):
            x = np.zeros((1, 1, self.vec_len))
            x[0, 0] = note
            feed = {self.inputs: x, self.init_state: state}
            [outputs, state] = sess.run([self.probs, self.final_state], feed)
            output = outputs[0].tolist()[0]

            indices = []
            for i in range(4):
                tmp = output[sum(self.config.vec_lengths[:i]):
                             sum(self.config.vec_lengths[:i+1])]
                indices.append(_sample(tmp))
            note = [self.config.encoders[i].active_features_[indices[i]] for i in range(4)]
            ret.append(note)

            note = [self.config.encoders[i].transform(note[i]).toarray().tolist()[0]
                    for i in range(4)]
            note = sum(note, [])

        return ret

    def save(self, sess):
        try:
            pass
        finally:
            print('saving model')
            self.saver.save(sess, os.path.join(self.config.save_dir, 'compo_net.sav'))
            print('saved')

    def restore(self, sess):
        self.saver.restore(sess, os.path.join(self.config.save_dir, 'compo_net.sav'))
