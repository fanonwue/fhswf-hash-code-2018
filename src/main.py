import json
from typing import Final, Iterable

from src.input_data import InputData
from src.input_files import InputFile
from src.ride import Ride
from src.vehicle import Vehicle
from functools import cmp_to_key
from pathlib import Path

root = Path(__file__).parent.parent

def read_input_file(file: InputFile) -> InputData:
    data_path = root / "data" / file.value
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

def write_result_file(file: str, vehicles: list[Vehicle]):
    def line_generator() -> Iterable[str]:
        for v in vehicles:
            rides = v.get_rides()
            ids = " ".join(map(lambda r: str(r.id), rides))
            yield f"{len(rides)} {ids}\n"

    with open(file, 'w') as f:
        f.writelines(line_generator())

def write_result_json(file: str, vehicles: list[Vehicle], input_data: InputData):
    def ride_code(ride: Ride) -> int:
        if ride.outstanding:
            return -1
        if not ride.was_on_time():
            return 0
        if not ride.started_on_time():
            return 1
        return 1000

    rides = []
    for v in vehicles:
        for r in v.get_rides():
            rides.append([r.start_row(), r.start_column(), r.end_row(), r.end_column(), ride_code(r)])

    json_data = {
        "row": input_data.layout_rows(),
        "column": input_data.layout_columns(),
        "rides": rides
    }

    with open(file, 'w') as f:
        json.dump(json_data, f)


if __name__ == '__main__':
    RIDE_COUNT_THRESHOLD: Final[int]    = 50
    USE_BONUS: Final[bool]              = True
    OUTPUT_FILE                         = root / "out.txt"
    OUTPUT_JSON                         = root / "out.json"
    DATA_FILE: Final[InputFile]         = InputFile.METROPOLIS


    input_data = read_input_file(DATA_FILE)
    vehicles: list[Vehicle] = []
    for i in range(input_data.layout_vehicles()):
        vehicles.append(Vehicle(i+1))

    bonus: int|None = None
    if USE_BONUS:
        bonus = input_data.layout_bonus()
    is_finished = False
    ride_count = 0

    while not is_finished:
        is_finished = True
        for v in vehicles:
            current_ride: Ride|None = None
            ride_count = 0
            for r in input_data.rides():
                if not r.outstanding:
                    continue
                ride_count += 1
                if current_ride is None or (v.evaluate(r, bonus) < v.evaluate(current_ride, bonus)):
                    current_ride = r

                if ride_count > RIDE_COUNT_THRESHOLD:
                    break

            if current_ride is None:
                break

            if v.get_current_tick() < input_data.layout_steps():
                is_finished = False

            current_ride.real_start_at = v.get_current_tick()
            distance_to_ride = current_ride.distance_to_start(v.position())

            delta_wait = v.get_current_tick() + distance_to_ride - current_ride.earliest_start

            if delta_wait < 0:
                c = v.get_current_tick()
                v.set_current_tick(v.get_current_tick() + abs(delta_wait))
                c2 = v.get_current_tick()
                current_ride.real_start_at = v.get_current_tick() + distance_to_ride

            new_tick = v.get_current_tick() + current_ride.get_route_length() + distance_to_ride
            if new_tick < input_data.layout_steps():
                v.set_current_tick( v.get_current_tick() + current_ride.get_route_length() + distance_to_ride)
                current_ride.arrived_at = v.get_current_tick()
                v.set_position(current_ride.end)
                v.add_ride(current_ride)
                current_ride.set_outstanding(False)
            else:
                current_ride.set_outstanding(False)

    print("Rides:")
    score = 0
    bonus_score = 0
    for v in vehicles:
        ids = ", ".join(map(lambda r: str(r.id), v.get_rides()))
        print(f"Vehicle: {v.id} - Rides: {ids}")
        on_time_rides = list(filter(lambda r: r.was_on_time(), v.get_rides()))
        print("Rides on time: " + str(len(on_time_rides)))
        for ride in on_time_rides:
            score += ride.get_route_length()
            if ride.started_on_time():
                bonus_score += input_data.layout_bonus()
    real_score = score + bonus_score
    print(f"Score: {real_score} ({score} + {bonus_score})")


    duplicate_rides = check_duplicate_rides(vehicles)
    assert len(duplicate_rides) == 0, "Got duplicate rides"
    print(f"Writing to output file at {str(OUTPUT_FILE.relative_to(root))}")
    write_result_file(str(OUTPUT_FILE), vehicles)
    print(f"Writing JSON output file at {str(OUTPUT_JSON.relative_to(root))}")
    write_result_json(str(OUTPUT_JSON), vehicles, input_data)