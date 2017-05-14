import six.moves.cPickle as pkl
from sys import stderr
import sklearn.preprocessing as preprocessing
import convert as mp
import numpy as np
import sklearn.externals.joblib as joblib
import os.path
import random


class Loader:
    def __init__(self, config):
        self.config = config

        # load into memory and normalize at the same time
        self.pitches = []
        self.dynamics = []
        self.rhythms = []
        self.durations = []
        with open(config.data_path, 'rb') as file:
            total = 0
            while True:
                try:
                    for data in pkl.load(file):
                        if data[2] != 1.0 or len(data[1]) < 512:
                            continue
                        for i in range(len(data[1])):
                            self.pitches.append(mp.map_pitch(data[1][i][0]))
                            self.dynamics.append(mp.map_dynamic(data[1][i][1]))
                            self.rhythms.append(mp.map_rhythm(data[1][i][2]))
                            self.durations.append(mp.map_duration(data[1][i][3]))
                        total += 1
                except EOFError:
                    print(':: loading finished, total {0}'.format(total), file=stderr)
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
                        os.path.join(config.save_dir, 'encoders.sav'))
        else:
            # load saved encoder
            [self.pitch_encoder,
             self.dynamic_encoder,
             self.rhythm_encoder,
             self.duration_encoder] = joblib.load(os.path.join(config.save_dir, 'encoders.sav'))
            pass

        config.vec_lengths = [len(self.pitch_encoder.active_features_),
                              len(self.dynamic_encoder.active_features_),
                              len(self.rhythm_encoder.active_features_),
                              len(self.duration_encoder.active_features_)]

        config.encoders = [self.pitch_encoder,
                           self.dynamic_encoder,
                           self.rhythm_encoder,
                           self.duration_encoder]

        self.pointer = 0
        self.num_batches = len(self.pitches) // config.seq_length
        print(':: dataset contains {:d} notes, ie. {:d} batches'
              .format(len(self.pitches), self.num_batches),
              file=stderr)

    def convert(self, pointer, length):
        pitches = self.pitch_encoder.transform(self.pitches[pointer:(pointer + length + 1)]).toarray().tolist()
        dynamics = self.dynamic_encoder.transform(self.dynamics[pointer:(pointer + length + 1)]).toarray().tolist()
        rhythms = self.rhythm_encoder.transform(self.rhythms[pointer:(pointer + length + 1)]).toarray().tolist()
        durations = self.duration_encoder.transform(self.durations[pointer:(pointer + length + 1)]).toarray().tolist()
        return pitches, dynamics, rhythms, durations

    def get_next_batch(self):
        ret = ([], [])
        for i in range(self.config.batch_size):
            pointer = random.randint(0, len(self.pitches) - self.config.seq_length - 1)
            ret[0].append([])
            ret[1].append([])

            pitches, dynamics, rhythms, durations = self.convert(pointer, self.config.seq_length)
            for j in range(self.config.seq_length):
                ret[0][i].append(pitches[j] + dynamics[j] + rhythms[j] + durations[j])
                ret[1][i].append(pitches[j+1] + dynamics[j+1] + rhythms[j+1] + durations[j+1])
        return ret

    def get_sequence(self, pointer=None, length=1024):
        if pointer is None:
            pointer = random.randint(0, len(self.pitches) - length)
        pitches, dynamics, rhythms, durations = self.convert(pointer, length)

        ret = []
        for i in range(length):
            ret.append(pitches[i] + dynamics[i] + rhythms[i] + durations[i])

        return ret
