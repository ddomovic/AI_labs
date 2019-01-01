import numpy as np 

class GeneticAlgorithm(object): 
    """
        Implement a simple generationl genetic algorithm as described in the instructions
    """

    def __init__(	self, chromosomeShape,
                    errorFunction,
                    elitism = 1,
                    populationSize = 25,
                    mutationProbability  = .1,
                    mutationScale = .5,
                    numIterations = 10000,
                    errorTreshold = 1e-6
                    ):

        self.populationSize = populationSize # size of the population of units
        self.p = mutationProbability # probability of mutation
        self.numIter = numIterations # maximum number of iterations
        self.e = errorTreshold # threshold of error while iterating
        self.f = errorFunction # the error function (reversely proportionl to fitness)
        self.keep = elitism  # number of units to keep for elitism
        self.k = mutationScale # scale of the gaussian noise

        self.i = 0 # iteration counter

        # initialize the population randomly from a gaussian distribution
        # with noise 0.1 and then sort the values and store them internally

        self.population = []
        for _ in range(populationSize):
            chromosome = np.random.randn(chromosomeShape) * 0.1

            fitness = self.calculateFitness(chromosome)
            self.population.append((chromosome, fitness))

        # sort descending according to fitness (larger is better)
        self.population = sorted(self.population, key=lambda t: -t[1])

    def step(self):
        """
            Run one iteration of the genetic algorithm. In a single iteration,
            you should create a whole new population by first keeping the best
            units as defined by elitism, then iteratively select parents from
            the current population, apply crossover and then mutation.

            The step function should return, as a tuple:

            * boolean value indicating should the iteration stop (True if
                the learning process is finished, False othwerise)
            * an integer representing the current iteration of the
                algorithm
            * the weights of the best unit in the current iteration

        """

        self.i += 1

        self.population = self.bestN(self.keep)

        while len(self.population) < self.populationSize:
            new_life = self.mutate(self.crossover(*self.selectParents()))
            self.population.append((new_life, self.calculateFitness(new_life)))

        self.population = sorted(self.population, key=lambda t: -t[1])

        if self.i < self.numIter:
            the_best = self.best()
            return self.f(the_best[0]) < self.e, self.i, the_best[0]
        else:
            return True, self.i, self.best()[0]


    def calculateFitness(self, chromosome):
        """
            Implement a fitness metric as a function of the error of
            a unit. Remember - fitness is larger as the unit is better!
        """
        chromosomeError = self.f(chromosome)

        return 1./chromosomeError


    def bestN(self, n):
        """
            Return the best n units from the population
        """

        if n > self.populationSize:
            n = self.populationSize
        pop_list = sorted(self.population, key=lambda tup: tup[1], reverse=True)

        return pop_list[:n]

    def best(self):
        """
            Return the best unit from the population
        """
        x = self.bestN(1)
        return x[0]


    def selectParents(self):
        """
            Select two parents from the population with probability of
            selection proportional to the fitness of the units in the
            population
        """

        fit_sum = sum([n[1] for n in self.population])
        #prob = np.random.uniform(low=0, high=fit_sum)
        prob = np.random.uniform()
        x = 0
        parent1 = parent2 = None

        for i in self.population:
            x += (i[1] / float(fit_sum))
            if x >= prob:
                parent1 = i
                break

        prob = np.random.uniform()
        x = 0

        for i in self.population:
            x += i[1] / fit_sum
            if x >= prob:
                parent2 = i
                break

        return parent1, parent2


    def crossover(self, p1, p2):
        """
            Given two parent units p1 and p2, do a simple crossover by
            averaging their values in order to create a new child unit
        """

        ret_list = []

        for i in range(p1[0].size):
            c = (p1[0][i] + p2[0][i])/2.
            ret_list.append(c)

        return np.asarray(ret_list)

    def mutate(self, chromosome):
        """
            Given a unit, mutate its values by applying gaussian noise
            according to the parameter k
        """

        mutated = []

        for i in chromosome:
            if np.random.uniform() <= self.p:
                mutated.append(i + np.random.normal(0, self.k))
            else:
                mutated.append(i)

        return np.asarray(mutated)


