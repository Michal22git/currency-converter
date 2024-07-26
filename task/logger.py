import logging
from logging import getLogger, StreamHandler

logger = getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = StreamHandler()
logger.addHandler(handler)
