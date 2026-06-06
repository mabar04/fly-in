from graph_modeling import EdgeInfo
from errors_class import PathError
import heapq


class Dijkstra:
    def __init__(self, label: str,
                 adjacency: dict[str, dict[str, EdgeInfo]]) -> None:
        self.label = label
        self.adjacency = adjacency

    def find_shortest_path(self, start: str, target: str) -> list[str] | None:
        distance: dict[str, float] = {node: float('inf')
                                      for node in self.adjacency}
        previous: dict[str, str | None] = {node: None for
                                           node in self.adjacency}

        distance[start] = 0
        heap: list[tuple[float, str]] = [(0, start)]
        visited: set[str] = set()

        while heap:
            current_dist, name = heapq.heappop(heap)
            if name in visited:
                continue
            visited.add(name)
            if name == target:
                break

            for neighbor, cost_class in self.adjacency[name].items():
                new_dist: float = current_dist + cost_class.cost

                if new_dist < distance[neighbor]:
                    distance[neighbor] = new_dist
                    previous[neighbor] = name
                    heapq.heappush(heap, (new_dist, neighbor))

                elif new_dist == distance[neighbor]:
                    if cost_class.zone_type == "priority":
                        previous[neighbor] = name
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

    def all_paths(self, start: str, target: str) -> list[list[str]]:
        paths: list[list[str]] = []
        while True:
            try:
                path = self.find_shortest_path(start, target)
                if isinstance(path, list):
                    paths.append(path)
                for _, inside in self.adjacency.items():
                    for name, cost_class in inside.items():
                        if isinstance(path, list):
                            if name in path:
                                cost_class.cost *= 2
                if len(paths) >= 2:
                    break
            except PathError:
                break
        return paths
