import allure
import requests
from allure_commons.types import Severity
from pytest import mark

from Data import places
from tests.test_api.enum_api import EnumAPI, EnumMessagesError

from . import search
from .search_schema import GeocodingData, GeometryData, PropertiesGeocodingData
from .search_schema_xml import SearchResultsXML


@allure.severity(Severity.BLOCKER)
@allure.tag('Search')
def test_status_code_search(search_fixture):
    """
    Проверка кода ответа сервера (search-запрос)
    """
    search_fixture.assert_status_code(200)


@allure.severity(Severity.NORMAL)
@allure.tag('Search')
def test_geocoding_data_search(search_fixture):
    """
    Проверка декодирования запроса сервером (search-запрос).
    """
    search_fixture.validate_geocoding_data(GeocodingData)
    allure.attach.file(
        'attachment/Query_example.png',
        name='Example query'
    )
    allure.attach.file(
        'attachment/Query_search.png',
        name='Decoding query'
    )


@allure.severity(Severity.NORMAL)
@allure.tag('Search')
def test_properties_geocoding_data_search(search_fixture):
    """
    Проверка возврата характеристик объекта (place_id)
    (search-запрос).
    """
    search_fixture.validate_properties_geocoding_data(PropertiesGeocodingData)
    allure.attach.file(
        'attachment/Query_example.png',
        name='Example query'
    )
    allure.attach.file(
        'attachment/Search_place_id.png',
        name='Check place_id'
    )


@allure.severity(Severity.NORMAL)
@allure.tag('Search')
def test_geometry_data_search(search_fixture):
    """
    Проверка возврата координат объекта (широта, долгота)
    (search-запрос)
    """
    search_fixture.validate_geometry_data(GeometryData)
    allure.attach.file(
        'attachment/Query_example.png',
        name='Example query'
    )
    allure.attach.file(
        'attachment/Coordinates.png',
        name='Example coordinates'
    )


@allure.severity(Severity.CRITICAL)
@allure.tag('Search')
@mark.parametrize("place",
                  places.city,
                  ids=[x for x in places.city])
def test_compares_places_and_coordinates(place):
    """
    Проверка возврата координат объекта.
    Сравнение данных search - reverse запросов (по osm_id).
    """
    with allure.step('Шаг 1: отправить search-запрос.'
                     'Параметры запроса - наименование обекта'):
        get_url_search = EnumAPI.SEARCH_OBJECT.value + f'{place}&format=json'
        response_search = requests.get(
            get_url_search
        )
    response_search_json = response_search.json()
    coordinates = []
    if len(response_search_json) != 0:
        with allure.step('Шаг 2: получить данные объекта (координаты, osm_id)'):
            osm_id_search = search.Search.get_osm_id(
                response_search_json[0],
                coordinates
            )
        with allure.step('Шаг 3: отправить reverse-запрос.'
                         'Параметры запроса - координаты объекта, полученные на шаге 2'):
            get_url_reverse = EnumAPI.REVERSE_OBJECT.value + f'{coordinates[0]}&lon={coordinates[1]}'
            response_reverse_json = requests.get(
                    get_url_reverse
            ).json()
        with allure.step('Шаг 4: получить osm_id объекта'):
            osm_id_reverse = response_reverse_json['osm_id']
        with allure.step('Шаг 5: сравнить osm_id объектов reverse и search запросов'):
            assert osm_id_reverse == osm_id_search,\
                EnumMessagesError.INVALID_OSM_ID.value


def test_search_xml_format():
    response_search = requests.get(
        EnumAPI.SEARCH_XML.value
    )
    SearchResultsXML.from_xml(response_search.content)
