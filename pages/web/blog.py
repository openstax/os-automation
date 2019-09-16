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
        """Return True when all of the blog article images are loaded.

        :return: ``True`` when the blog article background images are loaded
        :rtype: bool

        """
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
        """Return True if the blog pinned article is displayed.

        :return: ``True`` when the pinned blog article entry is displayed
        :rtype: bool

        """
        return self.find_element(*self._pinned_article_locator).is_displayed()

    @property
    def pinned(self):
        """Access the pinned entry.

        :return: the pinned blog entry tile
        :rtype: :py:class:`~pages.web.blog.Blog.Tile`

        """
        pinned_root = self.find_element(*self._pinned_article_locator)
        return self.Tile(self, pinned_root)

    def get_newsletter(self):
        """Select the 'Sign Up' button.

        :return: the OpenStax newsletter signup form in a new window
        :rtype: :py:class:`~pages.web.newsletter.NewsletterSignup`

        """
        Utility.switch_to(self.driver, self._newsletter_locator)
        from pages.web.newsletter import NewsletterSignup
        return go_to_(NewsletterSignup(self.driver, self.base_url))

    def get_rss(self):
        """Click the RSS feed icon.

        :return: None

        """
        Utility.switch_to(self.driver, self._rss_locator)
        if self.driver.capabilities.get('browserName').lower() != 'safari':
            self.wait.until(lambda _: 'about:blank' not in self.location)

    def test_rss_feed(self):
        """Query the RSS feed URL.

        :return: the result from a HEAD request to the RSS feed
        :rtype: :py:class:`~requests.Response`

        """
        from requests import head
        return head(self.find_element(*self._rss_locator)
                    .get_attribute('href'))

    def view_post(self, title=None, index=None):
        """Open a blog entry to view the full article.

        If no title or index is provided, return a random blog article

        :param str title: (optional) select an article to view by its title
        :param int index: (optional) select an article by it list index
        :return: a blog article
        :rtype: :py:class:`~pages.web.blog.Article`

        """
        # select an article by its title
        if title:
            for article in self.articles:
                if article.title == title:
                    return article.view()

        # or select an article by its position with 0 being the newest and n-1
        # being the oldest
        if index:
            return self.other_posts[index].view()

        # or select a random article
        return self.articles[Utility.random(0, len(self.articles) - 1)].view()

    @property
    def articles(self):
        """Return a list of articles.

        Include the pinned article, if it exists.

        :return: a list of available blog entries
        :rtype: list(:py:class:`~pages.web.blog.Article`)

        """
        try:
            self.find_element(*self._pinned_article_locator)
            return [self.pinned] + self.other_posts
        except WebDriverException:
            return self.other_posts

    @property
    def other_posts(self):
        """Return the other blog entry tiles.

        :return: a list of blog entries, excluding the pinned article
        :rtype: list(:py:class:`~pages.web.blog.Article`)

        """
        return [self.Tile(self, tile)
                for tile
                in self.find_elements(*self._other_posts_locator)]

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
            """Return True if the tile has children.

            :return: ``True`` if the tile is displayed and the tile has loaded
                child elements (it entered the viewable window for at least 0.1
                seconds)
            :rtype: bool

            """
            return (self.root.is_displayed() and
                    Utility.has_children(self.root))

        @property
        def image(self):
            r"""Return the tile picture element.

            :return: the tile's banner image element
            :rtype: :py:class:`~selenium.webdriver.remote \
                              .webelement.WebElement`

            """
            return self.find_element(*self._image_locator)

        @property
        def title(self):
            """Return the article title.

            :return: the blog article title
            :rtype: str

            """
            return (self.find_element(*self._title_locator)
                    .get_attribute('textContent'))

        @property
        def excerpt(self):
            """Return the article excerpt or subheading.

            :return: the trimmed article excerpt or the article subheading plus
                the excerpt
            :rtype: str

            """
            subheading = self.find_elements(*self._subheading_locator)
            content = subheading[0].get_attribute('textContent').strip() \
                if subheading else ''
            excerpt = (self.find_element(*self._excerpt_locator)
                       .get_attribute('textContent'))
            return f"{content} {excerpt}".strip()

        def view(self):
            """Open the article.

            :return: the full blog entry article
            :rtype: :py:class:`~pages.web.blog.Article`

            """
            link = self.find_element(*self._read_more_locator)
            article = link.get_attribute('href').split('/')[-1]
            Utility.click_option(self.driver, element=link)
            return go_to_(
                Article(self.driver, self.page.base_url, article=article))

        @property
        def authors(self):
            """Return the article authors and editors.

            :return: the article author(s)/editor(s) as a single string
            :rtype: str

            """
            return self.find_element(*self._author_locator).text

        @property
        def date(self):
            """Return the article publish date string.

            :return: the article's publish date string
            :rtype: str

            """
            return self.find_element(*self._date_locator).text

        def get_date(self):
            """Return a timezone-aware datetime of the publish date.

            :return: the article's publish date as a timezone-aware datetime
            :rtype: :py:class:`~datetime.datetime`

            """
            return datetime.strptime(self.date + ' +0000', '%b %d, %Y %z')


class Article(Blog):
    """The OpenStax web log article."""

    URL_TEMPLATE = '/blog/{article}'

    _hero_banner_locator = (By.CSS_SELECTOR, '.hero')
    _article_title_locator = (By.CSS_SELECTOR, '.article h1')
    _disqus_locator = (By.CSS_SELECTOR, '#disqus_thread')

    def wait_for_page_to_load(self):
        """Override the page load function.

        Wait for the other blog article tiles and the article banner to load.

        :return: None

        """
        super(Blog, self).wait_for_page_to_load()
        self.wait.until(
            lambda _: (self.find_element(*self._hero_banner_locator)
                       .is_displayed()))

    def is_displayed(self):
        """Return True if the blog article banner image is displayed.

        :return: ``True`` if the blog article banner image and the Disqus
            comments widget are displayed
        :rtype: bool

        """
        return (
            self.wait.until(expect.visibility_of_element_located(
                self._hero_banner_locator)).is_displayed() and
            self.wait.until(
                expect.presence_of_element_located(self._disqus_locator)
            ).is_displayed())

    @property
    def title(self):
        """Return the article title.

        :return: the blog article title
        :rtype: str

        """
        return self.find_element(*self._article_title_locator).text.strip()

    @property
    def disqus(self):
        """Return the Disqus iframe.

        :return: the Disqus iframe element
        :rtype: :py:class:`~selenium.webdriver.remote.webelement.WebElement`

        """
        return self.find_element(*self._disqus_locator)

    def view_comments(self):
        """Scroll to the Disqus comment section.

        :return: the blog article
        :rtype: :py:class:`~pages.web.blog.Article`

        """
        self.wait.until(lambda _: self.disqus.is_displayed())
        Utility.scroll_to(self.driver, element_locator=self._disqus_locator)
        return self

    def view_other_posts(self):
        """Scroll to the other blog article tiles.

        :return: the blog article
        :rtype: :py:class:`~pages.web.blog.Article`

        """
        Utility.scroll_to(self.driver,
                          element_locator=self._other_posts_locator)
        return self
