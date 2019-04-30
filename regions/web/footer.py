"""OpenStax Web's shared footer region."""

from pypom import Region
from selenium.webdriver.common.by import By

from utils.utilities import Utility, go_to_, go_to_external_
from utils.web import Web


class Footer(Region):
    """OpenStax Web footer region."""

    _root_locator = (By.CSS_SELECTOR, '#footer')
    _directory_locator = (By.CSS_SELECTOR, '.top .boxed')
    _supplemental_locator = (By.CSS_SELECTOR, '.bottom .boxed')

    @property
    def loaded(self):
        """Return True if the footer is currently displayed.

        :return: ``True`` if the Web footer is displayed, else ``False``
        :rtype: bool

        """
        return self.root.is_displayed()

    def is_displayed(self):
        """Return True if the region is displayed.

        :return: ``True`` if the Web footer is loaded, else ``False`
        :rtype: bool

        """
        return self.loaded

    @property
    def directory(self):
        """Access the directory.

        :return: the upper footer box directory
        :rtype: :py:class:`~Footer.Directory`

        """
        region_root = self.find_element(*self._directory_locator)
        return self.Directory(self, region_root)

    @property
    def supplemental(self):
        """Access the supplemental information and social services.

        :return: the lower footer box information
        :rtype: :py:class:`~Footer.Supplemental`

        """
        region_root = self.find_element(*self._supplemental_locator)
        return self.Supplemental(self, region_root)

    def show(self):
        """Scroll the section into view.

        :return: the parent Web page
        :rtype: :py:class:`~pages.web.WebBase`

        """
        Utility.scroll_to(self.driver, element=self.root)
        return self.page

    class Directory(Region):
        """The site map directory links."""

        _heading_locator = (By.CSS_SELECTOR, '[role=heading]')
        _mission_statement_locator = (By.CSS_SELECTOR, '.mission')
        _give_locator = (By.CSS_SELECTOR, '[href$=give]')

        _contact_us_locator = (By.CSS_SELECTOR, '[href$=contact]')
        _support_center_locator = (By.CSS_SELECTOR, '[href$=help]')
        _faq_locator = (By.CSS_SELECTOR, '[href$=faq]')

        _press_locator = (By.CSS_SELECTOR, '[href$=press]')
        _newsletter_locator = (By.CSS_SELECTOR, '[href*="www2.openstax.org"]')
        _careers_locator = (By.CSS_SELECTOR, '[href$=careers]')

        _accessibility_statement_locator = (
                                    By.CSS_SELECTOR, '[href*=accessibility]')
        _terms_of_use_locator = (By.CSS_SELECTOR, '[href$=tos]')
        _license_locator = (By.CSS_SELECTOR, '[href$=license]')
        _privacy_policy_locator = (By.CSS_SELECTOR, '[href$=privacy-policy]')

        @property
        def non_profit(self):
            """Return the non-profit text.

            :return: the Rice University non-profit statement
            :rtype: str

            """
            return self.find_element(*self._heading_locator).text

        @property
        def our_mission(self):
            """Return the OpenStax mission statement.

            :return: the OpenStax mission statement.
            :rtype: str

            """
            return self.find_element(*self._mission_statement_locator).text

        def donate(self):
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

        def contact_us(self):
            """Go to the contact form.

            :return: the contact form
            :rtype: :py:class:`~pages.web.contact.Contact`

            """
            link = self.find_element(*self._contact_us_locator)
            Utility.safari_exception_click(self.driver, element=link)
            from pages.web.contact import Contact
            return go_to_(
                Contact(self.driver, base_url=self.page.page.base_url))

        def support_center(self):
            """Go to the OpenStax Salesforce support site.

            :return: the Salesforce knowledge base in a new tab
            :rtype: :py:class:`~pages.salesforce.home.Salesforce`

            """
            link = self.find_element(*self._support_center_locator)
            Utility.switch_to(self.driver, element=link)
            from pages.salesforce.home import Salesforce
            return go_to_external_(
                Salesforce(self.driver, base_url=Web.SALESFORCE_SUPPORT))

        def faq(self):
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

        def press(self):
            """View the press page.

            :return: the OpenStax Marketing and Communications press page
            :rtype: :py:class:`~pages.web.press.Press`

            """
            link = self.find_element(*self._press_locator)
            Utility.click_option(self.driver, element=link)
            from pages.web.press import Press
            return go_to_(Press(self.driver, base_url=self.page.page.base_url))

        def newsletter(self):
            """Go to the newsletter signup form.

            :return: the newsletter signup form in a new tab
            :rtype: :py:class:`~pages.web.newsletter.NewsletterSignup`

            """
            link = self.find_element(*self._newsletter_locator)
            Utility.switch_to(self.driver, element=link)
            from pages.web.newsletter import NewsletterSignup
            return go_to_external_(
                NewsletterSignup(self.driver, base_url=Web.NEWSLETTER_SIGNUP))

        def careers(self):
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

        def accessibility_statement(self):
            """View the accessibility statement.

            :return: the accessibility statement page
            :rtype: :py:class:`~pages.web.accessibility.Accessibility`

            """
            link = self.find_element(*self._accessibility_statement_locator)
            Utility.click_option(self.driver, element=link)
            from pages.web.accessibility import Accessibility
            return go_to_(
                Accessibility(self.driver, base_url=self.page.page.base_url))

        def terms_of_use(self):
            """View the OpenStax webpage terms of use.

            :return: the terms of use page
            :rtype: :py:class:`~pages.web.legal.Terms`

            """
            link = self.find_element(*self._terms_of_use_locator)
            Utility.click_option(self.driver, element=link)
            from pages.web.legal import Terms
            return go_to_(Terms(self.driver, base_url=self.page.page.base_url))

        def licensing(self):
            """Go to the website licensing page.

            :return: the licensing page
            :rtype: :py:class:`~pages.web.legal.License`

            """
            link = self.find_element(*self._license_locator)
            Utility.safari_exception_click(self.driver, element=link)
            from pages.web.legal import License
            return go_to_(
                License(self.driver, base_url=self.page.page.base_url))

        def privacy_policy(self):
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

        _copyright_statement_locator = (
                                 By.CSS_SELECTOR, '[data-html=copyright]')
        _ap_statement_locator = (By.CSS_SELECTOR, '[data-html=apStatement]')
        _facebook_locator = (By.CSS_SELECTOR, '.facebook')
        _twitter_locator = (By.CSS_SELECTOR, '.twitter')
        _linkedin_locator = (By.CSS_SELECTOR, '.linkedin')
        _instagram_locator = (By.CSS_SELECTOR, '.instagram')

        # ------------------------------------------------ #
        # Copyrights and trademarks
        # ------------------------------------------------ #

        @property
        def copyright(self):
            """Return the OpenStax copyright statement.

            :return: the Rice University copyright statement
            :rtype: str

            """
            return self.find_element(*self._copyright_statement_locator).text

        @property
        def ap_statement(self):
            """Return the AP statement.

            :return: the AP trademark statement
            :rtype: str

            """
            return self.find_element(*self._ap_statement_locator).text

        # ------------------------------------------------ #
        # Social media
        # ------------------------------------------------ #

        def facebook(self):
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

        def twitter(self):
            """Go to OpenStax's Twitter page.

            :return: the OpenStax Twitter page
            :rtype: :py:class:`~pages.twitter.home.Twitter`

            """
            Utility.switch_to(
                self.driver, link_locator=self._twitter_locator)
            from pages.twitter.home import Twitter
            return go_to_(Twitter(self.driver))

        def linkedin(self):
            """Go to OpenStax's LinkedIn company page.

            :return: the OpenStax LinkedIn company page
            :rtype: :py:class:`~pages.linkedin.home.LinkedIn`

            """
            Utility.switch_to(
                self.driver, link_locator=self._linkedin_locator)
            from pages.linkedin.home import LinkedIn
            return go_to_(LinkedIn(self.driver))

        def instagram(self):
            """Go to OpenStax's Instagram page.

            :return: the OpenStax Instragram page
            :rtype: :py:class:`~pages.instagram.home.Instagram`

            """
            Utility.switch_to(
                self.driver, link_locator=self._instagram_locator)
            from pages.instagram.home import Instagram
            return go_to_(Instagram(self.driver))
