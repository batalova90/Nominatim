import json

import pytest
import requests
import logging
import allure

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


# log = logging.getLogger('conftest')


def pytest_exception_interact(node, call, report):

    logging.debug("[pytest_exception_interact] node: " + str(node.__dict__))

    testlib = node.__getattribute__('funcargs')
    for key, cls in testlib.items():
        logging.error(f'[pytest_exception]: {node.__dict__}')
        logging.error(f'[pytest_exception]: {key}')
        logging.error(f'[pytest_exception]: {cls}')
        # log_path = cls.service.log_path
        print(node.__dict__['originalname'])
        print(call)
"""
    for key, cls in testlib.items():
        logging.debug("[pytest_exception_interact] node: " + str(node.__dict__))
        logging.debug("[pytest_exception_interact] key: " + str(key))
        logging.debug("[pytest_exception_interact] cls: " + str(cls))
        log_path = cls.service.log_path
        log_name = str(key) + '.log'
        logging.debug("[pytest_exception_interact] log_name: " + str(log_name))
        logging.debug("[pytest_exception_interact] log_path: " + str(log_path))
        if (log_path is not None):
            logfile = open(log_path, 'r')
            lines = logfile.read()
            allure.attach(
               name=log_name,
               contents=lines,
               type=allure.constants.AttachmentType.TEXT)

"""



"""
https://www.lambdatest.com/automation-testing-advisor/python/pytest-pytest_exception_interact
"""


def pytest_addoption(parser):
    parser.addoption("--zoom", action="store", default="data_zoom.json")
    parser.addoption("--places", action="store", default="places.json")
    parser.addoption("--skip", action="store", default=None)


