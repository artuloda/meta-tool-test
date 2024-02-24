


class Vehicle:

    def __init__(self, id, capacity, tw_start, tw_end, vehicle_type):
        self.id = id
        self.capacity = capacity
        self.tw_start = tw_start
        self.tw_end = tw_end
        self.vehicle_type = vehicle_type


    def __str__(self) -> str:
        print('Vehicle:', self.id, ' Capacity:', self.capacity, ' Type:', self.vehicle_type)