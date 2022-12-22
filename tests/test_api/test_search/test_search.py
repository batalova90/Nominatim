import requests

from .Search import Search
from tests.src.enum_api import EnumAPI, EnumMessagesError
from .SearchSchema import GetSearch



def test_search_geocodejson():
    response = requests.get(
        EnumAPI.GEOCODE_JSON.value
    )
    search_response = Search(response)
    print(search_response.response_json['geocoding'])
    search_response.validate(GetSearch)
    search_response.assert_status_code(200)

