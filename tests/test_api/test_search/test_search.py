import json
import logging

import allure
import pytest
import requests
from allure_commons.types import Severity
from pydantic import ValidationError
from pytest import mark

from tests.test_api.enum_api import EnumAPI, EnumMessagesError

from ..request_response_output import (allure_attach_request,
                                       allure_attach_response)
from . import search
from .search_schema import GeocodingData, GeometryData, PropertiesGeocodingData
from .search_schema_xml import SearchResultsXML


@allure.severity(Severity.BLOCKER)
@allure.tag('Search')
@allure.title('Server status code (search request)')
@pytest.mark.check_server
@pytest.mark.usefixtures('search_fixture')
def test_status_code_search(search_fixture):
    """
    Проверка кода ответа сервера (search-запрос)
    """
    with allure.step('Шаг 1: отправить search-запроc.'):
        allure_attach_request(search_fixture.response)
        allure_attach_response(search_fixture.response)
    with allure.step('Шаг 2: проверить статус кода ответа сервера, '
                     'ожидаемый результат - 200'):
        search_fixture.assert_status_code(200)


@allure.severity(Severity.NORMAL)
@allure.tag('Search')
@allure.title('Validate geocoding data (search request)')
@pytest.mark.validate
@pytest.mark.usefixtures('search_fixture')
def test_geocoding_data_search(search_fixture):
    """
    Проверка декодирования запроса сервером (search-запрос).
    """
    with allure.step('Шаг 1: отправить search-запроc.'):
        allure_attach_request(search_fixture.response)
        allure_attach_response(search_fixture.response)
    with allure.step('Шаг 2: проверить json-схему ответа'
                     '(параметр - geocoding)'):
        try:
            search_fixture.validate_geocoding_data(GeocodingData)
        except ValidationError:
            # logging.exception('Validation error geocoding (search response)')
            raise


@allure.severity(Severity.NORMAL)
@allure.tag('Search')
@allure.title('Validate properties (search request)')
@pytest.mark.validate
@pytest.mark.usefixtures('search_fixture')
def test_properties_geocoding_data_search(search_fixture):
    """
    Проверка возврата характеристик объекта (place_id)
    (search-запрос).
    """
    with allure.step('Шаг 1: отправить search-запроc.'):
        allure_attach_request(search_fixture.response)
        allure_attach_response(search_fixture.response)
    with allure.step('Шаг 2: проверить json-схему ответа'
                     '(параметр - properties)'):
        try:
            search_fixture.validate_properties_geocoding_data(PropertiesGeocodingData)
        except ValidationError:
            logging.exception('Validation error properties (search response)')
            raise


@allure.severity(Severity.NORMAL)
@allure.tag('Search')
@allure.title('Validate coordinates (seqrch request)')
@pytest.mark.validate
@pytest.mark.usefixtures('search_fixture')
def test_geometry_data_search(search_fixture):
    """
    Проверка возврата координат объекта (широта, долгота)
    (search-запрос)
    """
    with allure.step('Шаг 1: отправить search-запроc.'):
        allure_attach_request(search_fixture.response)
        allure_attach_response(search_fixture.response)
    with allure.step('Шаг 2: проверить json-схему ответа'
                     '(параметр - geometry)'):
        try:
            search_fixture.validate_geometry_data(GeometryData)
        except ValidationError:
            logging.exception('Validation error geometry (search response)')
            raise


with open('./Data/city.json') as f:
    data_city = json.load(f)

with open('./Data/city_negative.json') as f_ngtv:
    data_city_negative = json.load(f_ngtv)


@allure.severity(Severity.CRITICAL)
@allure.tag('Search')
@mark.parametrize("place",
                  data_city,
                  ids=[x for x in data_city])
@allure.title('Compare places and coordinates (positive)')
def test_compares_places_and_coordinates_positive(place):
    compares_places_and_coordinates(place)


@allure.severity(Severity.CRITICAL)
@allure.tag('Search')
@mark.parametrize("place",
                  data_city_negative,
                  ids=[x for x in data_city_negative])
@pytest.mark.xfail
@allure.title('Compare places and coordinates (negative)')
def test_compares_places_and_coordinates_negative(place):
    compares_places_and_coordinates(place)


def compares_places_and_coordinates(place):
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


@allure.title('Validate xml format')
@pytest.mark.validate
def test_search_xml_format():
    with allure.step('Шаг 1: отправить search-запрос.'
                     'Формат ответа - xml'):
        response_search = requests.get(
            EnumAPI.SEARCH_XML.value
        )
        logging.info(
            f'Request: {response_search.url},\nResponse: {response_search.content}'
        )
    with allure.step('Шаг 2: проверить xml-схему ответа'):
        try:
            SearchResultsXML.from_xml(response_search.content)
        except ValidationError:
            logging.exception(
                'Validation error xml-format'
            )
            raise
