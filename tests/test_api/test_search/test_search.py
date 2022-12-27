import allure
import requests
from pytest import mark

from Data import places
from tests.src.enum_api import EnumMessagesError, EnumAPI

from . import Search
from .SearchSchema import GeocodingData, GeometryData, PropertiesGeocodingData


def test_status_code_search(search_fixture):
    """
    Проверка кода ответа сервера (search-запрос)
    """
    search_fixture.assert_status_code(200)


def test_geocoding_data_search(search_fixture):
    """
    Проверка декодирования запроса сервером (search-запрос).
    """
    search_fixture.validate_geocoding_data(GeocodingData)
    allure.attach.file(
        'attachment/Query_example.png', name='Example query'
    )
    allure.attach.file(
        'attachment/Query_search.png', name='Decoding query'
    )


def test_properties_geocoding_data_search(search_fixture):
    """
    Проверка возврата характеристик объекта (place_id)
    (search-запрос).
    """
    search_fixture.validate_properties_geocoding_data(PropertiesGeocodingData)
    allure.attach.file(
        'attachment/Query_example.png', name='Example query'
    )
    allure.attach.file(
        'attachment/Search_place_id.png', name='Check place_id'
    )


def test_geometry_data_search(search_fixture):
    """
    Проверка возврата координат объекта (широта, долгота)
    (search-запрос)
    """
    search_fixture.validate_geometry_data(GeometryData)
    allure.attach.file(
        'attachment/Query_example.png', name='Example query'
    )
    allure.attach.file(
        'attachment/Coordinates.png', name='Example coordinates'
    )


@mark.parametrize("place",
                  places.city,
                  ids=[x for x in places.city])
def test_compares_places_and_coordinates(place):
    """
    Проверка возврата координат объекта.
    Сравнение данных search - reverse запросов (по osm_id).
    """
    get_url_search = EnumAPI.SEARCH_OBJECT.value + f'{place}&format=json'
    response_search = requests.get(
        get_url_search
    )
    response_search_json = response_search.json()
    coordinates = []
    if len(response_search_json) != 0:
        osm_id_search = Search.Search.get_osm_id(
            response_search_json[0],
            coordinates
        )
        get_url_reverse = EnumAPI.REVERSE_OBJECT.value + f'{coordinates[0]}&lon={coordinates[1]}'
        response_reverse_json = requests.get(
                get_url_reverse
        ).json()
        osm_id_reverse = response_reverse_json['osm_id']
        assert osm_id_reverse == osm_id_search, EnumMessagesError.INVALID_OSM_ID.value
