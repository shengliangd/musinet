import tensorflow as tf
import numpy as np
from tensorflow.contrib import rnn
from tensorflow.contrib import legacy_seq2seq
import os.path
import random


class Config:
    def __init__(self, num_layers=3, rnn_size=128,
                 seq_length=256,
                 training=True, batch_size=3,
                 grad_clip=5,
                 save_path='save/',
                 log_path='log/',
                 output_dir='output/',
                 data_path='data/train.pkl',
                 learning_rate=0.02,
                 decay_rate=0.97,
                 encoders=None,
                 vec_lengths=None,
                 restore=True):
        self.num_layers = num_layers
        self.rnn_size = rnn_size
        self.seq_length = seq_length
        self.training = training
        self.batch_size = batch_size
        self.grad_clip = grad_clip
        self.save_path = save_path
        self.log_path = log_path
        self.restore = restore
        self.output_dir = output_dir
        self.data_path = data_path
        self.learning_rate = learning_rate
        self.decay_rate = decay_rate  # not in use now
        self.encoders = encoders
        self.vec_lengths = vec_lengths

        if not training:
            self.batch_size = 1
            self.seq_length = 1
            self.restore = True


def _sample(weights):
    summation = 0
    rand = random.random()
    threshold = 5/len(weights)
    for i in range(len(weights)):
        summation += weights[i]
        if weights[i] > threshold and summation >= rand:
            return i

    return len(weights)-1


class Model:
    # build the computing graph
    def __init__(self, config=Config()):
        assert config.vec_lengths is not None, "invalid config"

        self.config = config
        self.vec_len = sum(config.vec_lengths)
        # input placeholder
        self.inputs = tf.placeholder(tf.float32,
                                     [config.batch_size,
                                      config.seq_length,
                                      self.vec_len])
        self.targets = tf.placeholder(tf.float32,
                                      [config.batch_size,
                                       config.seq_length,
                                       self.vec_len])

        # create rnn cells and stack them together
        cells = []
        for _ in range(config.num_layers):
            cell = rnn.BasicLSTMCell(config.rnn_size)  # don't dropout for now
            cells.append(cell)
        self.cell = rnn.MultiRNNCell(cells, state_is_tuple=True)

        # process input for rnn, along with output converter
        w_output = tf.Variable(tf.truncated_normal([config.rnn_size, self.vec_len],
                                                   stddev=1/(config.rnn_size**0.5)),
                               trainable=True)
        b_output = tf.Variable(tf.truncated_normal([self.vec_len], stddev=1),
                               trainable=True)

        inputs = tf.split(self.inputs, config.seq_length, 1)  # [batch_size, 1, vec_len]*seq_length
        inputs = [tf.squeeze(_input, [1]) for _input in inputs]  # [batch_size, vec_len]*seq_length
        targets = tf.split(self.targets, config.seq_length, 1)
        targets = [tf.squeeze(_target, [1]) for _target in targets]

        # ???
        def loop(prev, _):
            return prev

        # state and output
        self.init_state = self.cell.zero_state(config.batch_size, tf.float32)
        outputs, self.final_state = legacy_seq2seq.rnn_decoder(inputs,
                                                               self.init_state,
                                                               self.cell,
                                                               loop_function=None if config.training else loop)

        # [batch_size, rnn_size]*seq_length -> [batch_size, vec_length]*seq_length
        outputs = [tf.matmul(_output, w_output)+b_output for _output in outputs]
        self.probs = []
        for elem in outputs:
            slices = []
            for i in range(4):
                _slice = tf.slice(elem, [0, sum(config.vec_lengths[:i])], [-1, config.vec_lengths[i]])
                _slice = tf.nn.softmax(_slice)
                slices.append(_slice)
            self.probs.append(tf.concat(slices, 1))

        if config.training:
            loss = 0
            if config.training:
                for i in range(config.seq_length):
                        loss += targets[i]*tf.log(self.probs[i])
                self.cost = -tf.reduce_sum(loss) / config.seq_length / config.batch_size / self.vec_len

            # optimizer
            tvars = tf.trainable_variables()
            grads, _ = tf.clip_by_global_norm(tf.gradients(self.cost, tvars),
                                              config.grad_clip)
            optimizer = tf.train.AdamOptimizer(learning_rate=config.learning_rate)
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
            self.saver.save(sess, os.path.join(self.config.save_path, 'compo_net.sav'))
            print('saved')

    def restore(self, sess):
        self.saver.restore(sess, os.path.join(self.config.save_path, 'compo_net.sav'))
