import algorithm
import numpy as np
import time


# def main():
if __name__ == '__main__':
    start_time = time.time()
    random_seed = 123456789
    np.random.seed(random_seed)

    # Read Parameters
    parameters = algorithm.Parameters()
    print(parameters)

    # Create Instance
    instance = algorithm.Instance(parameters)
    print(instance.nodes_df)
    print(instance.fleet_df)

    solution = algorithm.Solution(parameters, instance)

    print('____________________________________________________________________________________')
    print('------------------------------------------------------------------------------------')
    print('                                    END ALGORITHM                                   ')
    print('____________________________________________________________________________________')
    print('------------------------------------------------------------------------------------')
    end_time = time.time()
    print(solution.best_solution)
    print('Best FITNESS:', solution.fitness)
    print("Total Execution Time: " + str(round(end_time - start_time, 2)) + "s")
    # Execute Algorithm
    #result_dict, result_df = algorithm.main(input_file_path, output_file_path, nodes_df, vehicles_df)
    # result_dict, result_df = cvrp.main(input_file_path, output_file_path, nodes_df, vehicles_df)

    # # Draw Result into Map
    # draw_map.main(nodes_df, vehicles_df, result_dict, input_file_path, output_file_path, depot_info, city_name_zip_code_list, here_API_key)


# def main(input_file_path, output_file_path, here_API_key):

#     # Parameters and main variables
#     input_file_path = 'input_files/'
#     output_file_path = 'output_files/'

#     input_file_name = 'hospitalesEspanaDataSet.csv'
#     vehicles_file_name = 'vehicles.csv'

#     city_name_zip_code_list = ['SEVILLA', 'CADIZ', 'HUELVA', 'MADRID', 'BARCELONA']
#     depot_info = ['Depot', 37.38882519822593, -6.001603318439839]

#     # Process input data
#     nodes_df, vehicles_df = create_data.main(input_file_path, input_file_name, vehicles_file_name)

#     # Execute Algorithm
#     #result_dict, result_df = algorithm.main(input_file_path, output_file_path, nodes_df, vehicles_df)
#     result_dict, result_df = cvrp.main(input_file_path, output_file_path, nodes_df, vehicles_df)

#     # Draw Result into Map
#     draw_map.main(nodes_df, vehicles_df, result_dict, input_file_path, output_file_path, depot_info, city_name_zip_code_list, here_API_key)

#     return nodes_df, vehicles_df, result_df

