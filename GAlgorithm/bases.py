
import random
import operator
from math import ceil
from statistics import pstdev


class AbstractIndividual:
    def __init__(self, genes):
        '''An individual has a list of defining properties, known as genes. pass them in here.'''
        self._genes = genes
        self.fitness_is_unset = True


    @property
    def genes(self):
        return self._genes


    @genes.setter
    def genes(self, val):
        self._genes = val
        self.clear_fitness()


    @property
    def fitness(self):
        '''retreives the fitness of this route.
        You must call the "calc_fitness" method before
        accessing this property'''
        return self._fitness


    @fitness.setter
    def fitness(self, val):
        '''Sets the fitness value'''
        self._fitness = val
        self.fitness_is_unset = False


    def clear_fitness(self):
        '''Clears the fitness value.
        This forces a re-computation of the fitness'''
        self.fitness_is_unset = True


    def compute_fitness(self):
        '''Calculates fitness of this individual.
        Must assign the self.fitness value'''
        assert False, 'You must implement the "compute_fitness" method in the Individual class'


    def make_training_data(self):
        '''Makes X training data for the classifier'''
        assert False, 'You must implement the "make_training_data" method to use the classifier'


    def copy(self):
        '''Copies this individual based on whatever it is subclassed into'''
        return type(self)(self.genes.copy())


    def serialize(self):
        '''Export self as json dump compatible'''
        d = self.__dict__
        d['__Individual__'] = True
        return d


    def __len__(self):
        return len(self.genes)


    def __str__(self):
        return [c for c in self.genes]


class Population:
    def __init__(self, individuals:list):
        '''The population of individuals'''
        self.individuals = individuals
        self.original_size = len(self.individuals)
        self.f_evals = 0


    def add(self, pop):
        '''adds another population to this population'''
        self.individuals.extend(pop.individuals)


    def random_individual(self):
        '''Returns a random individual from the population'''
        return random.choice(self.individuals)


    def evaluate(self) -> int:
        '''Runs the objective function on the individuals in place
        Returns the number of times the objective function was run'''
        count = 0
        for i in self.individuals:
            if i.fitness_is_unset:
                i.compute_fitness()
                count += 1
            else:
                pass
        self.f_evals += count
        return count


    def rank(self):
        '''Ranks the list of individuals within this population'''
        self.individuals.sort(key=operator.attrgetter('fitness'), reverse=True)


    def copy(self):
        '''Returns a copy of this population
        Each individual will be copied'''
        new_inds = []
        for ind in self.individuals:
            new_inds.append(ind.copy())
        return Population(new_inds)


    @property
    def ranked(self):
        '''Returns the ranked routes, but doesn't change the internal state'''
        return sorted(self.individuals, key=operator.attrgetter('fitness'), reverse=True)


    @property
    def genes(self):
        '''Returns a copied list of the cities in the first route'''
        return self.individuals[0].genes.copy()


    @property
    def best_individual(self):
        '''Returns the individual route with the best fitness in this population'''
        return max(self.individuals, key=operator.attrgetter('fitness'))


    @property
    def mean_individual(self):
        '''Returns the individual route with the mean fitness in this population'''
        ranked = self.ranked
        num = len(ranked)
        mean_idx = int(num/2)
        return ranked[mean_idx]


    @property
    def max_fitness(self):
        '''Finds the maximum fitness route of the population'''
        return max(self.individuals, key=operator.attrgetter('fitness')).fitness


    @property
    def min_fitness(self):
        '''Finds the minimum fitness route of the population'''
        return min(self.individuals, key=operator.attrgetter('fitness')).fitness


    @property
    def mean_fitness(self):
        '''Finds the mean fitness of the population'''
        fitnesses = [i.fitness for i in self.individuals]
        return sum(fitnesses) / len(fitnesses)


    def get_percentile(self, k):
        '''returns the kth percentile individual'''
        index = ceil(k * len(self.individuals))
        return [r for i,r in enumerate(self.individuals) if i == index][0]


    def get_standard_deviation(self):
        '''Returns the standard deviation of the population's fitness'''
        fitnesses = [i.fitness for i in self.individuals]
        return pstdev(fitnesses)


    def serialize(self):
        '''Export self as json file'''
        return self.__dict__ #{'routes': len(self.routes), 'cities': len(self.routes[0])}


    def __repr__(self):
        return f'Pop; routes: {len(self.individuals)}; cities: {len(self.individuals[0])}'