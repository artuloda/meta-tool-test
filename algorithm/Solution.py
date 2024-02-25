from model import Population
from utils import IO

class Solution:

    def __init__(self, parameters, instance):
        self.IO = IO()
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

    
    def save_solution(self):
        result_routes_list = []
        for route in self.best_solution.routes:
            vehicle_id = route.vehicle.name
            for node in route.nodes:
                row = {
                'Vehicle': vehicle_id,
                'Id': node.id,
                'Name': node.name,
                'Address': node.address,
                'Location': node.location,
                'Province': node.province,
                'Zip_Code': node.zip_code,
                'Items': node.items,
                'Weight': node.weight,
                'Node_Type': node.node_type,
                'TW_Start': node.tw_start,
                'TW_End': node.tw_end,
                'Latitude': node.latitude,
                'Longitude': node.longitude,
                'Email': node.email,
                'Phone': node.phone,
                }
            result_routes_list.append(row)
        columns_name =['Vehicle', 'Id', 'Name', 'Address', 'Location', 'Province', 'Zip_Code', 'Items', 'Weight', 'Node_Type', 'TW_Start','TW_End', 'Latitude', 'Longitude', 'Email', 'Phone']
        result_df = self.IO.create_dataframe(result_routes_list, columns_name)
        self.IO.create_csv(result_df, self.parameters.output_file_path + 'results')

    def __str__(self) -> str:
        print('Solution:', self.best_solution)