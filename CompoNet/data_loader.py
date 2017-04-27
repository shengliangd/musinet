import six.moves.cPickle as pkl
from sys import stderr
import sklearn.preprocessing as preprocessing
import map_data as mp
import numpy as np
import sklearn.externals.joblib as joblib
import os.path

class Loader:
    """
        load data and create encoders for four channels
    """

    def __init__(self, config):
        self.config = config

        # load into memory and normalize at the same time
        self.pitches = []
        self.dynamics = []
        self.rhythms = []
        self.durations = []
        with open(config.data_path, 'rb') as file:
            while True:
                try:
                    for data in pkl.load(file):
                        for i in range(len(data[1])):
                            self.pitches.append(mp.map_pitch(data[1][i][0]))
                            self.dynamics.append(mp.map_dynamic(data[1][i][1]))
                            self.rhythms.append(mp.map_rhythm(data[1][i][2]))
                            self.durations.append(mp.map_duration(data[1][i][3]))
                except EOFError:
                    print(':: loading finished', file=stderr)
                    break

        self.pitches = np.array(self.pitches).reshape(-1, 1)
        self.dynamics = np.array(self.dynamics).reshape(-1, 1)
        self.rhythms = np.array(self.rhythms).reshape(-1, 1)
        self.durations = np.array(self.durations).reshape(-1, 1)

        self.pitch_encoder = preprocessing.OneHotEncoder()
        self.dynamic_encoder = preprocessing.OneHotEncoder()
        self.rhythm_encoder = preprocessing.OneHotEncoder()
        self.duration_encoder = preprocessing.OneHotEncoder()

        if config.training and not config.restore:
            self.pitch_encoder.fit(self.pitches)
            self.dynamic_encoder.fit(self.dynamics)
            self.rhythm_encoder.fit(self.rhythms)
            self.duration_encoder.fit(self.durations)

            joblib.dump([self.pitch_encoder,
                         self.dynamic_encoder,
                         self.rhythm_encoder,
                         self.duration_encoder],
                        os.path.join(config.save_path, 'encoders.sav'))
        else:
            # load saved encoder
            [self.pitch_encoder,
             self.dynamic_encoder,
             self.rhythm_encoder,
             self.duration_encoder] = joblib.load(os.path.join(config.save_path, 'encoders.sav'))
            pass

        self.pitches = self.pitch_encoder.transform(self.pitches).toarray().tolist()
        self.dynamics = self.dynamic_encoder.transform(self.dynamics).toarray().tolist()
        self.rhythms = self.rhythm_encoder.transform(self.rhythms).toarray().tolist()
        self.durations = self.duration_encoder.transform(self.durations).toarray().tolist()

        self.dataset = []
        for i in range(len(self.pitches)):
            self.dataset.append(self.pitches[i]+
                                 self.dynamics[i]+
                                 self.rhythms[i]+
                                 self.durations[i])

        config.vec_lengths = [len(self.pitches[0]),
                          len(self.dynamics[0]),
                          len(self.rhythms[0]),
                          len(self.durations[0])]

        config.encoders = [self.pitch_encoder,
                           self.dynamic_encoder,
                           self.rhythm_encoder,
                           self.duration_encoder]

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
            if self.pointer+self.config.seq_length >= len(self.dataset):
                self.pointer = 0
        return ret

    def get_sequence(self, length=None):
        if length is None:
            return self.dataset
        return self.dataset[:length]
