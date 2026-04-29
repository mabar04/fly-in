from src import Parsing_class


def main():
    parsing = Parsing_class()
    with open("test_file.txt") as f:
        d = parsing.basic_parsing(f)
    nb_drones = d["nb_drones"]
    hubs = parsing.hub_parsing(d["hubs"])
    connections = parsing.connection_parsing(d["connections"])

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)