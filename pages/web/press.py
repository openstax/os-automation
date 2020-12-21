"""The press and marketing page."""

from datetime import datetime

from pypom import Region
from requests import get, head
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By

from pages.web.base import WebBase
from utils.utilities import Utility, go_to_
from utils.web import Web


class Release(Region):
    """An OpenStax press release snippet."""

    _byline_locator = (By.CSS_SELECTOR, '.byline')
    _date_locator = (By.CSS_SELECTOR, '.date')
    _headline_locator = (By.CSS_SELECTOR, '.headline a')
    _excerpt_locator = (By.CSS_SELECTOR, '.excerpt')
    _continue_reading_locator = (By.CSS_SELECTOR, _excerpt_locator[1] + ' a')

    @property
    def byline(self):
        """Return the byline text."""
        return self.find_element(*self._byline_locator).text

    @property
    def author(self):
        """Return the name from the byline."""
        return self.byline.split('|')[0].strip()

    @property
    def date(self):
        """Return a timezone-aware date of release."""
        return datetime.strptime(
            self.find_element(*self._date_locator).text + " +0000",
            "%b %d, %Y %z")

    @property
    def headline(self):
        """Return the press release headline."""
        return self.find_element(*self._headline_locator).text.strip()

    @property
    def excerpt(self):
        """Return the excerpt."""
        try:
            return self.find_element(*self._excerpt_locator).text.strip()
        except WebDriverException:
            return ''

    @property
    def continue_reading(self):
        """Return the 'Continue reading' link if the excerpt is visible."""
        link = self.find_elements(*self._continue_reading_locator)
        if not link or not self.excerpt:
            return None
        return link[0]

    def select(self):
        """Select a press release to view the entire text."""
        if self.continue_reading:
            append = self.continue_reading.get_attribute('href').split('/')[-1]
            Utility.click_option(self.driver, element=self.continue_reading)
            return go_to_(PressRelease(driver=self.driver,
                                       base_url=self.page.base_url,
                                       article=append))


