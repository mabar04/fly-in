class Drone:
    def __init__(self, id: str, startzone: str, endzone: str):
        self.id = id
        self.startzone = startzone
        self.current_zone = None
        self.current_connection = None
        self.remaining_time = 0
        self.target = None
        self.target_connection = None
        self.path = []
        self.path_index = 0
        self.status = "waiting"
        self.endzone = endzone
        self.approved = False

    def get_info(self):
        return {
            "id": self.id,
            "startzone": self.startzone,
            "endzone": self.endzone,
            "current_zone": self.current_zone,
            "current_connection": self.current_connection,
            "path": self.path,
            "path_index": self.path_index,
            "status": self.status,
            "target": self.target,
            "target_connection": self.target_connection,
            "remaining_time": self.remaining_time
        }

    def get_log(self):
        print(f"{self.id}-{self.current_zone}-{self.remaining_time}")
