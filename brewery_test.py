from http import HTTPStatus

import pytest
import requests
import re


# задание базового url, получение статуса и ответа в формате json
def get_brewery(path, param):
    response = requests.get(
        f"https://api.openbrewerydb.org/v1/breweries/{path}", params=param
    )
    if response.status_code != HTTPStatus.OK:
        return response.status_code, None
    return response.status_code, response.json()


# проверка статуса 200 и ограничения количества записей
@pytest.mark.parametrize(
    "request_params, count",
    [
        ({"per_page": 2}, 2),
        ({"per_page": 5}, 5),
    ],
)
def test_brewery_200(request_params, count):
    status_code, brewery = get_brewery("", request_params)
    assert status_code == 200
    assert len(brewery) == count


# проверка статуса 404
def test_brewery_404():
    status_code, _ = get_brewery("test", "")
    assert status_code == 404


# проверка названия по заданному id
def test_brewery_id():
    _, brewery = get_brewery("b54b16e1-ac3b-4bff-a11f-f7ae9ddc27e0", "")
    assert brewery["name"] == "MadTree Brewing 2.0"


# проверка количества в заданной стране
@pytest.mark.parametrize(
    "request_params, brewery_count",
    [
        ({"by_country": "United States"}, 8032),
        ({"by_country": "South Korea"}, 61),
        ({"by_country": "France"}, 3),
    ],
)
def test_brewery_country(request_params, brewery_count):
    _, brewery = get_brewery("meta", request_params)
    assert int(brewery["total"]) == brewery_count


# проверка формирование списка для автозаполнения
@pytest.mark.parametrize(
    "request_params, search_str", [({"query": "Brewing"}, "Brewing")]
)
def test_brewery_autocomplete(request_params, search_str):
    _, brewery = get_brewery("autocomplete", request_params)
    result_search = re.search(search_str, brewery[0]["name"])
    assert list(brewery[0].keys()) == ["id", "name"]
    assert result_search.group(0) == search_str
