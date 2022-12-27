from pytest import mark
import requests

from tests.src.enum_api import EnumMessagesError, EnumAPI
from Data import places


@mark.parametrize("osm_id",
                  places.osm_id,
                  ids=[x['osm_id'] for x in places.osm_id])
def test_lookup_coordinates(osm_id):
    """
    Проверка возврата координат объекта.
    Lookup - запрос
    """
    osm_id_get = osm_id['osm_id']
    print(osm_id_get)
    get_url_lookup = EnumAPI.LOOKUP_JSON.value + f'{osm_id_get}'
    print(get_url_lookup)
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