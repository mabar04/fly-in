class hub_class:
    def __init__(self, name:str, label:str, coord:tuple[int, int], zone_type:str = "normal", color:str | None = None,
                 max_drones:int = 1, cost:float = 1):
        self.name = name
        self.label = label
        self.coord = coord
        self.zone_type = zone_type
        self.color = color
        self.cost = cost
        self.max_drones = max_drones
    
    def get_info(self) -> dict[str, object]:
        return {
            "name": self.name,
            "label": self.label,
            "coord": self.coord,
            "zone_type": self.zone_type,
            "color": self.color,
            "max_drones": self.max_drones,
            "cost": self.cost
        }