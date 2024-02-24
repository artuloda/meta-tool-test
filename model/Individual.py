


class Individual:

    def __init__(self):
        self.is_valid = False
        self.fitness = None


    def __str__(self) -> str:
        print('Individual:', self.is_valid, ' Fitness:', self.fitness)