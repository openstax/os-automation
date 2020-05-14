"""OpenStax book errata."""

from time import sleep

from pypom import Region
from selenium.webdriver.common.by import By

from pages.web.base import WebBase
from utils.utilities import Actions, Utility, go_to_
from utils.web import Web, WebException


class ErrataBase(Region):
    """Base region for errata entries."""

    @property
    def submitted_on(self):
        """Return the date the errata was submitted."""
        return self.find_element(*self._submit_date_locator).text.strip()

    def submission_date(self):
        """Return an aware date time."""
        from datetime import datetime
        return datetime.strptime(self.submitted_on, ('%m/%d/%Y %z' + '+0000'))

    @property
    def _errata(self):
        """Return the errata details link element."""
        return self.find_element(*self._errata_id_locator)

    @property
    def errata_id(self):
        """Return the errata ID number."""
        return self._errata.text.strip()

    def view_errata(self):
        """View the errata item in detail."""
        Utility.click_option(self.driver, element=self.errata)
        return go_to_(ErrataDetail(self.driver,
                                   base_url=self.base_url,
                                   _id=self.errata_id))

    @property
    def source(self):
        """Return the errata submission source."""
        return self.find_element(*self._source_locator).text.strip()

    @property
    def error_type(self):
        """Return the errata type."""
        return self.find_element(*self._error_type_locator).text.strip()

    @property
    def found_in(self):
        """Return the location of the error."""
        return self.find_element(*self._location_locator).text.strip()

    @property
    def decision(self):
        """Return the current errata decision."""
        return self.find_element(*self._decision_locator).text.strip()


