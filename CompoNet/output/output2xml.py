#!/usr/bin/python3

import xml.dom.minidom
import pickle as pkl
from sys import argv
'''
if len(argv) != 3:
    print('Usage: {} infile outfile'.format(argv[0]))
    exit(-1)
'''
dom = xml.dom.minidom.Document()

score = dom.createElement('Score')
dom.appendChild(score)

part = dom.createElement('Part')
score.appendChild(part)

phrase = dom.createElement('Phrase')
part.appendChild(phrase)

with open('output.pkl', 'rb') as file:
    while True:
        try:
            for tmp in pkl.load(file)[1]:
                note = dom.createElement('Note')
                note.setAttribute('pitch', str(tmp[0]))
                note.setAttribute('dynamic', str(tmp[1]))
                note.setAttribute('rhythmValue', str(tmp[2]))
                note.setAttribute('duration', str(tmp[3]))

                phrase.appendChild(note)
        except EOFError:
            break

dom.writexml(open('output.xml', 'w'), encoding='UTF-8')
