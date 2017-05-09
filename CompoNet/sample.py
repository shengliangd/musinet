#!/usr/bin/python3

import tensorflow as tf
import compo_net
import data_loader
import six.moves.cPickle as pkl
import os.path
import map_data as nm

if __name__ == '__main__':
    config = compo_net.Config(training=False,
                              data_path='output/input.pkl')
    loader = data_loader.Loader(config)
    model = compo_net.Model(config)
    sess = tf.Session()
    sess.run(tf.global_variables_initializer())
    model.restore(sess)

    inp = loader.get_sequence(pointer=0, length=20)
    with open(os.path.join(config.output_dir, 'output.pkl'), 'wb+') as file:
        output = model.sample(sess, inp, final_len=1024)
        for i in range(len(output)):
            output[i][0] = nm.unmap_pitch(output[i][0])
            output[i][1] = nm.unmap_dynamic(output[i][1])
            output[i][2] = nm.unmap_rhythm(output[i][2])
            output[i][3] = nm.unmap_duration(output[i][3])
        print(output)
        pkl.dump([48, output], file)
