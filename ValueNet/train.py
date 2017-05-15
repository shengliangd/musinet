#!/usr/bin/python3

import value_net
import data_loader
import config
import tensorflow as tf
import os.path


if __name__ == '__main__':
    model = value_net.Model()
    data_loader = data_loader.Loader()

    input(':: press enter to start training')

    learning_rate = config.default_lr
    times = 1
    while True:
        try:
            inputs, targets = data_loader.get_next_batch()
            cost = model.train(inputs, targets, learning_rate)

            # when use cross entroy, this may happen
            assert cost == cost, 'cost is nan'

            print('batch: {0}, cost: {1}'.format(times, cost))
            times += 1

        except KeyboardInterrupt:
            cmd = input('\noperation(w/q/c/l/t):')
            if cmd == 'w':
                model.save()
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
            elif cmd == 't':
                inputs, targets = data_loader.get_all()
                outputs = model.evaluate(inputs)
                input(outputs)
                deviation = 0
                count_total = {0.0: 0, 0.4: 0, 0.6: 0, 1.0: 0}
                count_good = {0.0: 0, 0.4: 0, 0.6: 0, 1.0: 0}
                for y, y_ in zip(targets, outputs):
                    y = y[0]
                    y_ = y_[0]
                    print('{0:.8f}, {1:.8f}'.format(y, y_))
                    deviation += (y-y_)**2
                    count_total[y] += 1
                    if abs(y-y_) < 0.1:
                        count_good[y] += 1
                print('0.0: {0:.3f}, 0.4: {1:.3f}, 0.6: {2:.3f}, 1.0: {3:.3f}'.
                      format(
                              count_good[0.0] / count_total[0.0],
                              count_good[0.4] / count_total[0.4],
                              count_good[0.6] / count_total[0.6],
                              count_good[1.0] / count_total[1.0]))
                print('deviation: {0:.8f}'.format((deviation/len(targets))**0.5))
                input(':: enter to continue')
            continue
