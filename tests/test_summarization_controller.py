import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from nltk.tokenize import sent_tokenize
from main import app as flask_app
from test_data import *


@pytest.fixture
def client():
    return flask_app.test_client()


def test_extractive(client):
    URL = '/summarization/extractive'
    text = get_extractive_text()

    response = client.post(URL, json=create_extractive_data('', 4))
    assert '' == response.data.decode('utf-8'), f'Отправляем по пути "{URL}" пустую строку'

    response = client.post(URL, json=create_extractive_data(text, -1))
    assert 0 == len(sent_tokenize(response.data.decode('utf-8'))), f'Отправляем по пути "{URL}" top_n=-1'

    response = client.post(URL, json=create_extractive_data(text, 0))
    assert 0 == len(sent_tokenize(response.data.decode('utf-8'))), f'Отправляем по пути "{URL}" top_n=0'

    response = client.post(URL, json=create_extractive_data(text, 2))
    assert 2 == len(sent_tokenize(response.data.decode('utf-8'))), f'Отправляем по пути "{URL}" top_n=2'

    response = client.post(URL, json=create_extractive_data(text, len(sent_tokenize(text)) + 1))
    assert len(sent_tokenize(text)) == len(sent_tokenize(
        response.data.decode('utf-8'))), f'Отправляем по пути "{URL}" top_n=кол-ву предложений в исходном тексте'


def test_abstractive(client):
    URL = '/summarization/abstractive'
    text = get_abstractive_text()
    text_length = len(text)
    max_length = int(0.7 * text_length)
    min_length = int(0.4 * text_length)

    response = client.post(URL, json=create_abstractive_data(text))
    assert '' == response.data.decode('utf-8'), f'Отправляем по пути "{URL}" пустую строку'

    response = client.post(URL, json=create_abstractive_data(text))
    response_text_length = len(response.data.decode('utf-8'))
    assert min_length <= response_text_length and max_length >= response_text_length, f'Получаем по пути "{URL}" текст длиной от {min_length} до {max_length} символов ({response_text_length})'
