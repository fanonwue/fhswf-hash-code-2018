from src.input_data import InputData
from src.input_files import InputFile
from src.ride import Ride
from src.vehicle import Vehicle
from functools import cmp_to_key


def read_input_file(file: InputFile) -> InputData:
    data_path = "../data/" + file.value
    data = InputData()

    with open(data_path, 'r') as f:
        data.layout_from_line(f.readline())
        for line in f:
            data.add_ride(Ride.from_line(line))

    return data

def sort_rides(rides: list[Ride]) -> list[Ride]:
    def compare(a: Ride, b: Ride) -> int:
        return a.earliest_start - b.earliest_start

    return sorted(rides, key=cmp_to_key(compare))

def check_duplicate_rides(vehicles: list[Vehicle]) -> list[Ride]:
    seen_ride_ids = set()
    duplicate_rides = []
    for v in vehicles:
        for r in v.get_rides():
            if r.id in seen_ride_ids:
                duplicate_rides.append(r)
            seen_ride_ids.add(r.id)

    return duplicate_rides


if __name__ == '__main__':
    ride_count_threshold = 50
    input_data = read_input_file(InputFile.METROPOLIS)
    vehicles: dict[int, Vehicle] = {}
    for i in range(input_data.layout_vehicles()):
        vehicles[i+1] = Vehicle(i+1)

    is_finished = False
    use_bonus = True
    ride_count = 0


    bonus: int|None = None
    if use_bonus:
        bonus = input_data.layout_bonus()

    while not is_finished:
        is_finished = True
        for v in vehicles.values():
            current_ride: Ride|None = None
            ride_count = 0
            for r in input_data.rides():
                if not r.outstanding:
                    continue
                ride_count += 1
                if current_ride is None or (v.evaluate(r, bonus) < v.evaluate(current_ride, bonus)):
                    current_ride = r

                if ride_count > ride_count_threshold:
                    break

            if current_ride is None:
                break

            if v.get_current_tick() < input_data.layout_steps():
                is_finished = False

            current_ride.real_start_at = v.get_current_tick()
            v.set_position(current_ride.end)

            distance_to_ride = current_ride.distance_to_start(v.position())

            delta_wait = v.get_current_tick() + distance_to_ride - current_ride.earliest_start

            v.set_current_tick( v.get_current_tick() + current_ride.get_route_length() + distance_to_ride)

            if delta_wait < 0:
                v.set_current_tick(v.get_current_tick() + abs(delta_wait))

            current_ride.arrived_at = v.get_current_tick()
            v.add_ride(current_ride)
            current_ride.set_outstanding(False)


    print("Rides:")
    score = 0
    bonus_score = 0
    for v in vehicles.values():
        ids = ", ".join(map(lambda r: str(r.id), v.get_rides()))
        print(f"Vehicle: {v.id} - Rides: {ids}")
        on_time_rides = list(filter(lambda r: r.was_on_time(), v.get_rides()))
        print("Rides on time: " + str(on_time_rides.__len__()))
        for ride in on_time_rides:
            score += ride.get_route_length()
            if ride.real_start_at == ride.earliest_start:
                bonus_score += input_data.layout_bonus()
    real_score = score + bonus_score
    print(f"Score: {real_score} ({score} + {bonus_score})")


    duplicate_rides = check_duplicate_rides(list(vehicles.values()))
    assert len(duplicate_rides) == 0, "Got duplicate rides"