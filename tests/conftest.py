"""Check for collection issue prior to testing."""

import os

import pytest
from dotenv import load_dotenv

DOTENV_PATH = os.path.join(
    os.path.realpath(os.path.dirname(__file__)), '../.env')
load_dotenv(dotenv_path=DOTENV_PATH)
# Import fixtures from our package so pytest can detect them


pytest_plugins = (
    'fixtures.accounts',
    'fixtures.base',
    'fixtures.exercises',
    'fixtures.payments',
    'fixtures.snapshot',
    'fixtures.tutor',
    'fixtures.users',
    'fixtures.web'
)


def pytest_addoption(parser):
    """Add branching parameters."""
    selenium_options = parser.getgroup('selenium', 'Selenium controls')
    url_options = parser.getgroup('url', 'Base test URLs')
    user_options = parser.getgroup('users', 'User accounts for testing')
    product_options = parser.getgroup('products', 'Products to test')

    # Runtime options
    selenium_options.addoption('--headless',
                               action='store_true',
                               default=os.getenv('HEADLESS', False),
                               help=('Enable headless mode for Chrome '
                                     ' and Firefox.'))
    selenium_options.addoption('--instance',
                               action='store',
                               default=os.getenv('INSTANCE', 'qa'),
                               help='Use a specific instance set.')
    selenium_options.addoption('--no-sandbox',
                               action='store_true',
                               default=os.getenv('NO_SANDBOX', False),
                               help="disable chrome's sandbox.")
    selenium_options.addoption('--print-page-source-on-failure',
                               action='store_true',
                               default=os.getenv(
                                    'PRINT_PAGE_SOURCE_ON_FAILURE', False),
                               help=('Print page source to stdout '
                                     'when a test fails.'))
    selenium_options.addoption('--run-social',
                               action='store_true',
                               default=False,
                               help='Run only social login tests.')
    selenium_options.addoption('--skip-social',
                               action='store_true',
                               default=False,
                               help='Ignore social login tests.')

    # Base URL options
    url_options.addoption('--accounts-base-url',
                          action='store',
                          default=os.getenv('ACCOUNTS_BASE_URL', None),
                          dest='accounts_base_url',
                          help='OpenStax Accounts homepage base URL')
    url_options.addoption('--exercises-base-url',
                          action='store',
                          default=os.getenv('EXERCISES_BASE_URL', None),
                          dest='exercises_base_url',
                          help='OpenStax Exercises homepage base URL')
    url_options.addoption('--payments-base-url',
                          action='store',
                          default=os.getenv('PAYMENTS_BASE_URL', None),
                          dest='payments_base_url',
                          help='OpenStax Tutor Payments base URL')
    url_options.addoption('--tutor-base-url',
                          action='store',
                          default=os.getenv('TUTOR_BASE_URL', None),
                          dest='tutor_base_url',
                          help='OpenStax Tutor homepage base URL')
    url_options.addoption('--web-base-url',
                          action='store',
                          default=os.getenv('WEB_BASE_URL', None),
                          dest='web_base_url',
                          help='OpenStax Web homepage base URL')

    # User options
    user_options.addoption('--student',
                           action='store',
                           nargs=2,
                           default=[os.getenv('STUDENT_USER'),
                                    os.getenv('STUDENT_PASSWORD_DEV'),
                                    os.getenv('STUDENT_PASSWORD_QA'),
                                    os.getenv('STUDENT_PASSWORD_STAGING'),
                                    os.getenv('STUDENT_PASSWORD_PROD')],
                           help='OpenStax test student account')
    user_options.addoption('--teacher',
                           action='store',
                           nargs=2,
                           default=[os.getenv('TEACHER_USER'),
                                    os.getenv('TEACHER_PASSWORD_DEV'),
                                    os.getenv('TEACHER_PASSWORD_QA'),
                                    os.getenv('TEACHER_PASSWORD_STAGING'),
                                    os.getenv('TEACHER_PASSWORD_PROD')],
                           help='OpenStax test instructor account')
    user_options.addoption('--admin',
                           action='store',
                           nargs=2,
                           default=[os.getenv('ADMIN_USER'),
                                    os.getenv('ADMIN_PASSWORD_DEV'),
                                    os.getenv('ADMIN_PASSWORD_QA'),
                                    os.getenv('ADMIN_PASSWORD_STAGING'),
                                    os.getenv('ADMIN_PASSWORD_PROD')],
                           help='OpenStax test administrative account')
    user_options.addoption('--content',
                           action='store',
                           nargs=2,
                           default=[os.getenv('CONTENT_USER'),
                                    os.getenv('CONTENT_PASSWORD_DEV'),
                                    os.getenv('CONTENT_PASSWORD_QA'),
                                    os.getenv('CONTENT_PASSWORD_STAGING'),
                                    os.getenv('CONTENT_PASSWORD_PROD')],
                           help='OpenStax test content manager account')
    user_options.addoption('--salesforce',
                           action='store',
                           nargs=2,
                           default=[os.getenv('SALESFORCE_USERNAME'),
                                    os.getenv('SALESFORCE_PASSWORD')],
                           help='OpenStax test Salesforce manager account')
    user_options.addoption('--facebook',
                           action='store',
                           nargs=2,
                           default=[os.getenv('FACEBOOK_USERNAME'),
                                    os.getenv('FACEBOOK_PASSWORD')],
                           help='OpenStax test Facebook account')
    user_options.addoption('--facebook-signup',
                           action='store',
                           nargs=2,
                           default=[os.getenv('FACEBOOK_SIGNUP'),
                                    os.getenv('FACEBOOK_SIGNUP_PASSWORD')],
                           help='OpenStax test Facebook user signup account')
    user_options.addoption('--google',
                           action='store',
                           nargs=2,
                           default=[os.getenv('GOOGLE_USERNAME'),
                                    os.getenv('GOOGLE_PASSWORD')],
                           help='OpenStax test Google account account')
    user_options.addoption('--google-signup',
                           action='store',
                           nargs=2,
                           default=[os.getenv('GOOGLE_SIGNUP'),
                                    os.getenv('GOOGLE_SIGNUP_PASSWORD')],
                           help='OpenStax test Google user signup account')

    # Product options
    product_options.addoption('--systems',
                              action='store',
                              nargs='+',
                              default=['accounts',
                                       'biglearn',
                                       'exercises',
                                       'hypothesis',
                                       'payments',
                                       'tutor',
                                       'web'],
                              help='Systems under test\n' +
                                   'Options: accounts, biglearn, exercises\n' +
                                   '         hypothesis, payments, tutor, web')


