"""Check for collection issue prior to testing."""

import os

import pytest
from dotenv import load_dotenv

DOTENV_PATH = os.path.join(
    os.path.realpath(os.path.dirname(__file__)), '../.env')
load_dotenv(dotenv_path=DOTENV_PATH)

# Import fixtures from our package so pytest can detect them
from fixtures.base import chrome_options, selenium  # Flake8: noqa
from fixtures.accounts import accounts_base_url
from fixtures.exercises import exercises_base_url
from fixtures.payments import payments_base_url
from fixtures.snapshot import snapshot
from fixtures.tutor import tutor_base_url
from fixtures.web import web_base_url


def pytest_addoption(parser):
    """Add branching parameters."""
    group = parser.getgroup('selenium', 'selenium')
    group.addoption('--accounts_base_url',
                    action='store',
                    default=os.getenv('ACCOUNTS_BASE_URL', None),
                    help='OpenStax Accounts homepage base URL')
    group.addoption('--exercises_base_url',
                    action='store',
                    default=os.getenv('EXERCISES_BASE_URL', None),
                    help='OpenStax Exercises homepage base URL')
    group.addoption('--headless',
                    action='store_true',
                    default=os.getenv('HEADLESS', False),
                    help='Enable headless mode for Chrome.')
    group.addoption('--instance',
                    action='store',
                    default=os.getenv('INSTANCE', 'qa'),
                    help='Use a specific instance set.')
    group.addoption('--no-sandbox',
                    action='store_true',
                    default=os.getenv('NO_SANDBOX', False),
                    help="disable chrome's sandbox.")
    group.addoption('--payments_base_url',
                    action='store',
                    default=os.getenv('PAYMENTS_BASE_URL', None),
                    help='OpenStax Tutor Payments base URL')
    group.addoption('--print-page-source-on-failure',
                    action='store_true',
                    default=os.getenv('PRINT_PAGE_SOURCE_ON_FAILURE', False),
                    help='Print page source to stdout when a test fails.')
    group.addoption('--skip-social',
                    action='store_true',
                    help='Ignore social login tests.')
    group.addoption('--tutor_base_url',
                    action='store',
                    default=os.getenv('TUTOR_BASE_URL', None),
                    help='OpenStax Tutor homepage base URL')
    group.addoption('--web_base_url',
                    action='store',
                    default=os.getenv('WEB_BASE_URL', None),
                    help='OpenStax Web homepage base URL')


def pytest_collection_modifyitems(config, items):
    """Runtime test options."""
    if config.getoption('--skip-social'):
        skip_social = pytest.mark.skip(reason='Skipping social login tests.')
        for item in items:
            if 'social' in items:
                item.add_marker(skip_social)


def pytest_collectreport(report):
    """Break for errors during test collection."""
    if report.failed:
        raise pytest.UsageError("Errors during collection, aborting")


# https://docs.pytest.org/en/latest/example/simple.html
# #making-test-result-information-available-in-fixtures
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Execute all other hooks to obtain the report object."""
    outcome = yield
    rep = outcome.get_result()

    # Set a report attribute for each phase of a call, which can be "setup",
    # "call", "teardown" can be used by yield fixtures to determine if the
    # test failed (see selenium fixture)
    setattr(item, 'rep_{when}'.format(when=rep.when), rep)
