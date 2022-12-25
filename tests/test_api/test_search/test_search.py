import allure
from pytest import mark
import requests
from random import randint

from .SearchSchema import GeocodingData, PropertiesGeocodingData, GeometryData
from Data import places

def test_status_code_search(search_fixture):
    """
    Проверка кода ответа сервера (search-запрос)
    """
    search_fixture.assert_status_code(200)



def test_geocoding_data_search(search_fixture):
    """
    Проверка декодирования запроса сервером (search-запрос)
    """
    search_fixture.validate_geocoding_data(GeocodingData)
    allure.attach.file('attachment/Query_example.png', name='Example query')
    allure.attach.file('attachment/Query_search.png', name='Decoding query')


def test_properties_geocoding_data_search(search_fixture):
    """
    Проверка возврата характеристик объекта (place_id)
    (search-запрос)
    """
    search_fixture.validate_properties_geocoding_data(PropertiesGeocodingData)
    allure.attach.file('attachment/Query_example.png', name='Example query')
    allure.attach.file('attachment/Search_place_id.png', name='Check place_id')


def test_geometry_data_search(search_fixture):
    """
    Проверка возврата координат объекта (широта, долгота)
    (search-запрос)
    """
    search_fixture.validate_geometry_data(GeometryData)
    allure.attach.file('attachment/Query_example.png', name='Example query')
    allure.attach.file('attachment/Coordinates.png', name='Example coordinates')


@mark.parametrize('execution_number', range(5))
def test_test_compares_places_and_coordinates(execution_number):
    """
    Проверка возврата координат объекта по ключевым словам
    и городу (search/reverse-запросы)
    """
    special_word = places.special_phrases[randint(0, len(places.special_phrases)-1)]
    city_word = places.city[randint(0, len(places.city)-1)]
    limit = randint(1, 50)
    response_search = requests.get(
        f'https://nominatim.openstreetmap.org/?addressdetails=1&q={special_word}+{city_word}&format=json&limit={limit}'
    )
    response_search_json = response_search.json()
    # получить массив координат, затем прогнать запросы по reverse,
    # сравнить между собой по индексу, либо индексу и координатам
    print(response_search_json)