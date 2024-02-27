import numpy as np
from scipy.spatial.distance import squareform
from scipy.cluster.hierarchy import fcluster, linkage

import model

class Individual:

    def __init__(self, parameters, instance):
        self.parameters = parameters
        self.instance = instance
        self.routes = list()
        self.is_valid = False
        self.fitness = None


    # Main function to solve the CVRP
    def solve_cvrp(self):

        print("Start Creating Initial Solution...")
        self.initialize_routes_hierarchical_clustering()
        #self.initialize_routes_nearest_neighbor()
        print("End Creating Initial Solution...")

        print("Start Improving Each Initial Route...")
        self.improve_single_route()
        print("End Improving Each Initial Route. Current Fitness:", self.fitness)

        print("Start Improving Routes...")
        self.improve_routes()
        print("End Improving Routes. Current Fitness:", self.fitness)


    def initialize_routes_hierarchical_clustering(self):
        """
        Generate an initial feasible solution for the Vehicle Routing Problem using
        the hierarchical clustering considering vehicles capacities
        """
        # Index of the depot node
        depot_index = self.instance.nodes_df[self.instance.nodes_df['Node_Type'] == 'Depot'].index.item()
        client_indices = self.instance.nodes_df[self.instance.nodes_df['Node_Type'] != 'Depot'].index.tolist()

        # Ensure we have vehicle IDs in the correct format (assuming they are in self.instance.fleet_df['Id'])
        vehicle_ids = self.instance.fleet_df['Id'].tolist()
        n_vehicles = len(vehicle_ids)
        if len(client_indices) < n_vehicles:
            raise ValueError("More vehicles than clients!")

        # Initialize clusters and vehicle loads using vehicle IDs
        routes = {vehicle_id: [] for vehicle_id in vehicle_ids}
        vehicle_loads = {vehicle_id: 0 for vehicle_id in vehicle_ids}
        vehicle_capacities = {vehicle_id: capacity for vehicle_id, capacity in zip(vehicle_ids, self.instance.fleet_df['Capacity'].tolist())}

        # Convert the full distance matrix to a condensed form required by linkage
        condensed_distance_matrix = squareform(self.instance.distance_matrix[client_indices][:, client_indices])

        # Perform hierarchical clustering
        Z = linkage(condensed_distance_matrix, 'ward')

        # Determine the number of routes based on the vehicle capacities
        routes_labels = fcluster(Z, n_vehicles, criterion='maxclust')

        # Map cluster labels to vehicle IDs
        label_to_vehicle_id = {label: vehicle_id for label, vehicle_id in zip(np.unique(routes_labels), vehicle_ids)}

        # Assign clients to routes based on labels
        for client_idx, label in zip(client_indices, routes_labels):
            client_demand = self.instance.nodes_df.at[client_idx, 'Items']
            vehicle_id = label_to_vehicle_id[label]

            if vehicle_loads[vehicle_id] + client_demand <= vehicle_capacities[vehicle_id]:
                routes[vehicle_id].append(client_idx)
                vehicle_loads[vehicle_id] += client_demand
            else:
                # If the vehicle is full, try to assign the client to another vehicle
                for other_vehicle_id in vehicle_ids:
                    if vehicle_loads[other_vehicle_id] + client_demand <= vehicle_capacities[other_vehicle_id]:
                        routes[other_vehicle_id].append(client_idx)
                        vehicle_loads[other_vehicle_id] += client_demand
                        break
                else:
                    # If no vehicle has enough capacity, raise an error
                    raise ValueError(f"No vehicle with enough capacity for client {client_idx}")

        # Convert route indices to client IDs
        for vehicle_id in routes:
            routes[vehicle_id] = [self.instance.nodes_df.at[idx, 'Id'] for idx in routes[vehicle_id]]

        # Create Routes Objects
        print(routes)
        self.create_routes_object(routes)


    def initialize_routes_nearest_neighbor(self):
        """
        Generate an initial feasible solution for the Vehicle Routing Problem using
        the Nearest Neighbor heuristic.
        """
        
        # Initialize a dictionary to hold the routes for each vehicle
        routes = {}
        for vehicle in self.instance.fleet_df.itertuples():
            routes[vehicle.Id] = []
        
        # Set of all nodes that have not been visited, excluding the depot
        # Assuming the depot's 'Id' is known and is the first in nodes_df
        depot_id = self.instance.nodes_df.iloc[0]['Id']
        unvisited_nodes = set(self.instance.nodes_df['Id']) - {depot_id}
        
        # Iterate over each vehicle to create a route
        for vehicle in self.instance.fleet_df.itertuples():
            if unvisited_nodes:
                # Start with a random node from the unvisited set
                current_node = unvisited_nodes.pop()
                route = [current_node]
                capacity_remaining = vehicle.Capacity  # Initialize vehicle's remaining capacity
                
                # Continue creating the route until there are no unvisited nodes or capacity is full
                while unvisited_nodes and capacity_remaining > 0:
                    last_node = route[-1]
                    nearest_next = None
                    min_dist = float('inf')
                    
                    # Find the nearest unvisited node
                    for next_node in unvisited_nodes:
                        dist = self.instance.distance_matrix[last_node, next_node]
                        if dist < min_dist:
                            min_dist = dist
                            nearest_next = next_node
                    
                    # Check if the nearest node can be added to the route considering the remaining capacity
                    if nearest_next:
                        next_node_items = self.instance.nodes_df[self.instance.nodes_df['Id'] == nearest_next]['Items'].values[0]
                        if next_node_items <= capacity_remaining:
                            unvisited_nodes.remove(nearest_next)  # Mark the node as visited
                            route.append(nearest_next)  # Add node to the route
                            capacity_remaining -= next_node_items  # Update capacity
                        else:
                            break  # Break if no more nodes can be added to the route
                    else:
                        break  # If no nearest node was found, break the loop
                    
                # Assign the created route to the vehicle
                routes[vehicle.Id] = route
                # Break out of the loop if there are no more unvisited nodes
                if not unvisited_nodes:
                    break

        # Once all routes are generated, create Routes Objects
        print(routes)
        self.create_routes_object(routes)


    def create_routes_object(self, routes):
        """
        """
        # Add the depot at the start and end of each route
        depot_node = model.Node(self.parameters, self.instance, 0)
        initial_routes = list()   
        for vehicle_index in routes:
            if routes[vehicle_index]:                
                route = model.Route(self.parameters, self.instance, vehicle_index) # Create Route
                route.nodes.append(depot_node) # Add depot start                
                for node_id in routes[vehicle_index]: # Add nodes in route
                    current_node = model.Node(self.parameters, self.instance, node_id)
                    route.nodes.append(current_node)
                route.nodes.append(depot_node) # Add depot end

                route.fitness = route.calculate_route_distance(route.nodes)
                route.load = route.calculate_route_load()
                initial_routes.append(route)

        # Set routes
        self.routes = initial_routes
        

    def improve_single_route(self):
        """
        Apply routes improvements to each route created in initial solution
        """
        print("Executing 2-opt, 3-opt...")
        solution_fitness = 0
        for route in self.routes:
            print('Mejorando Ruta:', route.id, '... FITNESS:', route.fitness)

            route.two_opt() # Apply 2-opt to each route
            print('\tFitness tras 2-opt:', route.id, '... FITNESS:', route.fitness)

            route.three_opt_first_improvement() # Apply 3-opt first improvent to each route
            print('\tFitness tras 3-opt first improvement:', route.id, '... FITNESS:', route.fitness)

            route.three_opt() # Apply 3-opt to each route
            print('\tFitness tras 3-opt:', route.id, '... FITNESS:', route.fitness)

            route.lin_kernighan(max_iter=10000, max_time_seconds=60) # Apply lin_kernighan to each route
            print('\tFitness tras lin_kernighan:', route.id, '... FITNESS:', route.fitness)

            solution_fitness = solution_fitness + route.fitness
            print('----------------------------------------------------------------')
        self.fitness = solution_fitness

    def improve_routes(self):
        i = 0

    def print_solution(self):
        for route in self.routes:
            print(route)

    def __str__(self) -> str:
        ind_str = 'Fitness: ' + str(self.fitness) + '\n'
        for route in self.routes:
            ind_str += str(route) + '\n'
        return ind_str