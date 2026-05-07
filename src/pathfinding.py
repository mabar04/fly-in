
from .graph_modeling import EdgeInfo

class Dijkstra:
    def __init__(self, label: str, adjacency: dict[str, dict[str, EdgeInfo]]) -> None:
        self.label = label
        self.adjacency = adjacency

    def find_shortest_path(self) -> list[str] | None:
        unvisited = set(self.adjacency.keys())
        distance = {node: float('inf') for node in self.adjacency}
        distance[self.label] = 0
        print(unvisited)
        print(distance)
        previous = {}
        while unvisited:
            zone = unvisited.pop()
            for zone_name, connection in self.adjacency[zone].items():
                print(f"{zone} => {zone_name}")

            