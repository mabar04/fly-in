from colorama import Fore, Style, init


class Drone:
    def __init__(self, id: str, startzone: str, endzone: str):
        self.id = id
        self.startzone = startzone
        self.current_zone = ""
        self.current_connection = ""
        self.remaining_time: float = 0
        self.target = ""
        self.target_connection = ""
        self.path: list[str] = []
        self.path_index = 0
        self.status = "waiting"
        self.endzone = endzone
        self.approved = False

    def get_info(self) -> dict[str, object]:
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
            "remaining_time": self.remaining_time,
            "approved": self.approved
        }

    def get_log(self) -> None:
        init()
        if self.status != "finished":
            if self.target == "":
                if self.remaining_time < 1:
                    print(Fore.GREEN + Style.BRIGHT +
                          f"{self.id}-{self.current_zone}", end=" ")
            elif self.remaining_time == 1:
                print(Fore.GREEN + Style.BRIGHT +
                      f"{self.id}-{self.current_connection}", end=" ")
        print(Style.RESET_ALL, end="")
