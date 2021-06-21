import logging


def monitoring(func):
    logging.basicConfig(filename='monitoring.txt',
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%Y.%m.%d %H:%M:%S',
                        level=logging.INFO)

    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)

            a = [i for i in args if isinstance(i, bytes) or isinstance(i, str)]
            logging.info('Running {} with arguments {}'.format(func.__name__, a))

            if result:
                logging.info('{}'.format(result))

        except:
            logging.exception('Something went wrong in {}'.format(func.__name__))

    return wrapper
