import model


class Route:

    def __init__(self, parameters, instance, id):
        self.parameters = parameters
        self.instance = instance
        self.id = id
        self.nodes = list()
        self.load = 0
        self.vehicle = None
        self.fitness = 100_000_000

        self.set_vehicle()


    def set_vehicle(self):
        """
        """
        self.vehicle = model.Vehicle(self.parameters, self.instance, self.id)


    # Function to calculate the total load of a route
    def calculate_route_load(self):
        total_load = 0
        for node in self.nodes:
            total_load += node.items
        return total_load


    # Function to calculate the total distance of a route
    def calculate_route_distance(self):
        return sum(self.instance.distance_matrix[self.nodes[i].id, self.nodes[i+1].id] for i in range(len(self.nodes)-1))
        

    # Functions to apply 2-opt optimization on a single route
    def two_opt(self):
        best_distance = self.fitness
        print("aaa", self.nodes)
        improved = True
        while improved:
            improved = False
            for i in range(1, len(self.nodes) - 2):
                for j in range(i + 1, len(self.nodes) - 1):
                    new_route = self.nodes[:i] + self.nodes[i:j+1][::-1] + self.nodes[j+1:]
                    print('bbb', new_route)
                    new_distance = self.calculate_route_distance()
                    if new_distance < best_distance:
                        self.nodes = new_route
                        self.fitness = new_distance
                        improved = True


    # Functions to apply 3-opt in fisrt improvement
    def three_opt_first_improvement(self, max_segment_length=10):
        """Applies a limited 3-opt search that looks for the first improvement."""
        length = len(self.nodes)
        improved = True
        while improved:
            improved = False
            for i in range(1, length - 2):
                for j in range(i + 1, min(i + max_segment_length, length - 1)):
                    for k in range(j + 1, min(j + max_segment_length, length)):
                        before_change = self.calculate_route_distance()                
                        self.reverse_segment_if_improves(i, j) # Try reversing the segment [i, j]           
                        self.reverse_segment_if_improves(j, k) # Try reversing the segment [j, k]                    
                        after_change = self.calculate_route_distance() # Check if there was an improvement
                        if after_change < before_change:
                            improved = True
                            break  # Exit the innermost loop on the first improvement
                        else:
                            # Revert changes if no improvement
                            self.reverse_segment_if_improves(j, k)  # Revert previous reversal
                            self.reverse_segment_if_improves(i, j)  # Revert first reversal
                    if improved:
                        break  # Break the second loop if improved
                if improved:
                    break  # Break the outer loop if improved


    def reverse_segment_if_improves(self, start, end):
        """Reverses the segment in the route if it results in an improvement."""
        self.nodes[start:end] = self.nodes[start:end][::-1]


    def __str__(self) -> str:
        route_str = 'Vehicle: ' +  str(self.vehicle.name) + ' Fitness: ' +  str(self.fitness) + ' Load: ' +  str(self.load) + ' Total Nodes: ' +  str(len(self.nodes)) + ' ---> '
        for node in self.nodes:
            route_str += str(node.id) + '-'
        return route_str[:-1]