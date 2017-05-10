#!/usr/bin/python3

import value_net
import data_loader
import config
import tensorflow as tf
import os.path

if __name__ == '__main__':
    if not os.path.exists('save/'):
        os.mkdir('save')

    model = value_net.Model()
    data_loader = data_loader.Loader()

    sess = tf.Session()
    if config.restore:
        model.restore(sess)
    sess.run(tf.global_variables_initializer())

    learning_rate = config.default_lr
    times = 1
    while True:
        try:
            inputs, targets = data_loader.get_next_batch()
            [cost, _] = sess.run([model.cost, model.train_op],
                                 {model.inputs: inputs, model.targets: targets,
                                  model.learning_rate: learning_rate})

            assert cost == cost, 'cost is nan'

            print('batch: {0}, cost: {1}'.format(times, cost))

        except KeyboardInterrupt:
            cmd = input('Operation(w/q/c/l)')
            if cmd == 'w':
                model.save(sess)
            elif cmd == 'q':
                exit()
            elif cmd == 'l':
                print('current learning rate: {0}'.format(learning_rate))
                try:
                    tmp = float(input('input new learning rate:'))
                except ValueError:
                    print(':: invalid learning rate')
                else:
                    learning_rate = tmp
            continue
