"""Test the helper functions for OpenStax Pages."""

import pytest
from pytest_testrail.plugin import pytestrail
from selenium.webdriver.common.by import By

from pages.accounts.home import AccountsHome as Home
from pages.utils.utilities import Utility


@pytestrail.case('C195539')
@pytest.mark.nondestructive
def test_menu_select(base_url, selenium):
    """Basic start test."""
    page = Home(selenium, base_url).open()
    selenium.get('https://accounts-qa.openstax.org/signup')
    assert(page)
    select = Utility.select(selenium, (By.ID, 'signup_role'), 'Student')
    assert(select.first_selected_option.text == 'Student')
    assert(Utility.selected_option(selenium, (By.ID, 'signup_role')) ==
           'Student')


@pytestrail.case('C195540')
@pytest.mark.nondestructive
def test_random(base_url, selenium):
    """Get a random number between 0 and 50, inclusive, 10 times."""
    for _ in range(10):
        value = Utility.random(0, 50)
        assert(value >= 0 and value <= 50)


@pytestrail.case('C195541')
@pytest.mark.nondestructive
def test_random_name(base_url, selenium):
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


@pytestrail.case('C200528')
@pytest.mark.nondestructive
def test_browser_tab_open(base_url, selenium):
    """Test opening a second browser tab."""
    Home(selenium, base_url).open()
    handles = Utility.new_tab(selenium)
    assert(len(handles) > 1), 'Only one window handle available'
