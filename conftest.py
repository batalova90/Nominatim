import json

import pytest
import requests
import logging
import inspect
# import sys
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


@pytest.mark.trylast
def pytest_configure(config):
    terminal = config.pluginmanager.getplugin('terminalreporter')
    config.pluginmanager.register(TestDescriptionPlugin(terminal), 'testdescription')
    print(config)


class TestDescriptionPlugin:
    def __init__(self, terminal):
        self.terminal_reporter = terminal
        self.desc = None

    def pytest_runtest_protocol(self, item):
        self.desc = inspect.getdoc(item.obj)

        #print(self.terminal_reporter.showlongtestinfo)
        # self.terminal_reporter = item.name

    @pytest.hookimpl(hookwrapper=True, tryfirst=True)
    def pytest_runtest_logstart(self, nodeid, location):
        # print(self.terminal_reporter)
        # print(self.write_fspath_result(nodeid, 'bgtrbrt'))
        if self.terminal_reporter.showlongtestinfo:
            line = self.terminal_reporter._locationline(nodeid, *location) # [:self.terminal_reporter._locationline.find('[')]
            # print(f'----------74-----------{line}\t{location}')
            fsid = nodeid.split("[")[0]
            self.terminal_reporter.write_ensure_prefix(fsid, "")
        if self.terminal_reporter.verbosity == 0:
            yield
        else:
            self.terminal_reporter.write('\n')
            yield


def pytest_collection_modifyitems(session, config, items: list):
    skip_parameter = config.getoption('--skip')
    items_temp = []
    if not (skip_parameter is None):
        for item in items:
            if skip_parameter in item.keywords:
                item.add_marker(pytest.mark.skip)
    for item in items:
        item.name = item.originalname or item.name
        items_temp.append(item)

        # print(item.name)
    items[:] = items_temp
    # print(items)


"""
def pytest_itemcollected(item):
    # print(item)
    # item.name = item.name[:item.name.find('[')]
    i =  random.randint(1, 1000)
    item._node_id = item._nodeid[:item._nodeid.find('[')] + str(i)

"""
"""
def pytest_report_collectionfinish(config, start_path, startdir, items):
    for item in items:
        item.name = item.name[:item.name.find('[')]
        print(f'item.name: {item._nodeid}')
        # item.name = item.name.encode('utf-8').decode('unicode-escape')
        # item._nodeid = item.nodeid.encode('utf-8').decode('unicode-escape')
        # print(item.reportinfo())
    print(items)
"""


@pytest.hookimpl(tryfirst=True)
def pytest_exception_interact(node, call, report):
    if 'search_fixture' in node.__dict__['fixturenames']:
        search_fixture = node.__getattribute__('funcargs')['search_fixture']
        msg = get_message(call, node.name, search_fixture)
        logging.exception(
            msg
        )
        return
    if 'reverse_fixture' in node.__dict__['fixturenames']:
        reverse_fixture = node.__getattribute__('funcargs')['reverse_fixture']
        msg = get_message(call, node.name, reverse_fixture)
        logging.exception(
            msg
        )
        return
    msg = get_message(call, node.name)
    logging.exception(msg)

def get_message(call_info, name, fixture=None):
    seporator = 5*'------------------'
    if fixture is not None:
        return (f'Name test: {name}\n'
                f'Request: {fixture.response.url}\n'
                f'Response: {fixture.response.json()}\n{call_info.excinfo}'
                f'\nDuration: {call_info.duration}\n{seporator}\n')
    return (f'Name test: {name}\n'
            f'{call_info.excinfo}'
            f'\nDuration: {call_info.duration}\n{seporator}\n')


"""
https://www.lambdatest.com/automation-testing-advisor/python/pytest-pytest_exception_interact
"""


def pytest_addoption(parser):
    parser.addoption("--zoom", action="store", default="data_zoom.json")
    parser.addoption("--places", action="store", default="places.json")
    parser.addoption("--skip", action="store", default=None)


