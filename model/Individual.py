import numpy as np
from scipy.spatial.distance import cdist, pdist, squareform
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
        client_demands =  self.instance.nodes_df['Items'].tolist()  # Agregar los pesos de los nodos
        vehicle_capacities =  self.instance.fleet_df['Capacity'].tolist()  # Capacidades de los vehículos

        print(client_demands, vehicle_capacities)
        # Initial Solution
        print("Creating Initial Solution...")
        self.initialize_routes()
        self.improve_single_route()


    def initialize_routes(self):
        # Index of the depot node
        depot_index = self.instance.nodes_df[self.instance.nodes_df['Node_Type'] == 'Depot'].index.item()
        client_indices = self.instance.nodes_df[self.instance.nodes_df['Node_Type'] != 'Depot'].index.tolist()

        n_vehicles = len(self.instance.fleet_df)
        if len(client_indices) < n_vehicles:
            raise ValueError("More vehicles than clients!")

        # Initialize clusters and vehicle loads
        clusters = {i: [] for i in range(n_vehicles)}
        vehicle_loads = {i: 0 for i in range(n_vehicles)}
        vehicle_capacities = self.instance.fleet_df['Capacity'].tolist()

        # Convert the full distance matrix to a condensed form required by linkage
        condensed_distance_matrix = squareform(self.instance.distance_matrix[client_indices][:, client_indices])

        # Perform hierarchical clustering
        Z = linkage(condensed_distance_matrix, 'ward')

        # Determine the number of clusters based on the vehicle capacities
        clusters_labels = fcluster(Z, n_vehicles, criterion='maxclust')

        # Map cluster labels to vehicle indices
        label_to_vehicle = {label: idx for idx, label in enumerate(np.unique(clusters_labels))}

        # Assign clients to clusters based on labels
        for client_idx, label in zip(client_indices, clusters_labels):
            client_demand = self.instance.nodes_df.at[client_idx, 'Items']
            vehicle_idx = label_to_vehicle[label]

            if vehicle_loads[vehicle_idx] + client_demand <= vehicle_capacities[vehicle_idx]:
                clusters[vehicle_idx].append(client_idx)
                vehicle_loads[vehicle_idx] += client_demand
            else:
                # If the vehicle is full, try to assign the client to another vehicle
                for other_vehicle_idx in range(n_vehicles):
                    if vehicle_loads[other_vehicle_idx] + client_demand <= vehicle_capacities[other_vehicle_idx]:
                        clusters[other_vehicle_idx].append(client_idx)
                        vehicle_loads[other_vehicle_idx] += client_demand
                        break
                else:
                    # If no vehicle has enough capacity, raise an error
                    raise ValueError(f"No vehicle with enough capacity for client {client_idx}")

        # Add the depot at the start and end of each route
        depot_node = model.Node(self.parameters, self.instance, 0)
        initial_routes = list()   
        for vehicle_index in clusters:
            if clusters[vehicle_index]:                
                route = model.Route(self.parameters, self.instance, vehicle_index + 1) # Create Route
                route.nodes.append(depot_node) # Add depot start                
                for node_id in clusters[vehicle_index]: # Add nodes in route
                    current_node = model.Node(self.parameters, self.instance, node_id)
                    route.nodes.append(current_node)
                route.nodes.append(depot_node) # Add depot end

                route.fitness = route.calculate_route_distance()
                route.load = route.calculate_route_load()
                initial_routes.append(route)

        # Set routes
        self.routes = initial_routes
        

    def improve_single_route(self):
        
        print("Executing 2-opt, 3-opt...")
        for route in self.routes:
            print('Mejorando Ruta:', route.id, '... FITNESS:', route.fitness)
            route.two_opt() # Apply 2-opt to each route
            print('\tFitness tras 2-opt:', route.id, '... FITNESS:', route.fitness)

            route.three_opt_first_improvement() # Apply 3-opt to each route
            print('\tFitness tras 3-opt:', route.id, '... FITNESS:', route.fitness)
            print('----------------------------------------------------------------')


    def print_solution(self):
        for route in self.routes:
            print(route)

    def __str__(self) -> str:
        print('Individual:', self.is_valid, ' Fitness:', self.fitness)