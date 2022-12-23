import allure

from .SearchSchema import GeocodingData, PropertiesGeocodingData, GeometryData


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

