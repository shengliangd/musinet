#!/usr/bin/python3
import sys, os
from argparse import ArgumentParser
import pickle as pkl
musinet_root = '/'.join(os.path.realpath(sys.argv[0]).split('/')[:-2])
sys.path.append(musinet_root)
from Biosphere.biosphere import Biosphere

parser = ArgumentParser()
parser.add_argument('--initial', default=os.path.join(musinet_root, 'data', 'random.pkl'))
parser.add_argument('--output', default=os.path.join(musinet_root, 'output', 'elite.pkl'))
parser.add_argument('--pm', type=float, default=0.01)
parser.add_argument('--pc', type=float, default=0.1)
args = parser.parse_args()

bio = Biosphere(args.initial, pm=args.pm, pc=args.pc)
epoch = 0
best_fitness = 0.0
avg_fitness = 0.0
try:
    while avg_fitness < 0.9:
        avg_fitness, best_fitness = bio.describe()
        print('epoch %d, avg.=%f, best=%f' % (epoch, avg_fitness, best_fitness))
        bio.select()
        bio.mutate()
        bio.crossover()
        bio.rank()
        epoch = epoch + 1
except KeyboardInterrupt:
    print('your coffee is finished, right?')
result = bio.result()
with open(args.output, 'wb') as f:
    pkl.dump(result, f)
