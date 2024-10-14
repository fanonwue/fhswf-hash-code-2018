from ride import Ride

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
        return int(result)

    def add_ride(self, ride: Ride):
        self.__rides.append(ride)

    def rides(self) -> list[Ride]:
        return self.__rides