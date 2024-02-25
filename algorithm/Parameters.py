from utils import IO

class Parameters:
    def __init__(self):  

        self.IO = IO()
        parameters_df = self.IO.read_csv(file_path='input_files/parameters.csv', separator=';', decimal='.', encoding='utf-8')
        parameters_dict = dict(zip(parameters_df['Parameter'], parameters_df['Value']))
        self.input_file_path = str(parameters_dict['input_file_path'])
        self.output_file_path = str(parameters_dict['output_file_path'])
        self.input_file_name = str(parameters_dict['input_file_name'])
        self.fleet_file_name = str(parameters_dict['fleet_file_name'])
        self.here_API_key = str(parameters_dict['here_API_key'])
        self.city_name_zip_code_list = eval(parameters_dict['city_name_zip_code_list'])
        self.TAM_POPULATION = int(parameters_dict['TAM_POPULATION'])

    def __str__(self) -> str:
        class_str = 'Instance input_file_path: ' + str(self.input_file_path) + '\n'
        class_str += 'Instance output_file_path: ' + str(self.output_file_path) + '\n'
        class_str += 'Instance input_file_name: ' + str(self.input_file_name) + '\n'
        class_str += 'Instance fleet_file_name: ' + str(self.fleet_file_name) + '\n'
        class_str += 'Instance here_API_key: ' + str(self.here_API_key) + '\n'
        class_str += 'Instance city_name_zip_code_list: ' + str(self.city_name_zip_code_list) + '\n'
        class_str += 'Instance TAM_POPULATION: ' + str(self.TAM_POPULATION) + '\n'
        return class_str
