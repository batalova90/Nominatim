import os.path

import pytest
import requests

from tests.logger import AllureCatchLogs
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


def pytest_collection_modifyitems(session, config, items: list):
    for item in items:
        item.name = item.name.encode('utf-8').decode('unicode-escape')
        item._nodeid = item.nodeid.encode('utf-8').decode('unicode-escape')
        print(item.keywords)
    skip_validate = pytest.mark.skip(reason="need validate option to skip")
    if config.getoption('skipvalidate') is not None:
        for item in items:
            if 'validate' in item.keywords:
                print(item.keywords)
                item.add_marker(skip_validate)


def pytest_addoption(parser):
    parser.addoption("skipvalidate",
                     action="store",
                     default=None)
    parser.addoption("skipcheck",
                     action="store",
                     default=None)


"""

def pytest_addoption(parser):
    parser.addoption(
        "--runslow", action="store_true", default=False, help="run slow tests"
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: mark test as slow to run")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--runslow"):
        #  опция --runslow запрошена в командной строке: медленные тесты не пропускаем
        return
    skip_slow = pytest.mark.skip(reason="need --runslow option to run")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)
"""

