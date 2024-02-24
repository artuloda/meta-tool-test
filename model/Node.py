


class Node:

    def __init__(self, id, demand, latitude, longitude, tw_start, tw_end, node_type):
        self.id = id
        self.demand = demand
        self.latitude = latitude
        self.longitude = longitude
        self.tw_start = tw_start
        self.tw_end = tw_end
        self.node_type = node_type


    def __str__(self) -> str:
        print('Node:', self.id, ' Demand:', self.demand, ' Coords:', self.latitude, ' - ', self.longitude)