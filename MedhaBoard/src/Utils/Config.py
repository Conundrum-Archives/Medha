import json

def get_config():
    with open("config.json", "r") as cfg:
        return json.load(cfg)