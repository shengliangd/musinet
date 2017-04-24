import six.moves.cPickle as pkl
import matplotlib.pyplot as plt
import numpy as np
import math

def map_pitch(x):
    if x < 0:
        return 0.0
    return 1/(1+math.exp(-(x-58)/12))

def map_dynamic(x):
    if x == 0:
        return 0.0
    return 1/(1+math.exp(-(x-75)/16))

def map_rhythm(x):
    if x == 0:
        return 0.0
    return math.log2(x*200)/math.log2(800)

def map_duration(x):
    if x == 0:
        return 0.0
    return math.log2(x*50)/math.log2(500)

pitches = [0 for _ in range(0, 100)]
dynamics = [0 for _ in range(0, 100)]
rhythms = [0 for _ in range(0, 100)]
durations = [0 for _ in range(0, 100)]
try:
    file = open('data.pkl', 'rb')
    while True:
        for part in pkl.load(file):
            for note in part[1]:

                tmp = int(map_pitch(note[0])*100)
                pitches[tmp] += 1
            '''
                tmp = int(map_dynamic(note[1])*100)
                dynamics[tmp] += 1

                tmp = int(map_rhythm(note[2])*100)
                if tmp >= 100:
                    tmp = 99
                if tmp < 0:
                    tmp = 0
                rhythms[tmp] += 1

                tmp = int(map_duration(note[3])*100)
                if tmp >= 100:
                    tmp = 99
                if tmp < 0:
                    tmp = 0
                durations[tmp] += 1
            '''
except EOFError:
    pass

# pitches
plt.figure(figsize=(18, 8))
x = np.linspace(0, 100, 100)
plt.plot(x, pitches, label='pitches')
plt.title('statistics on pitches')
plt.xlabel('pitch')
plt.ylabel('count')
plt.show()

# dynamics
plt.figure(figsize=(18, 8))
x = np.linspace(0, 100, 100)
plt.plot(x, dynamics, label='dynamics')
plt.title('statistics on dynamics')
plt.xlabel('dynamic')
plt.ylabel('count')
plt.show()

# rhythms
plt.figure(figsize=(18, 8))
x = np.linspace(0, 100, 100)
plt.plot(x, rhythms, label='rhythms')
plt.title('statistics on rhythms')
plt.xlabel('rhythm*100')
plt.ylabel('count')
plt.show()

# durations
plt.figure(figsize=(18, 8))
x = np.linspace(0, 100, 100)
plt.plot(x, durations, label='durations')
plt.title('statistics on durations')
plt.xlabel('duration*100')
plt.ylabel('count')
plt.show()
