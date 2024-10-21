from src.ride import Ride

class Vehicle:
    def __init__(self, id: int):
        self._position: tuple[int, int] = (0, 0)
        self._current_tick: int = 0
        self._rides: list[Ride] = []
        self.id = id

    def evaluate(self, ride: Ride, bonus: int|None) -> int:
        if bonus is None:
            return self._evaluate_no_bonus(ride)
        return self._evaluate_with_bonus(ride, bonus)


    def _evaluate_no_bonus(self, ride: Ride) -> int:
        distance_to_start = self.distance_to_ride(ride)
        estimate = distance_to_start
        #estimate = ride.calculate_distance_to_start(self._position_row, self._position_column)
        delta_wait = self._current_tick + distance_to_start - ride.earliest_start
        if delta_wait < 0:
            delta_wait = 0

        if (ride.get_route_length() + distance_to_start + self._current_tick + delta_wait) > ride.latest_finish:
            # some high number
            return 10_000_000

        return estimate + delta_wait

    def _evaluate_with_bonus(self, ride: Ride, bonus: int) -> int:
        distance_to_start = self.distance_to_ride(ride)
        estimate = ride.get_route_length()

        delta_wait = self._current_tick + distance_to_start - ride.earliest_start
        if delta_wait < 0:
            delta_wait = 0

        if (ride.get_route_length() + distance_to_start + self._current_tick + delta_wait) > ride.latest_finish:
            # some high number
            return 10_000_000

        if distance_to_start + self._current_tick < ride.earliest_start:
            estimate += bonus

        return estimate - delta_wait

    def distance_to_ride(self, ride: Ride) -> int:
        return ride.distance_to_start(self._position)

    def get_current_tick(self) -> int:
        return self._current_tick

    def set_current_tick(self, new_tick: int):
        self._current_tick = new_tick

    def set_position(self, pos: tuple[int, int]):
        self._position = pos

    def position(self) -> tuple[int, int]:
        return self._position

    def add_ride(self, ride: Ride):
        self._rides.append(ride)

    def get_rides(self) -> list[Ride]:
        return self._rides