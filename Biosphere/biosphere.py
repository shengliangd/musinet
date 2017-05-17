#!/usr/bin/python3
import pickle as pkl
import numpy as np
import random
from ValueNet import value_net, convert
import math

gene_len = 16

class Biosphere:
    """
    Genetic Algorithm for Musinet
    """
    population = []
    pop_fitness = []
    evaluator = value_net.Model()
    best_fitness = 0.0
    best = 0

    def __init__(self, initial_file, pop_size=1000, chromlen=512, pm=0.1, pc=0.8):
        self.pop_size = pop_size
        self.chromlen = chromlen
        self.pm = pm
        self.pc = pc
        self.load(initial_file)
        self.rank()

    def load(self, path):
        """
        Load a PKL-collection file as the initial population.
        PKLs are normalized when they're read.
        """
        f = open(path, 'rb')
        for i in range(0, self.pop_size):
            score = pkl.load(f)
            notes = score[0][1] # NOTE: will always use the first track
            for note in notes:
                note[0] = convert.convert_pitch(note[0])
                note[1] = convert.convert_dynamic(note[1])
                note[2] = convert.convert_rhythm(note[2])
                note[3] = convert.convert_duration(note[3])
            self.population.append(notes)

    def rank(self):
        """
        Rank every individual in the population
        """
        self.pop_fitness = self.evaluator.evaluate(self.population)
        for i in range(len(self.pop_fitness)):
            self.pop_fitness[i][0] = 1/(1+math.exp((0.5-self.pop_fitness[i][0])*12))

    def mutate(self):
        """
        Genetic mutation on every individual in the population. Probability is @self.pm.
        Each time only one point in a channel is changed.
        """
        def mutate_single(individual):
            channel = random.randint(0, 3)
            point = random.randint(0, self.chromlen-1)
            individual[point][channel] = random.random()
            return individual
        for individual in self.population:
            if random.random() < self.pm:
                individual = mutate_single(individual)

    def select(self):
        """
        Emulate natural selection using Roulette algorithm.
        Turn current population into a mating pool.
        This also maintains best and best_fitness.
        """
        def next_i(M):
            S = 0.0
            i = 0
            while i < self.pop_size and S + self.pop_fitness[i][0] < M:
                S += self.pop_fitness[i][0]
                if self.pop_fitness[i][0] > self.best_fitness:
                    self.best = i
                    self.best_fitness = self.pop_fitness[i][0]
                i += 1
            return i
        total_fitness = np.sum(self.pop_fitness)
        selected = []
        for n in range(0, self.pop_size):
            M = random.uniform(0, total_fitness)
            i = next_i(M)
            selected.append(self.population[i])
        self.population = selected

    def crossover(self):
        """
        Cross over using one-point selection. Probability is @self.pc.
        It exchanges a piece of chromosome of length gene_len.
        """
        def cross_chromosome(A, B):
            point = random.randint(0, self.chromlen-gene_len)
            A_ = A[:point] + B[point:point+gene_len] + A[point+gene_len:]
            B_ = B[:point] + A[point:point+gene_len] + B[point+gene_len:]
            return A_, B_
        next_gen = []
        prev = None
        for individual in self.population:
            if random.random() < self.pc:
                if prev is None:
                    prev = individual
                else:
                    next_gen.extend(cross_chromosome(prev, individual))
                    prev = None
            else:
                next_gen.append(individual)
        self.population = next_gen
        if prev is not None:
            self.population.append(prev)

    def describe(self):
        """
        Get current average of fitness and the best fitness
        """
        return np.mean(self.pop_fitness), self.best_fitness

    def result(self):
        best = self.population[self.best]
        # print(best)
        notes = []
        for note in best:
            notes.append([convert.deconvert_pitch(note[0]),
                          convert.deconvert_dynamic(note[1]),
                          convert.deconvert_rhythm(note[2]),
                          convert.deconvert_duration(note[3])])
        part = [48, notes, self.best_fitness]
        score = [part]
        return score

