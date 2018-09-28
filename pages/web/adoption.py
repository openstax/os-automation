"""The book adoption form."""

from time import sleep

from pypom import Region
from selenium.webdriver.common.by import By

from pages.web.base import WebBase
from utils.utilities import go_to_


class Adoption(WebBase):
    """The adoption form page."""

    URL_TEMPLATE = '/adoption'

    _loaded_locator = (By.CLASS_NAME, 'page-loaded')
    _drop_down_menu_locator = (By.CLASS_NAME, 'proxy-select')
    _interest_form_link_locator = (By.CSS_SELECTOR, '[href$=interest]')
    _form_root_locator = (By.CLASS_NAME, 'role-selector')

    @property
    def loaded(self):
        """Wait until the form is displayed."""
        return (
            self.find_element(*self._loaded_locator).is_displayed() and
            self.find_element(*self._drop_down_menu_locator).is_displayed()
        )

    def is_displayed(self):
        """Return True if the adoption form is displayed."""
        return self.find_element(*self._drop_down_menu_locator).is_displayed()

    def go_to_interest(self):
        """Switch to the interest form."""
        self.wait.until(
            lambda _: self.find_element(*self._interest_form_link_locator)
        ).click()
        sleep(1.0)
        from pages.web.interest import Interest
        return go_to_(Interest(self.driver))

    @property
    def form(self):
        """Access the adoption form."""
        form_root = self.find_element(*self._form_root_locator)
        return self.Form(self, form_root)

    class Form(Region):
        """The adoption form."""

        _user_select_locator = (By.CLASS_NAME, 'proxy-select')
        _user_select_option_locator = (By.CSS_SELECTOR, '.options .option')
        _student_message_locator = (By.CSS_SELECTOR,
                                    '.student-form .text-content')
        _go_back_button_locator = (By.CSS_SELECTOR, '.student-form button')

        @property
        def loaded(self):
            """Return True when the form is visible."""
            return self.root.is_displayed()

        @property
        def options(self):
            """Return the option menu responses."""
            return self.find_elements(*self._user_select_option_locator)

        def select(self, user_type):
            """Select a user type from the user drop down menu."""
            self.find_element(*self._user_select_locator).click()
            sleep(0.25)
            [option for option in self.options
             if option.get_attribute('data-value') == user_type][0].click()
            return self

        @property
        def student_message(self):
            """Return the message content for student users.

            Drop the text from the child element first.
            """
            message = self.find_element(*self._student_message_locator).text
            message = message.split('\n')[0]
            return message

        def go_back(self):
            """Click the student GO BACK button."""
            self.find_element(*self._go_back_button_locator).click()
            sleep(1.0)
            return go_to_(WebBase(self.driver))


class AdoptionConfirmation(WebBase):
    """The adoption confirmation page."""

    URL_TEMPLATE = '/adoption-confirmation'

    _confirmation_locator = (By.CLASS_NAME, 'adoption-confirmation')

    @property
    def loaded(self):
        """Wait until the confirmation is displayed."""
        return self.find_element(*self._confirmation_locator).is_displayed()
