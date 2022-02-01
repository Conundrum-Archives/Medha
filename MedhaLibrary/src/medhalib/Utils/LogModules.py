import logging

LOGGER_NAME = "MEDHABOARD"
METHOD_ENTRY = "Entered method"
METHOD_EXIT = "Exit method"

def init_logger():
    logging.getLogger("paramiko").setLevel(logging.DEBUG)
    # init log module
    logging.basicConfig(
        format='%(asctime)-15s - %(levelname)8s - %(module)10s [%(filename)s:%(lineno)d] - %(message)s',
        level=logging.DEBUG,
        datefmt='%m/%d/%Y %I:%M:%S.%p',
        handlers=[
            # logging.FileHandler("poc1.log"),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(LOGGER_NAME)
