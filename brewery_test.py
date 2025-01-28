import requests
import re


# задание базового url, получение статуса и ответа в формате json
def get_brewery(path, param):
    response = requests.get(
        f"https://api.openbrewerydb.org/v1/breweries/{path}", params=param
    )
    return [response.status_code, response.json()]


# проверка статуса 200 и ограничения количества записей
def test_brewery_200():
    param_count = {"per_page": 2}
    brewery = get_brewery("", param_count)
    assert brewery[0] == 200
    assert len(brewery[1]) == 2


# проверка статуса 404
def test_brewery_404():
    brewery = get_brewery("test", "")
    assert brewery[0] == 404


# проверка названия по заданному id
def test_brewery_id():
    brewery = get_brewery("b54b16e1-ac3b-4bff-a11f-f7ae9ddc27e0", "")
    assert brewery[1]["name"] == "MadTree Brewing 2.0"


# проверка количества в заданной стране
def test_brewery_country():
    param_dist = {"by_country": "United States"}
    brewery = get_brewery("meta", param_dist)
    assert int(brewery[1]["total"]) == 8032


# проверка формирование списка для автозаполнения
def test_brewery_autocomplete():
    param_query = {"query": "Brewing"}
    brewery = get_brewery("autocomplete", param_query)
    result_search = re.search(r"Brewing", brewery[1][0]["name"])
    assert list(brewery[1][0].keys()) == ["id", "name"]
    assert result_search.group(0) == "Brewing"
