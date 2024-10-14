from src.InputData import InputData, RideData

def read_input_file(path: str) -> InputData:
    data = InputData()

    with open(path, 'r') as f:
        data.layout_from_line(f.readline())
        for line in f:
            ride = RideData.from_line(line)
            data.add_ride(ride)

    return data


if __name__ == '__main__':
    input_data = read_input_file("../data/a_example.in")

    for r in input_data.rides():
        print(r.start)