class Drone:
    def __init__(self, id:str, startzone:str, endzone:str):
        self.id = id
        self.startzone = startzone
        self.endzone = endzone

    def get_info(self):
        return {
            "id": self.id,
            "startzone": self.startzone,
            "endzone": self.endzone
        }