import logging

import allure
import requests
from allure_commons.types import Severity
from pytest import mark

from Data import places
from tests.test_api.enum_api import EnumAPI, EnumMessagesError

from ..request_response_output import (allure_attach_request,
                                       allure_attach_response)


@allure.severity(Severity.CRITICAL)
@allure.tag('Lookup')
@mark.parametrize("osm_id",
                  places.osm_id,
                  ids=[x['osm_id'] for x in places.osm_id])
@allure.title("Coordinates: {osm_id[lat]}, {osm_id[lon]}")
def test_lookup_coordinates(osm_id):
    """
    Проверка возврата координат объекта.
    Lookup - запрос
    """
    osm_id_get = osm_id['osm_id']
    with allure.step('Шаг 1: отправить lookup-запрос.'
                     'Параметры запроса - osm_id объекта'):
        get_url_lookup = EnumAPI.LOOKUP_JSON.value + f'{osm_id_get}'
        response_lookup = requests.get(
            get_url_lookup
        )
    response_lookup_json = response_lookup.json()
    allure_attach_request(response_lookup)
    allure_attach_response(response_lookup)
    if len(response_lookup_json) != 0:
        with allure.step('Шаг 2: получить данные объекта (широту и долготу)'):
            coordinates_latitude = float(response_lookup_json[0]['lat'])
            coordinates_longitude = float(response_lookup_json[0]['lon'])
            logging.info(f'Coordinates: lat {coordinates_latitude}, '
                         f'lon {coordinates_longitude} (lookup response)')
        with allure.step('Шаг 3: сравнить координаты объекта (широту и долготу) '
                         'с входными данными'):
            assert coordinates_longitude == osm_id['lon'],\
                EnumMessagesError.INVALID_LONGITUDE_LOOKUP.value
            assert coordinates_latitude == osm_id['lat'], \
                EnumMessagesError.INVALID_LATITUDE_LOOKUP.value