class Press(WebBase):
    """The press and marketing page."""

    URL_TEMPLATE = '/press'

    _hero_banner_selector = '.hero h1'
    _press_releases_selector = '.press-releases'
    _sidebar_selector = '.sidebar'
    _news_mentions_selector = '.news-mentions'

    _title_locator = (
        By.CSS_SELECTOR, '.hero h1')
    _see_toggle_locator = (
        By.CSS_SELECTOR, '.more-fewer > [role=button]')
    _image_locator = (
        By.CSS_SELECTOR, 'img')
    _menu_select_locator = (
        By.CSS_SELECTOR, '.selector-button')
    _menu_item_locator = (
        By.CSS_SELECTOR, '.mobile-selector [role=menuitem]')
    _current_menuitem_locator = (
        By.CSS_SELECTOR, '.mobile-selector span')
    _mission_statement_locator = (
        By.CSS_SELECTOR, '.our-mission div')

    _viewing_fewer_locator = (
        By.CSS_SELECTOR, '.fewer:not([hidden])')
    _releases_full_excerpt_locator = (
        By.CSS_SELECTOR, '.press-releases .fewer .press-excerpt')
    _releases_full_locator = (
        By.CSS_SELECTOR, '.hidden-on-mobile:not(.active):not(.news-mentions) .press-excerpt')  # NOQA
    _releases_mobile_locator = (
        By.CSS_SELECTOR, '.press-releases.active .mobile-only .press-excerpt')
    _newer_releases_full_locator = (
        By.CSS_SELECTOR, '.more-fewer .nav-buttons > div:first-child')
    _newer_releases_mobile_locator = (
        By.CSS_SELECTOR, '.mobile-only .nav-buttons > div:first-child')
    _older_releases_full_locator = (
        By.CSS_SELECTOR, '.more-fewer .nav-buttons > div:nth-child(2)')
    _older_releases_mobile_locator = (
        By.CSS_SELECTOR, '.mobile-only .nav-buttons > div:nth-child(2)')

    _mentions_full_locator = (
        By.CSS_SELECTOR, '.news-mentions .press-excerpt')
    _newer_mentions_full_locator = (
        By.CSS_SELECTOR, '.news-mentions .nav-buttons > div:first-child')  # NOQA
    _older_mentions_full_locator = (
        By.CSS_SELECTOR, '.news-mentions .nav-buttons > div:nth-child(2)')  # NOQA
    _mentions_mobile_locator = (
        By.CSS_SELECTOR, '.news-mentions .press-excerpt')
    _newer_mentions_mobile_locator = _newer_mentions_full_locator
    _older_mentions_mobile_locator = _older_mentions_full_locator

    _contact_full_locator = (
        By.CSS_SELECTOR, '.contact')
    _contact_mobile_locator = _contact_full_locator

    _social_full_locator = (
        By.CSS_SELECTOR, '.find-us a')
    _social_mobile_locator = _social_full_locator

    _press_kit_full_locator = (
        By.CSS_SELECTOR, '[href*=press_kit]')
    _press_kit_mobile_locator = _press_kit_full_locator

    _experts_full_locator = (
        By.CSS_SELECTOR, '.booking')
    _experts_mobile_locator = _experts_full_locator

    @property
    def loaded(self):
        """Return True when the four root elements are found."""
        locator = (
            By.CSS_SELECTOR,
            '{banner} , {press} , {sidebar} , {news}'
            .format(banner=self._hero_banner_selector,
                    press=self._press_releases_selector,
                    sidebar=self._sidebar_selector,
                    news=self._news_mentions_selector))
        merged = self.find_elements(*locator)
        sections_found = len(merged) == 4
        images_visible = Utility.is_image_visible(
            self.driver, locator=self._image_locator)
        try:
            contact_found = (
                self.contact.name
                if not isinstance(self.contact, list)
                else self.contact[0].name)
        except Exception:
            contact_found = ''
        return (super().loaded and
                sections_found and
                images_visible and
                (contact_found or self.is_phone))

    def is_displayed(self):
        """Return True if the heading is displayed."""
        return self.find_element(*self._title_locator).is_displayed()

    @property
    def title(self):
        """Return the title."""
        return self.find_element(*self._title_locator).text

    def select(self, option):
        """Select a mobile menu option."""
        if option == self.current_menu_item or not self.is_phone:
            return self
        menu = self.find_element(*self._menu_select_locator)
        Utility.click_option(self.driver, element=menu)
        for section in self.menu_options:
            if section.text == option:
                Utility.click_option(self.driver, element=section)
                return self
        raise(ValueError('"{0}" is not an available section'.format(option)))

    @property
    def menu_options(self):
        """Return the list of selection options."""
        return self.find_elements(*self._menu_item_locator)

    @property
    def current_menu_item(self):
        """Return the currently selected mobile menu option."""
        return self.find_element(*self._current_menuitem_locator).text

    @property
    def releases(self):
        """Access the press releases."""
        if self.is_phone:
            locator = self._releases_mobile_locator
        elif self.viewing_fewer_releases:
            locator = self._releases_full_excerpt_locator
        else:
            locator = self._releases_full_locator
        return [Release(self, release)
                for release in self.find_elements(*locator)]

    @property
    def viewing_fewer_releases(self):
        """Return True if viewing the top two press releases."""
        return (self.find_elements(*self._viewing_fewer_locator) and
                not self.is_phone)

    def see_more_releases(self):
        """Toggle the fewer / more press releases switch."""
        switch = self.find_element(*self._see_toggle_locator)
        Utility.click_option(self.driver, element=switch)
        return self

    def see_fewer_releases(self):
        """Toggle the fewer / more press releases switch."""
        return self.see_more_releases()

    def view_older_releases(self):
        """View older OpenStax press releases."""
        return self._move_pagination(
            self._older_releases_mobile_locator,
            self._older_releases_full_locator)

    def view_newer_releases(self):
        """View newer OpenStax press releases."""
        return self._move_pagination(
            self._newer_releases_mobile_locator,
            self._newer_releases_full_locator)

    @property
    def mentions(self):
        """Access the news articles mentioning OpenStax."""
        if self.is_phone:
            locator = self._mentions_mobile_locator
        else:
            locator = self._mentions_full_locator
        return [self.Mention(self, article)
                for article
                in self.find_elements(*locator)]

    def view_older_mentions(self):
        """View older news articles mentioning OpenStax."""
        return self._move_pagination(
            self._older_mentions_mobile_locator,
            self._older_mentions_full_locator)

    def view_newer_mentions(self):
        """View newer news articles mentioning OpenStax."""
        return self._move_pagination(
            self._newer_mentions_mobile_locator,
            self._newer_mentions_full_locator)

    @property
    def mission_statement(self):
        """Return the OpenStax mission statement."""
        return self.find_element(*self._mission_statement_locator).text

    @property
    def mission_displayed(self):
        """Return True if the mission statements are displayed."""
        return self.driver.execute_script(
            'return document.querySelector("{0}").clientHeight > 0;'
            .format(self._sidebar_selector))

    @property
    def contact(self):
        """Return the press contact information."""
        if self.is_phone:
            locator = self._contact_mobile_locator
        else:
            locator = self._contact_full_locator
        contacts = self.find_elements(*locator)
        assert(contacts), 'No contact person/people found'
        if len(contacts) > 1:
            return [self.Contact(self, person)
                    for person in contacts]
        return self.Contact(self, contacts[0])

    @property
    def social(self):
        """Access the OpenStax social pages."""
        if self.is_phone:
            locator = self._social_mobile_locator
        else:
            locator = self._social_full_locator
        return [self.Social(self, company)
                for company in self.find_elements(*locator)]

    @property
    def press_kit(self):
        """Return the press kit download button."""
        if self.is_phone:
            locator = self._press_kit_mobile_locator
        else:
            locator = self._press_kit_full_locator
        return self.find_element(*locator)

    def check_press_kit(self):
        """Request the HEAD of the press kit download."""
        return head(self.press_kit.get_attribute('href'))

    @property
    def experts(self):
        """Access the OpenStax experts cards."""
        if self.is_phone:
            locator = self._experts_mobile_locator
        else:
            locator = self._experts_full_locator
        return [self.Expert(self, person)
                for person in self.find_elements(*locator)]

    def _move_pagination(self, mobile, full):
        """Pagination helper for press releases and news mentions."""
        if self.is_phone:
            switch = self.find_element(*mobile)
        else:
            switch = self.find_element(*full)
        if 'presentation' not in switch.get_attribute('role'):
            # there is another pagination group of older or newer links
            Utility.click_option(self.driver, element=switch)
        return self

    class Mention(Region):
        """A news article mentioning OpenStax."""

        _logo_locator = (By.CSS_SELECTOR, 'img')
        _source_locator = (By.CSS_SELECTOR, '.source')
        _byline_date_locator = (By.CSS_SELECTOR, '.byline .date')
        _headline_locator = (By.CSS_SELECTOR, '.headline a')

        @property
        def logo(self):
            """Return the logo."""
            return self.find_element(*self._logo_locator)

        @property
        def source(self):
            """Return the source organization name."""
            return self.find_element(*self._source_locator).text.strip()

        @property
        def date(self):
            """Return a timezone-aware date of publication."""
            return datetime.strptime(
                self.find_element(*self._byline_date_locator).text
                .split('-', 1)[-1].strip() + ' +0000',
                '%b %d, %Y %z')

        @property
        def headline_element(self):
            """Return the headline element."""
            return self.find_element(*self._headline_locator)

        @property
        def headline(self):
            """Return the article headline."""
            return self.headline_element.text.strip()

        def select(self):
            """Follow the article link."""
            Utility.switch_to(self.driver, element=self.headline_element)
            return self.driver

        def check_article(self):
            """Check the HEAD request for the article URL."""
            return head(self.url)

        @property
        def url(self):
            """Return the article URL."""
            return self.headline_element.get_attribute('href')

    class Contact(Region):
        """An OpenStax MarComm point of contact."""

        _name_locator = (By.CSS_SELECTOR, 'div:first-child')
        _phone_locator = (By.CSS_SELECTOR, 'div:nth-child(2) a')
        _email_locator = (By.CSS_SELECTOR, 'div:last-child a')

        @property
        def name(self):
            """Return the contact person's name."""
            return self.find_element(*self._name_locator).text.strip()

        @property
        def phone(self):
            """Return the contact telephone number."""
            return self.find_element(*self._phone_locator).text.strip()

        @property
        def email(self):
            """Return the contact email address."""
            return self.find_element(*self._email_locator).text.strip()

    class Social(Region):
        """A social media option."""

        _icon_locator = (By.CSS_SELECTOR, 'svg')

        @property
        def name(self):
            """Return the Social media company name."""
            destination_url = self.url
            for company in Web.MEDIA:
                if company in destination_url:
                    return Web.MEDIA.get(company)

        @property
        def url_name(self):
            """Return the case-lowered company name found in the URL."""
            return self.name.lower()

        @property
        def url(self):
            """Return the link URL."""
            return self.root.get_attribute('href')

        @property
        def select(self):
            """Go to the OpenStax social media page."""
            return Utility.switch_to(self.driver, element=self.root)

        def check_media_link(self):
            """Request the HEAD of the media page."""
            if self.url_name in [Web.INSTAGRAM, Web.TWITTER]:
                return get(self.url)
            return head(self.url)

    class Expert(Region):
        """An OpenStax expert."""

        _card_locator = (By.CSS_SELECTOR, '.card')
        _portrait_locator = (By.CSS_SELECTOR, 'img')
        _name_locator = (By.CSS_SELECTOR, '.name')
        _role_locator = (By.CSS_SELECTOR, _name_locator[1] + ' ~ div')
        _bio_locator = (By.CSS_SELECTOR, '.span-2')

        def is_displayed(self):
            """Return True if the portrait is loaded and in the frame."""
            Utility.scroll_to(self.driver, element=self.portrait, shift=-20)
            card = self.find_element(*self._card_locator)
            return (Utility.is_image_visible(
                        self.driver, image=self.portrait) and
                    Utility.in_viewport(
                        self.driver, element=card, display_marks=True))

        @property
        def portrait(self):
            """Return the expert's picture."""
            return self.find_element(*self._portrait_locator)

        @property
        def has_portrait(self):
            """Return True if the portrait exists."""
            return Utility.is_image_visible(self.driver, image=self.portrait)

        @property
        def name(self):
            """Return the expert's name."""
            return self.find_element(*self._name_locator).text.strip()

        @property
        def role(self):
            """Return the expert's role or job description."""
            return self.find_element(*self._role_locator).text.strip()

        @property
        def bio(self):
            """Return the expert's short biography."""
            return self.find_element(*self._bio_locator).text.strip()


