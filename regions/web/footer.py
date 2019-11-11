"""OpenStax Web's shared footer region."""

from __future__ import annotations

from typing import List

from pypom import Page, Region
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from utils.utilities import Utility, go_to_, go_to_external_
from utils.web import Web, WebException


class FooterPopUp(Region):
    """Shared dialog box features."""

    @property
    def root(self) -> WebElement:
        """Return the dialog box root element.

        :return: the dialog box root element
        :rtype: :py:class:`~selenium.webdriver.remote.webelement.WebElement`

        """
        return self.driver.execute_script(
            f'return document.querySelector("{self._root_selector}");')

    def is_displayed(self) -> bool:
        """Return True if the pop up box is displayed.

        :return: ``True`` if the pop up box exists, has content and is not
            hidden
        :rtype: bool

        """
        exists = bool(self.root)
        if not exists:
            return False
        has_content = Utility.has_children(self.root)
        is_not_hidden = self.driver.execute_script(
            'return arguments[0].hidden != true'
            ' && arguments[0].style.display != "none";',
            self.root)
        return has_content and is_not_hidden


class Dialog(FooterPopUp):
    """A footer-based dialog box."""

    _title_locator = (By.CSS_SELECTOR, '#dialog-title')

    _root_selector = '#dialog'

    @property
    def title(self) -> str:
        """Return the dialog box title.

        :return: the dialog box title
        :rtype: str

        """
        return self.find_element(*self._title_locator).text

    def view_privacy_policy(self) -> Page:
        """Click the privacy policy link.

        :return: the privacy policy page
        :rtype: :py:class:`~pages.web.legal.PrivacyPolicy`

        """
        link = self.find_element(*self._privacy_policy_locator)
        Utility.click_option(self.driver, element=link)
        from pages.web.legal import PrivacyPolicy
        return go_to_(
            PrivacyPolicy(driver=self.driver, base_url=self.page.base_url))

    def got_it(self) -> Page:
        """Click the 'Got it!' button to accept and close the dialog box.

        :return: the parent page
        :rtype: :py:class:`~pypom.Page`

        """
        button = self.find_element(*self._got_it_button_locator)
        Utility.click_option(self.driver, element=button)
        return self.page