def pytest_collection_modifyitems(config, items):
    """Runtime test options."""
    # Runtime markers
    run_social = config.getoption('--run-social')
    mark_run_social = pytest.mark.skip(reason='Skipping non-social tests.')
    skip_social = config.getoption('--skip-social')
    mark_skip_social = pytest.mark.skip(reason='Skipping social login tests.')

    run_systems = config.getoption('--systems')
    mark_skip_accounts = pytest.mark.skip(reason='Skipping Accounts tests.')
    mark_skip_biglearn = pytest.mark.skip(reason='Skipping BigLearn tests.')
    mark_skip_exercises = pytest.mark.skip(reason='Skipping Exercises tests.')
    mark_skip_hypothesis = pytest.mark.skip(
                                        reason='Skipping Hypothesis tests.')
    mark_skip_payments = pytest.mark.skip(reason='Skipping Payments tests.')
    mark_skip_tutor = pytest.mark.skip(reason='Skipping Tutor tests.')
    mark_skip_web = pytest.mark.skip(reason='Skipping Web tests.')

    # Apply runtime markers
    for item in items:
        if skip_social and 'social' in item.keywords:
            item.add_marker(mark_skip_social)
        if run_social and 'social' not in item.keywords:
            item.add_marker(mark_run_social)
        if run_systems:
            if 'accounts' not in run_systems and 'accounts' in item.keywords:
                item.add_marker(mark_skip_accounts)
            if 'biglearn' not in run_systems and 'biglearn' in item.keywords:
                item.add_marker(mark_skip_biglearn)
            if 'exercises' not in run_systems and 'exercises' in item.keywords:
                item.add_marker(mark_skip_exercises)
            if ('hypothesis' not in run_systems
                    and 'hypothesis' in item.keywords):
                item.add_marker(mark_skip_hypothesis)
            if 'payments' not in run_systems and 'payments' in item.keywords:
                item.add_marker(mark_skip_payments)
            if 'tutor' not in run_systems and 'tutor' in item.keywords:
                item.add_marker(mark_skip_tutor)
            if 'web' not in run_systems and 'web' in item.keywords:
                item.add_marker(mark_skip_web)


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
