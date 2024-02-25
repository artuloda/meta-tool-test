from model import Population


class Solution:

    def __init__(self, parameters, instance):
        self.parameters = parameters
        self.instance = instance
        self.best_solution = None
        self.fitness = None

        self.constructive()


    def constructive(self):
        population = Population(self.parameters, self.instance)
        population.construct()
        self.best_solution = population.best_individual
        self.fitness = population.best_fitness


    def __str__(self) -> str:
        print('Solution:', self.best_solution)