class Footer(Region):
    """OpenStax Web footer region."""

    _root_locator = (By.CSS_SELECTOR, '#footer')
    _directory_locator = (By.CSS_SELECTOR, '.top .boxed')
    _supplemental_locator = (By.CSS_SELECTOR, '.bottom .boxed')

    @property
    def loaded(self) -> bool:
        """Return True if the footer is currently displayed.

        :return: ``True`` if the Web footer is displayed, else ``False``
        :rtype: bool

        """
        return self.root.is_displayed()

    def is_displayed(self) -> bool:
        """Return True if the region is displayed.

        :return: ``True`` if the Web footer is loaded, else ``False`
        :rtype: bool

        """
        return self.loaded

    @property
    def directory(self) -> Footer.Directory:
        """Access the directory.

        :return: the upper footer box directory
        :rtype: :py:class:`~regions.web.footer.Footer.Directory`

        """
        region_root = self.find_element(*self._directory_locator)
        return self.Directory(self, region_root)

    @property
    def supplemental(self) -> Footer.Supplemental:
        """Access the supplemental information and social services.

        :return: the lower footer box information
        :rtype: :py:class:`~regions.web.footer.Footer.Supplemental`

        """
        region_root = self.find_element(*self._supplemental_locator)
        return self.Supplemental(self, region_root)

    def show(self) -> Page:
        """Scroll the section into view.

        :return: the parent Web page
        :rtype: :py:class:`~pages.web.base.WebBase`

        """
        Utility.scroll_to(self.driver, element=self.root)
        return self.page

    class Directory(Region):
        """The site map directory links."""

        _accessibility_statement_locator = (
            By.CSS_SELECTOR, '[href*=accessibility]')
        _careers_locator = (
            By.CSS_SELECTOR, '[href$=careers]')
        _contact_us_locator = (
            By.CSS_SELECTOR, '[href$=contact]')
        _faq_locator = (
            By.CSS_SELECTOR, '[href$=faq]')
        _give_locator = (
            By.CSS_SELECTOR, '[href$=give]')
        _heading_locator = (
            By.CSS_SELECTOR, 'h2')
        _license_locator = (
            By.CSS_SELECTOR, '[href$=license]')
        _mission_statement_locator = (
            By.CSS_SELECTOR, '.mission')
        _newsletter_locator = (
            By.CSS_SELECTOR, '[href*="www2.openstax.org"]')
        _press_locator = (
            By.CSS_SELECTOR, '[href$=press]')
        _privacy_policy_locator = (
            By.CSS_SELECTOR, '[href$=privacy-policy]')
        _support_center_locator = (
            By.CSS_SELECTOR, '[href$=help]')
        _terms_of_use_locator = (
            By.CSS_SELECTOR, '[href$=tos]')

        @property
        def non_profit(self) -> str:
            """Return the non-profit text.

            :return: the Rice University non-profit statement
            :rtype: str

            """
            return self.find_element(*self._heading_locator).text

        @property
        def our_mission(self) -> str:
            """Return the OpenStax mission statement.

            :return: the OpenStax mission statement.
            :rtype: str

            """
            return self.find_element(*self._mission_statement_locator).text

        def donate(self) -> Page:
            """Click on the 'donating' link.

            :return: the donation page
            :rtype: :py:class:`~pages.web.donation.Give`

            """
            link = self.find_element(*self._donate_locator)
            Utility.switch_to(self.driver, element=link)
            from pages.web.donation import Give
            return go_to_(Give(self.driver, base_url=self.page.page.base_url))

        # ------------------------------------------------ #
        # Help
        # ------------------------------------------------ #

        def contact_us(self) -> Page:
            """Go to the contact form.

            :return: the contact form
            :rtype: :py:class:`~pages.web.contact.Contact`

            """
            link = self.find_element(*self._contact_us_locator)
            Utility.safari_exception_click(self.driver, element=link)
            from pages.web.contact import Contact
            return go_to_(
                Contact(self.driver, base_url=self.page.page.base_url))

        def support_center(self) -> Page:
            """Go to the OpenStax Salesforce support site.

            :return: the Salesforce knowledge base in a new tab
            :rtype: :py:class:`~pages.salesforce.home.Salesforce`

            """
            link = self.find_element(*self._support_center_locator)
            Utility.switch_to(self.driver, element=link)
            from pages.salesforce.home import Salesforce
            return go_to_external_(
                Salesforce(self.driver, base_url=Web.SALESFORCE_SUPPORT))

        def faq(self) -> Page:
            """View frequently asked questions.

            :return: the OpenStax FAQ
            :rtype: :py:class:`~pages.web.faq.FAQ`

            """
            link = self.find_element(*self._faq_locator)
            Utility.click_option(self.driver, element=link)
            from pages.web.faq import FAQ
            return go_to_(FAQ(self.driver, base_url=self.page.page.base_url))

        # ------------------------------------------------ #
        # OpenStax information
        # ------------------------------------------------ #

        def press(self) -> Page:
            """View the press page.

            :return: the OpenStax Marketing and Communications press page
            :rtype: :py:class:`~pages.web.press.Press`

            """
            link = self.find_element(*self._press_locator)
            Utility.click_option(self.driver, element=link)
            from pages.web.press import Press
            return go_to_(Press(self.driver, base_url=self.page.page.base_url))

        def newsletter(self) -> Page:
            """Go to the newsletter signup form.

            :return: the newsletter signup form in a new tab
            :rtype: :py:class:`~pages.web.newsletter.NewsletterSignup`

            """
            link = self.find_element(*self._newsletter_locator)
            Utility.switch_to(self.driver, element=link)
            from pages.web.newsletter import NewsletterSignup
            return go_to_external_(
                NewsletterSignup(self.driver, base_url=Web.NEWSLETTER_SIGNUP))

        def careers(self) -> Page:
            """View the careers page.

            :return: the open positions at OpenStax page
            :rtype: :py:class:`~pages.web.careers.Careers`

            """
            link = self.find_element(*self._careers_locator)
            Utility.click_option(self.driver, element=link)
            from pages.web.careers import Careers
            return go_to_(
                Careers(self.driver, base_url=self.page.page.base_url))

        # ------------------------------------------------ #
        # Policies
        # ------------------------------------------------ #

        def accessibility_statement(self) -> Page:
            """View the accessibility statement.

            :return: the accessibility statement page
            :rtype: :py:class:`~pages.web.accessibility.Accessibility`

            """
            link = self.find_element(*self._accessibility_statement_locator)
            Utility.click_option(self.driver, element=link)
            from pages.web.accessibility import Accessibility
            return go_to_(
                Accessibility(self.driver, base_url=self.page.page.base_url))

        def terms_of_use(self) -> Page:
            """View the OpenStax webpage terms of use.

            :return: the terms of use page
            :rtype: :py:class:`~pages.web.legal.Terms`

            """
            link = self.find_element(*self._terms_of_use_locator)
            Utility.click_option(self.driver, element=link)
            from pages.web.legal import Terms
            return go_to_(Terms(self.driver, base_url=self.page.page.base_url))

        def licensing(self) -> Page:
            """Go to the website licensing page.

            :return: the licensing page
            :rtype: :py:class:`~pages.web.legal.License`

            """
            link = self.find_element(*self._license_locator)
            Utility.safari_exception_click(self.driver, element=link)
            from pages.web.legal import License
            return go_to_(
                License(self.driver, base_url=self.page.page.base_url))

        def privacy_policy(self) -> Page:
            """View the OpenStax webpage privacy policy.

            :return: the privacy policy page
            :rtype: :py:class:`~pages.web.legal.PrivacyPolicy`

            """
            link = self.find_element(*self._privacy_policy_locator)
            Utility.click_option(self.driver, element=link)
            from pages.web.legal import PrivacyPolicy
            return go_to_(
                PrivacyPolicy(self.driver, base_url=self.page.page.base_url))

    class Supplemental(Region):
        """Trademarks and OpenStax social program Links."""

        _ap_statement_locator = (
            By.CSS_SELECTOR, '[data-html=apStatement]')
        _copyright_statement_locator = (
            By.CSS_SELECTOR, '[data-html=copyright]')
        _facebook_locator = (
            By.CSS_SELECTOR, '.facebook')
        _instagram_locator = (
            By.CSS_SELECTOR, '.instagram')
        _linkedin_locator = (
            By.CSS_SELECTOR, '.linkedin')
        _twitter_locator = (
            By.CSS_SELECTOR, '.twitter')

        # ------------------------------------------------ #
        # Copyrights and trademarks
        # ------------------------------------------------ #

        @property
        def copyright(self) -> str:
            """Return the OpenStax copyright statement.

            :return: the Rice University copyright statement
            :rtype: str

            """
            return (self.find_element(*self._copyright_statement_locator)
                    .get_attribute('textContent').replace('\n', ' '))

        @property
        def ap_statement(self) -> str:
            """Return the AP statement.

            :return: the AP trademark statement
            :rtype: str

            """
            return (self.find_element(*self._ap_statement_locator)
                    .get_attribute('textContent').replace('\n', ' '))

        # ------------------------------------------------ #
        # Social media
        # ------------------------------------------------ #

        def facebook(self) -> Page:
            """Go to OpenStax's Facebook page.

            :return: the OpenStax Facebook page
            :rtype: :py:class:`~pages.facebook.home.Facebook`

            """
            facebook = self.find_element(*self._facebook_locator)
            url = facebook.get_attribute('href')[:-8]
            script = ('arguments[0].setAttribute("href", "{url}");'
                      .format(url=url))
            self.driver.execute_script(script, facebook)
            Utility.switch_to(
                self.driver, link_locator=self._facebook_locator)
            from pages.facebook.home import Facebook
            return go_to_(Facebook(self.driver))

        def twitter(self) -> Page:
            """Go to OpenStax's Twitter page.

            :return: the OpenStax Twitter page
            :rtype: :py:class:`~pages.twitter.home.Twitter`

            """
            Utility.switch_to(
                self.driver, link_locator=self._twitter_locator)
            from pages.twitter.home import Twitter
            return go_to_(Twitter(self.driver))

        def linkedin(self) -> Page:
            """Go to OpenStax's LinkedIn company page.

            :return: the OpenStax LinkedIn company page
            :rtype: :py:class:`~pages.linkedin.home.LinkedIn`

            """
            Utility.switch_to(
                self.driver, link_locator=self._linkedin_locator)
            from pages.linkedin.home import LinkedIn
            return go_to_(LinkedIn(self.driver))

        def instagram(self) -> Page:
            """Go to OpenStax's Instagram page.

            :return: the OpenStax Instragram page
            :rtype: :py:class:`~pages.instagram.home.Instagram`

            """
            Utility.switch_to(
                self.driver, link_locator=self._instagram_locator)
            from pages.instagram.home import Instagram
            return go_to_(Instagram(self.driver))


