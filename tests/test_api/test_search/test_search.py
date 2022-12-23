import requests
from .Search import Search
from tests.src.enum_api import EnumAPI, EnumMessagesError
from .SearchSchema import GeocodingData, PropertiesGeocodingData, GeometryData



def test_search_geocodejson():
    response = requests.get(
        EnumAPI.GEOCODE_JSON.value
    )
    search_response = Search(response)
    #search_response.validate(GeocodingData)
    #search_response.validate(PropertiesGeocodingData)
    search_response.validate(GeometryData)
    search_response.assert_status_code(200)

