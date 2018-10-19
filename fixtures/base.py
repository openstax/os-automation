"""Pytest fixture primary control."""

import pytest

__all__ = ['selenium', 'chrome_options', 'firefox_options']


# https://docs.pytest.org/en/latest/example/simple.html
# #making-test-result-information-available-in-fixtures
@pytest.fixture
def selenium(request, selenium, pytestconfig):
    """Set default information for webdriver instances."""
    selenium.implicitly_wait(0)
    selenium.set_window_size(width=1024, height=768)
    yield selenium
    # request.node is an "item" because we use the default "function" scope
    if (pytestconfig.getoption('--print-page-source-on-failure') and
       request.node.rep_setup.passed and
       request.node.rep_call.failed):
        # print page source on failure
        print('\n------------------------------- Begin Page Source'
              '-------------------------------')
        print(selenium.page_source)
        print('------------------------------- End Page Source'
              '-------------------------------')


@pytest.fixture
def chrome_options(chrome_options, pytestconfig):
    """Set Chrome options."""
    if pytestconfig.getoption('--headless'):
        chrome_options.headless = True
    chrome70 = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/70.0.3538.67 Safari/537.36')
    chrome_options.add_argument('--user-agent={agent}'
                                .format(agent=chrome70))

    # Required to run in Travis containers
    if pytestconfig.getoption('--no-sandbox'):
        chrome_options.add_argument('--no-sandbox')

    # This ensures the tests will still pass for someone who selected
    # a language other than English as their preferred language in Chrome
    chrome_options.add_argument('--lang=en')

    # Disable Chrome notifications
    chrome_options.add_experimental_option(
        'prefs', {
            'profile.default_content_setting_values.notifications': 2, })
    chrome_options.add_argument('--auto-open-devtools-for-tabs')

    return chrome_options


@pytest.fixture
def firefox_options(firefox_options, pytestconfig):
    """Set Firefox options."""
    if pytestconfig.getoption('--headless'):
        firefox_options.headless = True
    firefox62 = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:62.0) '
                 'Gecko/20100101 Firefox/62.0')
    firefox_options.add_argument('--user-agent={agent}'
                                 .format(agent=firefox62))

    return firefox_options
