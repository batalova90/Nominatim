import allure
import pytest
from allure_commons.types import Severity
import logging
from pydantic import ValidationError

from tests.test_api.enum_api import EnumAPI

from ..request_response_output import (allure_attach_request,
                                       allure_attach_response)
from ..test_search.search_schema import GeometryData
from .reverse_schema import (GeocodingDataReverse,
                             PropertiesGeocodingDataReverse)


@allure.severity(Severity.BLOCKER)
@allure.tag('Reverse')
def test_status_code_reverse(reverse_fixture):
    """
    Проверка кода ответа сервера (reverse-запрос)
    """
    allure_attach_request(reverse_fixture.response)
    allure_attach_response(reverse_fixture.response)
    reverse_fixture.assert_status_code(200)


@allure.severity(Severity.NORMAL)
@allure.tag('Reverse')
def test_geocoding_data_reverse(reverse_fixture):
    """
    Проверка запроса (reverse-запрос)
    """
    allure_attach_request(reverse_fixture.response)
    allure_attach_response(reverse_fixture.response)
    try:
        reverse_fixture.validate_geocoding_data(GeocodingDataReverse)
    except ValidationError as e:
        logging.exception(f'Validation error geocoding (reverse response) {e}')
        raise


@allure.severity(Severity.NORMAL)
@allure.tag('Reverse')
def test_properties_geocoding_data_reverse(reverse_fixture):
    """
    Проверка возврата характеристик объекта (place_id, label, name и т.д.)
    (reverse-запрос)
    """
    allure_attach_request(reverse_fixture.response)
    allure_attach_response(reverse_fixture.response)
    try:
        reverse_fixture.validate_properties_geocoding_data(
            PropertiesGeocodingDataReverse
        )
    except ValidationError:
        logging.exception(
            'Validation error properties (reverse response)'
        )


@allure.severity(Severity.NORMAL)
@allure.tag('Reverse')
def test_geometry_data_reverse(reverse_fixture):
    """
    Проверка возврата координат объекта (широта, долгота)
    (reverse-запрос)
    """
    allure_attach_request(reverse_fixture.response)
    allure_attach_response(reverse_fixture.response)
    try:
        reverse_fixture.validate_geometry_data(GeometryData)
    except ValidationError:
        logging.exception(
            'Validation error geometry (reverse response)')


@allure.severity(Severity.NORMAL)
@allure.tag('Reverse')
@pytest.mark.parametrize("zoom",
                         ['3', '6', '8', '12', '14', '18'])
@allure.title("Zoom: {zoom}")
def test_zoom_reverse(reverse_fixture, zoom):
    """
    Проверка возврата lable объекта при изменении параметра zoom
    (reverse-запрос)
    """
    reverse_fixture.set_response_json(
        EnumAPI.REVERSE_ZOOM.value, zoom
    )
    label = reverse_fixture.response_json['features'][0]['properties']['geocoding']['label']
    logging.info(
        f'Response label: {label}, zoom: {zoom}'
    )
    reverse_fixture.validate_zoom(zoom)
    reverse_fixture.set_response_json(
        EnumAPI.REVERSE_JSON.value
    )
