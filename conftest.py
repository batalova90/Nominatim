import pytest
import requests

from tests.src.enum_api import EnumAPI
from tests.test_api.test_search.Search import Search


@pytest.fixture(scope="session")
def search_fixture(request):
    response = requests.get(
        EnumAPI.GEOCODE_JSON.value
    )
    fixture = Search(response)
    return fixture


