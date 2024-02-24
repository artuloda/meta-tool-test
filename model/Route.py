


class Route:

    def __init__(self, id):
        self.id = id
        self.nodes = list()
        self.load = 0
        self.vehicle = None
        self.fitness = 0

    def __str__(self) -> str:
        print('Route:', self.id, ' Vehicle:', self.vehicle, ' Load:', self.load, ' Fitness:', self.fitness, ' Nodes:', self.nodes)