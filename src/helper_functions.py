class zone_helper:
    def zone_count(self, zones: list):
        start_zone = 0
        end_zone = 0
        for zone in zones:
            if zone.name == "start_hub":
                start_zone += 1
            elif zone.name == "end_hub":
                end_zone += 1
        return start_zone, end_zone