from model import Individual

class Population:

    def __init__(self, parameters, instance):
        self.parameters = parameters
        self.instance = instance
        self.individuals = list()
        self.individuals_fitness = list()
        self.best_individual = None
        self.best_fitness = 0

    def construct(self):
        """
        """
        # Creation
        for iteration in range(self.parameters.TAM_POPULATION):
            print('Start Iteration:', iteration, '...')
            individual = Individual(self.parameters, self.instance)
            individual.solve_cvrp()
            self.individuals.append(individual)
            self.individuals_fitness.append(individual.fitness)
            print('End Iteration:', iteration, ' FITNESS:', individual.fitness)

        # Evaluation
        best_solution_index = self.individuals_fitness.index(min(self.individuals_fitness))
        self.best_individual = self.individuals[best_solution_index]
        self.best_fitness = self.individuals_fitness[best_solution_index]
        

    def __str__(self) -> str:
        print('Population:', self.individuals, ' BEST SOLUTION:', self.best_individual.fitness)