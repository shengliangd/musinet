#!/usr/bin/python3


import data_loader
import argparse
import tensorflow as tf
import value_net


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='evaluate note sequence using ValueNet')
    parser.add_argument('-f', '--file', help='Indicate the input file')
    args = parser.parse_args()

    inputs = data_loader.load_file(args.file)
    value_net = value_net.Model()
    with tf.Session() as sess:
        value_net.restore(sess)
        outputs = value_net.evaluate(sess, inputs)
    print('ranks: {0}'.format(outputs))
    print('average: {0}'.format(sum(outputs)/len(outputs)))
