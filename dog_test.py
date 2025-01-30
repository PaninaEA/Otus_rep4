import pytest
import requests


# задание базового url, получение ответа в формате json
def get_dog(path):
    response = requests.get(f"https://dog.ceo/api/{path}")
    return response.json()


# проверка статуса
def test_dog_status():
    dog = get_dog("breeds/list/all")
    assert dog["status"] == "success"


# проверка статуса 404
def test_dog_404():
    dog = get_dog("test")
    assert dog["status"] == "error"
    assert dog["code"] == 404


# проверка получения корректной ссылки в рандом-запросе
def test_dog_random():
    dog = get_dog("breeds/image/random")
    random_breed = requests.get(dog["message"])
    assert random_breed.status_code == 200


# проверка списка подвидов
@pytest.mark.parametrize(
    "breed, sub_breed",
    [
        (
            "hound",
            ["afghan", "basset", "blood", "english", "ibizan", "plott", "walker"],
        ),
        (
            "mastiff",
            ["bull", "english", "indian", "tibetan"]
        ),
    ],
)
def test_dog_sub_breed(breed, sub_breed):
    dog = get_dog(f"breed/{breed}/list")
    assert dog["message"] == sub_breed


# проверка получения рандомной картинки для породы Гончая
def test_dog_random_image():
    dog = get_dog("breed/hound/images/random")
    random_image = requests.get(dog["message"])
    assert random_image.status_code == 200
