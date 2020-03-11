"""Accounts copyright and terms of use."""

from __future__ import annotations

from time import sleep
from typing import List

from pypom import Page, Region
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from pages.accounts.base import AccountsBase
from utils.accounts import AccountsException, Selector
from utils.utilities import Utility, go_to_


class AcceptTerms(AccountsBase):
    """Accept a new Accounts legal contract."""

    URL_TEMPLATE = '/terms/pose?terms%5B%5D={contract}'

    class Content(AccountsBase.Content):
        """The contract acceptance form."""

        _content_message_locator = (
            By.CSS_SELECTOR, '.title ~ p')
        _header_text_locator = (
            By.CSS_SELECTOR, '.title')
        _i_agree_button_locator = (
            By.CSS_SELECTOR, '[type=submit]')
        _i_agree_checkbox_locator = (
            By.CSS_SELECTOR, '#agreement_i_agree')
        _contract_language_locator = (
            By.CSS_SELECTOR, '.well')

        @property
        def message(self) -> str:
            """Return the contract change text.

            :return: the policy change explanation text
            :rtype: str

            """
            return self.find_element(*self._content_message_locator).text

        @property
        def contract(self) -> str:
            """Return the full contract text.

            :return: the complete contract body text
            :rtype: str

            """
            return (self.find_element(*self._contract_language_locator)
                    .get_attribute('textContent'))

        def i_have_read_and_agree_to_the_terms_listed_above(self):
            """Click the 'I have read and agree' checkbox.

            :return: None

            """
            checkbox = self.find_element(*self._i_agree_checkbox_locator)
            Utility.click_option(self.driver, element=checkbox)

        def i_agree(self) -> Page:
            """Click the 'I AGREE' button.

            :return: the user's profile, another policy accept page, or the
                redirect back to the page that preceded the log in
            :rtype: :py:class:`~pypom.Page`

            """
            another_contract = '&terms' in self.driver.current_url
            base_url = self.page.base_url
            button = self.find_element(*self._i_agree_button_locator)
            Utility.click_option(self.driver, element=button)
            if another_contract:
                return go_to_(AcceptTerms(self.driver, base_url=base_url))
            sleep(1.0)
            if 'profile' in self.driver.current_url:
                from pages.accounts.profile import Profile
                return go_to_(Profile(self.driver, base_url=base_url))
            return Page(self.driver)

    class MenuBar(AccountsBase.MenuBar):
        """The contract acceptance page menu bar."""

        _logo_locator = (
            By.CSS_SELECTOR, '#top-nav-logo a')


class Copyright(AccountsBase):
    """The Accounts copyright page."""

    URL_TEMPLATE = '/copyright'

    class Content(AccountsBase.Content):
        """The copyright and licensing overview."""

        _copyright_content_locator = (
            By.CSS_SELECTOR, '.ox-card.copyright p')
        _header_text_locator = (
            By.CSS_SELECTOR, '.title')

        @property
        def content(self) -> List[str]:
            """Return the copyright overview text.

            :return: the copyright overview text paragraphs
            :rtype: list(str)

            """
            return [paragraph.get_attribute('textContent')
                    for paragraph
                    in self.find_elements(*self._copyright_content_locator)]


class Terms(AccountsBase):
    """The Accounts terms of use and privacy policy page."""

    URL_TEMPLATE = '/terms'

    @property
    def modal_is_open(self) -> bool:
        """Return True if the legal contract modal is currently open.

        :return: ``True`` if the ``modal-open`` class is found in the current
            page
        :rtype: bool

        """
        return self.driver.execute_script(
            'return document.querySelector(".modal-open") != null;')

    class Content(AccountsBase.Content):
        """The Terms of Use and Privacy Policy content."""

        _content_overview_locator = (
            By.CSS_SELECTOR, '.ox-card p')
        _view_privacy_policy_link_locator = (
            By.CSS_SELECTOR, '.ox-card a:last-child')
        _view_terms_of_use_link_locator = (
            By.CSS_SELECTOR, '.ox-card a:first-child')

        @property
        def overview(self) -> str:
            """Return the legal overview content.

            :return: the body text content for the terms and policy page
            :rtype: str

            """
            return (self.find_element(*self._content_overview_locator)
                    .get_attribute('textContent'))

        def view_privacy_policy(self) -> Terms.Content.LegalModal:
            """Click the 'Privacy Policy' link.

            :return: the privacy policy modal
            :rtype: :py:class:`~pages.accounts.legal.Terms.Content.LegalModal`
            :raises :py:class:`~utils.accounts.AccountsException`: if the modal
                is not found

            """
            return self._open_modal(self._view_privacy_policy_link_locator)

        def view_terms_of_use(self) -> Terms.Content.LegalModal:
            """Click the 'Terms of Use' link.

            :return: the terms of use modal
            :rtype: :py:class:`~pages.accounts.legal.Terms.Content.LegalModal`
            :raises :py:class:`~utils.accounts.AccountsException`: if the modal
                is not found

            """
            return self._open_modal(self._view_terms_of_use_link_locator)

        def _open_modal(self, link_locator: Selector) \
                -> Terms.Content.LegalModal:
            """Open a legal modal.

            :return: a legal modal based on the ``link_locator``
            :rtype: :py:class:`~pages.accounts.legal.Terms.Content.LegalModal`
            :raises :py:class:`~utils.accounts.AccountsException`: if the modal
                is not found

            """
            link = self.find_element(*link_locator)
            Utility.click_option(self.driver, element=link)
            try:
                self.wait.until(lambda _: self.page.modal_is_open)
            except TimeoutException:
                raise AccountsException('Legal modal not open')
            return self.LegalModal(self)

        class LegalModal(Region):
            """The legal contract modal."""

            _root_locator = (
                By.CSS_SELECTOR, '#terms_dialog')

            _close_button_locator = (
                By.CSS_SELECTOR, '.close')
            _modal_content_locator = (
                By.CSS_SELECTOR, '.modal-body p, .modal-body li')
            _modal_section_locator = (
                By.CSS_SELECTOR, '.sectionHead')
            _modal_title_locator = (
                By.CSS_SELECTOR, '.modal-header h3')

            @property
            def content(self) -> List[str]:
                """Return the legal contract content.

                :return: the content of the legal contract
                :rtype: list(str)

                """
                return [content.get_attribute('textContent')
                        for content
                        in self.find_elements(*self._modal_content_locator)]

            @property
            def sections(self) -> List[str]:
                """Return the list of section titles.

                :return: the list of section names found within the current
                    contract
                :rtype: list(str)

                """
                return [section.text
                        for section
                        in self.find_elements(*self._modal_section_locator)]

            @property
            def title(self) -> str:
                """Return the contract title.

                :return: the contract title
                :rtype: str

                """
                return self.find_element(*self._modal_title_locator).text

            def close(self) -> Terms:
                """Click the 'x' button to close the modal.

                :return: the terms page
                :rtype: :py:class:`~pages.accounts.legal.Terms`
                :raises :py:class:`~utils.accounts.AccountsException`: if the
                    legal modal does not close

                """
                button = self.find_element(*self._close_button_locator)
                Utility.click_option(self.driver, element=button)
                try:
                    self.wait.until(lambda _: not self.page.page.modal_is_open)
                except TimeoutException:
                    raise AccountsException('Legal modal did not close')
                return self.page.page
