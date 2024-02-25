# -*- coding: latin-1 -*-
import pandas as pd
import folium

from utils import io_utils
from utils import folium_utils
from utils import here_utils
from utils import geolocation_utils


def main(nodes_df, vehicles_df, result_dict, input_file_path, output_file_path, depot_info, city_name_zip_code_list, here_API_key):
    """
    Comprueba la  distancia entre las coodenadas proporionadas por cliente y las obtenidas de HERE
    """    
    logo_img_file = 'static/logo.png'
    colors_dataframe = pd.read_csv(input_file_path + 'map/HEXADECIMAL_COLORS.csv', sep=';', encoding='utf-8', index_col=False, decimal=',') # Dataframe con los colores
    colors = folium_utils.get_input_colors(colors_dataframe, 0) # Lista desordenada de colores en hexadecimal
    colors_high_contrast = folium_utils.get_input_colors(colors_dataframe, 1) # Lista desordenada de colores en hexadecimal

    spain_zip_codes_data = folium_utils.get_spain_zip_codes(input_file_path)
    draw_map(nodes_df, vehicles_df, result_dict, colors, colors_high_contrast, logo_img_file, depot_info, output_file_path, city_name_zip_code_list, spain_zip_codes_data, here_API_key) 


def draw_map(nodes_df, vehicles_df, result_dict, colors, colors_high_contrast, logo_img_file, depot_info, output_file_path, city_name_zip_code_list, spain_zip_codes_data, here_API_key):
    """
    Main Method: Creates HTML MAP USING FOLIUM
    """
    depot_coords = [depot_info[1], depot_info[2]]
    map_object = folium_utils.initialize_folium_map(depot_coords, logo_img_file)

    draw_zip_codes(colors_high_contrast, city_name_zip_code_list, spain_zip_codes_data, map_object)
    draw_nodes(nodes_df, colors_high_contrast, map_object)
    draw_heat_map(nodes_df, map_object)
    draw_routes(nodes_df, vehicles_df, result_dict, colors_high_contrast, map_object, here_API_key)  

    output_file_name = 'static/' + 'map-' + str(depot_info[0])
    folium_utils.create_folium_map(output_file_name, map_object) # Guarda el mapa en formato .html y ajusta ciertos parametros del mapa


def draw_zip_codes(colors_high_contrast, city_name_zip_code_list, spain_zip_codes_data, map_object):
    """
    """
    layer_color = '#00008B'
    layer_txt = 'Codigos Postales'
    initial_show = False
    dynamic = False
    zip_codes_layer = folium_utils.create_feature_group_folium(map_object, layer_color, layer_txt, initial_show, dynamic)

    index_color = 0
    for file, geojson in spain_zip_codes_data.items():
        if not file in city_name_zip_code_list:
            continue
        polygon_color, index_color = folium_utils.get_node_color(index_color, colors_high_contrast)
        for position in range(len(geojson['features'])):
            single_geojson = geojson['features'][position]
            single_geojson_id = single_geojson['properties']['COD_POSTAL']
            tooltip = layer_txt + ' - ' + str(file) + ' CP:' + str(single_geojson_id) 
            folium_utils.add_polygon_to_map(single_geojson, zip_codes_layer, polygon_color, tooltip, tooltip)


def draw_nodes(nodes_df, colors_high_contrast, map_object):
    """
    """
    nodes_by_province_df_list = io_utils.cluster_dataframe_by_condition(nodes_df, 'Province')
    layer_color = '#00008B'
    layer_txt = 'Nodos Totales'
    initial_show = False
    dynamic = False
    index_color = 0
    nodes_layer = folium_utils.create_feature_group_folium(map_object, layer_color, layer_txt, initial_show, dynamic)
    for nodes_by_province_df in nodes_by_province_df_list:
        province = nodes_by_province_df['Province'].values[0]
        node_color, index_color = folium_utils.get_node_color(index_color, colors_high_contrast)
        for index, node in nodes_by_province_df.iterrows():
            node_id = node['Id']
            node_name = node['Name']
            address = node['Address']
            location = node['Location']
            province = node['Province']
            zip_code = node['Zip_Code']
            node_type = node['Node_Type']
            weight = node['Weight']
            lat = node['Latitude']
            long = node['Longitude']

            icon_name = get_icon_name(node_type)
            #print(node_type, icon_name)
            tooltip_folium = 'Node: ' + str(node_id) + '-' + str(node_name)
            add_html_node(nodes_layer, node_color, tooltip_folium, node_id, node_name, address, location, province, zip_code, node_type, weight, lat, long, icon_name)


def get_icon_name(node_type):
    """
    """
        
    # icon_dict = {'PSIQUIÁTRICO': 'meh-oh',
    # 'MÉDICO-QUIRÚRGICO': 'user-md',
    # 'GENERAL': 'hospital-o',
    # 'GERIATRÍA Y/O LARGA ESTANCIA': 'ambulance',
    # 'REHABILITACIÓN PSICOFÍSICA': 'wheelchair',
    # 'MATERNO-INFANTIL': 'smile-o',
    # 'QUIRÚRGICO': 'gears',
    # 'INFANTIL': 'lemon-o',
    # 'TRAUMATOLOGÍA Y/O REHABILITACIÓN': 'wheelchair-alt',
    # 'OTROS MONOGRÁFICOS': 'stethoscope',
    # 'OFTÁLMICO U ORL': 'eye',
    # 'ONCOLÓGICO': 'life-buoy',
    # 'OTRA FINALIDAD': 'medkit',
    # 'MATERNAL': 'heart'}

    icon_dict = {'PSIQUIÁTRICO': 'glyphicon-filter',
    'MÉDICO-QUIRÚRGICO': 'glyphicon-plus-sign',
    'GENERAL': 'glyphicon-plus',
    'GERIATRÍA Y/O LARGA ESTANCIA': 'glyphicon-apple',
    'REHABILITACIÓN PSICOFÍSICA': 'glyphicon-apple',
    'MATERNO-INFANTIL': 'glyphicon-asterisk',
    'QUIRÚRGICO': 'glyphicon-apple',
    'INFANTIL': 'glyphicon-apple',
    'TRAUMATOLOGÍA Y/O REHABILITACIÓN': 'glyphicon-cog',
    'OTROS MONOGRÁFICOS': 'glyphicon-ice-lolly',
    'OFTÁLMICO U ORL': 'glyphicon-eye-open',
    'ONCOLÓGICO': 'glyphicon-piggy-bank',
    'OTRA FINALIDAD': 'glyphicon-asterisk',
    'MATERNAL': 'glyphicon-piggy-bank',
    'Depot': 'glyphicon-home'}

    try:
        icon_name = icon_dict[node_type]
    except:
        icon_name = 'glyphicon-tint'
    return icon_name


