class Drone:
    def __init__(self, id: str, startzone: str, endzone: str):
        self.id = id
        self.startzone = startzone
        self.current_zone = ""
        self.target = ""
        self.path = []
        self.path_index = 0
        self.status = "waiting"
        self.endzone = endzone

    def get_info(self):
        return {
            "id": self.id,
            "startzone": self.startzone,
            "endzone": self.endzone
        }
