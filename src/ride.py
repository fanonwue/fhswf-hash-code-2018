from src.util import distance

class Ride:
    def __init__(self, start: [int, int], end: [int, int], earliest_start: int, latest_finish: int):
        self.start = start
        self.end = end
        self.earliest_start = earliest_start
        self.latest_finish = latest_finish
        self.outstanding: bool = True
        self.arrived_at: int|None = None

    def start_row(self):
        return self.start[0]

    def start_column(self):
        return self.start[1]

    def end_row(self):
        return self.start[0]

    def end_column(self):
        return self.start[1]

    def calculate_distance_to_start_row(self, vehicle_location_row: int):
        return self.start_row() - vehicle_location_row

    def calculate_distance_to_start_column(self, vehicle_location_column: int):
        return self.start_column() - vehicle_location_column

    def calculate_distance_to_start(self, vehicle_location_row: int, vehicle_location_column: int) -> int:
        """
        Calculate the distance traveled to the start of the ride.
        :param vehicle_location_row: the row location of the vehicle.
        :param vehicle_location_column: the column location of the vehicle.
        :return: the distance traveled to the start of the ride.
        """
        return self.calculate_distance_to_start_row(vehicle_location_row) + self.calculate_distance_to_start_column(vehicle_location_column)

    def calculate_distance_to_finish_row(self, vehicle_location_row: int) -> int:
        return self.end_row() - vehicle_location_row

    def calculate_distance_to_finish_column(self, vehicle_location_column: int) -> int:
        return self.end_column() - vehicle_location_column

    def calculate_distance_to_finish(self, vehicle_location_row: int, vehicle_location_column: int) -> int:
        """
        Calculate the distance traveled to the finish of the ride.
        :param vehicle_location_row: the row location of the vehicle.
        :param vehicle_location_column: the column location of the vehicle.
        :return: the distance traveled to the finish of the ride.
        """
        return self.calculate_distance_to_finish_row(vehicle_location_row) + self.calculate_distance_to_finish_column(vehicle_location_column)

    def get_route_length(self):
        """
        Calculate the length of the route.
        :return: the length of the route.
        """
        return distance(self.start, self.end)

    def set_arrived_at(self, tick: int):
        self.arrived_at = tick

    def was_on_time(self) -> bool:
        if self.arrived_at is None:
            return False

        # Ride is on time if it has arrived one tick before the latest_finish
        return (self.arrived_at + 1) <= self.latest_finish

    def calculate_slack(self):
        return (self.latest_finish - self.earliest_start) - self.get_route_length()

    @staticmethod
    def from_line(line: str):
        parts = line.strip(" \n").split(' ')
        if len(parts) != 6:
            raise Exception("Invalid ride line")

        start = (int(parts[0]), int(parts[1]))
        end = (int(parts[2]), int(parts[3]))
        return Ride(start, end, int(parts[4]), int(parts[5]))