class Errata(WebBase):
    """The errata list for a particular book."""

    URL_TEMPLATE = '/errata/?book={book}'

    # Filter by...
    ALL = 0
    IN_REVIEW = 1
    REVIEWED = 2
    CORRECTED = 3

    # Sort by...
    DATE = 0
    ID = 1
    SOURCE = 2
    TYPE = 3
    DECISION = 4

    # Using...
    ASCENDING = 'sortdir1'
    DESCENDING = 'sortdir-1'

    _table_locator = (By.CSS_SELECTOR, '.summary-table tbody')
    _title_locator = (By.CSS_SELECTOR, '.hero h1')
    _tooltip_base_locator = (By.CSS_SELECTOR, '.with-tooltip')
    _schedule_locator = (By.CSS_SELECTOR, '.tooltip p')
    _filter_toggle_locator = (By.CSS_SELECTOR, '.filter-buttons')
    _filter_button_locator = (By.CSS_SELECTOR, '.filter-button')
    _header_locator = (By.CSS_SELECTOR, '[data-sort-fn]')
    _errata_locator = (By.CSS_SELECTOR, '.summary-table tbody tr')
    _mobile_errata_locator = (By.CSS_SELECTOR, '.summary-table-mobile')

    @property
    def loaded(self):
        """Wait for the page loader and table data.

        If there isn't data (eg a new book), sleep 3 seconds then return.
        """
        return (
            super().loaded and
            (Utility.has_children(self.find_element(*self._table_locator)) or
             (sleep(3) or True)))

    def is_displayed(self):
        """Return True if the errata table is displayed."""
        if self.driver.get_window_size().get('width') > Web.PHONE:
            table = self.find_elements(*self._table_locator)
        else:
            table = self.find_elements(*self._mobile_errata_locator)
        if self.loaded and not table:
            raise WebException('Errata table is empty')
        return self.loaded and table[0].is_displayed()

    @property
    def title(self):
        """Return the book title."""
        return self.find_element(*self._title_locator).text.split(' Errata')[0]

    @property
    def tooltip(self):
        """Return the tooltip anchor."""
        return self.find_element(*self._tooltip_base_locator)

    @property
    def correction_schedule(self):
        """Return the tooltip."""
        return self.find_element(*self._schedule_locator)

    def view_correction_schedule(self):
        """Mouse over the schedule and check that it shows."""
        result = (
            Actions(self.driver)
            .move_to_element(self.tooltip)
            .pause(1)
            .get_js_data(self._schedule_locator[1], 'height', '0px')
            .perform())
        return not result

    @property
    def filters(self):
        """Access the errata filters."""
        return [self.Filter(self, _filter)
                for _filter
                in self.find_elements(*self._filter_button_locator)]

    def filter_by(self, _filter=ALL):
        """Select an errata display filter."""
        if self.driver.get_window_size().get('width') < Web.PHONE:
            self.filter_toggle()
        self.filters[_filter].select()
        return self

    @property
    def order_options(self):
        """Access the sort options."""
        return [option for option in self.find_elements(*self._header_locator)]

    def sort_by(self, sort=DATE, direction=DESCENDING):
        """Sort the errata list by a column header."""
        current = (
            self.order_options[sort]
            .find_element_by_tag_name('span')
            .get_attribute('class'))
        if 'will-sort' not in current and direction in current:
            # requested category already sorted correctly
            pass
        elif 'will-sort' not in current and direction not in current:
            # requested category active but need to flip the sort direction
            self.order_options[sort].click()
        else:
            # requested category is inactive
            if direction == self.DECENDING:
                # set direction to most recent first
                self.order_options[sort].click()
            else:
                # set direction to oldest first
                self.order_options[sort].click()
                self.order_options[sort].click()
        return self

    @property
    def errors(self):
        """Access the individual errata entries."""
        if self.driver.get_window_size().get('width') > Web.PHONE:
            return [self.ErrataItem(self, error)
                    for error in self.find_elements(*self._errata_locator)]
        return [self.MobileErrataItem(self, error)
                for error in self.find_elements(*self._mobile_errata_locator)]

    class Filter(Region):
        """An errata filter."""

        _value_locator = (By.CSS_SELECTOR, '[data-html]')

        @property
        def value(self):
            """Return the filter option name."""
            return self.find_element(*self._value_locator).text.strip()

        @property
        def is_selected(self):
            """Return True if the filter is currently selected."""
            return self.root.get_attribute('aria-pressed') == 'true'

        def select(self):
            """Select the errata filter."""
            self.root.click()
            sleep(0.5)
            return self.page

    class ErrataItem(ErrataBase):
        """An errata entry."""

        _submit_date_locator = (By.CSS_SELECTOR, 'td:first-child')
        _errata_id_locator = (By.CSS_SELECTOR, 'td:nth-child(2) a')
        _source_locator = (By.CSS_SELECTOR, 'td:nth-child(3)')
        _error_type_locator = (By.CSS_SELECTOR, 'td:nth-child(4)')
        _location_locator = (By.CSS_SELECTOR, 'td:nth-child(5)')
        _description_locator = (By.CSS_SELECTOR, 'td:nth-child(6)')
        _decision_locator = (By.CSS_SELECTOR, 'td:last-child')

    class MobileErrataItem(ErrataBase):
        """An errata entry for a mobile display."""

        _submit_date_locator = (By.CSS_SELECTOR, 'tr:first-child div')
        _errata_id_locator = (By.CSS_SELECTOR, 'tr:nth-child(2) a')
        _source_locator = (By.CSS_SELECTOR, 'tr:nth-child(3) div')
        _error_type_locator = (By.CSS_SELECTOR, 'tr:nth-child(4) div')
        _location_locator = (By.CSS_SELECTOR, 'tr:nth-child(5) div')
        _description_locator = (By.CSS_SELECTOR, 'tr:nth-child(6) div')
        _decision_locator = (By.CSS_SELECTOR, 'tr:last-child div')


