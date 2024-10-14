from src.ride import Ride

class Vehicle:
    _position_row: int = 0
    _position_column: int = 0
    _has_moved_in_current_tick = False
    _current_ride: Ride | None = None
    _has_passenger: bool = False

    def __init__(self, id: int):
        self.id = id


    def position(self) -> tuple[int, int]:
        return self._position_row, self._position_column

    def wait(self) -> None:
        """
        Wait without moving the vehicle.
        """
        self._has_moved_in_current_tick = True

    def can_move(self) -> bool:
        """
        Check whether the vehicle can move (has a valid ride and has not moved yet this tick).
        :return:
        """
        return self._current_ride is not None and self._has_moved_in_current_tick is False

    def is_available(self):
        return self._current_ride is None

    def _approach_point(self, location: str):
        """
        Approach the start or end point of the current ride.
        :param location: the location to move towards. Must be 'start' or 'finish'
        :return:
        """
        if ('start' != location and 'finish' != location) or self._current_ride is None:
            # TODO signal error cause
            return

        if 'start' == location:
            column_distance = self._current_ride.calculate_distance_to_start_column(self._position_column)
            row_distance = self._current_ride.calculate_distance_to_start_row(self._position_row)
        else:
            column_distance = self._current_ride.calculate_distance_to_finish_column(self._position_column)
            row_distance = self._current_ride.calculate_distance_to_finish_row(self._position_row)

        if column_distance < 0:
            self._position_column -= 1
            self._has_moved_in_current_tick = True
        elif column_distance > 0:
            self._position_column += 1
            self._has_moved_in_current_tick = True
        else:
            if row_distance == 0 and column_distance == 0:
                if 'start' == location:
                    self._has_passenger = True
                    if not self._has_moved_in_current_tick:
                        self.approach_ride_finish()
                else:
                    # TODO score ride
                    self._current_ride = None
                    self._has_passenger = False

        if self._has_moved_in_current_tick:
            return

        if row_distance < 0:
            self._position_row -= 1
            self._has_moved_in_current_tick = True
        elif row_distance > 0:
            self._position_row += 1
            self._has_moved_in_current_tick = True
        else:
            if row_distance == 0 and column_distance == 0:
                if 'start' == location:
                    self._has_passenger = True
                    if not self._has_moved_in_current_tick:
                        self.approach_ride_finish()
                else:
                    # TODO score ride
                    self._current_ride = None
                    self._has_passenger = False

    def approach_ride_start(self) -> None:
        """
        Approach the starting point of the current ride.
        :return:
        """
        if not self.can_move():
            # TODO signal error cause
            return

        self._approach_point('start')

    def approach_ride_finish(self) -> None:
        """
        Approach the finishing point of the current ride.
        :return:
        """
        if not self.can_move():
            # TODO signal error cause
            return

        self._approach_point('finish')

    def drive(self) -> None:
        if self._current_ride is None:
            return
        if self._has_moved_in_current_tick:
            return

        if self._has_passenger:
            self.approach_ride_finish()
        else:
            self.approach_ride_start()

    def set_current_ride(self, ride: Ride) -> None:
        self._current_ride = ride

    def reset_tick(self) -> None:
        self._has_moved_in_current_tick = False