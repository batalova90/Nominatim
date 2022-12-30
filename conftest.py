import pytest
import requests

from tests.test_api.enum_api import EnumAPI
from tests.test_api.test_reverse.reverse import Reverse
from tests.test_api.test_search.search import Search


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


def exist_name_package(name_package: str, name: str) -> bool:
    return name in name_package.split("/")[2].split('_')


# отключить пакеты
def pytest_collection_modifyitems(session, config, items: list):
    for item in items:
        item.name = item.name.encode('utf-8').decode('unicode-escape')
        item._nodeid = item.nodeid.encode('utf-8').decode('unicode-escape')
        if not(exist_name_package(item._nodeid, 'search')):
            print(item.get_closest_marker)
            items.remove(item)


"""
def pytest_configure(config):
    # register an additional marker (see pytest_collection_modifyitems)
    config.addinivalue_line(
        "markers", "dont_collect: marks a test that should not be collected (avoids skipping it)"
    )
https://github.com/yzc1114/DLProfiler/blob/ce6d93a655c69958928a1b9d2332356b0a42b56f/model_factory/repos/pytorch_vision_v0.10.0/test/conftest.py
def pytest_collection_modifyitems(items):
    # This hook is called by pytest after it has collected the tests (google its name!)
    # We can ignore some tests as we see fit here. In particular we ignore the tests that
    # we have marked with the custom 'dont_collect' mark. This avoids skipping the tests,
    # since the internal fb infra doesn't like skipping tests.
    to_keep = [item for item in items if item.get_closest_marker('dont_collect') is None]
    items[:] = to_keep
"""
