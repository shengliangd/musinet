import six.moves.cPickle as pkl
import matplotlib.pyplot as plt
import numpy as np

pitches = [0 for _ in range(0, 200)]
dynamics = [0 for _ in range(0, 200)]
rhythms = [0 for _ in range(0, 200)]
durations = [0 for _ in range(0, 200)]
try:
    file = open('data.pkl', 'rb')
    while True:
        for part in pkl.load(file):
            for note in part[1]:
                tmp = note[0]
                if tmp < 0:
                    tmp = 0
                pitches[tmp] += 1

                tmp = note[1]
                if tmp >= 200:
                    tmp = 199
                dynamics[tmp] += 1

                tmp = int(note[2] * 100)
                if tmp >= 200:
                    tmp = 199
                rhythms[tmp] += 1

                tmp = int(note[3] * 100)
                if tmp >= 200:
                    tmp = 199
                durations[tmp] += 1
except EOFError:
    pass

# pitches
plt.figure(figsize=(18, 8))
x = np.linspace(0, 200, 200)
plt.plot(x, pitches, label='pitches')
plt.title('statistics on pitches')
plt.xlabel('pitch')
plt.ylabel('count')
plt.show()

# dynamics
plt.figure(figsize=(18, 8))
x = np.linspace(0, 200, 200)
plt.plot(x, dynamics, label='dynamics')
plt.title('statistics on dynamics')
plt.xlabel('dynamic')
plt.ylabel('count')
plt.show()

# rhythms
plt.figure(figsize=(18, 8))
x = np.linspace(0, 200, 200)
plt.plot(x, rhythms, label='rhythms')
plt.title('statistics on rhythms')
plt.xlabel('rhythm*100')
plt.ylabel('count')
plt.show()

# durations
plt.figure(figsize=(18, 8))
x = np.linspace(0, 200, 200)
plt.plot(x, durations, label='durations')
plt.title('statistics on durations')
plt.xlabel('duration*100')
plt.ylabel('count')
plt.show()
