"""
data_loader for ValueNet
train.pkl should be of format [instrument_code, [seq], value(score)]
"""


import pickle
import config
import convert


class Loader:
    def __init__(self):
        self.inputs = []
        self.targets = []
        self.num_sequences = {0.0: 0, 0.4: 0, 0.6: 0, 1.0: 0}
        with open(config.data_path, 'rb') as data_file:
            while True:
                try:
                    for item in pickle.load(data_file):
                        # deal with length
                        item[1] = item[1][:config.seq_length]
                        if len(item[1]) < config.seq_length:
                            continue

                        for i in range(len(item[1])):
                            item[1][i][0] = convert.convert_pitch(item[1][i][0])
                            item[1][i][1] = convert.convert_dynamic(item[1][i][1])
                            item[1][i][2] = convert.convert_rhythm(item[1][i][2])
                            item[1][i][3] = convert.convert_duration(item[1][i][3])

                        self.inputs.append(item[1])
                        self.targets.append([item[2]])
                        self.num_sequences[item[2]] += 1
                except EOFError:
                    break
        self.pointer = 0

        print(':: loaded {0} sequences'.format(sum(self.num_sequences)))
        print(':: {0}'.format(self.num_sequences))

    def get_next_batch(self):
        inputs = []
        targets = []
        try:
            for i in range(config.batch_size):
                inputs.append(self.inputs[self.pointer+i])
                targets.append(self.targets[self.pointer+i])
        except IndexError:
            pass
        self.pointer += config.batch_size
        if self.pointer >= len(self.inputs):
            self.pointer = 0
        return inputs, targets

    def get_all(self):
        return self.inputs, self.targets

