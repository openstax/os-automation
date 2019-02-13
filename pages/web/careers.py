"""The OpenStax jobs board."""

import re

from selenium.webdriver.common.by import By

from pages.web.base import WebBase
from utils.utilities import Utility, go_to_


class Careers(WebBase):
    """The OpenStax jobs board."""

    URL_TEMPLATE = '/careers'

    _banner_locator = (By.CSS_SELECTOR, 'h1')
    _subheading_locator = (
        By.CSS_SELECTOR, '[data-html=content] p:first-child')
    _careers_content_locator = (
                    By.CSS_SELECTOR, '#main [data-html=content] p:first-child')
    _job_list_locator = (By.CSS_SELECTOR, '[data-html=content] p:nth-child(5)')

    @property
    def loaded(self):
        """Return True when text content is found."""
        content = (self.find_element(*self._careers_content_locator)
                   .text.strip())
        banner = self.find_element(*self._banner_locator)
        return content and banner

    def is_displayed(self):
        """Return True if the heading is displayed."""
        return self.job_list

    @property
    def job_list(self):
        """Return the content within the open positions element."""
        listings = self.wait.until(
            lambda _: self.find_element(*self._job_list_locator))
        return listings.get_attribute('innerHTML')

    @property
    def jobs(self):
        """Access the available jobs."""
        segments = (re.sub(r'(<br[\/ ]{0,2}>){2}', '|||', self.job_list)
                    .split('|||'))
        return [self.Job(self, text) for text in segments]

    class Job():
        """A job entry."""

        def __init__(self, page, job_string):
            """Initialize an open job position object."""
            self.page = page
            try:
                href = re.search(r'href=\"[\w\d\/\:\*\.]*\"', job_string)
                self._url = href.group().split('"')[1] if href else ''
            except AttributeError:
                self._url = ''
            try:
                title = (re.search(r'<b>[^(<\/)]*<\/b>', job_string)
                         .group().split('>', 1)[-1])
                self._title = re.sub(r'<b>|<\/b>', '', title)
            except AttributeError:
                self._title = ''
            try:
                self._description = re.split(r'<\/b>|<br>', job_string)[-1]
            except AttributeError:
                self._description = ''

        @property
        def title(self):
            """Return the job title."""
            return self._title

        @property
        def description(self):
            """Return the job summary."""
            return self._description

        @property
        def url(self):
            """Return the Rice Jobs posting URL."""
            return self._url

        def view_position(self):
            """Click on the position name to view the Rice Jobs board."""
            button = self.page.find_element(By.LINK_TEXT, self.title)
            Utility.switch_to(self.page.driver, element=button)
            from pages.rice.jobs import RiceJobs
            return go_to_(RiceJobs(self.page.driver))
