import logging

logging.basicConfig(
    filename='trading.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s'
)

logger = logging.getLogger()
logger.info("Logger initialized.")