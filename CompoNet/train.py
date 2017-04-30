#!/usr/bin/python3

# 默认从data/train.pkl中读取训练数据
# 保存训练结果到save文件夹

import tensorflow as tf
import compo_net
import data_loader
import os

if __name__ == '__main__':
    config = compo_net.Config(training=True, learning_rate=0.0002)
    config.restore = bool(os.listdir(config.save_dir))
    if config.restore:
        print('restore from saved model')

    loader = data_loader.Loader(config)
    model = compo_net.Model(config)
    merged_summary = tf.summary.merge_all()
    sess = tf.Session()
    summary_writer = tf.summary.FileWriter(config.log_dir, sess.graph)

    sess.run(tf.global_variables_initializer())

    if config.restore:
        model.restore(sess)

    times = 1
    cost = 0
    while True:
        try:
            inputs, targets = loader.get_next_batch()

            [_cost, _] = sess.run([model.cost, model.train], {model.inputs: inputs, model.targets: targets})
            cost += _cost
            if cost != cost:
                print(':: cost is nan, abort')
                exit(-1)
            if times % loader.num_batches == 0:
                print('epoch: %d, cost: %.8f' % (times / loader.num_batches, cost / loader.num_batches))
                cost = 0
            if times % 3000 == 0:
                model.save(sess)
            times += 1
        except KeyboardInterrupt:
            cmd = input('Operation(w/q/c/l):')
            if 'w' == cmd:
                model.save(sess)
            if 'q' == cmd:
                exit()
            if 'l' == cmd:  # change learning rate, not implemented yet
                print('not implemented yet')
            continue
