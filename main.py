from src import Parsing_class
from src import Check_errors

def main():
    parsing = Parsing_class()
    errors = Check_errors()
    with open("test_file1.txt") as f:
        d = parsing.basic_parsing(f)
    if isinstance(d["hubs"], dict):
        errors.metadata_check(d["hubs"])
        hubs = parsing.hub_parsing(d["hubs"])
    if isinstance(d["connections"], dict):
        errors.metadata_check(d["connections"])
        connections = parsing.connection_parsing(d["connections"])
    print(hubs)
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)