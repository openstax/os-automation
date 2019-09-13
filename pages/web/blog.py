"""The OpenStax blog."""

from datetime import datetime
from time import sleep

from pypom import Region
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect

from pages.web.base import WebBase
from utils.utilities import Utility, go_to_


class Blog(WebBase):
    """The OpenStax web log."""

    URL_TEMPLATE = '/blog'

    _article_locator = (By.CSS_SELECTOR, '.card')
    _initial_image_locators = (By.CSS_SELECTOR, '.link-image')
    _pinned_article_locator = (By.CSS_SELECTOR, '.pinned-article')
    _newsletter_locator = (By.CSS_SELECTOR, '.cta')
    _rss_locator = (By.CSS_SELECTOR, '.rss-link')
    _other_posts_locator = (By.CSS_SELECTOR, '.card')

    @property
    def loaded(self):
        """Return True when all of the blog article images are loaded."""
        timer = 0
        repeat = 15.0
        pause = 0.25
        articles = self.find_elements(*self._article_locator)
        while not articles and timer < (repeat / pause):
            sleep(pause)
            timer = timer + 1
            articles = self.find_elements(*self._article_locator)
        if not articles:
            return False
        for article in articles:
            Utility.scroll_to(self.driver, element=article)
            sleep(0.25)
        Utility.scroll_top(self.driver)
        test = Utility.load_background_images(
            driver=self.driver,
            locator=self._initial_image_locators)
        sleep(3.0)
        return test

    def is_displayed(self):
        """Return True if the blog pinned article is displayed."""
        return self.find_element(*self._pinned_article_locator).is_displayed()

    @property
    def pinned(self):
        """Access the pinned entry."""
        pinned_root = self.find_element(*self._pinned_article_locator)
        return self.Tile(self, pinned_root)

    def get_newsletter(self):
        """Select the 'Sign Up' button."""
        Utility.switch_to(self.driver, self._newsletter_locator)
        from pages.web.newsletter import NewsletterSignup
        return go_to_(NewsletterSignup(self.driver, self.base_url))

    def get_rss(self):
        """Click the RSS feed icon."""
        Utility.switch_to(self.driver, self._rss_locator)
        if self.driver.capabilities.get('browserName').lower() != 'safari':
            self.wait.until(lambda _: 'about:blank' not in self.location)
        return self.driver

    def test_rss_feed(self):
        """Query the RSS feed URL."""
        from requests import head
        return head(self.find_element(*self._rss_locator)
                    .get_attribute('href'))

    def view_post(self, title=None, index=None):
        """Open a blog entry to view the full article."""
        if title:
            for article in self.articles:
                if article.title == title:
                    return article.view()
        if index:
            return self.other_posts[index].view()
        return self.articles[Utility.random(0, len(self.articles) - 1)].view()

    @property
    def articles(self):
        """Return a list of articles."""
        try:
            self.find_element(*self._pinned_article_locator)
            return [self.pinned] + self.other_posts
        except WebDriverException:
            return self.other_posts

    @property
    def other_posts(self):
        """Return the other blog entry tiles."""
        return [self.Tile(self, tile)
                for tile in self.find_elements(*self._other_posts_locator)]

    class Tile(Region):
        """A blog entry overview tile."""

        _image_locator = (By.CSS_SELECTOR, 'a.link-image')
        _title_locator = (By.CSS_SELECTOR, 'h2 a')
        _subheading_locator = (By.CSS_SELECTOR, 'h3')
        _excerpt_locator = (By.CSS_SELECTOR, '.article-blurb')
        _read_more_locator = (By.CSS_SELECTOR, '.go-to')
        _author_locator = (By.CSS_SELECTOR, '.author')
        _date_locator = (By.CSS_SELECTOR, '.date')

        def is_displayed(self):
            """Return True if the tile has children."""
            return (self.root.is_displayed() and
                    Utility.has_children(self.root))

        @property
        def image(self):
            """Return the tile picture element."""
            return self.find_element(*self._image_locator)

        @property
        def title(self):
            """Return the article title."""
            return (self.find_element(*self._title_locator)
                    .get_attribute('textContent'))

        @property
        def excerpt(self):
            """Return the article excerpt or subheading."""
            subheading = self.find_elements(*self._subheading_locator)
            content = subheading[0].get_attribute('textContent').strip() \
                if subheading else ''
            excerpt = (self.find_element(*self._excerpt_locator)
                       .get_attribute('textContent'))
            return f"{content} {excerpt}".strip()

        def view(self):
            """Open the article."""
            link = self.find_element(*self._read_more_locator)
            article = link.get_attribute('href').split('/')[-1]
            Utility.click_option(self.driver, element=link)
            return go_to_(
                Article(self.driver, self.page.base_url, article=article))

        @property
        def authors(self):
            """Return the article authors and editors."""
            return self.find_element(*self._author_locator).text

        @property
        def date(self):
            """Return the article publish date string."""
            return self.find_element(*self._date_locator).text

        def get_date(self):
            """Return a timezone-aware datetime of the publish date."""
            return datetime.strptime(self.date + ' +0000', '%b %d, %Y %z')


class Article(Blog):
    """The OpenStax web log article."""

    URL_TEMPLATE = '/blog/{article}'

    _hero_banner_locator = (By.CSS_SELECTOR, '.hero')
    _article_title_locator = (By.CSS_SELECTOR, '.article h1')
    _disqus_locator = (By.CSS_SELECTOR, '#disqus_thread')

    def wait_for_page_to_load(self):
        """Override the page load function."""
        super(Blog, self).wait_for_page_to_load()
        self.wait.until(
            lambda _: (self.find_element(*self._hero_banner_locator)
                       .is_displayed()))

    def is_displayed(self):
        """Return True if the blog article banner image is displayed."""
        return (
            self.wait.until(expect.visibility_of_element_located(
                self._hero_banner_locator)).is_displayed() and
            self.wait.until(
                expect.presence_of_element_located(self._disqus_locator)
            ).is_displayed())

    @property
    def title(self):
        """Return the article title."""
        return self.find_element(*self._article_title_locator).text.strip()

    @property
    def disqus(self):
        """Return the Disqus iframe."""
        return self.find_element(*self._disqus_locator)

    def view_comments(self):
        """Scroll to the Disqus comment section."""
        self.wait.until(lambda _: self.disqus.is_displayed())
        Utility.scroll_to(self.driver, element_locator=self._disqus_locator)
        return self

    def view_other_posts(self):
        """Scroll to the other blog article tiles."""
        Utility.scroll_to(self.driver,
                          element_locator=self._other_posts_locator)
        return self
