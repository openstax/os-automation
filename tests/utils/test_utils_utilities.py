"""Test the helper functions for OpenStax Pages."""

from selenium.webdriver.common.by import By

from pages.accounts.home import AccountsHome as Home
from pages.utils.utilities import Utility
from tests.markers import accounts, nondestructive, test_case


@test_case('C195539')
@nondestructive
@accounts
def test_menu_select(accounts_base_url, selenium):
    """Basic start test."""
    page = Home(selenium, accounts_base_url).open()
    selenium.get('https://accounts-qa.openstax.org/signup')
    assert(page)
    select = Utility.select(selenium, (By.ID, 'signup_role'), 'Student')
    assert(select.first_selected_option.text == 'Student')
    assert(Utility.selected_option(selenium, (By.ID, 'signup_role')) ==
           'Student')


@test_case('C195540')
@nondestructive
def test_random(selenium):
    """Get a random number between 0 and 50, inclusive, 10 times."""
    for _ in range(10):
        value = Utility.random(0, 50)
        assert(value >= 0 and value <= 50)


@test_case('C195541')
@nondestructive
def test_random_name(selenium):
    """Test the random name generator list."""
    for _ in range(25):
        name = Utility.random_name()
        assert(len(name) == 4), 'Incorrect length'
        assert(len(name[1]) > 0), 'Missing first name'
        assert(len(name[2]) > 0), 'Missing last name'
    name = Utility.random_name(is_male=True)
    assert(len(name) == 4), 'Incorrect length'
    assert(len(name[1]) > 0), 'Missing first name'
    assert(len(name[2]) > 0), 'Missing last name'
    name = Utility.random_name(is_female=True)
    assert(len(name) == 4), 'Incorrect length'
    assert(len(name[1]) > 0), 'Missing first name'
    assert(len(name[2]) > 0), 'Missing last name'


@test_case('C200528')
@nondestructive
@accounts
def test_browser_tab_open(accounts_base_url, selenium):
    """Test opening a second browser tab."""
    Home(selenium, accounts_base_url).open()
    handles = Utility.new_tab(selenium)
    assert(len(handles) > 1), 'Only one window handle available'