class PressRelease(WebBase):
    """A press release page."""

    URL_TEMPLATE = '/press/{article}'

    _article_locator = (By.CSS_SELECTOR, '.page > .article')
    _headline_locator = (By.CSS_SELECTOR, 'article h1')
    _author_locator = (By.CSS_SELECTOR, '.author')
    _date_locator = (By.CSS_SELECTOR, '.date')
    _content_locator = (By.CSS_SELECTOR, '.body p')
    _see_toggle_locator = (By.CSS_SELECTOR, '.see')
    _viewing_fewer_locator = (By.CSS_SELECTOR, '.fewer:not([hidden])')
    _newer_releases_locator = (By.CSS_SELECTOR, '.nav-buttons div:first-child')
    _older_releases_locator = (By.CSS_SELECTOR, '.nav-buttons div:last-child')
    _releases_excerpt_locator = (
        By.CSS_SELECTOR, '.fewer .press-excerpt')
    _releases_locator = (
        By.CSS_SELECTOR,
        '.more .headline-container:not([hidden]) .press-excerpt')

    @property
    def loaded(self):
        """Return True when the press release text is displayed."""
        return super().loaded and bool(self.content)

    def is_displayed(self):
        """Return True if the press release sections are available."""
        return self.headline and self.author and self.date and self.content

    @property
    def is_an_article(self):
        """Return True if the page is a press release article."""
        return bool(self.find_elements(*self._article_locator))

    @property
    def headline(self):
        """Return the headline text."""
        return self.find_element(*self._headline_locator).text.strip()

    @property
    def author(self):
        """Return the press release author."""
        return self.find_element(*self._author_locator).text.strip()

    @property
    def date(self):
        """Return a timezone-aware date of publication."""
        return datetime.strptime(
            self.find_element(*self._date_locator).text.strip() + ' +0000',
            '%b %d, %Y %z')

    @property
    def content(self):
        """Return the press release content."""
        return [paragraph.text.strip()
                for paragraph in self.find_elements(*self._content_locator)]

    @property
    def other_releases(self):
        """Access the press releases."""
        locator = (self._releases_excerpt_locator
                   if self.viewing_fewer_releases
                   else self._releases_locator)
        return [Release(self, release)
                for release in self.find_elements(*locator)]

    @property
    def viewing_fewer_releases(self):
        """Return True if viewing the top two press releases."""
        return bool(self.find_elements(*self._viewing_fewer_locator))

    def see_more_releases(self):
        """Toggle the fewer / more press releases switch."""
        switch = self.find_element(*self._see_toggle_locator)
        Utility.click_option(self.driver, element=switch)
        return self

    def see_fewer_releases(self):
        """Toggle the fewer / more press releases switch."""
        return self.see_more_releases()

    def view_older_releases(self):
        """View older OpenStax press releases."""
        if not self.viewing_fewer_releases:
            switch = self.find_element(*self._older_releases_locator)
            if 'presentation' not in switch.get_attribute('role'):
                # there is another pagination group of older or newer links
                Utility.click_option(self.driver, element=switch)
        return self

    def view_newer_releases(self):
        """View newer OpenStax press releases."""
        if not self.viewing_fewer_releases:
            switch = self.find_element(*self._newer_releases_locator)
            if 'presentation' not in switch.get_attribute('role'):
                # there is another pagination group of older or newer links
                Utility.click_option(self.driver, element=switch)
        return self
