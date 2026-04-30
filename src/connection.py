class Connection_class:
    def __init__(self, name, startzone, endzone, max_link_capacity = 1):
        self.name = name
        self.start_zone = startzone
        self.end_zone = endzone
        self.max_link_capacity = max_link_capacity

    def get_info(self):
        return {
            "name": self.name,
            "start_zone": self.start_zone,
            "end_zone": self.end_zone,
            "max_link_capacity": self.max_link_capacity
        }
