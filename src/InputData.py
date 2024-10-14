from src.util import distance


class RideData:
    def __init__(self, start: [int, int], end: [int, int], earliest_start: int, latest_finish: int):
        self.start = start
        self.end = end
        self.earliest_start = earliest_start
        self.latest_finish = latest_finish

    def start_row(self):
        return self.start[0]

    def start_column(self):
        return self.start[1]

    def end_row(self):
        return self.start[0]

    def end_column(self):
        return self.start[1]

    def distance(self):
        return distance(self.start, self.end)

    @staticmethod
    def from_line(line: str):
        parts = line.strip(" \n").split(' ')
        if len(parts) != 6:
            raise Exception("Invalid ride line")

        start = (int(parts[0]), int(parts[1]))
        end = (int(parts[2]), int(parts[3]))
        return RideData(start, end, int(parts[4]), int(parts[5]))

class InputData:
    def __init__(self):
        self.__layout = None
        self.__rides = []

    def layout_from_line(self, layout_line: str):
        # Strip all spaces and new lines from the start and end before splitting
        parts = layout_line.strip(" \n").split(' ')
        if len(parts) != 6:
            raise Exception("Invalid layout line")

        self.__layout = {
            "R": parts[0],
            "C": parts[1],
            "F": parts[2],
            "N": parts[3],
            "B": parts[4],
            "T": parts[5],
        }

    def layout_rows(self):
        return self.__read_layout("R")

    def layout_columns(self):
        return self.__read_layout("C")

    def layout_vehicles(self):
        return self.__read_layout("F")

    def layout_rides(self):
        return self.__read_layout("N")

    def layout_bonus(self):
        return self.__read_layout("B")

    def layout_steps(self):
        return self.__read_layout("T")

    def __read_layout(self, key: str):
        if self.__layout is None:
            raise Exception("Layout is empty")
        result = self.__layout[key]
        if result is None:
            raise Exception("Invalid layout key")
        return result

    def add_ride(self, ride: RideData):
        self.__rides.append(ride)

    def rides(self) -> list[RideData]:
        return self.__rides