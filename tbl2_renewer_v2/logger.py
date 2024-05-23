# logger_setup.py
import logging

def setup_logger():
    logging.basicConfig(filename='latex.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    return logger

# Создаем экземпляр логгера
logger = setup_logger()