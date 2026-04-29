class Connection_class:
    def __init__(self, name, startzone, endzone):
        self.name = name
        self.startzone = startzone
        self.endzone = endzone
    
    def get_info(self):
        return {
            "name": self.name,
            "start_zone": self.startzone,
            "end_zone": self.endzone,
        }
