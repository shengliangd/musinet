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
        bio.select()
        bio.mutate()
        bio.crossover()
        bio.rank()
        avg_fitness, best_fitness = bio.describe()
        print('epoch %d, avg.=%f, best=%f' % (epoch, avg_fitness, best_fitness))
        epoch = epoch + 1
    except KeyboardInterrupt:
        tmp = input('\noperation(q/o/m/c/g):')
        if tmp == 'q':
            break
        elif tmp == 'o':
            result = bio.result()
            with open(args.output, 'wb') as f:
                pkl.dump(result, f)
        elif tmp == 'm':
            try:
                pm = float(input('current pm: {0}, new pm:'.format(bio.pm)))
            except ValueError:
                print(':: invalid pm')
                continue
            except KeyboardInterrupt:
                continue
            bio.pm = pm
        elif tmp == 'c':
            try:
                pc = float(input('current pc: {0}, new pc:'.format(bio.pc)))
            except ValueError:
                print(':: invalid pc')
                continue
            except KeyboardInterrupt:
                continue
            bio.pc = pc
        continue
