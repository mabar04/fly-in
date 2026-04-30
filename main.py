from src import Parsing_class
from src import Check_errors

def main():
    parsing = Parsing_class()
    errors = Check_errors()
    with open("test_file1.txt") as f:
        d = parsing.basic_parsing(f)
    nb_drones = d["nb_drones"]
    hubs = parsing.hub_parsing(d["hubs"])
    connections = parsing.connection_parsing(d["connections"])
    errors.zone_check(hubs)
    errors.connection_check(connections)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)