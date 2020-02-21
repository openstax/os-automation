"""Accounts admin user search and editing."""

from datetime import datetime
from time import sleep

from pypom import Region
from selenium.webdriver.common.by import By

from pages.accounts.admin.base import AccountsAdmin
from pages.accounts.base import AccountsBase
from utils.utilities import Utility, go_to_


class SearchHelp(AccountsBase):
    """Accounts admin user search API manual."""

    URL_TEMPLATE = '/api/docs/v1/users/index'

    @property
    def at_user_api(self):
        """Return True if at the user API page."""
        return SearchHelp.URL_TEMPLATE in self.driver.current_url


class Search(AccountsAdmin):
    """Accounts admin user search."""

    URL_TEMPLATE = '/admin/users'

    _search_term_locator = (By.CSS_SELECTOR, '#search_terms')
    _ordering_locator = (By.CSS_SELECTOR, '#search_order_by')
    _search_button_locator = (By.CSS_SELECTOR, '[type=submit]')
    _search_help_locator = (By.CSS_SELECTOR, '.user-search-help a')

    _row_locator = (By.CSS_SELECTOR, 'tr')

    def search_for(self, **terms):
        """Enter the search terms or name.

        Search terms are comma-separated values. Usernames and account holders
        are wildcard searches while ID, email, and UUID are exact matches.
        Searches without a term apply to the username, first name, last name,
        and full name. Two word searches without a term are matched as:
        first_name:<first_word> last_name:<last_word>

        Args:
            username: match against the partial or full username field
            first_name: match against the partial or full first name field
            last_name: match against the partial or full last name field
            name: match against the partial or full first name field, last
                  name field, and full name field
            id: match against the exact Accounts user ID
            email: match against the exact email
            uuid: match against the exact UUID number

        """
        text = []
        if terms.get('literal'):
            text.append(terms.get('literal'))
        else:
            for term in terms:
                if ', ' in terms.get(term):
                    terms[term] = terms.get(term).replace(', ', ',')
                elif ' ' in terms.get(term):
                    terms[term] = f'"{terms.get(term)}"'
                text.append(f'{term}:{terms.get(term)}')
        search_bar = self.find_element(*self._search_term_locator)
        search_bar.send_keys(' '.join(text))
        return self

    def order_by(self, **terms):
        """Enter the ordering.

        Ordering options are by field equaling a direction
            ie: username=Accounts.ASCENDING
            to sort by the username in an ascending order

        Args:
            literal: send a literal string to the ordering bar
                     overrides other options
            username: alpha ordering on usernames
            first_name: alpha ordering on first names
            last_name: alpha ordering on last names
            id: numeric ordering by Accounts IDs
            role: alpha ordering on user roles

        """
        text = []
        if terms.get('literal'):
            text.append(terms.get('literal'))
        else:
            for term in terms:
                text.append(f'{term} {terms.get(term)}')
        order_bar = self.find_element(*self._ordering_locator)
        order_bar.send_keys(', '.join(text))
        return self

    def view_search_help(self):
        """Display the search API help page."""
        search_help = self.find_element(*self._search_help_locator)
        Utility.click_option(self.driver, element=search_help)
        return go_to_(SearchHelp(self.driver))

    def submit_search(self):
        """Click the search button."""
        search = self.find_element(*self._search_button_locator)
        Utility.click_option(self.driver, element=search)
        return self

    def find(self, terms, ordering=None):
        """Search for a set of terms and order the results."""
        self.search_for(**terms)
        sleep(0.5)
        if ordering:
            self.order_by(**ordering)
            sleep(0.5)
        self.submit_search()
        sleep(1.0)
        self.wait_for_page_to_load()
        return self

    @property
    def users(self):
        """Access the search results."""
        results = []
        for index, row in enumerate(self.find_elements(*self._row_locator)):
            if index == 0:
                continue
            if index % 2 == 1:
                results.append(self.Result(self, row, index + 2))
        return results

    class Result(Region):
        """A pair of rows containing account information."""

        # odd/even fields
        _expand_locator = (By.CSS_SELECTOR, 'td:first-child a')
        _user_id_locator = (By.CSS_SELECTOR, '[href$=edit]')
        _first_name_locator = (By.CSS_SELECTOR, 'td:nth-child(3)')
        _last_name_locator = (By.CSS_SELECTOR, 'td:nth-child(4)')
        _username_locator = (By.CSS_SELECTOR, 'td:nth-child(5)')
        _faculty_status_locator = (By.CSS_SELECTOR, 'td:nth-child(6)')
        _role_locator = (By.CSS_SELECTOR, 'td:nth-child(7)')
        _school_type_locator = (By.CSS_SELECTOR, 'td:nth-child(8)')
        _impersonate_locator = (By.CSS_SELECTOR, 'td:last-child a')

        DETAILS = 'tr.details:nth-child({index}) '

        def __init__(self, page, root, pos):
            """Override the initialization to include a position number."""
            super(Region, self).__init__(page.driver, page.timeout, pm=page.pm)
            self._root = root
            self.page = page
            self.wait_for_region_to_load()
            self._index = pos
            self._created_on_locator = (
                self.DETAILS.format(index=pos) + '.created')
            self._updated_on_locator = (
                self.DETAILS.format(index=pos) + '.updated')
            self._full_name_locator = (
                self.DETAILS.format(index=pos) + '.full-name')
            self._security_log_link_locator = (
                self.DETAILS.format(index=pos) + '.security_log a')
            self._state_locator = (
                self.DETAILS.format(index=pos) + '.state')
            self._uuid_locator = (
                self.DETAILS.format(index=pos) + '.uuid')
            self._support_identifier_locator = (
                self.DETAILS.format(index=pos) + '.support_identifier')
            self._emails_locator = (
                self.DETAILS.format(index=pos) + '.email')

        def edit(self):
            """Edit the user account data."""
            user = self.find_element(*self._user_id_locator)
            user_id = self.id
            Utility.switch_to(self.driver, element=user)
            sleep(1.5)
            return go_to_(Details(driver=self.driver,
                                  base_url=self.page.base_url,
                                  user_id=user_id))

        @property
        def id(self):
            """Return the Account ID."""
            return self.find_element(*self._user_id_locator).text

        @property
        def first_name(self):
            """Return the user's first name."""
            return self.find_element(*self._first_name_locator).text

        @property
        def last_name(self):
            """Return the user's last name."""
            return self.find_element(*self._last_name_locator).text

        @property
        def username(self):
            """Return the account username."""
            return self.find_element(*self._username_locator).text

        @property
        def faculty(self):
            """Return the faculty status for the account."""
            return self.find_element(*self._faculty_status_locator).text

        @property
        def role(self):
            """Return the user's self-reported role."""
            return self.find_element(*self._role_locator).text

        @property
        def school_type(self):
            """Return the account's associated school type."""
            return self.find_element(*self._school_type_locator).text

        def impersonate(self):
            """Log in as the user."""
            impersonate = self.find_element(*self._impersonate_locator)
            Utility.click_option(self.driver, element=impersonate)
            self.driver.switch_to_alert().accept()
            sleep(1.0)
            from pages.accounts.profile import Profile
            profile = Profile(self.driver, self.page.base_url)
            profile.open()
            sleep(10)
            return profile

        @property
        def created_on(self):
            """Return the account creation date and time."""
            return self._get_date_time(
                self._get_from_details(self._created_on_locator)
                .get_attribute('innerHTML'))

        @property
        def updated_on(self):
            """Return the most recent update date and time."""
            return self._get_date_time(
                self._get_from_details(self._updated_on_locator)
                .get_attribute('innerHTML'))

        @property
        def full_name(self):
            """Return the account user's full name."""
            return self._get_from_details(self._full_name_locator).text

        def view_security_log(self):
            """View the security log for the user."""
            log = self._get_from_details(self._security_log_link_locator)
            Utility.click_option(self.driver, element=log)
            from pages.accounts.admin.security import Security
            return go_to_(Security(self.driver))

        @property
        def state(self):
            """Return the account state."""
            return self._get_field_value(
                self._get_from_details(self._state_locator).text)

        @property
        def uuid(self):
            """Return the account UUID."""
            return self._get_field_value(
                self._get_from_details(self._uuid_locator).text)

        @property
        def support_id(self):
            """Return the account support identification number."""
            return self._get_field_value(
                self._get_from_details(self._support_identifier_locator).text)

        @property
        def emails(self):
            """Return the emails associated with the account."""
            return [self.Email(self, el)
                    for el in self._get_from_details(self._emails_locator,
                                                     True)]

        class Email(Region):
            """An account email."""

            _address_locator = (By.TAG_NAME, 'a')

            @property
            def email(self):
                """Return the email address."""
                return self.find_element(*self._address_locator).text

            @property
            def is_confirmed(self):
                """Return True if the email has been confirmed."""
                status = (self.root.get_attribute('innerHTML')
                          .split('>')[-1].strip())
                return status == '(confirmed)'

        def _get_from_details(self, css_selector, multiple=False):
            """Get element by document selector."""
            script = ('return document.querySelector{all}("{selector}")'
                      .format(all='All' if multiple else '',
                              selector=css_selector))
            return self.driver.execute_script(script)

        def _get_date_time(self, field_text):
            """Convert the date and time string to a zone-aware datetime."""
            return datetime.strptime(
                field_text.split('>')[-1].strip(), '%Y-%m-%d %H:%M:%S %z')

        def _get_field_value(self, field_text):
            """Get the field value from the text string."""
            return field_text.split(':')[-1].strip()


