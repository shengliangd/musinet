#!/usr/bin/python3

# 目前实现的是模仿char-rnn的方法
# 从data/train.pkl中读取训练数据
# 保存训练结果到save文件夹，保存训练记录到log文件夹

import tensorflow as tf
import compo_net
import data_loader

if __name__ == '__main__':
    config = compo_net.Config(training=True, restore=True)
    loader = data_loader.Loader(config)
    model = compo_net.Model(config)
    sess = tf.Session()
#    sess.run(tf.variables_initializer(model.variables))  # fail to initialize rnn weights
    sess.run(tf.global_variables_initializer())

    if config.restore:
        model.restore(sess)

    loader.reset_pointer()
    times = 1
    cost = 0
    while True:
        try:
            data = loader.get_next_batch()
            [_cost, _] = sess.run([model.cost, model.train], {model.inputs: data})
            cost += _cost
            if times % loader.num_batches == 0:
                print('epoch: %d, cost: %.8f' % (times / loader.num_batches, cost / loader.num_batches))
                cost = 0
            if times % 1000 == 0:
                print('saving model')
                model.save(sess)
                print('saved')
            times += 1
        except KeyboardInterrupt:
            cmd = input('Operation(w/q/c/l):')
            if 'w' == cmd:
                model.save(sess)
            if 'q' == cmd:
                exit()
            if 'l' == cmd:  # change learning rate, not implemented yet
                tmp = input()
            continue
