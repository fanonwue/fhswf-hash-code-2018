from input_data import InputData
from ride import Ride
from src.vehicle import Vehicle
from sys import maxsize
from functools import cmp_to_key, reduce

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
    sorted_rides = sorted(outstanding_rides, key=cmp_to_key(lambda r1, r2: r1.calculate_slack() - r2.calculate_slack()))
    for ride in sorted_rides:
        # metrics is an aggregation of the distance to drive to the start point and the earliest start tick
        distance_to_start = abs(ride.calculate_distance_to_start(vehicle_pos[0], vehicle_pos[1]))
        time_to_start = global_tick - ride.earliest_start
        time_to_finish = global_tick - ride.latest_finish
        ride_length_total = distance_to_start + ride.get_route_length()
        can_finish_ride = time_to_finish <= ride_length_total
        if ((distance_to_start - time_to_start + ride.get_route_length()) < most_urgent_ride_urgency) and can_finish_ride:
            most_urgent_ride = ride
            most_urgent_ride_urgency = distance_to_start - time_to_start

    # TODO take bonus into account
    return most_urgent_ride

def fetch_vehicle_for_ride(ride, vehicles: list[Vehicle]) -> Vehicle | None:
    nearest_vehicle = None
    for vehicle in vehicles:



        pass

def attach_ride_to_vehicle(ride, vehicle):
    vehicle.set_current_ride(ride)
    ride.outstanding = False
    pass

def move_vehicles(vehicles):
    for vehicle in list(filter(lambda lambda_vehicle: lambda_vehicle.can_move(), vehicles)):
        vehicle.drive(current_tick = global_tick)

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

    # start alternative implementation
    # while not is_finished:
    #     outstanding_rides = filter(lambda r: r.outstanding, input_data.rides())
    #     if outstanding_rides is None:
    #         # TODO skip, wait for remaining vehicles to finish
    #         pass
    #     sorted_rides = sorted(outstanding_rides, key=cmp_to_key(lambda r1, r2: r1.earliest_start - r2.earliest_start))
    #     for r in sorted_rides:
    #         vehicle = fetch_vehicle_for_ride(r, list(vehicles.values()))
    #         if vehicle is not None:
    #             attach_ride_to_vehicle(r, vehicle)

    while not is_finished:
        filtered_vehicles = filter(lambda v: v.is_available(), vehicles.values())
        available_vehicles = set(map(lambda v: v.id, filtered_vehicles))
        #print(f"Idle vehicles: {available_vehicles}")
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

    on_time_rides = list(filter(lambda r: r.was_on_time(), input_data.rides()))
    score = 0
    for ride in on_time_rides:
        score += ride.get_route_length()
    not_on_time_rides = list(filter(lambda r: not r.was_on_time(), input_data.rides()))

    print(f"Rides on time: {len(on_time_rides)}")
    print(f"SCORE: {score}")
    print(f"Rides NOT on time: {len(not_on_time_rides)}")

    #print(available_vehicles)