class Details(AccountsAdmin):
    """Accounts user account details."""

    URL_TEMPLATE = '/admin/users/{user_id}/edit'

    # User controls
    _username_locator = (By.CSS_SELECTOR, '#user_username')
    _name_locator = (By.CSS_SELECTOR, '[for=user_name] + div p')
    _become_user_locator = (By.CSS_SELECTOR, _name_locator[1] + ' a')
    _first_name_locator = (By.CSS_SELECTOR, '#user_first_name')
    _last_name_locator = (By.CSS_SELECTOR, '#user_last_name')
    _set_password_locator = (By.CSS_SELECTOR, '#user_password')
    _emails_locator = (By.CSS_SELECTOR, '[for=user_email_addresses] + ul li')
    _new_email_locator = (By.CSS_SELECTOR, '#user_email_address')

    # Salesforce information
    _saleforce_id_locator = (
        By.CSS_SELECTOR, '[for=user_salesforce_contact] + div p')
    _view_on_salesforce_locator = (
        By.CSS_SELECTOR, _saleforce_id_locator[1] + ' a')
    _set_contact_locator = (By.CSS_SELECTOR, '#user_salesforce_contact_id')
    _faculty_status_locator = (By.CSS_SELECTOR, '#user_faculty_status')
    _current_faculty_status_locator = (
        By.CSS_SELECTOR, '#user_faculty_status [selected]')
    _school_type_locator = (By.CSS_SELECTOR, '#user_school_type')
    _current_school_type_locator = (
        By.CSS_SELECTOR, '#user_school_type [selected]')

    # OpenStax security information
    _apps_locator = (By.CSS_SELECTOR, '[for=user_apps] + ul li')
    _log_in_options_locator = (
        By.CSS_SELECTOR, '[for=user_login_methods] + div p')
    _security_log_locator = (By.CSS_SELECTOR, '[href*=security]')

    # Account permissions
    _admin_flag_locator = (By.CSS_SELECTOR, '#user_is_administrator')
    _test_user_flag_locator = (By.CSS_SELECTOR, '#user_is_test')

    _save_button_locator = (By.CSS_SELECTOR, '[type=submit]')

    @property
    def username(self):
        """Return the currently assigned username."""
        return (self.find_element(*self._username_locator)
                .get_attribute('value'))

    @username.setter
    def username(self, username):
        """Change the username."""
        field = self.find_element(*self._username_locator)
        field.clear()
        field.send_keys(username)
        return self

    @property
    def name(self):
        """Return the user's name."""
        return self.find_element(*self._name_locator).text.strip()

    def become_user(self):
        """Impersonate the user."""
        become = self.find_element(*self._become_user_locator)
        Utility.click_option(self.driver, element=become)
        self.driver.switch_to_alert.accept()
        sleep(1.0)
        from pages.accounts.profile import Profile
        profile = Profile(self.driver, self.base_url)
        profile.open()
        return profile

    @property
    def salesforce_contact_id(self):
        """Return the Salesforce contact ID."""
        return self.find_element(*self._saleforce_id_locator).text.strip()

    @salesforce_contact_id.setter
    def salesforce_contact_id(self, contact_id):
        """Set the contact ID."""
        contact = self.find_element(*self._set_contact_locator)
        contact.clear()
        sleep(0.5)
        contact.send_keys(contact_id)
        return self

    def view_salesforce_contact(self):
        """View the contact information on Salesforce."""
        contact = self.find_element(*self._view_on_salesforce_locator)
        Utility.click_option(self.driver, element=contact)
        from pages.salesforce.home import Salesforce
        return go_to_(Salesforce(self.driver))

    def remove_contact_id(self):
        """Clear the Salesforce contact ID."""
        self.set_salesforce_contact_id = 'remove'
        return self

    @property
    def has_contact(self):
        """Return True if the user has a Salesforce contact ID set.

        If set, faculty status and school type are controlled from
        Salesforce and cannot be changed in Accounts.
        """
        return self.salesforce_contact_id != 'Not Set'

    @property
    def faculty_status(self):
        """Return the current faculty status."""
        return self.find_element(*self._current_faculty_status_locator).text

    @faculty_status.setter
    def faculty_status(self, status):
        """Set the faculty status for the user."""
        if self.has_contact:
            raise CannotAssignValueException(
                'Cannot set faculty status for users '
                'with a Salesforce contact')
        Utility.select(self.driver, self._faculty_status_locator, status)
        return self

    @property
    def school_type(self):
        """Return the current school type."""
        return self.find_element(*self._current_school_type_locator).text

    @school_type.setter
    def school_type(self, school_type):
        """Set the school type for the user."""
        if self.has_contact:
            raise CannotAssignValueException(
                'Cannot set the school type for users '
                'with a Salesforce contact')
        Utility.select(self.driver, self._school_type_locator, school_type)
        return self

    @property
    def first_name(self):
        """Return the user's first name."""
        return (self.find_element(*self._first_name_locator)
                .get_attribute('value'))

    @first_name.setter
    def first_name(self, name):
        """Change the first name."""
        first = self.find_element(*self._first_name_locator)
        first.clear()
        sleep(0.5)
        first.send_keys(name)
        return self

    @property
    def last_name(self):
        """Return the user's last name."""
        return (self.find_element(*self._last_name_locator)
                .get_attribute('value'))

    @last_name.setter
    def last_name(self, name):
        """Change the last name."""
        last = self.find_element(*self._last_name_locator)
        last.clear()
        sleep(0.5)
        last.send_keys(name)
        return self

    @property
    def new_password(self):
        """Getter not needed."""
        return ''

    @new_password.setter
    def new_password(self, password):
        """Change the password."""
        self.find_element(*self._set_password_locator).send_keys(password)
        return self

    @property
    def emails(self):
        """Return the account emails."""
        return [self.Email(self, el)
                for el in self.find_elements(*self._emails_locator)]

    def add_email(self, email):
        """Add a new email to the account."""
        self.find_element(*self._new_email_locator).send_keys(email)
        return self

    @property
    def apps(self):
        """Return the applications in use by the account."""
        return [self.App(self, el)
                for el in self.find_elements(*self._apps_locator)]

    @property
    def login_methods(self):
        """Return the list of logins in use by the account."""
        return (self.find_elements(*self._log_in_options_locator)
                .text
                .split(', '))

    def view_security_log(self):
        """View the security log for the account."""
        log = self.find_element(*self._security_log_locator)
        Utility.click_option(self.driver, element=log)
        from pages.accounts.admin.security import Security
        return go_to_(Security(self.driver))

    @property
    def is_admin(self):
        """Return True if the account is or will be an administrator."""
        return (self.find_element(*self._admin_flag_locator)
                .get_attribute('checked') == 'checked')

    def toggle_admin(self):
        """Click on the admin permissions checkbox."""
        return self._toggle_helper(self._admin_flag_locator, self.is_admin)

    @property
    def is_a_test_user(self):
        """Return True if the account is or will be a test user."""
        return (self.find_element(*self._test_user_flag_locator)
                .get_attribute('checked') == 'checked')

    def toggle_tester(self):
        """Click on the test user permissions checkbox."""
        return self._toggle_helper(self._test_user_flag_locator,
                                   self.is_a_test_user)

    def _toggle_helper(self, locator, test):
        """Click on a checkbox and set the checked attribute."""
        checkbox = self.find_element(*locator)
        Utility.click_option(self.driver, element=checkbox)
        sleep(1.0)
        self.driver.execute_script(
            'arguments[0].setAttribute("checked", "{value}");'
            .format(value='' if test else 'checked'),
            checkbox)
        return self

    def save(self):
        """Click the save button to preserve the current account settings."""
        button = self.find_element(*self._save_button_locator)
        Utility.click_option(self.driver, element=button)
        return self

    class Email(Region):
        """User-assigned email, status, and forced confirmation."""

        _confirmation_link_locator = (By.TAG_NAME, 'a')

        @property
        def email(self):
            """Return the email address."""
            return self.root.text.split()[0]

        @property
        def is_confirmed(self):
            """Return True if the email was confirmed."""
            return 'Confirmed' in self.root.text

        def confirm_address(self):
            """Force the confirmation of an email."""
            link = self.find_element(*self._confirmation_link_locator)
            Utility.click_option(self.driver, element=link)
            self.driver.switch_to_alert().accept()
            return Details(self.driver, user_id=self.url_kwargs.get('user_id'))

    class App(Region):
        """Applications associated with a user."""

        _view_app_user_info_locator = (By.TAG_NAME, 'a')

        @property
        def app(self):
            """Return the app name."""
            return self.root.split('[')[0].strip()

        def view_tutor_data(self):
            """View user information on Tutor."""
            if 'Tutor' in self.app:
                user = self.find_element(*self._view_app_user_info_locator)
                Utility.click_option(self.driver, element=user)
                from pages.tutor.admin.users import Details as TutorDetails
                return go_to_(TutorDetails(self.driver))


