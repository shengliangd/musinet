#!/usr/bin/python3

import os.path
from six.moves import cPickle as pkl

root_dir = '../pkl/'

outfile = open('../data.pkl', 'wb+')

for fname in os.listdir(root_dir):
    infile = open(os.path.join(root_dir, fname), 'rb')
    pkl.dump(pkl.load(infile), outfile)
    infile.close()

outfile.close()