from .graph_modeling import EdgeInfo
from .errors_class import PathError


class Dijkstra:
    def __init__(self, label: str,
                 adjacency: dict[str, dict[str, EdgeInfo]]) -> None:
        self.label = label
        self.adjacency = adjacency

    def get_smallest(self, distance: dict[str, float],
                     unvisited: set[str]) -> str:
        smallest = float("inf")
        smallest_name = ""
        for k, v in distance.items():
            if v < smallest and k in unvisited:
                smallest = v
                smallest_name = k
        return smallest_name

    def find_shortest_path(self, start: str, target: str) -> list[str] | None:
        unvisited = set(self.adjacency.keys())
        distance: dict[str, float] = {node: float('inf')
                                      for node in self.adjacency}
        distance[start] = 0
        previous: dict[str, str | None] = {}
        for k in distance.keys():
            previous.update({k: None})
        while unvisited:
            name = self.get_smallest(distance, unvisited)
            if name == "":
                break
            for neighbor, cost_class in self.adjacency[name].items():
                if distance[name] + cost_class.cost < distance[neighbor]:
                    distance[neighbor] = distance[name] + cost_class.cost
                    previous[neighbor] = name
            unvisited.remove(name)
        if distance[target] == float("inf"):
            raise PathError("Dijkstra Error: No path to the target")
        path: list[str] = []
        while target != start:
            path.append(target)
            next_node = previous[target]
            if next_node is None:
                break
            target = next_node
        path.append(start)
        path.reverse()
        return path
