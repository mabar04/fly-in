class hub_class:
    def __init__(self, name, label, coord, zone_type, color,
                 max_drones, cost):
        self.name = name
        self.label = label
        self.coord = coord
        self.zone_type = zone_type
        self.color = color
        self.cost = cost
        self.max_drones = max_drones
    
    def get_info(self):
        return {
            "name": self.name,
            "label": self.label,
            "coord": self.coord,
            "zone_type": self.zone_type,
            "color": self.color,
            "max_drones": self.max_drones,
            "cost": self.cost
        }