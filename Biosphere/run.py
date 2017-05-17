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
args = parser.parse_args()

bio = Biosphere(args.initial)
epoch = 0
best_fitness = 0.0
avg_fitness = 0.0
while True:
    try:
        avg_fitness, best_fitness = bio.describe()
        print('epoch %d, avg.=%f, best=%f' % (epoch, avg_fitness, best_fitness))
        bio.select()
        bio.mutate()
        bio.crossover()
        bio.rank()
        epoch = epoch + 1
    except KeyboardInterrupt:
        tmp = input('\noperation(q/o/(p)m/(p)c):')
        if tmp == 'q':
            break
        elif tmp == 'o':
            result = bio.result()
            with open(args.output, 'wb') as f:
                pkl.dump(result, f)
        elif tmp == 'm':
            print(':: not implemented')
        elif tmp == 'c':
            print(':: not implemented')

