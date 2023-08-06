import logging
import logging.handlers
import sys
import os
sys.path.append('../')
from common.variables import LOGGING_LEVEL, LOGGING_FORMATTER


PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'client.log')

CLIENT = logging.getLogger("client")

ERROR_STREAM_HANDLER = logging.StreamHandler(sys.stderr)
ERROR_STREAM_HANDLER.setFormatter(LOGGING_FORMATTER)
ERROR_STREAM_HANDLER.setLevel(logging.ERROR)
LOG_FILE = logging.handlers.TimedRotatingFileHandler(PATH, encoding='utf8', interval=1, when='D')
LOG_FILE.setFormatter(LOGGING_FORMATTER)

CLIENT.addHandler(ERROR_STREAM_HANDLER)
CLIENT.addHandler(LOG_FILE)
CLIENT.setLevel(LOGGING_LEVEL)

if __name__ == '__main__':
    CLIENT.critical('Критическая ошибка')
    CLIENT.error('Ошибка')
    CLIENT.debug('Отладочная информация')
    CLIENT.info('Информационное сообщение')