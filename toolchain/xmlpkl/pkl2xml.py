#!/usr/bin/python3

from sys import argv
from .xmlpkl import pkl2xml

'''
if len(argv) != 3:
    print('Usage: {} infile outfile'.format(argv[0]))
    exit(-1)
'''

def pkl2xml(infile, outfile):
    dom = xml.dom.minidom.Document()
    
    score = dom.createElement('Score')
    dom.appendChild(score)
    
    part = dom.createElement('Part')
    score.appendChild(part)
    
    phrase = dom.createElement('Phrase')
    part.appendChild(phrase)
    
    with open(infile, 'rb') as file:
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
    
    dom.writexml(open(outfile, 'w'), encoding='UTF-8')

if __name__ == '__main__':
    pkl2xml('output.pkl', 'output.xml')
