from src import Parsing_class
from src import Check_errors
from src import Drone
def main():
    parsing = Parsing_class()
    errors = Check_errors()
    drones_list = []
    with open("test_file1.txt") as f:
        d = parsing.basic_parsing(f)
    if isinstance(d["hubs"], dict):
        errors.metadata_check(d["hubs"])
        hubs = parsing.hub_parsing(d["hubs"])
    if isinstance(d["connections"], dict):
        errors.metadata_check(d["connections"])
        connections = parsing.connection_parsing(d["connections"])
    for hub in hubs:
        if hub.name == "start_hub":
            start_hub = hub.label
        if hub.name == "end_hub":
            end_hub = hub.label
    for i in range(0, d["nb_drones"]):
        drone_inst = Drone(f"D{i}", start_hub, end_hub)
        drones_list.append(drone_inst)
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)