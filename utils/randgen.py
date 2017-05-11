#!/usr/bin/python3
import os
import sys
from optparse import OptionParser
import pickle as pkl
import random

def get_params():
    try:
        opt = OptionParser()
        opt.add_option('--template', dest='template', type=str, default='')
        opt.add_option('--pitch', action='store_true', dest='pitch')
        opt.add_option('--dynamic', action='store_true', dest='dynamic')
        opt.add_option('--rhythm', action='store_true', dest='rhythm')
        opt.add_option('--duration', action='store_true', dest='duration')
        opt.add_option('--output', dest='output', type=str, default='')
        opt.add_option('--dump', action='store_true', dest='dump')
        (options, args) = opt.parse_args()
        if not (options.pitch or options.dynamic or options.rhythm or options.duration):
            print('must provide at least one channel', file=sys.stderr)
            return None
        return options
    except Exception as ex:
        print('unhandled exception :{0}'.format(str(ex)), file=sys.stderr)
        return None

def indices(options):
    indices = []
    if options.pitch:
        indices.append(0)
    if options.dynamic:
        indices.append(1)
    if options.rhythm:
        indices.append(2)
    if options.duration:
        indices.append(3)
    return indices

def rand_pitch():
    pitch = random.randint(20, 95)
    if pitch == 20:
        pitch = -2147483648
    return pitch

def rand_dynamic():
    dynamic = random.randint(2000, 13000)
    if dynamic == 2000:
        dynamic = 0
    return dynamic / 10000

def rand_rhythm():
    return random.randint(0, 20000) / 10000

def rand_duration():
    return random.randint(0, 20000) / 10000

def rand(idx):
    "random for channel idx"
    return [rand_pitch, rand_dynamic, rand_rhythm, rand_duration][idx]()

def process_phrase(phrase, indices):
    "Substitute channel idx of @phrase with randomly generated rubbish, where idx is in @indices"
    phrase[2] = 0.0
    seq = phrase[1]
    for note in seq:
        for idx in indices:
            note[idx] = rand(idx)

options = get_params()
if options == None:
    exit(1)

if (True, True, True, True) == (options.pitch, options.dynamic, options.rhythm, options.duration):
    notes = [[rand_pitch(), rand_dynamic(), rand_rhythm(), rand_duration()] for x in range(0, 1024)]
    phrase = [48, notes, 0.0] # rank is 0.0
    score = [phrase]
else:
    if options.template == '':
        print('must provide a template', file=sys.stderr)
        exit(1)
    with open(options.template, 'rb') as fin:
        score = pkl.load(fin)
        for phrase in score:
            process_phrase(phrase, indices(options))
if options.dump == True:
    print(score)
if options.output != '':
    with open(options.output, 'wb') as fout:
        pkl.dump(score, fout)

# Done
print('%s' % options.template)
