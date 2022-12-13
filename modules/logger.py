import logging

logger = logging.getLogger('LOG')
f_handler = logging.FileHandler('exceptions.log')
f_handler.setLevel(logging.ERROR)

f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_handler.setFormatter(f_format)

logger.addHandler(f_handler)
