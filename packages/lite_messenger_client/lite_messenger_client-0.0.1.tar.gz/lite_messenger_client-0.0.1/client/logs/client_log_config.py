"""Кофнфиг клиентского логгера."""

import os
import sys
import logging

from common.settings import ENCODING, LOGGING_LEVEL

sys.path.append('../')

# создаём формировщик логов (formatter):
CLIENT_FORMATTER = logging.Formatter('%(asctime)s %(levelname)s '
                                     '%(filename)s %(message)s')

# Подготовка имени файла для логирования
PATH = os.getcwd()
PATH = os.path.join(PATH, 'log_files\\client.log')

# создаём потоки вывода логов
STREAM_HANDLER = logging.StreamHandler(sys.stderr)
STREAM_HANDLER.setFormatter(CLIENT_FORMATTER)
STREAM_HANDLER.setLevel(logging.INFO)
LOG_FILE = logging.FileHandler(PATH, encoding=ENCODING)
LOG_FILE.setFormatter(CLIENT_FORMATTER)

# создаём регистратор и настраиваем его
LOGGER = logging.getLogger('client')
LOGGER.addHandler(STREAM_HANDLER)
LOGGER.addHandler(LOG_FILE)
LOGGER.setLevel(LOGGING_LEVEL)

# отладка
if __name__ == '__main__':
    LOGGER.critical('Критическая ошибка')
    LOGGER.error('Ошибка')
    LOGGER.debug('Отладочная информация')
    LOGGER.info('Информационное сообщение')