class Survey(FooterPopUp):
    """A Pulse Insights survey pop up footer."""

    _answer_option_locator = (
        By.CSS_SELECTOR, '._pi_answers_container a')
    _answer_response_text_box_locator = (
        By.CSS_SELECTOR, '._pi_free_text_question_field')
    _question_text_locator = (
        By.CSS_SELECTOR, '._pi_question')
    _submit_button_locator = (
        By.CSS_SELECTOR, '[type=submit]')
    _x_close_button_locator = (
        By.CSS_SELECTOR, '._pi_closeButton')

    _root_selector = '#_pi_surveyWidgetContainer'

    def close(self) -> Page:
        """Click the 'x' close button.

        :return: the parent page
        :rtype: :py:class:`~pypom.Page`

        """
        button = self.find_element(*self._x_close_button_locator)
        Utility.click_option(self.driver, element=button)
        return self.page

    @property
    def question_stem(self) -> WebElement:
        """Return the question stem element.

        :return: the question stem element
        :rtype: :py:class:`~selenium.webdriver.remote.webelement.WebElement`

        """
        return self.find_element(*self._question_text_locator)

    @property
    def is_free_response(self) -> bool:
        """Return True if the survey answer is a free response.

        :return: ``True`` if the survey question accepts a free response answer
        :rtype: bool

        """
        return 'free_text' in self.question_stem.get_attribute('class')

    @property
    def is_multiple_choice(self) -> bool:
        """Return True if the survey answer is multiple choice.

        :return: ``True`` if the survey question accepts specific answers
        :rtype: bool

        """
        return 'single_choice' in self.question_stem.get_attribute('class')

    @property
    def question(self) -> str:
        """Return the survey question text.

        :return: the survey question
        :rtype: str

        """
        return self.question_stem.text

    @property
    def answer(self) -> WebElement:
        """Return the free response answer box.

        :return: the free response answer box, if found
        :rtype: :py:class:`~selenium.webdriver.remote.webelement.WebElement`
        :raises: :py:class:`~utils.web.WebException` if the survey answer is
            multiple choice

        """
        if self.is_multiple_choice:
            raise WebException(
                'Free response box not available for '
                'multiple choice questions')
        return self.find_element(*self._answer_response_text_box_locator)

    @answer.setter
    def answer(self, answer: str) -> None:
        """Send the answer text.

        :param str answer: the user's answer to the open-ended question
        :return: None

        """
        if self.is_free_response:
            self.answer.send_keys(answer)

    @property
    def answers(self) -> List[Survey.Answer]:
        """Access the survey answer options.

        :return: the list of possible answers
        :rtype: list(:py:class:`~regions.web.footer.Survey.Answer`)
        :raises: :py:class:`~utils.web.WebException` if the survey answer is
            a free response

        """
        if self.is_free_response:
            raise WebException(
                'Multiple choice answers not available for '
                'free response questions')
        return [self.Answer(self, option)
                for option
                in self.find_elements(*self._answer_option_locator)]

    @answers.setter
    def answers(self, answer: str) -> None:
        """Select the answer choice.

        :param str answer: the user's multiple choice answer
        :return: None
        :raises: :py:class:`~utils.web.WebException` if the answer is not
            available for the survey question

        """
        if self.is_multiple_choice:
            for option in self.answers:
                if option.answer.lower() == answer.lower():
                    option.select()
                    return
            raise WebException(f'"{answer}" not available for {self.question}')

    class Answer(Region):
        """A survey question response."""

        _answer_label_locator = (By.CSS_SELECTOR, 'label')

        @property
        def answer(self) -> str:
            """Return the answer option text.

            :return: the survey response text
            :rtype: str

            """
            return self.find_element(*self._answer_label_locator).text

        def select(self) -> None:
            """Select the answer response.

            :return: None

            """
            Utility.click_option(self.driver, element=self.root)
            self.wait.until(lambda _: (not self.page.is_displayed()))
