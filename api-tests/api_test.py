import pytest
import requests
from requests import Response
from api_tests_reqres_in.tools import tools
from datetime import date
from schemas import reqres
from pytest_voluptuous import S


def test_get_single_user_status_code():
    """Статус код 200"""
    url = "https://reqres.in/api/users/2"

    response: Response = requests.get(url)

    assert response.status_code == 200


@pytest.mark.parametrize('user_id', [2, 3, 4, 5])
def test_get_single_user_id(user_id):
    """id равно значению запроса из url"""
    url = f"https://reqres.in/api/users/{user_id}"

    response: Response = requests.get(url)

    assert response.json()["data"]["id"] == user_id


def test_get_single_user_length_single():
    """В ответе один пользователь"""
    url = "https://reqres.in/api/users/2"

    response: Response = requests.get(url)
    resp = response.json()
    assert tools.data_len(resp) == 1


def test_get_single_user_header_server():
    """В headers ключ Server имеет значение cloudflare"""
    url = "https://reqres.in/api/users/2"

    response: Response = requests.get(url)
    assert response.headers.get("Server") == "cloudflare"


def test_get_single_user_time_to_request():
    """Запрос выполняется быстрее 0,2 секунды"""
    url = "https://reqres.in/api/users/2"

    response: Response = requests.get(url)
    assert response.elapsed.total_seconds() < 0.2


@pytest.mark.parametrize('name', ['Ivan', 'Dima', 'Misha'])
def test_post_create_new_user_name(name):
    """Создается пользователь с отправленным в запросе именем"""
    url = "https://reqres.in/api/users"
    request_body = {
        "name": f"{name}",
        "job": "leader"
    }
    response: Response = requests.post(url, request_body)
    assert response.json()["name"] == name


def test_post_create_actual_date():
    """Дата создания соответствует текущей"""
    url = "https://reqres.in/api/users"
    request_body = {
        "name": "Zoi",
        "job": "leader"
    }
    response: Response = requests.post(url, request_body)
    assert tools.get_date(response.json()["createdAt"]) == date.today().strftime('%Y-%m-%d')


def test_post_register_schema():
    """Дата создания соответствует текущей"""
    url = "https://reqres.in/api/register"
    request_body = {
        "email": "eve.holt@reqres.in",
        "password": "pistol"
    }
    response: Response = requests.post(url, request_body)
    assert S(reqres.user_schema) == response.json()
