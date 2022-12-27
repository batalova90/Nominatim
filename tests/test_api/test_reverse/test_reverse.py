import allure
import pytest

from tests.src.enum_api import EnumAPI

from ..test_search.SearchSchema import GeometryData
from .ReverseSchema import GeocodingDataReverse, PropertiesGeocodingDataReverse


@allure.tag('Reverse')
def test_status_code_reverse(reverse_fixture):
    """
    Проверка кода ответа сервера (reverse-запрос)
    """
    reverse_fixture.assert_status_code(200)


@allure.tag('Reverse')
def test_geocoding_data_reverse(reverse_fixture):
    """
    Проверка запроса (reverse-запрос)
    """
    reverse_fixture.validate_geocoding_data(GeocodingDataReverse)
    allure.attach.file(
        'attachment/Query_example_reverse.png',
        name='Example query'
    )
    allure.attach.file(
        'attachment/Query_reverse.png',
        name='Query'
    )


@allure.tag('Reverse')
def test_properties_geocoding_data_reverse(reverse_fixture):
    """
    Проверка возврата характеристик объекта (place_id, label, name и т.д.)
    (reverse-запрос)
    """
    reverse_fixture.validate_properties_geocoding_data(
        PropertiesGeocodingDataReverse
    )
    allure.attach.file(
        'attachment/Query_example_reverse.png',
        name='Example query'
    )
    allure.attach.file(
        'attachment/Geocoding_data.png',
        name='Geocoding data'
    )


@allure.tag('Reverse')
def test_geometry_data_reverse(reverse_fixture):
    """
    Проверка возврата координат объекта (широта, долгота)
    (reverse-запрос)
    """
    reverse_fixture.validate_geometry_data(GeometryData)
    allure.attach.file(
        'attachment/Query_example_reverse.png',
        name='Example query'
    )
    allure.attach.file(
        'attachment/Geometry_data.png',
        name='Geometry data'
    )


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
    reverse_fixture.validate_zoom(zoom)
    reverse_fixture.set_response_json(EnumAPI.REVERSE_JSON.value)
    allure.attach.file(
        f'attachment/Query_example_reverse{zoom}.png',
        name=f'Example query(zoom={zoom})'
    )
