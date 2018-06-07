# ospages

Automated test framework for the OpenStax Tutor and Web projects

## Getting started

### Clone the repository

If you have cloned this project already then you can skip this, otherwise you'll need to clone this repo using Git. _If you do not know how to clone a GitHub repository, check out this [help page][git-clone] from GitHub._

### Create and activate a virtual environment

    venv: https://docs.python.org/3/library/venv.html
    virtualenvwrapper: https://gist.github.com/apavamontri/4516816

### Run the tests

Tests are run using the command line using the `tox` command. By default this will run all of the environments configured, including checking your tests against recommended style conventions using [flake8][flake8].

To run against a different instance set, pass in a value for a specific system`--<systen>_base_url`:

```bash
$ tox -- --driver chrome --accounts_base_url=https://accounts.openstax.org
```

or instance set:

```bash
$ tox -- --driver chrome --instance=qa
```

To run Chrome in headless mode, pass in `--headless` or set the HEADLESS environment variable:

```bash
$ tox -- --driver chrome --headless
```

To run against a different browser, pass in a value for `--driver`:

```bash
$ tox -- --driver firefox
```

_Accepted standalone values: `chrome`, `firefox`, `safari`, `edge`, `ie`_

_Values requiring capabilities: `saucelabs`, `browserstack`_

SauceLabs: _http://pytest-selenium.readthedocs.io/en/latest/user_guide.html#sauce-labs_

BrowserStack: _http://pytest-selenium.readthedocs.io/en/latest/user_guide.html#browserstack_

To run a specific test, pass in a value for `-k`:

```bash
$ tox -- --driver chrome -k test_my_feature
```

### Additional Options

The pytest plugin that we use for running tests has a number of advanced command line options available. To see the options available, run `pytest --help`. The full documentation for the plugin can be found [here][pytest-selenium].

## Framework Design

This testing framework heavily relies on the [PyPOM][pypom]. The [PyPOM][pypom]
library is the Python implementation of the [PageObject][pageobject] design pattern.

The [PageObject][pageobject] pattern creates a nice API abstraction around
an HTML page allowing the test creator to focus on the intent of a test
rather than decyphering HTML code. This design pattern makes the test framework
much more maintainable as any code changes to the page can occur in the
[PageObject][pageobject] rather than within the test code.

According to Siman Stewart,

> If you have WebDriver APIs in your test methods, You're Doing It Wrong.

The usage of [pytest][pytest], [pytest-selenium][pytest-selenium] plugin,
and the [PageObject][pageobject] pattern allows for a succinct test structure
like so:

```python
from tests.markers import accounts, nondestructive, test_case

from pages.accounts.home import AccountsHome as Home

@test_case('C000000')
@nondestructive
@accounts
def test_open_home_page(accounts_base_url, selenium):
    """Basic start test."""
    # GIVEN the main Accounts URL and the Selenium driver
    page = Home(selenium, accounts_base_url).open()

    # WHEN The main website URL is fully loaded
    assert(page.header.is_header_displayed), 'Accounts header is not shown'
    assert(page.footer.is_footer_displayed), 'Accounts footer is not shown'
    page.header.go_to_accounts_home()

    # THEN The login page is displayed
    assert(page.current_url == accounts_base_url + '/login')
```

`@test_case('C000000')` is the TestRail case ID number

The inspiration for this framework is based on the [Mozilla Addons Server Project][mozilla]
and plenty of examples can be gleamed from their fantastic usage of the
pattern.

[cnx-org]: https://cnx.org
[git-clone]: https://help.github.com/articles/cloning-a-repository/
[python]: https://www.python.org/downloads/
[flake8]: http://flake8.readthedocs.io/
[pytest-selenium]: http://pytest-selenium.readthedocs.org/
[pypom]: https://pypom.readthedocs.io/en/latest/user_guide.html#regions
[pageobject]: https://martinfowler.com/bliki/PageObject.html
[pytest]: https://docs.pytest.org/en/latest/
[mozilla]: https://github.com/mozilla/addons-server