class Actions(AccountsAdmin):
    """Accounts user actions."""

    URL_TEMPLATE = '/admin/users/actions'

    _mark_updated_button_locator = (By.CSS_SELECTOR, '[type=submit]')

    def mark_as_updated(self):
        """Mark all accounts as recently updated."""
        updated = self.find_element(*self._mark_updated_button_locator)
        Utility.click_option(self.driver, element=updated)
        return self


class PreAuth(AccountsAdmin):
    """Pre-authenticated users."""

    URL_TEMPLATE = '/admin/pre_auth_states'

    _one_day_filter_locator = (By.CSS_SELECTOR, '.searches a:first-child')
    _one_week_filter_locator = (By.CSS_SELECTOR, '.searches a:nth-child(2)')
    _two_weeks_filter_locator = (By.CSS_SELECTOR, 'searches a:nth-child(3)')
    _all_pending_filter_locator = (By.CSS_SELECTOR, 'searches a:last-child')
    _entries_locator = (By.CSS_SELECTOR, '.entry')

    def view_one_day(self):
        """View pre-auth for the past day."""
        one_day = self.find_element(*self._one_day_filter_locator)
        Utility.click_option(self.driver, element=one_day)
        return self

    def view_one_week(self):
        """View pre-auth for the past week."""
        one_week = self.find_element(*self._one_week_filter_locator)
        Utility.click_option(self.driver, element=one_week)
        return self

    def view_two_weeks(self):
        """View pre-auth for the past two weeks."""
        two_weeks = self.find_element(*self._two_weeks_filter_locator)
        Utility.click_option(self.driver, element=two_weeks)
        return self

    def view_all(self):
        """View all accounts in pre-auth."""
        view_all = self.find_element(*self._all_pending_filter_locator)
        Utility.click_option(self.driver, element=view_all)
        return self

    @property
    def requests(self):
        """Return the list of accounts in a pre-auth state."""
        return [self.Pending(self, el)
                for el in self.find_elements(*self._entries_locator)]

    class Pending(Region):
        """Account signup in a pre-authorization state."""

        EMAIL = 0
        STATE = 1
        PIN = 2
        USER_TYPE = 3
        CREATED = 4

        _content_locator = (By.CSS_SELECTOR, '.basics')
        _token_url_locator = (By.CSS_SELECTOR, 'token')

        @property
        def email(self):
            """Return the registration email."""
            return self._split_basic(self.EMAIL)

        @property
        def email_state(self):
            """Return the registration email state."""
            return self._split_basic(self.STATE)

        @property
        def verification_pin(self):
            """Return the email confirmation pin."""
            return self._split_basic(self.PIN)

        @property
        def user_type(self):
            """Return the self-reported user type."""
            return self._split_basic(self.USER_TYPE)

        @property
        def requested_on(self):
            """Return the registration date and time.

            Use a timezone-aware datetime.
            """
            return self._split_basic(self.CREATED)

        def _split_basic(self, segment):
            """Split the basic data fields."""
            content = (
                self.find_element(*self._content_locator)
                .get_attribute('innerHTML')
                .split('|')
                [segment]
                .strip())
            if segment == self.EMAIL or segment == self.STATE:
                return content
            content = content.split('>')[1].split('<')[0]
            if segment == self.PIN or segment == self.USER_TYPE:
                return content
            return datetime.strptime(content.replace('UTC', '+0000'),
                                     '%Y-%m-%d %H:%M:%S %z')


