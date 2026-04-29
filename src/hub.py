class hub_class:
    def __init__(self, name, label, coord, metadata):
        self.name = name
        self.label = label
        self.coord = coord
        self.metadata = metadata
    
    def get_info(self):
        return {
            "name": self.name,
            "label": self.label,
            "coord": self.coord,
            "metadata": self.metadata
        }