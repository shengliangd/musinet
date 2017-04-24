#!/usr/bin/python3

from sys import argv
from copy import deepcopy, copy
import xml.dom.minidom

def xml_copy_attr(dst, src, attr_name):
    tmp = src.getAttribute(attr_name)
    if tmp != '':
        dst.setAttribute(attr_name, tmp)

if __name__ == '__main__':
    if len(argv) != 3:
        print("Usage: python3 %s infile outfile" % argv[0])
        exit(-1)

    dom = xml.dom.minidom.parse(argv[1])
    new_dom = xml.dom.minidom.Document()

    score = dom.getElementsByTagName('Score')[0]

    new_score = dom.createElement('Score')
    xml_copy_attr(new_score, score, 'tempo')
    xml_copy_attr(new_score, score, 'keySignature')
    xml_copy_attr(new_score, score, 'numerator')
    xml_copy_attr(new_score, score, 'denominator')
   # ah, ugly, but I didn't find better way :(
    new_dom.appendChild(new_score)

    for part in score.getElementsByTagName('Part'):
        new_part = dom.createElement('Part')
        xml_copy_attr(new_part, part, 'channel')
        xml_copy_attr(new_part, part, 'instrument')

        new_score.appendChild(new_part)

        times = []
        phrases = []
        for phrase in part.getElementsByTagName('Phrase'):
            timeseq = []
            phr = []

            time = phrase.getAttribute('startTime')
            if time == '':
                time = 0.0
            else:
                time = float(time)

            for note in phrase.getElementsByTagName('Note'):
                timeseq.append(time)
                phr.append(note)
                tmp = note.getAttribute('rhythmValue')
                if tmp != '':
                    time += eval(tmp)

            phrases.append(phr)
            times.append(timeseq)
     
        assert len(phrases) == len(times), "fa"

        new_phrase = dom.createElement('Phrase')
        new_part.appendChild(new_phrase)

        seeks = [0 for _ in range(len(times))]

        prev_time = 0.0
        prev_note = dom.createElement('Note')
        prev_note.setAttribute('pitch', '-2147483648')
        prev_note.setAttribute('rhythmValue', '0')
        new_phrase.appendChild(prev_note)
        while True:
            min_time = 9.0e9
            min_i = 50000
            finished = [False for _ in range(len(times))]
            for i in range(len(times)):
                try:
                    if times[i][seeks[i]] < min_time:
                        min_time = times[i][seeks[i]]
                        min_i = i
                except IndexError:
                    finished[i] = True

            if all(finished):
                break
            
            phrases[min_i][seeks[min_i]].setAttribute('rhythmValue', str(min_time - prev_time))
            new_phrase.appendChild(phrases[min_i][seeks[min_i]])

            if prev_note:
                prev_note.setAttribute('rhythmValue', str(min_time-prev_time))

            prev_time = times[min_i][seeks[min_i]]
            prev_note = phrases[min_i][seeks[min_i]]

            seeks[min_i] += 1

    new_dom.writexml(open(argv[2], 'w'), encoding='UTF-8')
