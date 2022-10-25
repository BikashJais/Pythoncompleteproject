import logging

def config():
    logging.basicConfig(filename='log3.log', level=logging.INFO, format='%(levelname)s %(asctime)s %(message)s')


def info(msg):
    logging.info(msg)


def error(msg):
    logging.error(msg)


def warning(msg):
    logging.warning(msg)