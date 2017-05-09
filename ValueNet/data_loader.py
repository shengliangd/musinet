"""data_loader for ValueNet
    train.pkl should be of format [instrument_code, [seq], value(score)]
"""


import pickle
import config
import convert


class Loader:
    def __init__(self):
        self.inputs = []
        self.targets = []
        with open(config.data_path, 'rb') as data_file:
            for item in pickle.load(data_file):
                # deal with length
                item[1] = item[1][:config.seq_length]
                while len(item[1]) < config.seq_length:
                    item[1].append([0, 0, 0, 0])

                # convert data
                for i in range(len(item[1])):
                    item[1][i][0] = convert.convert_pitch(item[1][i][0])
                    item[1][i][1] = convert.convert_pitch(item[1][i][1])
                    item[1][i][2] = convert.convert_pitch(item[1][i][2])
                    item[1][i][3] = convert.convert_pitch(item[1][i][3])

                self.inputs.append(item[1])
                self.targets.append(item[2])
        self.pointer = 0

    def get_next_batch(self):
        inputs = []
        targets = []
        try:
            for i in range(config.batch_size):
                inputs.append(self.inputs[self.pointer+i])
                targets.append(self.targets[self.pointer+i])
        except IndexError:
            pass
        return inputs, targets

if __name__ == '__main__':
    loader = Loader()
    print(loader.get_next_batch())
