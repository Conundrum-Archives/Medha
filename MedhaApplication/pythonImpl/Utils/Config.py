import json

def get_config():
  with open("config.json", "r") as cfg:
    return json.load(cfg)

def get_app_config(app_id=None):
  if (app_id is None):
    raise ValueError("Invalid application. supplied: {appid}".format(appid=app_id))
  else:
    cfg = get_config()
    if (app_id not in cfg):
      raise LookupError("Configuration not set for application id: {appid}".format(appid=app_id))
    else:
      return cfg[app_id]