class ErrataDetail(WebBase):
    """A detailed view for a single errata item."""

    URL_TEMPLATE = '/errata/{_id}'

    _progress_bar_locator = (By.CSS_SELECTOR, '.progress-bar-labels')
    _in_review_locator = (By.CSS_SELECTOR, '.label:first-child .date')
    _reviewed_on_locator = (By.CSS_SELECTOR, '.label:nth-child(2) .date')
    _completed_on_locator = (By.CSS_SELECTOR, '.label:last-child .date')
    _errata_id_locator = (By.CSS_SELECTOR, '[data-html*="\'id\'"]')
    _book_locator = (By.CSS_SELECTOR, 'div[data-html*=bookTitle]')
    _source_locator = (By.CSS_SELECTOR, '[data-html*=source]')
    _status_locator = (By.CSS_SELECTOR, '[data-html*=displayStatus]')
    _error_type_locator = (By.CSS_SELECTOR, '[data-html*=error_type]')
    _location_locator = (By.CSS_SELECTOR, '[data-html*=location]')
    _description_locator = (By.CSS_SELECTOR, '[data-html*="\'detail\'"]')
    _submit_date_locator = (By.CSS_SELECTOR, '[data-html*="\'date\'"]')
    _return_to_errata_locator = (By.CSS_SELECTOR, '[href*="/errata/?"]')

    @property
    def loaded(self):
        """Return True when an errata ID is found."""
        return self.find_element(*self._errata_id_locator)

    def is_displayed(self):
        """Return True if the progress bar is displayed."""
        return self.find_element(*self._progress_bar_locator).is_displayed()

    @property
    def in_review(self):
        """Return the date the errata was submitted."""
        return self.find_element(*self._in_review_locator).text

    @property
    def reviewed_on(self):
        """Return the date the errata was reviewed."""
        return self.find_element(*self._reviewed_on_locator).text

    @property
    def completed_on(self):
        """Return the date the errata review was completed."""
        return self.find_element(*self._completed_on_locator).text

    @property
    def errata_id(self):
        """Return the errata ID."""
        return self.find_element(*self._errata_id_locator).text

    @property
    def title(self):
        """Return the book title."""
        return self.find_element(*self._book_locator).text

    @property
    def source(self):
        """Return the errata source location."""
        return self.find_element(*self._source_locator).text

    @property
    def status(self):
        """Return the current status of the errata submission."""
        return self.find_element(*self._status_locator).text

    @property
    def error_type(self):
        """Return the errata type."""
        return self.find_element(*self._error_type_locator).text

    @property
    def found_in(self):
        """Return the location where the issue was found."""
        return self.find_element(*self._location_locator).text

    @property
    def description(self):
        """Return the full issue description."""
        return self.find_element(*self._description_locator).text.strip()

    @property
    def submitted_on(self):
        """Return the date the errata was submitted."""
        return self.find_element(*self._submit_date_locator).text

    @property
    def errata_list(self):
        """Return the errata list link element."""
        return self.find_element(*self._return_to_errata_locator)

    def return_to_errata_list(self):
        """Return to the book's errata list."""
        book = self.errata_list.get_attribute('href').split('=')[-1]
        Utility.click_option(self.driver, self.errata_list)
        return go_to_(Errata(self.driver, base_url=self.base_url, book=book))


class ErrataForm(WebBase):
    """The errata submission form."""

    URL_TEMPLATE = '/errata/form?book={book}'

    _form_locator = (By.CSS_SELECTOR, '.body-block')
    _subject_locator = (By.CSS_SELECTOR, '.hero h1')

    @property
    def loaded(self):
        """Return True when an errata form and book title are found."""
        return (super().loaded and
                bool(self.find_elements(*self._form_locator)) and
                bool(self.find_elements(*self._subject_locator)) and
                'errata/form' in self.location)

    def is_displayed(self):
        """Return True if the form is displayed."""
        return self.find_element(*self._form_locator).is_displayed()

    @property
    def subject(self):
        """Return the currently selected book title."""
        return self.find_element(*self._subject_locator).text
