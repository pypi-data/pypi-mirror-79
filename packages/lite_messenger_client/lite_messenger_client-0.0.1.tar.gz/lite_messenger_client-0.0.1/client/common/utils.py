"""Утилиты."""

import json
import sys

from common.decorators import log
from common.settings import MAX_PACKAGE_LENGTH, ENCODING

sys.path.append('../')


@log
def get_message(client):
    """
    Функция приёма и декодирования сообщения.
    Принимает байты выдаёт словарь,
    если принято что-то другое отдаёт ошибку значения.
    : param client: сокет для передачи данных.
    : return: словарь - сообщение.
    """
    encoded_response = client.recv(MAX_PACKAGE_LENGTH)
    json_response = encoded_response.decode(ENCODING)
    response = json.loads(json_response)
    if isinstance(response, dict):
        return response
    else:
        raise TypeError


@log
def send_message(sock, message):
    """
    Функция отправки словарей через сокет.
    Кодирует словарь в формат JSON и отправляет через сокет.
    : param sock: сокет для передачи
    : param message: словарь для передачи
    : return: ничего не возвращает
    """
    js_message = json.dumps(message)
    encoded_message = js_message.encode(ENCODING)
    sock.send(encoded_message)
