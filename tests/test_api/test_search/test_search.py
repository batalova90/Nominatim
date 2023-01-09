import logging

import allure
import requests
from allure_commons.types import Severity
from pydantic import ValidationError
from pytest import mark

from Data import places
from tests.test_api.enum_api import EnumAPI, EnumMessagesError

from ..request_response_output import (allure_attach_request,
                                       allure_attach_response)
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
    allure_attach_request(search_fixture.response)
    allure_attach_response(search_fixture.response)
    try:
        search_fixture.validate_geocoding_data(GeocodingData)
    except ValidationError:
        logging.exception('Validation error geocoding (search response)')
        raise


@allure.severity(Severity.NORMAL)
@allure.tag('Search')
def test_properties_geocoding_data_search(search_fixture):
    """
    Проверка возврата характеристик объекта (place_id)
    (search-запрос).
    """
    allure_attach_request(search_fixture.response)
    allure_attach_response(search_fixture.response)
    try:
        search_fixture.validate_properties_geocoding_data(PropertiesGeocodingData)
    except ValidationError:
        logging.exception('Validation error properties (search response)')
        raise



@allure.severity(Severity.NORMAL)
@allure.tag('Search')
def test_geometry_data_search(search_fixture):
    """
    Проверка возврата координат объекта (широта, долгота)
    (search-запрос)
    """
    allure_attach_request(search_fixture.response)
    allure_attach_response(search_fixture.response)
    try:
        search_fixture.validate_geometry_data(GeometryData)
    except ValidationError:
        logging.exception('Validation error geometry (search response)')
        raise



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
    allure_attach_request(response_search)
    allure_attach_response(response_search)
    if len(response_search_json) != 0:
        with allure.step('Шаг 2: получить данные объекта (координаты, osm_id)'):
            osm_id_search = search.Search.get_osm_id(
                response_search_json[0],
                coordinates
            )
            logging.info(f'Place lat: {coordinates[0]}, '
                         f'lon: {coordinates[1]} (search response)')

        with allure.step('Шаг 3: отправить reverse-запрос.'
                         'Параметры запроса - координаты объекта, полученные на шаге 2'):
            get_url_reverse = EnumAPI.REVERSE_OBJECT.value + f'{coordinates[0]}&lon={coordinates[1]}'
            response_reverse_json = requests.get(
                    get_url_reverse
            ).json()
            coordinates_reverse = [
                response_reverse_json['lat'], response_reverse_json['lon']
            ]
            logging.info(f'Place lat: {coordinates_reverse[0]},'
                         f'lon: {coordinates_reverse[1]} (reverse response)\n')
        with allure.step('Шаг 4: получить osm_id объекта'):
            osm_id_reverse = response_reverse_json['osm_id']
        with allure.step('Шаг 5: сравнить osm_id объектов reverse и search запросов'):
            assert osm_id_reverse == osm_id_search,\
                EnumMessagesError.INVALID_OSM_ID.value


def test_search_xml_format():
    response_search = requests.get(
        EnumAPI.SEARCH_XML.value
    )
    logging.info(
        f'Request: {response_search.url},\nResponse: {response_search.content}'
    )
    try:
        SearchResultsXML.from_xml(response_search.content)
    except ValidationError:
        logging.exception(
            f'Validation error xml-format'
        )
        raise


def test_foo(search_fixture):
    logging.info(
        search_fixture.response.status_code
    )
    assert 1 == 2