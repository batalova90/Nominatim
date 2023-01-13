import allure
import pytest
from allure_commons.types import Severity

from tests.test_api.enum_api import EnumAPI

from ..request_response_output import (allure_attach_request,
                                       allure_attach_response)
from ..test_search.search_schema import GeometryData
from .reverse_schema import (GeocodingDataReverse,
                             PropertiesGeocodingDataReverse)


@allure.severity(Severity.BLOCKER)
@allure.tag('Reverse')
@allure.title('Server status code (reverse request)')
@pytest.mark.check_server
@pytest.mark.usefixtures('reverse_fixture')
def test_status_code_reverse(reverse_fixture):
    """
    Проверка кода ответа сервера (reverse-запрос)
    """
    with allure.step('Шаг 1: отправить reverse-запроc.'
                     'Параметры запроса - широта и долгота'):
        allure_attach_request(reverse_fixture.response)
        allure_attach_response(reverse_fixture.response)
    with allure.step('Шаг 2: проверить статус кода ответа сервера, '
                     'ожидаемый результат - 200'):
        reverse_fixture.assert_status_code(200)


@allure.severity(Severity.NORMAL)
@allure.tag('Reverse')
@allure.title('Validate geocoding data (reverse request)')
@pytest.mark.validate
@pytest.mark.usefixtures('reverse_fixture')
def test_geocoding_data_reverse(reverse_fixture):
    """
    Проверка запроса (reverse-запрос)
    """
    with allure.step('Шаг 1: отправить reverse-запроc.'
                     'Параметры запроса - широта и долгота'):
        allure_attach_request(reverse_fixture.response)
        allure_attach_response(reverse_fixture.response)
    with allure.step('Шаг 2: проверить json-схему ответа'
                     '(параметр - geocoding)'):
        reverse_fixture.validate_geocoding_data(GeocodingDataReverse)


@allure.severity(Severity.NORMAL)
@allure.tag('Reverse')
@allure.title('Validate properties (reverse request)')
@pytest.mark.validate
@pytest.mark.usefixtures('reverse_fixture')
def test_properties_geocoding_data_reverse(reverse_fixture):
    """
    Проверка возврата характеристик объекта (place_id, label, name и т.д.)
    (reverse-запрос)
    """
    with allure.step('Шаг 1: отправить reverse-запроc.'
                     'Параметры запроса - широта и долгота'):
        allure_attach_request(reverse_fixture.response)
        allure_attach_response(reverse_fixture.response)
    with allure.step('Шаг 2: проверить json-схему ответа'
                     '(параметр - properties)'):
        reverse_fixture.validate_properties_geocoding_data(
            PropertiesGeocodingDataReverse
        )


@allure.severity(Severity.NORMAL)
@allure.tag('Reverse')
@allure.title('Validate coordinates (reverse request)')
@pytest.mark.validate
@pytest.mark.usefixtures('reverse_fixture')
def test_geometry_data_reverse(reverse_fixture):
    """
    Проверка возврата координат объекта (широта, долгота)
    (reverse-запрос)
    """
    with allure.step('Шаг 1: отправить reverse-запроc.'
                     'Параметры запроса - широта и долгота'):
        allure_attach_request(reverse_fixture.response)
        allure_attach_response(reverse_fixture.response)
    with allure.step('Шаг 2: проверить json-схему ответа'
                     '(параметр - geometry)'):
        reverse_fixture.validate_geometry_data(GeometryData)


@allure.severity(Severity.NORMAL)
@allure.tag('Reverse')
@pytest.mark.parametrize('zoom',
                         ['3', '6', '8', '12', '14', '18', ''])
@allure.title('Zoom: {zoom}')
@pytest.mark.usefixtures('reverse_fixture', 'zoom_fixture')
def test_zoom_reverse(reverse_fixture, zoom_fixture, zoom):
    """
    Проверка возврата lable объекта при изменении параметра zoom
    (reverse-запрос)
    """
    with allure.step('Шаг 1: отправить reverse-запроc.'
                     'Параметры запроса - широта, долгота, zoom'):
        reverse_fixture.set_response_json(
            EnumAPI.REVERSE_ZOOM.value,
            zoom
        )
    with allure.step('Шаг 2: получить label объекта'):
        label = reverse_fixture.response_json['features'][0]['properties']['geocoding']['label']
    with allure.step('Шаг 3: сравнить label объекта с входными данными'):
        reverse_fixture.validate_zoom(zoom_fixture[zoom])
        reverse_fixture.set_response_json(
            EnumAPI.REVERSE_JSON.value
        )
