import pytest
import requests


# Получение url
@pytest.fixture
def get_url(request):
    return request.config.getoption("--url")


# Получение статуса
@pytest.fixture
def get_status(request):
    return request.config.getoption("--status_code")


# Проверка статуса запроса по заданному url
def test_url_status(get_url, get_status):
    response = requests.get(get_url)
    assert response.status_code == get_status
