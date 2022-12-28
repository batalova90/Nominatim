import pytest
import requests

from tests.test_api.enum_api import EnumAPI
from tests.test_api.test_reverse.Reverse import Reverse
from tests.test_api.test_search.Search import Search


@pytest.fixture(scope="session")
def search_fixture(request):
    response = requests.get(
        EnumAPI.GEOCODE_JSON.value
    )
    fixture = Search(response)
    return fixture


@pytest.fixture(scope="session")
def reverse_fixture(request):
    response = requests.get(
        EnumAPI.REVERSE_JSON.value
    )
    fixture = Reverse(response)
    return fixture
