class Parsing_Errors(Exception):
    pass

class Zone_Errors(Exception):
    pass

class Connection_Errors(Exception):
    pass

class Check_errors:
    def zone_check(cls, zones: list):
        pass

    def connection_check(cls, connections):
        pass