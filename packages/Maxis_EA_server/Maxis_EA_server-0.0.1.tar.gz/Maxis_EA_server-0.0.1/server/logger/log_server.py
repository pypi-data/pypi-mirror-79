import logging
import logging.handlers
import sys
import os
sys.path.append('../')
from common.variables import LOGGING_LEVEL, LOGGING_FORMATTER

SERVER = logging.getLogger("server")

PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'server.log')


ERROR_STREAM_HANDLER = logging.StreamHandler(sys.stderr)
ERROR_STREAM_HANDLER.setFormatter(LOGGING_FORMATTER)
ERROR_STREAM_HANDLER.setLevel(logging.ERROR)
LOG_FILE = logging.handlers.TimedRotatingFileHandler(PATH, encoding='utf8', interval=1, when='D')
LOG_FILE.setFormatter(LOGGING_FORMATTER)

SERVER.addHandler(ERROR_STREAM_HANDLER)
SERVER.addHandler(LOG_FILE)
SERVER.setLevel(LOGGING_LEVEL)

if __name__ == '__main__':
    SERVER.critical('Критическая ошибка')
    SERVER.error('Ошибка')
    SERVER.debug('Отладочная информация')
    SERVER.info('Информационное сообщение')