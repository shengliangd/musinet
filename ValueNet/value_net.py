import tensorflow as tf
import config


class Model:
    def __init__(self):
        # NHWC format
        self.inputs = tf.placeholder(tf.float32,
                                     [None, config.seq_length, config.num_channels])
        self.targets = tf.placeholder(tf.float32,
                                      [None, 1])

        # convolution layer
        conv1_filter_width = 8
        conv1_num_filters = 8
        w_conv1 = tf.Variable(tf.truncated_normal([conv1_filter_width,
                                                   int(self.inputs.shape[2]),
                                                   conv1_num_filters],
                                                  stddev=0.1))
        b_conv1 = tf.Variable(tf.truncated_normal([conv1_num_filters], stddev=0.1))
        conv1 = tf.nn.relu(tf.nn.conv1d(self.inputs, w_conv1,
                                        stride=1, padding='SAME')
                           + b_conv1)

        # pooling layer
        pool2_width = 4
        pool2 = tf.nn.max_pool(tf.reshape(conv1,
                                          [-1, 1,
                                           int(conv1.shape[1]),
                                           int(conv1.shape[2])]),
                               [1, 1, pool2_width, 1],
                               [1, 1, pool2_width, 1],
                               padding='VALID')
        pool2 = tf.squeeze(pool2, 1)

        # convolution layer
        conv3_filter_width = 4
        conv3_num_filters = 16
        w_conv3 = tf.Variable(tf.truncated_normal([conv3_filter_width,
                                                   int(pool2.shape[2]),
                                                   conv3_num_filters],
                                                  stddev=0.1))
        b_conv3 = tf.Variable(tf.truncated_normal([conv3_num_filters], stddev=0.1))
        conv3 = tf.nn.relu(tf.nn.conv1d(pool2, w_conv3,
                                        stride=1, padding='SAME')
                           + b_conv3)

        # pooling layer
        pool4_width = 8
        pool4 = tf.nn.max_pool(tf.reshape(conv3,
                                          [-1, 1,
                                           int(conv3.shape[1]),
                                           int(conv3.shape[2])]),
                               [1, 1, pool4_width, 1],
                               [1, 1, pool4_width, 1],
                               padding='VALID')
        pool4 = tf.squeeze(pool4, 1)
        pool4_flat = tf.reshape(pool4, [-1, int(pool4.shape[1])*int(pool4.shape[2])])

        # fully connected layer
        w_full = tf.Variable(tf.truncated_normal([int(pool4_flat.shape[1]),
                                                  1],
                                                 stddev=0.1))
        b_full = tf.Variable(tf.truncated_normal([1], stddev=0.1))
        self.outputs = tf.matmul(pool4_flat , w_full) + b_full

        # cost
        # mean_square for now
        self.cost = tf.reduce_mean(tf.square(self.targets - self.outputs))

        # optimizer and train operator
        self.learning_rate = tf.placeholder(tf.float32)
        optimizer = tf.train.AdamOptimizer(self.learning_rate)
        self.train_op = optimizer.minimize(self.cost)

    def evaluate(self, seq):
        pass

    def save(self, sess):
        try:
            pass
        finally:
            print(':: saving model')
            self.saver.save(sess, config.save_path)
            print(':: saved')

    def restore(self, sess):
        pass

if __name__ == '__main__':
    model = Model()
