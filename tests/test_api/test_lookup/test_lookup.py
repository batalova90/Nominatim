import allure
import requests
from allure_commons.types import Severity
from pytest import mark

from Data import places
from tests.test_api.enum_api import EnumAPI, EnumMessagesError


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
    get_url_lookup = EnumAPI.LOOKUP_JSON.value + f'{osm_id_get}'
    response_lookup = requests.get(
        get_url_lookup
    )
    response_lookup_json = response_lookup.json()
    if len(response_lookup_json) != 0:
        coordinates_latitude = float(response_lookup_json[0]['lat'])
        coordinates_longitude = float(response_lookup_json[0]['lon'])
        assert coordinates_longitude == osm_id['lon'],\
            EnumMessagesError.INVALID_LONGITUDE_LOOKUP.value
        assert coordinates_latitude == osm_id['lat'], \
            EnumMessagesError.INVALID_LATITUDE_LOOKUP.value
    allure.attach.file(
        'attachment/Query_example_lookup.png',
        name='Example query'
    )
    allure.attach.file(
        'attachment/Response_example_lookup.png',
        name='Example response'
    )
