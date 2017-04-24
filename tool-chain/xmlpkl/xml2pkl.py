#!/usr/bin/python3

from sys import argv
import six.moves.cPickle as pickle
import xml.dom.minidom

if __name__ == '__main__':
    if len(argv) != 3:
        print("Usage: %s infile outfile" % argv[0])
        exit(-1)
    
    dom = xml.dom.minidom.parse(argv[1])
    output = open(argv[2], 'wb+')

    raw_parts = []

    for part in dom.getElementsByTagName('Part'):

        # in sequentialized xmls, there is only one phrase
        raw_notes = []

        phrase = part.getElementsByTagName('Phrase')[0]
        for note in phrase.getElementsByTagName('Note'):
            pitch = note.getAttribute('pitch')
            dynamic = note.getAttribute('dynamic')
            rhythmValue = note.getAttribute('rhythmValue')
            duration = note.getAttribute('duration')

            if pitch == '':
                continue
            pitch = int(pitch)

            if dynamic == '':
                dynamic = '80'
            dynamic = int(dynamic)

            if rhythmValue == '':
                rhythmValue = '0.0'
            rhythmValue = float(eval(rhythmValue))

            if duration == '':
                duration = '0.0'
            duration = float(eval(duration))

            raw_notes.append([pitch, dynamic, rhythmValue, duration])

        instrument = part.getAttribute('instrument')
        if instrument == '':
            instrument = '48'
        instrument = int(instrument)

        raw_parts.append([instrument, raw_notes])

    pickle.dump(raw_parts, output)
