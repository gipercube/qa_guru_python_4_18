import pytest
import requests
from requests import Response
from api_tests_reqres_in.helpers import tools, urls, request_bodies
from datetime import date
from schemas import reqres
from pytest_voluptuous import S


def test_get_single_user_status_code():
    """Статус код 200"""
    response: Response = requests.get(urls.get_single_user_2_url)
    assert response.status_code == 200


@pytest.mark.parametrize('user_id', [2, 3, 4, 5])
def test_get_single_user_id(user_id):
    """id равно значению запроса из url"""
    response: Response = requests.get(f'{urls.get_single_user_url}/{user_id}')
    assert response.json()["data"]["id"] == user_id


def test_get_single_user_length_single():
    """В ответе один пользователь"""
    response: Response = requests.get(urls.get_single_user_2_url)
    resp = response.json()
    assert tools.data_len(resp) == 1


def test_get_single_user_header_server():
    """В headers ключ Server имеет значение cloudflare"""
    response: Response = requests.get(urls.get_single_user_2_url)
    assert response.headers.get("Server") == "cloudflare"


def test_get_single_user_time_to_request():
    """Запрос выполняется быстрее 0,2 секунды"""
    response: Response = requests.get(urls.get_single_user_2_url)
    assert response.elapsed.total_seconds() < 0.2


@pytest.mark.parametrize('name', ['Ivan', 'Dima', 'Misha'])
def test_post_create_new_user_name(name):
    """Создается пользователь с отправленным в запросе именем"""
    response: Response = requests.post(urls.post_create_new_user_url, tools.insert_name(name))
    assert response.json()["name"] == name



def test_post_create_actual_date():
    """Дата создания соответствует текущей"""
    response: Response = requests.post(urls.post_create_new_user_url, request_bodies.create_new_user)
    assert tools.get_date(response.json()["createdAt"]) == date.today().strftime('%Y-%m-%d')


def test_post_register_schema():
    """Проверка JSON-Schema ответа"""
    response: Response = requests.post(urls.post_register_url, request_bodies.register_new_user)
    assert S(reqres.user_schema) == response.json()


def test_post_register_token_length():
    """Длина токена равна 17 символам"""
    response: Response = requests.post(urls.post_register_url, request_bodies.register_new_user)
    assert len(response.json()["token"]) == 17


def test_post_login_unsuccessful():
    """Статус код 400, ошибка в теле ответа"""
    response: Response = requests.post(urls.post_login_url, request_bodies.login_unsuccessful)
    assert response.status_code == 400
    assert response.json()["error"] == "Missing password"
