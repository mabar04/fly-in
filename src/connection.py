class Connection_class:
    def __init__(self, name: str, startzone: str, endzone: str,
                 max_link_capacity: int = 1):
        self.name = name
        self.start_zone = startzone
        self.end_zone = endzone
        self.max_link_capacity = max_link_capacity
        self.current_drones = 0

    def get_info(self) -> dict[str, object]:
        return {
            "name": self.name,
            "start_zone": self.start_zone,
            "end_zone": self.end_zone,
            "max_link_capacity": self.max_link_capacity
        }
