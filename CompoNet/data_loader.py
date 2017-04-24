import six.moves.cPickle as pkl
import map_data as nm
from sys import stderr
import numpy as np


class Loader:
    def __init__(self, config):
        self.config = config

        # load into memory and normalize at the same time
        self.dataset = []
        self.num_batches = 0
        with open(config.data_path, 'rb') as file:
            while True:
                try:
                    for data in pkl.load(file):
                        for i in range(len(data[1])):
                            data[1][i][0] = nm.map_pitch(data[1][i][0])
                            data[1][i][1] = nm.map_dynamic(data[1][i][1])
                            data[1][i][2] = nm.map_rhythm(data[1][i][2])
                            data[1][i][3] = nm.map_duration(data[1][i][3])
                        self.dataset += data[1] + [[0, 0, 0, 0]
                                                   for _ in range(config.seq_length-len(data[1])%config.seq_length)]
                except EOFError:
                    print(':: loading finished', file=stderr)
                    break

        self.num_batches = len(self.dataset) // config.seq_length
        print(':: dataset contains {:d} notes, ie. {:d} batches'
              .format(len(self.dataset), self.num_batches)
              , file=stderr)
        self.pointer = 0


    def reset_pointer(self):
        self.pointer = 0

    def get_next_batch(self):
        ret = []
        for i in range(self.config.batch_size):
            ret.append(self.dataset[self.pointer:(self.pointer+self.config.seq_length)])
            self.pointer += self.config.seq_length
            if self.pointer >= len(self.dataset):
                self.pointer = 0
        ret = [ret, ret[1:]+[ret[0]]]
        return ret

    def get_sequence(self, length=None):
        if length is None:
            return self.dataset
        return self.dataset[:length]
