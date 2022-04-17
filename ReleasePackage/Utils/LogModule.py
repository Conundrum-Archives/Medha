import logging
# import coloredlogs

LOGGER_NAME = "MedhaApplication"
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

    # logging.getLogger(LOGGER_NAME).addHandler(TqdmLoggingHandler())
    
    # coloredlogs.install(level='DEBUG')
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger('matplotlib.font_manager').disabled = True
    logging.getLogger('PIL.PngImagePlugin').disabled = True
    return logging.getLogger(LOGGER_NAME)
