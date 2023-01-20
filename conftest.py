import pytest
import _pytest
import logging
import inspect
from typing import Sequence
import random
from _pytest import terminal

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
        # print(item.runtest())
    # print(items_temp)



def pytest_runtest_protocol(item, nextitem):
    print(f'after: {item} before{nextitem}\n')

def pytest_runtest_logfinish(nodeid, location):
    print(f'fifnish: {nodeid}')

"""
@pytest.mark.trylast
def pytest_configure(config):
    terminal = config.pluginmanager.getplugin('terminalreporter')
    config.pluginmanager.register(TestDescriptionPlugin(terminal, config), 'testdescription')
    
class TestDescriptionPlugin(terminal.TerminalReporter):
    def __init__(self, terminal, config):
        super().__init__(config)
        # self.terminal_reporter = terminal
        # self.desc = None

    def write_fspath_result(nodeid, res, **markup):
        print(f'nodeid: {nodeid}\n')

    def pytest_terminal_summary(self):
        print(super().currentfspath)

        def pytest_runtest_protocol(self, item):
        self.desc = inspect.getdoc(item.obj)
        tw = item.config.get_terminal_writer()
        tw.line()
        tw.write(" " * 8)
        tw.write(item.nodeid)
        tw.flush()
        print(self.terminal_reporter.writer())

    @pytest.hookimpl(hookwrapper=True, tryfirst=True)
    def pytest_runtest_logstart(self, nodeid, location):
        if self.terminal_reporter.showlongtestinfo:
            # print(f'\n{self.terminal_reporter._tw.fullwidth}\n')
            # self.terminal_reporter._showlongtestinfo = False
            line = self.terminal_reporter._locationline(nodeid, *location)# [:self.terminal_reporter._locationline.find('[')]
            # print(f'---------------{line}')
            new_name = line.split('[')[0]
            # print(f'{new_name}\n\n')
            self.terminal_reporter.rewrite(new_name)# , *new_name)
            # print(new_name)
            # fsid = nodeid.split("[")[0]
            # self.terminal_reporter.write_ensure_prefix(fsid, "")
        if self.terminal_reporter.verbosity == 0:
            yield
        else:
            self.terminal_reporter.write('\n')
            yield    
 
        def pytest_runtest_logstart(self, nodeid, location):
        # ensure that the path is printed before the
        # 1st test of a module starts running
        # print(f'----------61\n')
        if self.terminal_reporter.showlongtestinfo:
            line = self.terminal_reporter._locationline(nodeid, *location)
            fsid = nodeid.split("::")[0]
            self.terminal_reporter.write_fspath_result(fsid, "")
            # print(f'65\n')
        elif self.terminal_reporter.showfspath:
            fsid = nodeid.split("::")[0]
            self.terminal_reporter.write_fspath_result(fsid, "")
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

https://happytest-apidoc.readthedocs.io/en/latest/api/_pytest.terminal/# terminal
"""


def pytest_addoption(parser):
    parser.addoption("--zoom", action="store", default="data_zoom.json")
    parser.addoption("--places", action="store", default="places.json")
    parser.addoption("--skip", action="store", default=None)


pytest_plugins = [
    'fixtures.read_data_fixture',
    'fixtures.request_fixture',
]
