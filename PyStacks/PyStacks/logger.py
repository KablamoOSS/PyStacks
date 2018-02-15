import logging


class Logger:

    log = None

    @staticmethod
    def create_logger():
        logger = logging.getLogger('pystacks')
        logger.setLevel(logging.DEBUG)

        # create file handler which logs even debug messages
        # fh = logging.FileHandler('pystacks.log')
        # fh.setLevel(logging.DEBUG)

        # create console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # add the handlers to the log
        # logger.addHandler(fh)
        logger.addHandler(ch)

        # Do some logging
        logger.debug('Pystacks logger initialised')

        Logger.log = logger

    def __init__(self):
        if not Logger.log:
            Logger.create_logger()


def get_pystacks_log():
    logger = Logger()
    return logger.log
