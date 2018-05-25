"""Helper functions for OpenStax Pages."""
from random import randint
from time import sleep

from faker import Faker
from selenium.webdriver.support.ui import Select


class Utility(object):
    """Helper functions for various Pages functions."""

    HEX_DIGITS = '0123456789ABCDEF'

    @classmethod
    def select(cls, driver, element_locator, label):
        """Select an Option from a menu."""
        return Utility.fast_multiselect(driver, element_locator, [label])

    @classmethod
    def fast_multiselect(cls, driver, element_locator, labels):
        """Select menu multiselect options.

        Daniel Abel multiselect
        'https://sqa.stackexchange.com/questions/1355/
        what-is-the-correct-way-to-select-an-option-using-seleniums-
        python-webdriver#answer-2258'
        """
        select = Select(driver.find_element(*element_locator))
        for label in labels:
            select.select_by_visible_text(label)
        return select

    @classmethod
    def selected_option(cls, driver, element_locator):
        """Return the currently selected option."""
        return Select(driver.find_element(*element_locator)) \
            .first_selected_option \
            .text

    @classmethod
    def random_hex(cls, length=20):
        """Return a random hex number of size length."""
        return ''.join([Utility.HEX_DIGITS[randint(0, 0xF)]
                       for _ in range(length)])

    @classmethod
    def random(cls, start=0, end=100000):
        """Return a random integer from start to end."""
        return randint(start, end)

    @classmethod
    def random_name(cls, is_male=None, is_female=None):
        """Generate a random name list for Accounts users."""
        fake = Faker()
        name = ['', '', '', '']
        if is_female:
            use_male_functions = False
        elif is_male:
            use_male_functions = True
        else:
            use_male_functions = randint(0, 2) == 0
        has_prefix = randint(0, 10) >= 6
        has_suffix = randint(0, 10) >= 8

        if has_prefix:
            name[0] = fake.prefix_male() if use_male_functions else \
                fake.prefix_female()
        name[1] = fake.first_name_male() if use_male_functions else \
            fake.first_name_female()
        name[2] = fake.last_name()
        if has_suffix:
            name[3] = fake.suffix_male() if use_male_functions else \
                fake.suffix_female()
        return name

    @classmethod
    def new_tab(cls, driver):
        """Open another browser tab."""
        driver.execute_script('window.open();')
        sleep(1)
        return driver.window_handles
