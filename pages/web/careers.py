"""The OpenStax jobs board."""

from __future__ import annotations

from typing import List

from pypom import Region
from selenium.webdriver.common.by import By

from pages.web.base import WebBase
from utils.utilities import Utility, go_to_


class Careers(WebBase):
    """The OpenStax jobs board."""

    URL_TEMPLATE = '/careers'

    _banner_locator = (By.CSS_SELECTOR, 'h1')
    _careers_content_locator = (
        By.CSS_SELECTOR, '#maincontent')
    _job_list_locator = (By.XPATH, '//*[@id="maincontent"]/div/p[a]')
    _job_title_locator = (By.CSS_SELECTOR, 'a')

    @property
    def loaded(self) -> bool:
        """Return True when text content is found.

        :return: ``True`` when the text content is found and the async overlay
            is not
        :rtype: bool

        """
        content = (self.find_element(*self._careers_content_locator)
                   .text.strip())
        banner = self.find_element(*self._banner_locator)
        return super().loaded and content and banner

    def is_displayed(self) -> bool:
        """Return True if the heading is displayed.

        :return: ``True`` if the job list is populated
        :rtype: bool

        """
        return self.job_list

    @property
    def job_list(self) -> str:
        """Return the content within the open positions element.

        :return: the job list content inner HTML
        :rtype: str

        """
        listings = self.wait.until(
            lambda _: self.find_element(*self._job_list_locator))
        return listings.get_attribute('innerHTML')

    @property
    def jobs(self) -> List[Careers.Job]:
        """Access the available jobs.

        :return: the list of available OpenStax jobs
        :rtype: list(:py:class:`~pages.web.careers.Careers.Job`)

        """
        jobs = self.find_element(*self._job_list_locator)
        return [self.Job(self, position)
                for position
                in jobs.find_elements(*self._job_title_locator)]

    class Job(Region):
        """A job entry."""

        @property
        def title(self) -> str:
            """Return the job title.

            :return: the job title
            :rtype: str

            """
            return self.root.get_attribute('textContent').strip()

        @property
        def url(self) -> str:
            """Return the Rice Jobs posting URL.

            :return: the Rice jobs board posting for the position
            :rtype: str

            """
            return self.root.get_attribute('href')

        def view_position(self):
            """Click on the position name to view the Rice Jobs board.

            :return: the job posting on the Rice Jobs board
            :rtype: :py:class:`~pages.rice.jobs.RiceJobs`

            """
            Utility.switch_to(self.page.driver, element=self.root)
            from pages.rice.jobs import RiceJobs
            return go_to_(RiceJobs(self.page.driver))
