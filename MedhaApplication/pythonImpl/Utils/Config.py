import os.path
import json
from jsonschema import validate
from Utils.LogModule import init_logger

# initialize logger
log = init_logger()

# read config.json file
def get_config():
  with open("../config.json", "r") as cfg:
    return json.load(cfg)

def prevalidate_application1_config(cfgdata):
  with open(os.path.join("config.schema.json"), "r") as scjs:
    schema = json.loads(scjs.read())
    validate(instance=cfgdata, schema=schema)
  
  if (not cfgdata["operating_device"]["modules"]["baseservo"]["enabled"]):
    raise ValueError("baseservo.enabled must be true for application1")
  if (not cfgdata["operating_device"]["modules"]["upperservo"]["enabled"]):
    raise ValueError("upperservo.enabled must be true for application1")

  # precheck samples configuration
  prechecktime = 0
  userread_buffertime = 4
  if (cfgdata["scan_config"]["baseservo_start_angle"] != 0):
    log.warning("\nstart_angle for base servo is: {startangle}.\n\nMapping may not detect (or not accurately detect) right hand side border of environment\nNote: start with zero angle get right hand side distance".format(startangle=cfgdata["scan_config"]["baseservo_start_angle"]))
    prechecktime = prechecktime + userread_buffertime

  if (90 % cfgdata["scan_config"]["baseservo_sampling"] != 0):
    log.warning("\nSampling rate for base servo is: {sample}.\n\nMapping may not detect (or not accurately detect) front side border of environment\nNote: provide sample size which is factor of 90 to get front side distance".format(sample=cfgdata["scan_config"]["baseservo_sampling"]))
    prechecktime = prechecktime + userread_buffertime

  # if (prechecktime >= userread_buffertime):
  #   time.sleep(prechecktime)

# get config for specific application
def get_app_config(app_id=None, checkkey=False):
  if (app_id is None):
    raise ValueError("Invalid application. supplied: {appid}".format(appid=app_id))
  else:
    cfg = get_config()
    if (app_id not in cfg):
      raise LookupError("Configuration not set for application id: {appid}".format(appid=app_id))
    else:
      # pre-check required configurations for application1
      if checkkey and app_id == "application1":
        prevalidate_application1_config(cfg[app_id])
      return cfg[app_id]