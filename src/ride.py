from src.util import distance

class Ride:
    _next_ride_id = 1

    def __init__(self, id: int, start: tuple[int, int], end: tuple[int, int], earliest_start: int, latest_finish: int):
        self.id = id
        self.start = start
        self.end = end
        self.earliest_start = earliest_start
        self.latest_finish = latest_finish
        self.outstanding: bool = True
        self.arrived_at: int|None = None
        self.real_start_at: int|None = None

    def set_outstanding(self, outstanding: bool):
        self.outstanding = outstanding

    def start_row(self):
        return self.start[0]

    def start_column(self):
        return self.start[1]

    def end_row(self):
        return self.end[0]

    def end_column(self):
        return self.end[1]


    def distance_to_start(self, from_pos: tuple[int, int]) -> int:
        return abs(from_pos[0] - self.start_column()) + abs(from_pos[1] - self.start_row())

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

    @staticmethod
    def from_line(line: str):
        parts = line.strip(" \n").split(' ')
        if len(parts) != 6:
            raise Exception("Invalid ride line")

        start = (int(parts[0]), int(parts[1]))
        end = (int(parts[2]), int(parts[3]))
        id = Ride._next_ride_id
        Ride._next_ride_id += 1
        return Ride(id, start, end, int(parts[4]), int(parts[5]))