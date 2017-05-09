import six.moves.cPickle as pickle
import xml.dom.minidom

def xml2pkl(infile, outfile):
    dom = xml.dom.minidom.parse(infile)
    output = open(outfile, 'wb+')

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
