#!/usr/bin/python3
"""
musinet.py - entry of musinet

./musinet.py --convert-all-midi --train
./musinet.py --sample --output result.mid
"""

import os, sys, subprocess, tempfile
from sys import stderr
from optparse import OptionParser
from toolchain.xmlseq.xml2seq2 import xml2seq
from toolchain.xmlpkl.xmlpkl import xml2pkl, pkl2xml

musinet_root = os.path.split(os.path.realpath(sys.argv[0]))[0]
midi_dir = os.path.join(musinet_root, 'mid')
pkl_dir = os.path.join(musinet_root, 'pkl')
jmusic_dir = os.path.join(musinet_root, 'toolchain', 'jmusic')

def get_params():
    try:
        opt = OptionParser()

        opt.add_option('--convert', dest='convert', default='')
        opt.add_option('--output', dest='output', default='')
        opt.add_option('--convert-all-midi', action='store_true',
                       dest='convert_all_midi', default=False)

        opt.add_option('--pkl-dir', dest='pkl_dir', default=pkl_dir)
        opt.add_option('--midi-dir', dest='midi_dir', default=midi_dir)

        opt.add_option('--train', dest='train', default=False)
        opt.add_option('--sample', dest='sample', default=False)

        (values, args) = opt.parse_args()
        return values
    except Exception as ex:
        print('unhandled exception {0}'.format(str(ex)), file=stderr)

def call_converter(path_in, path_out):
    jar_path = os.path.join(jmusic_dir, 'converter.jar')
    subprocess.call(['java', '-jar', jar_path, path_in, path_out])

def convert_midi_pkl(midi_path, pkl_path):
    xml_path = tempfile.mktemp()
    if pkl_path == '':
        pkl_path = os.path.splitext(os.path.basename(midi_path))[0]+'.pkl'
    call_converter(midi_path, xml_path)
    xml2seq(xml_path, xml_path)
    xml2pkl(xml_path, pkl_path)
    os.remove(xml_path)

def convert_pkl_midi(pkl_path, midi_path):
    xml_path = tempfile.mktemp()
    pkl2xml.pkl2xml(pkl_path, xml_path)
    call_converter(xml_path, midi_path)
    os.remove(xml_path)


## Handlers
def handle_convert(path_in, path_out):
    if path_in[-4:].lower() == '.mid':
        convert_midi_pkl(path_in, path_out)
    elif path_in[-4:].lower() == '.pkl':
        convert_pkl_midi(path_in, path_out)

def handle_convert_all_midi(midi_dir, pkl_dir):
    print(':: start converting')
    if not os.path.exists(pkl_dir):
        os.mkdir(pkl_dir)
    for root, dirs, files in os.walk(midi_dir):
        for fn in files:
            midi_path = os.path.join(root, fn)
            # FIXME: this should keep directory hierachy
            pkl_path = os.path.join(pkl_dir, os.path.splitext(fn)[0]+'.pkl')
            convert_midi_pkl(midi_path, pkl_path)

def handle_train():
    print(':: start training')
    # TODO train

def handle_sample():
    print(':: start sampling')
    # TODO sample

## Entry
def main(opt):
    if opt.convert != '':
        handle_convert(opt.convert, opt.output)
    if opt.convert_all_midi:
        handle_convert_all_midi(opt.midi_dir, opt.pkl_dir)
    if opt.train:
        handle_train()
    if opt.sample:
        handle_sample()

if __name__ == '__main__':
    options = get_params()
    if options == None:
        exit(1)
    main(options)
else:
    print('this is intended to be run as a standalone program')
