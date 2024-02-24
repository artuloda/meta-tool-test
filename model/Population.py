


class Population:

    def __init__(self):
        self.individuals = list()
        self.best_individual = None


    def __str__(self) -> str:
        print('Population:', self.individuals, ' BEST SOLUTION:', self.best_individual.fitness)