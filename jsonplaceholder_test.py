import json

import pytest
import requests


def get_url(path):
    url = f"https://jsonplaceholder.typicode.com/{path}"
    return url


def get_headers():
    headers = {"Content-type": "application/json; charset=UTF-8"}
    return headers


# проверка статуса 200 и получения первой записи
def test_resource_200():
    response = requests.get(get_url("posts/1"))
    first_resource = response.json()
    assert response.status_code == 200
    assert first_resource["id"] == 1


# проверка статуса 404
def test_resource_404():
    response = requests.get(get_url("404"))
    assert response.status_code == 404


# проверка добавления новой записи
@pytest.mark.parametrize(
    "new_resource",
    [
        ({"title": "foo", "body": "bar", "userId": 1}),
        ({"title": "foo_test", "body": "bar_test", "userId": 2}),
    ],
)
def test_resource_post(new_resource):
    response = requests.post(
        get_url("posts"), data=json.dumps(new_resource), headers=get_headers()
    )
    assert response.status_code == 201


# проверка изменения записи с заданным id
@pytest.mark.parametrize(
    "fields_update, id_resource, result_resource",
    [
        (
            {"title": "test", "body": "test_patch"},
            100,
            {
                "id": 100,
                "title": "test",
                "body": "test_patch",
                "userId": 10,
            },
        ),
        (
            {"title": "test1", "body": "test_patch1"},
            50,
            {
                "id": 50,
                "title": "test1",
                "body": "test_patch1",
                "userId": 5,
            },
        ),
    ],
)
def test_resource_patch(fields_update, id_resource, result_resource):
    response = requests.patch(
        get_url(f"posts/{id_resource}"),
        data=json.dumps(fields_update),
        headers=get_headers(),
    )
    assert response.json() == result_resource


# проверка удаления записи
def test_resource_delete():
    response = requests.delete(get_url("posts/99"))
    assert response.status_code == 200


# проверка фильтрации по заданному userId
def test_resource_filter():
    response = requests.get(get_url("posts?userId=5"))
    result = response.json()
    assert response.status_code == 200
    assert result[0]["userId"] == 5
