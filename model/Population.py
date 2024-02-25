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
            individual, individual_fitness = self.create_individual() 
            self.individuals.append(individual)
            self.individuals_fitness.append(individual_fitness)
            print('End Iteration:', iteration)

        # Evaluation
        best_solution_index = self.individuals_fitness.index(min(self.individuals_fitness))
        self.best_individual = self.individuals[best_solution_index]
        self.best_fitness = self.individuals_fitness[best_solution_index]
        

    def create_individual(self):
        """
        """
        individual = Individual(self.parameters, self.instance)
        routes, individual_fitness = individual.solve_cvrp()


        return routes, individual_fitness

    def __str__(self) -> str:
        print('Population:', self.individuals, ' BEST SOLUTION:', self.best_individual.fitness)