"""Pytest fixture primary control."""

import pytest
from bs4 import BeautifulSoup

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
    if request.node.rep_setup.passed and request.node.rep_call.failed:
        # print the current driver URL for failures to assist debugging
        print(f'URL at failure: {selenium.current_url}')

        if pytestconfig.getoption('--print-page-source-on-failure'):
            # print page source on failure
            print('\n------------------------------- '
                  'Begin Page Source '
                  '-------------------------------'
                  '** Note: <path>, <script>, & <style> tags stripped **\n\n')
            # the page source may be a mess so use a parser to clean it up
            soup = BeautifulSoup(selenium.page_source, 'html5lib')
            [s.extract() for s in soup(['path', 'script', 'style'])]
            print(soup.body.prettify())
            print('------------------------------- '
                  'End Page Source '
                  '-------------------------------\n')


@pytest.fixture
def chrome_options(chrome_options, pytestconfig):
    """Set Chrome options."""
    if pytestconfig.getoption('--headless'):
        chrome_options.headless = True
    chrome75 = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/75.0.3770.100 Safari/537.36')
    chrome_options.add_argument(f'--user-agent="{chrome75}"')

    # Required to run in Travis containers
    if (pytestconfig.getoption('--no-sandbox') or
            pytestconfig.getini('no_sandbox')):
        chrome_options.add_argument('--no-sandbox')

    # This ensures the tests will still pass for someone who selected
    # a language other than English as their preferred language in Chrome
    chrome_options.add_argument('--lang=en')

    # Disable Chrome notifications
    chrome_options.add_experimental_option(
        'prefs', {
            'profile.default_content_setting_values.notifications': 2, })

    # Open developer tools for each tab
    # chrome_options.add_argument('--auto-open-devtools-for-tabs')

    return chrome_options


@pytest.fixture
def firefox_options(firefox_options, pytestconfig):
    """Set Firefox options."""
    if pytestconfig.getoption('--headless'):
        firefox_options.headless = True
    firefox68 = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:68.0) '
                 'Gecko/20100101 Firefox/68.0')
    firefox_options.add_argument(f'--user-agent="{firefox68}"')

    return firefox_options