class Reports(AccountsAdmin):
    """User counts."""

    URL_TEMPLATE = '/admin/reports'

    _user_counts_locator = (By.CSS_SELECTOR, '.errors + h3 + p')
    _faculty_counts_locator = (By.CSS_SELECTOR, 'p + h3 + p')

    @property
    def users(self):
        """Access the user totals."""
        users_root = self.find_element(*self._user_counts_locator)
        return self.Users(self, users_root)

    @property
    def faculty(self):
        """Access the faculty totals."""
        faculty_root = self.find_element(*self._faculty_counts_locator)
        return self.Faculty(self, faculty_root)

    class Users(Region):
        """Accounts users totals."""

        TOTAL = 1
        STUDENTS = 2
        INSTRUCTORS = 3
        UNKNOWN = 4

        @property
        def total(self):
            """Return the total number of user accounts."""
            return self._pull_number(self.TOTAL)

        @property
        def students(self):
            """Return the number of student accounts."""
            return self._pull_number(self.STUDENTS)

        @property
        def faculty(self):
            """Return the number of instructor accounts."""
            return self._pull_number(self.INSTRUCTORS)

        @property
        def unknown(self):
            """Return the number of accounts without a set role."""
            return self._pull_number(self.UNKNOWN)

        def _pull_number(self, segment):
            """Pull the requested number from the list."""
            data = self.root.get_attribute('innerHTML').split(':')
            return int(data[segment].split('<')[0].strip())

    class Faculty(Region):
        """Faculty user breakdown."""

        CONFIRMED = 1
        PENDING = 2
        REJECTED = 3
        UNKNOWN = 4

        @property
        def confirmed(self):
            """Return the total number of confirmed faculty."""
            return self._pull_number(self.CONFIRMED)

        @property
        def pending(self):
            """Return the total number of faculty with a pending request."""
            return self._pull_number(self.PENDING)

        @property
        def rejected(self):
            """Return the total number of faculty with a rejected request."""
            return self._pull_number(self.REJECTED)

        @property
        def unknown(self):
            """Return the total number of faculty with an unknown role."""
            return self._pull_number(self.UNKNOWN)

        def _pull_number(self, segment):
            """Pull the requested number from the list."""
            data = self.root.get_attribute('innerHTML').split(':')
            return int(data[segment].split('<')[0].strip())


class CannotAssignValueException(Exception):
    """Accounts cannot change values for user with a Salesforce contact."""

    pass
