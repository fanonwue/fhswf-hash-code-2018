from input_data import InputData
from ride import Ride
from src.vehicle import Vehicle
from sys import maxsize

global_tick = 0
available_vehicles: set[int] = set()

def read_input_file(path: str) -> InputData:
    data = InputData()

    with open(path, 'r') as f:
        data.layout_from_line(f.readline())
        for line in f:
            ride = Ride.from_line(line)
            data.add_ride(ride)

    return data


def fetch_ride_from_pool(vehicle, rides) -> Ride | None:
    outstanding_rides = list(filter(lambda lambda_ride: lambda_ride.outstanding, rides))
    if len(outstanding_rides) == 0:
        # signal that ride pool is empty
        return None
    most_urgent_ride = None
    most_urgent_ride_urgency = maxsize
    vehicle_pos = vehicle.position()
    for index, ride in enumerate(outstanding_rides):
        # metrics is an aggregation of the distance to drive to the start point and the earliest start tick
        distance_to_start = abs(ride.calculate_distance_to_start(vehicle_pos[0], vehicle_pos[1]))
        time_to_start = global_tick - ride.earliest_start
        if (distance_to_start - time_to_start + ride.get_route_length()) < most_urgent_ride_urgency:
            most_urgent_ride = ride
            most_urgent_ride_urgency = distance_to_start - time_to_start

    # TODO take bonus into account
    return most_urgent_ride

def attach_ride_to_vehicle(ride, vehicle):
    vehicle.set_current_ride(ride)
    ride.outstanding = False
    pass

def move_vehicles(vehicles):
    for vehicle in list(filter(lambda lambda_vehicle: lambda_vehicle.can_move(), vehicles)):
        vehicle.drive()

def reset_vehicle_ticks(vehicles):
    for vehicle in list(filter(lambda lambda_vehicle: not lambda_vehicle.can_move(), vehicles)):
        vehicle.reset_tick()
    pass

if __name__ == '__main__':
    input_data = read_input_file("../data/b_should_be_easy.in")
    vehicles: dict[int, Vehicle] = {}
    for i in range(input_data.layout_vehicles()):
        vehicles[i+1] = Vehicle(i+1)

    is_finished = False

    while not is_finished:
        filtered_vehicles = filter(lambda v: v.is_available(), vehicles.values())
        available_vehicles = set(map(lambda v: v.id, filtered_vehicles))
        print(f"Idle vehicles: {available_vehicles}")
        for v in available_vehicles:
            vehicle = vehicles[v]
            ride = fetch_ride_from_pool(vehicle, input_data.rides())
            if ride is not None:
                attach_ride_to_vehicle(ride, vehicle)
            else:
                is_finished = True
        move_vehicles(vehicles.values())
        reset_vehicle_ticks(vehicles.values())
        global_tick += 1


    print(f"FINISHED IN {global_tick} TICKS")

    print(available_vehicles)
