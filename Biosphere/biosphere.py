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
    total_fitness = 0

    def __init__(self, initial_file, pop_size=1000, chromlen=512, pm=0.0, pc=0.8):
        self.pop_size = pop_size
        self.chromlen = chromlen
        self.pm = pm
        self.pc = pc
        self.load(initial_file)

    def load(self, path):
        """
        Load a PKL-collection file as the initial population.
        PKLs are normalized when they're read.
        """
        f = open(path, 'rb')
        for i in range(0, self.pop_size):
            score = pkl.load(f)
            notes = score[0][1] # NOTE: will always use the first track
            '''
            for note in notes:
                note[0] = convert.convert_pitch(note[0])
                note[1] = convert.convert_dynamic(note[1])
                note[2] = convert.convert_rhythm(note[2])
                note[3] = convert.convert_duration(note[3])
            '''
            self.population.append(notes)

    def rank(self):
        """
        Rank every individual in the population
        """
        self.best_fitness = 0.0
        self.pop_fitness = self.evaluator.evaluate(self.population)
        '''
        # conver fitness for better perf
        for i in range(self.pop_size):
            self.pop_fitness[i][0] = 1/(1+math.exp((0.5-self.pop_fitness[i][0])*8))
        '''
        for i in range(self.pop_size):
            if self.pop_fitness[i][0] > self.best_fitness:
                self.best_fitness = self.pop_fitness[i][0]
                self.best = i
        self.total_fitness = np.sum(self.pop_fitness)

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

        for _individual in self.population:
            if random.random() < self.pm:
                mutate_single(_individual)

    def choose_by_fitness(self):
        M = random.uniform(0, self.total_fitness)
        S = 0.0
        i = 0
        while i < self.pop_size-1 and S + self.pop_fitness[i][0] < M:
            S += self.pop_fitness[i][0]
            i += 1
        return i

    def choose_by_reverse_fitness(self):
        M = random.uniform(0, self.pop_size - self.total_fitness)
        S = 0.0
        i = 0
        while i < self.pop_size-1 and S + (1-self.pop_fitness[i][0]) < M:
            S += 1-self.pop_fitness[i][0]
            i += 1
        return i

    def select(self):
        """
        Emulate natural selection using Roulette algorithm.
        Turn current population into a mating pool.
        This also maintains best and best_fitness.
        """

        self.rank()
        selected = []
        for n in range(0, self.pop_size):
            i = self.choose_by_fitness()
            selected.append(self.population[i])
        self.population = selected

    def crossover(self):
        """
        Cross over using one-point selection. Probability is @self.pc.
        It exchanges a piece of chromosome of length gene_len.
        """
        def cross_chromosome(A, B):
            point = random.randint(0, self.chromlen-gene_len-1)
            return A[:point] + B[point:(point+gene_len)] + A[(point+gene_len):]

        self.rank()  # need this to calculate crossover prob
        for i in range(self.pop_size):
            ind1 = self.choose_by_fitness()
            ind2 = self.choose_by_fitness()
            self.population[self.choose_by_reverse_fitness()] = cross_chromosome(self.population[ind1],
                                                                                 self.population[ind2])

    def describe(self):
        """
        Get current average of fitness and the best fitness
        """
        self.rank()
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
