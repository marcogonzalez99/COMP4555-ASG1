import json

class Settings:
    def __init__(self):
        # Load Settings
        file = open("config.json")
        data = json.load(file)
        self.level_settings = data["level_settings"]

    def get_level(self, level_num):
        for level in self.level_settings:
            if level["level"] == level_num:
                return level
        return self.level_settings[0]

    def get_value(self, level_num, key):
        level = self.get_level(level_num)
        return level[key]


