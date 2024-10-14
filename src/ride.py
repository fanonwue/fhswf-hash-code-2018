class Ride:
    _start_location_row: int = 0
    _start_location_column: int = 0
    _end_location_row: int = 0
    _end_location_column: int = 0
    _earliest_start: int = 0
    _earliest_finish: int = 0

    def __init__(self, start_location_row: int, start_location_column: int, end_location_row: int, end_location_column: int, earliest_start: int, earliest_finish: int):
        """
        Initialize a new Ride object.
        :param start_location_row: the start location on the grid - row.
        :param start_location_column: the start location on the grid - column.
        :param end_location_row: the destination location on the grid - row.
        :param end_location_column: the destination location on the grid - column.
        :param earliest_start: the earliest tick the ride can start.
        :param earliest_finish: the latest tick the ride may finish.
        """
        self._start_location_row = start_location_row
        self._start_location_column = start_location_column
        self._end_location_row = end_location_row
        self._end_location_column = end_location_column
        self._earliest_start = earliest_start
        self._earliest_finish = earliest_finish

    def calculate_distance_to_start_row(self, vehicle_location_row: int):
        return self._start_location_row - vehicle_location_row

    def calculate_distance_to_start_column(self, vehicle_location_column: int):
        return self._start_location_column - vehicle_location_column

    def calculate_distance_to_start(self, vehicle_location_row: int, vehicle_location_column: int) -> int:
        """
        Calculate the distance traveled to the start of the ride.
        :param vehicle_location_row: the row location of the vehicle.
        :param vehicle_location_column: the column location of the vehicle.
        :return: the distance traveled to the start of the ride.
        """
        return self.calculate_distance_to_start_row(vehicle_location_row) + self.calculate_distance_to_start_column(vehicle_location_column)

    def calculate_distance_to_finish_row(self, vehicle_location_row: int) -> int:
        return self._end_location_row - vehicle_location_row

    def calculate_distance_to_finish_column(self, vehicle_location_column: int) -> int:
        return self._end_location_column - vehicle_location_column

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
        return abs(self._start_location_row - self._end_location_row) + abs(self._start_location_column - self._end_location_column)