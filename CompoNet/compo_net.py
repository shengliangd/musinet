# 目前模仿char-rnn

import tensorflow as tf
import numpy as np
from tensorflow.contrib import rnn
from tensorflow.contrib import legacy_seq2seq

from sys import stderr


class Config:
    def __init__(self, num_layers=2, rnn_size=64,
                 seq_length=32, num_channels=4,
                 training=True, batch_size=4,
                 grad_clip=5,
                 save_path='save/save',
                 log_path='log/log',
                 output_dir='output/',
                 data_path='data/train.pkl',
                 input_keep_prob=1,
                 output_keep_prob=1,
                 learning_rate=0.001,
                 decay_rate=0.97,
                 restore=True):
        self.num_layers = num_layers
        self.rnn_size = rnn_size
        self.seq_length = seq_length
        self.num_channels = num_channels
        self.training = training
        self.batch_size = batch_size
        self.grad_clip = grad_clip
        self.save_path = save_path
        self.log_path = log_path
        self.restore = restore
        self.output_dir = output_dir
        self.data_path = data_path
        self.input_keep_prob = input_keep_prob
        self.output_keep_prob = output_keep_prob
        self.learning_rate = learning_rate
        self.decay_rate = decay_rate  # not in use now
        if not training:
            self.batch_size = 1
            self.seq_length = 1
            self.restore = True


class Model:
    # build the computing graph
    def __init__(self, config=Config()):
        self.config = config
        # input placeholder
        self.inputs = tf.placeholder(tf.float32,
                                     [config.batch_size,
                                      config.seq_length,
                                      config.num_channels])

        # create rnn cells and stack them together
        cells = []
        for _ in range(config.num_layers):
            cell = rnn.BasicLSTMCell(config.rnn_size)  # don't dropout for now
            cells.append(cell)
        self.cell = rnn.MultiRNNCell(cells, state_is_tuple=True)

        # process input for rnn, along with output converter
        ''' don't convert input for now
        w_input = tf.Variable(tf.truncated_normal([config.num_channels, config.rnn_size], stddev=0.1),
                              trainable=True)
        b_input = tf.Variable(tf.truncated_normal([config.rnn_size], stddev=0.1),
                              trainable=True)
        '''
        w_output = tf.Variable(tf.truncated_normal([config.rnn_size, config.num_channels],
                                                   stddev=0.1),
                               trainable=True)
        b_output = tf.Variable(tf.truncated_normal([config.num_channels], stddev=0.1),
                               trainable=True)

        inputs = tf.split(self.inputs, config.seq_length, 1)  # [batches, 1, num_channels]*seq_length
        inputs = [tf.squeeze(_input, [1]) for _input in inputs]  # [batches, num_channels]*seq_length
        cell_inputs = inputs

        def loop(prev, _):
            return tf.matmul(prev, w_output)+b_output
#            return prev

        # state and output
        self.init_state = self.cell.zero_state(config.batch_size, tf.float32)
        cell_outputs, self.final_state = legacy_seq2seq.rnn_decoder(cell_inputs,
                                                                    self.init_state,
                                                                    self.cell,
                                                                    loop_function=None if config.training else loop)
        # self.cell_output: [batches, rnn_size]*seq_length
        # now need to convert cell_output to proper vector
        self.outputs = [(tf.matmul(_output, w_output)+b_output) for _output in cell_outputs]  #[batches, channels]*seq_length

        # loss
        loss = 0
        if config.training:
            for i in range(config.seq_length-1):
                for j in range(config.batch_size):
                    loss += tf.square(inputs[i+1][j] - self.outputs[i][j])
            self.cost = tf.reduce_sum(loss) / (config.seq_length-1) / config.batch_size / config.num_channels

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

        for note in init_seq[:-1]:
            x = np.zeros((1, 1, self.config.num_channels))
            x[0][0] = note
            feed = {self.inputs: x, self.init_state: state}
            [state] = sess.run([self.final_state], feed)

        ret = init_seq
        note = init_seq[-1]
        for _ in range(final_len-len(init_seq)):
            x = np.zeros((1, 1, self.config.num_channels))
            x[0, 0] = note
            feed = {self.inputs: x, self.init_state: state}
            [outputs, state] = sess.run([self.outputs, self.final_state], feed)
            ret += outputs[0].tolist()
            note = outputs[0].tolist()[0]
        return ret

    def save(self, sess):
        self.saver.save(sess, self.config.save_path)

    def restore(self, sess):
        self.saver.restore(sess, self.config.save_path)