def add_html_node(nodes_layer, node_color, tooltip_folium, node_id, node_name, address, location, province, zip_code, node_type, weight, lat, long, icon_name):
    """
    """
    left_col_color = '#36454F'
    right_col_color = '#FBFBF9'

    html = folium_utils.add_beggining_HTML_table(node_id)
    html = html + folium_utils.add_row_to_HTML_table('Identificador Nodo', node_id, None, left_col_color, right_col_color)
    html = html + folium_utils.add_row_to_HTML_table('Nombre', node_name, None, left_col_color, right_col_color)
    html = html + folium_utils.add_row_to_HTML_table('Dirección', address, None, left_col_color, right_col_color)
    html = html + folium_utils.add_row_to_HTML_table('Localidad', location, None, left_col_color, right_col_color)
    html = html + folium_utils.add_row_to_HTML_table('Provincia', province, None, left_col_color, right_col_color)
    html = html + folium_utils.add_row_to_HTML_table('Código Postal', zip_code, None, left_col_color, right_col_color)
    html = html + folium_utils.add_row_to_HTML_table('Tipo Nodo', node_type, None, left_col_color, right_col_color)
    html = html + folium_utils.add_row_to_HTML_table('Peso', weight, 'kg.', left_col_color, right_col_color)
    html = html + folium_utils.add_row_to_HTML_table('Latitud', lat, None, left_col_color, right_col_color)
    html = html + folium_utils.add_row_to_HTML_table('Longitud', long, None, left_col_color, right_col_color)
    html = html + folium_utils.add_end_HTML_table()

    tooltip_folium = 'NODO: ' + str(node_id)
    popUP = folium.Popup(folium.Html(html, script=True), max_width=500)
    folium.Marker(location=[lat, long],
                popup=popUP,
                tooltip=tooltip_folium, 
                name=node_name, 
                icon=folium.Icon(color='black', icon=icon_name, icon_color=node_color)).add_to(nodes_layer)
                #   icon=folium.Icon(color='cadetblue', icon=icon_name, icon_color=node_color, prefix='fa')).add_to(nodes_layer)


def draw_routes(nodes_df, vehicles_df, result_dict, colors_high_contrast, map_object, here_API_key):
    """
    """
    index_color = 0
    for vehicle, route_nodes in result_dict.items():
        layer_color = '#FF0000'
        layer_txt = 'Ruta ' + str(vehicle)
        initial_show = False
        dynamic = False
        route_layer = folium_utils.create_feature_group_folium(map_object, layer_color, layer_txt, initial_show, dynamic)
        node_color, index_color = folium_utils.get_node_color(index_color, colors_high_contrast)
        latitudes = list()
        longitudes = list()
        for node_id in route_nodes:
            node_df = nodes_df[nodes_df['Id'] == node_id]
            node_id = node_df['Id'].values[0]
            node_name = node_df['Name'].values[0]
            address = node_df['Address'].values[0]
            location = node_df['Location'].values[0]
            province = node_df['Province'].values[0]
            zip_code = node_df['Zip_Code'].values[0]
            node_type = node_df['Node_Type'].values[0]
            weight = node_df['Weight'].values[0]
            lat = node_df['Latitude'].values[0]
            long = node_df['Longitude'].values[0]

            latitudes.append(lat)
            longitudes.append(long)

            icon_name = get_icon_name(node_type)
            #print(node_type, icon_name)
            tooltip_folium = 'Node: ' + str(node_id) + '-' + str(node_name)
            add_html_node(route_layer, node_color, tooltip_folium, node_id, node_name, address, location, province, zip_code, node_type, weight, lat, long, icon_name)

        coordinates = geolocation_utils.create_list_of_list_coordinates(latitudes, longitudes)
        if len(coordinates) > 2:
            route_info_here = here_utils.calculate_route_HERE(coordinates, 'car', here_API_key)
            route_coordinates_here = route_info_here[0]
            route_distance = route_info_here[1]
            route_time = route_info_here[2]
            print('La ruta:', layer_txt, ' tiene una distancia de ', route_distance, ' y un tiempo de ', route_time)
            folium_utils.add_route_to_map(route_coordinates_here, node_color, layer_txt, route_layer, 2)


def draw_heat_map(nodes_df, map_object):
    """
    """
    layer_color = '#00008B'
    layer_txt = 'Mapa Calor'
    initial_show = False
    dynamic = False
    heat_map_layer = folium_utils.create_feature_group_folium(map_object, layer_color, layer_txt, initial_show, dynamic)

    selected_columns = nodes_df[['Latitude', 'Longitude', 'Items']]
    heat_map_data = selected_columns.values.tolist() # Convierte estas columnas en una lista de listas
    folium_utils.add_heat_map(heat_map_data, heat_map_layer)

