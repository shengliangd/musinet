import os.path


seq_length = 512
num_channels = 4
save_path = 'save/value_net.sav'
data_path = '../data/train.pkl'
batch_size = 32
default_lr = 0.0004


def init_value_net_dir(dir):
    global save_path, data_path
    save_path = os.path.join(dir, save_path)
    data_path = os.path.join(dir, data_path)


def can_restore():
    return os.path.exists(os.path.join(os.path.dirname(save_path), 'checkpoint'))


