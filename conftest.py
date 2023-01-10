import json
import os.path

import pytest
import requests

from tests.test_api.enum_api import EnumAPI
from tests.test_api.test_reverse.reverse import Reverse
from tests.test_api.test_search.search import Search


@pytest.fixture(scope="session")
def search_fixture():
    response = requests.get(
        EnumAPI.GEOCODE_JSON.value
    )
    fixture = Search(response)
    return fixture


@pytest.fixture(scope="session")
def reverse_fixture():
    response = requests.get(
        EnumAPI.REVERSE_JSON.value
    )
    fixture = Reverse(response)
    return fixture


@pytest.fixture(scope="function")
def zoom_fixture(request):
    file_zoom = request.config.getoption("--zoom")
    with open(f'./Data/{file_zoom}') as f:
        data_zoom = json.load(f)
    return data_zoom


@pytest.fixture(scope="session")
def places_fixture(request):
    file_places = request.config.getoption("--places")
    with open(f'./Data/{file_places}') as f:
        data_places = json.load(f)
    return data_places


def pytest_collection_modifyitems(session, config, items: list):
    for item in items:
        item.name = item.name.encode('utf-8').decode('unicode-escape')
        item._nodeid = item.nodeid.encode('utf-8').decode('unicode-escape')
    skip_parameter = config.getoption('--skip')
    if skip_parameter is None:
        return items
    for item in items:
        if skip_parameter in item.keywords:
            item.add_marker(pytest.mark.skip)
    return items


def pytest_addoption(parser):
    parser.addoption("--zoom", action="store", default="data_zoom.json")
    parser.addoption("--places", action="store", default="places.json")
    parser.addoption("--skip", action="store", default=None)


