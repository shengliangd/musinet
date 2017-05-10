import os.path


seq_length = 512
num_channels = 4
save_path = 'save/value_net.sav'
data_path = '../data/train.pkl'
batch_size = 32
default_lr = 0.0004


def can_restore():
    return os.path.exists(os.path.join(os.path.dirname(save_path), 'checkpoint'))
