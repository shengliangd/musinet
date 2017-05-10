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
                deviation = 0
                for y, y_ in zip(targets, outputs):
                    print('{0:.8f}, {1:.8f}'.format(y[0], y_[0]))
                    deviation += (y[0]-y_[0])**2
                print('deviation: {0:.8f}'.format((deviation/len(targets))**0.5))
                input(':: enter to continue')
            continue
