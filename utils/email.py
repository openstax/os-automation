"""Email providers."""

import base64
import re
import smtplib
from contextlib import contextmanager
from datetime import datetime, timezone
from email.mime.text import MIMEText
from email.utils import formataddr as format_address
from time import sleep

import requests
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import client, file, tools
from pypom import Page, Region
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect

from utils.utilities import Utility

PIN_MATCHER = re.compile(r'(PIN\:? \d{6})')
URL_MATCHER = re.compile(
    r'(https:\/\/accounts([-\w]*)?\.openstax\.org\/confirm\?code=\w{1,64})'
)
RESET_MATCHER = re.compile(
    r'(https:\/\/accounts([-\w]*)?\.openstax\.org\/i\/' +
    r'([_\w]*)\?token=\w{1,64})'
)


class GoogleBase(Page):
    """Use Gmail."""

    URL_TEMPLATE = (
        'https://accounts.google.com/AccountChooser?service=mail&continue='
        'https://mail.google.com/mail/')

    def wait_for_page_to_load(self):
        """Override page load."""
        self.wait.until(
            expect.presence_of_element_located((By.TAG_NAME, 'body')))

    def log_in(self, username, password):
        """Log into google account."""
        sleep(1)
        if 'google' in self.driver.current_url:
            return self.login.go(username, password)
        else:
            return Google(self.driver)

    @property
    def login(self):
        """Return the Login control."""
        return self.Login(self)

    class Login(Region):
        """Gmail login."""

        _root_locator = (By.ID, 'view_container')
        _email_locator = (By.CSS_SELECTOR, '[type=email]')
        _email_next_locator = (By.ID, 'identifierNext')
        _password_locator = (By.CSS_SELECTOR, '[type=password]')
        _password_next_locator = (By.ID, 'passwordNext')

        def go(self, email, password):
            """Log into Google."""
            self.wait.until(
               expect.presence_of_element_located(
                   self._email_locator))\
                .send_keys(email)
            self.find_element(*self._email_next_locator).click()
            sleep(1.0)
            Utility.scroll_to(self.driver, self._password_locator)
            self.find_element(*self._password_locator).send_keys(password)
            self.find_element(*self._password_next_locator).click()
            return Google(self.driver)


class Google(GoogleBase):
    """Logged in e-mail interaction."""

    URL_TEMPLATE = 'https://mail.google.com/mail/u/0/#inbox'

    _root_locator = (By.CSS_SELECTOR, '.bkL .F')
    _email_row_locator = (By.CSS_SELECTOR, '.bkL .F tr')

    def wait_for_page_to_load(self):
        """Override page load."""
        self.wait.until(
            expect.presence_of_element_located(self._root_locator))

    @property
    def emails(self):
        """Return the first page of e-mail results."""
        self.wait_for_page_to_load()
        return [self.Email(self, el)
                for el in self.find_elements(*self._email_row_locator)]

    class Email(Region):
        """Email container."""

        _from_locator = (By.CSS_SELECTOR, '.yW span[email]')
        _subject_locator = (By.CLASS_NAME, 'bog')
        _excerpt_old_locator = (By.CSS_SELECTOR, '.y6 .y2')
        _excerpt_new_locator = (By.CSS_SELECTOR, '.y6 + .y2')
        _sent_locator = (By.CSS_SELECTOR, '.xW span[title]')

        @property
        def sender(self):
            """Return the e-mail sender."""
            return self.find_element(*self._from_locator) \
                .get_attribute('email')

        @property
        def subject(self):
            """Return the e-mail subject."""
            return self.find_element(*self._subject_locator).text

        @property
        def excerpt(self):
            """Return the e-mail body excerpt."""
            segment_one = ''
            segment_two = ''
            try:
                segment_one = self.find_element(
                    *self._excerpt_old_locator).text
            except Exception:
                pass
            try:
                segment_two = self.find_element(
                    *self._excerpt_new_locator).text
            except Exception:
                pass
            return segment_one if len(segment_one) > len(segment_two) else \
                segment_two

        @property
        def has_pin(self):
            """Return True if a pin string is in the body excerpt."""
            return bool(PIN_MATCHER.search(self.excerpt) or
                        PIN_MATCHER.search(self.subject))

        @property
        def get_pin(self):
            """Return the numeric pin."""
            if self.has_pin:
                try:
                    return (PIN_MATCHER.search(self.excerpt).group())[-6:]
                except Exception:
                    return (PIN_MATCHER.search(self.subject).group())[-6:]
            raise EmailVerificationError('No pin found')

        @property
        def sent(self):
            """Return the sent time and date."""
            return datetime.strptime(
                self.find_element(*self._sent_locator).get_attribute('title'),
                '%a, %b %d, %Y, %I:%M %p'
            )

        def __str__(self):
            """Override the string method."""
            return self.__unicode__()

        def __unicode__(self):
            """Write an email printer."""
            return (
                'From:    {sender}\n'
                'Subject: {subject}\n'
                'Excerpt: {excerpt}\n'
                'Sent:    {sent}\n'
                'PIN:     {has} : {pin}\n'
            ).format(
                sender=self.sender,
                subject=self.subject,
                excerpt=self.excerpt,
                sent=self.sent,
                has=self.has_pin,
                pin=self.get_pin if self.has_pin else ''
            )

        @property
        def is_new(self):
            """Return True if the email was sent less than 5 minutes ago."""
            return ((datetime.now() - self.sent).seconds / 60.0) < 5.0


class GmailReader(object):
    """Read the user's inbox."""

    def __init__(self, tag=''):
        """Initialize the reader."""
        # If modifying the scope(s), delete the file token.json.
        self._scopes = 'https://www.googleapis.com/auth/gmail.readonly'
        self._inbox = []
        self._tag = '_{suffix}'.format(suffix=tag) if tag else ''
        self._file = 'client_secret{suffix}.json'.format(suffix=self._tag)
        print('"{one}": "{two}" "{three}"'.format(one=tag, two=self._tag,
                                                  three=self._file))

    def add_email(self, request_id, response, exception):
        """Do something with the batch response.

        Args:
            request_id: a unique identifier for each request
            response: the deserialized response object from the request
            exception: a googleapiclient.errors.HttpError exception if
                       an error occurred or None
        Raises:
            googleapiclient.errors.HttpError

        """
        if exception:
            print('{id} blew up! {ex}'.format(request_id, exception))
            raise exception
        else:
            self._inbox.append(self.Email(response))

    def read_mail(self, user='me', labels=['INBOX']):
        """Query Gmail and download the the inbox mail.

        Args:
            user: the Gmail user to query for
                  default uses 'me' from the token file if it exists
            labels: a list of labels to match
                    default to just the inbox

        """
        store = file.Storage('token{suffix}.json'
                             .format(suffix=self._tag))
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(self._file, self._scopes)
            creds = tools.run_flow(flow, store)
        service = build('gmail', 'v1', http=creds.authorize(Http()))
        data_line = []
        request = (service
                   .users()
                   .messages()
                   .list(userId=user, labelIds=labels))

        # For each page of emails, download the email IDs for use later
        # Google returns the lists in pre-selected batches of up to 100 items
        while request is not None:
            data = request.execute()
            data_line.append(data.get('messages'))
            request = (service
                       .users()
                       .messages()
                       .list_next(request, data))

        # For each list of email IDs, download the emails as batches to
        # minimize the number of HTTP requests
        for batch in data_line:
            request = service.new_batch_http_request()
            for email in batch:
                request.add(
                    service
                    .users()
                    .messages()
                    .get(userId='me', id=email.get('id')),
                    callback=self.add_email
                )
            request.execute()
        return self

    def sort_mail(self, newest_first=True):
        """Sort the inbox.

        Args:
            newest_first: sort the box in the reverse order to have the
                          most recent mail first

        """
        self._inbox.sort(reverse=newest_first)
        return self

    @property
    def size(self):
        """Return the number of messages in the inbox."""
        return len(self._inbox)

    def get(self, key):
        """Return the email at the key's location."""
        return self.__getitem__(key)

    @property
    def latest(self):
        """Return the most recent email."""
        return self.get(0)

    def __getitem__(self, key):
        """Enable the bracket operator for the inbox list."""
        if not self._inbox:
            raise EmptyInboxError('Inbox is empty')
        return self._inbox[key]

    class Email(object):
        """A Gmail email from an API call."""

        def __init__(self, email):
            """Construct a new email.

            Args:
                email: a Gmail message dictionary

            """
            self._id = email.get('id', '')
            self._thread = email.get('threadId', '')
            self._labels = email.get('labelIds', [])
            self._excerpt = email.get('snippet', '')
            self._history = email.get('historyId')
            epoch = int(email.get('internalDate'))
            self._created_at = datetime.fromtimestamp(
                epoch / 1000,
                timezone.utc
            )
            self._since_epoch = epoch
            self._payload = email.get('payload')
            self._body = ''
            self._recipients = ''
            self._sender = ''
            self._subject = ''
            for part in self._payload.get('parts'):
                for header in part.get('headers'):
                    name = header.get('name')
                    value = header.get('value')
                    if (name == 'Content-Transfer-Encoding'
                            and value == 'base64'):
                        self._body = (base64.urlsafe_b64decode(
                            bytes(part.get('body').get('data'), 'UTF-8'))
                        ).decode('UTF-8')
                        break
            for header in self._payload.get('headers'):
                name = header.get('name')
                if name == 'To':
                    self._recipients = header.get('value')
                elif name == 'From':
                    self._sender = header.get('value')
                elif name == 'Subject':
                    self._subject = header.get('value')
            self._size = int(email.get('sizeEstimate'))
            self._raw = email.get('raw')

        def __lt__(self, rhs):
            """Override less than for sorting the inbox."""
            if not isinstance(rhs, type(self)):
                return NotImplemented
            return self._since_epoch < rhs.epoch

        def __str__(self):
            """Print the email."""
            return self.__unicode__()

        def __unicode__(self):
            """Print the email."""
            return (
                'From:    {sender}\n'
                'To:      {recipients}\n'
                'Subject: {subject}\n'
                'Excerpt: {excerpt}\n'
                'Body:\n{body}\n'
            ).format(
                sender=self._sender if self._sender else '',
                recipients=self._recipients if self._recipients else '',
                subject=self._subject if self._subject else '',
                excerpt=self._excerpt if self._excerpt else '',
                body=self._body if self._body else '')

        @property
        def epoch(self):
            """Return the milliseconds since 1970.

            Standard Epoch is the seconds since 1970 so divide by 1000
            """
            return self._since_epoch

        @property
        def excerpt(self):
            """Return the short text snippet as displayed by Gmail."""
            return self._excerpt

        @property
        def body(self):
            """Return the body text as displayed by selecting the email."""
            return self._body

        @property
        def get_pin(self):
            """Return the numeric pin."""
            match = PIN_MATCHER.search(self.excerpt)
            if match:
                return (match.group())[-6:]


class EmptyInboxError(IndexError):
    """The inbox is empty."""

    def __init__(self, *args, **kwargs):
        """Initialize for an empty inbox error."""
        IndexError.__init__(self, *args, **kwargs)


class GuerrillaMail(Page):
    """Use Guerrilla short term mail."""

    URL_TEMPLATE = 'https://www.guerrillamail.com/'

    _root_locator = (By.ID, 'guerrilla_mail')
    _mail_locator = (By.CLASS_NAME, 'mail_row')
    _compose_locator = (By.CSS_SELECTOR, '[title=Compose]')

    def wait_for_page_to_load(self):
        """Override page load."""
        self.wait.until(
            lambda _: self.find_element(*self._root_locator).is_displayed())

    def wait_for_email(self):
        """Wait for more than one email in inbox."""
        n = len(self.emails)
        self.wait.until(lambda _: len(self.emails) > n)

    @property
    def header(self):
        """Return the e-mail control panel."""
        return self.Header(self)

    @property
    def emails(self):
        """Return the e-mail inbox."""
        return [self.Emails(self, el)
                for el in self.find_elements(*self._mail_locator)]

    @property
    def compose(self):
        """Return a composition page."""
        self.find_element(*self._compose_locator).click()
        return Compose(self.driver)

    @property
    def openedmail(self):
        """Return a opened email region."""
        return self.OpenedMail(self)

    class Header(Region):
        """E-mail address controls."""

        _root_locator = (By.CLASS_NAME, 'show_address')
        _address_id_locator = (By.ID, 'inbox-id')
        _address_id_edit_locator = (By.CSS_SELECTOR, '#inbox-id [type]')
        _save_button_locator = (By.CSS_SELECTOR, '.save.button')
        _cancel_button_locator = (By.ID, 'edit-cancel')
        _address_stem_locator = (By.ID, 'gm-host-select')
        _forget_address_locator = (By.ID, 'forget_button')
        _email_locator = (By.ID, 'email-widget')
        _scramble_address_locator = (By.ID, 'use-alias')

        @property
        def is_header_displayed(self):
            """Header is displayed."""
            return self.loaded

        @property
        def is_scrambled(self):
            """Return True if the e-mail ID is scrambled."""
            return self.find_element(*self._scramble_address_locator) \
                .is_selected()

        def scramble(self):
            """Toggle between scrambled and unscrambled IDs."""
            self.find_element(*self._scramble_address_locator).click()
            return self

        @property
        def email(self):
            """Return the current e-mail."""
            return self.find_element(*self._email_locator).text

        @email.setter
        def email(self, new_id):
            """Change the email ID."""
            self.find_element(*self._address_id_locator).click()
            self.find_element(*self._address_id_edit_locator).clear()
            self.find_element(*self._address_id_edit_locator).send_keys(new_id)
            self.find_element(*self._save_button_locator).click()
            sleep(0.5)
            return self

        @property
        def host(self):
            """Host name suffix."""
            return Utility.selected_option(
                self.selenium,
                self._address_stem_locator)

        @host.setter
        def host(self, host_name):
            """Set a new host name."""
            Utility.select(self.selenium,
                           self._address_stem_locator,
                           host_name)
            return self

        def forget_address(self):
            """Purge the current e-mail."""
            self.find_element(*self._forget_address_locator).click()
            sleep(1.0)
            return self

    class Emails(Region):
        """E-mail inbox."""

        _subject_locator = (By.CLASS_NAME, 'td3')
        _excerpt_locator = (By.CLASS_NAME, 'email-excerpt')
        _emails_locator = (By.CSS_SELECTOR, 'tbody > tr')

        @property
        def subject(self):
            """Message subject."""
            return self.find_element(*self._subject_locator).text

        @property
        def excerpt(self):
            """Body excerpt."""
            return self.find_element(*self._excerpt_locator).text

        @property
        def has_pin(self):
            """Return True if a pin string is in the body excerpt."""
            return PIN_MATCHER.search(self.excerpt)

        @property
        def get_pin(self):
            """Return the numeric pin."""
            if self.has_pin:
                return (PIN_MATCHER.search(self.excerpt).group())[-6:]
            raise EmailVerificationError('No pin found')

        @property
        def is_new(self):
            """Short circuit timing for GuerrillaMail."""
            return True

        def open_email(self):
            """Open this email."""
            Utility.scroll_to(self.driver, self._subject_locator)
            sleep(4)
            self.find_element(*self._subject_locator).click()
            sleep(0.5)
            self.driver.refresh()

        def __unicode__(self):
            """Print out an email."""
            return ('Subject: {subject}\nExcerpt: {excerpt}'
                    ).format(self.subject, self.excerpt)

    class OpenedMail(Region):
        """The email page after it's opened."""

        _confirmation_link_locator = (By.CSS_SELECTOR, '.email_body a')

        def confirm_email(self):
            """Clicks the openstax email confirmation link."""
            Utility.switch_to(self.driver, self._confirmation_link_locator)


class Compose(GuerrillaMail):
    """Compose an e-mail."""

    URL_TEMPLATE = '/compose'

    _root_locator = (By.ID, 'send-form')
    _to_field_locator = (By.CSS_SELECTOR, '[name=to]')
    _subject_field_locator = (By.CSS_SELECTOR, '[name=subject]')
    _body_field_locator = (By.CSS_SELECTOR, '[name=body]')
    _send_button_locator = (By.ID, 'send-button')

    def wait_for_page_to_load(self):
        """Override page loading."""
        self.wait.until(
            lambda _: self.find_element(*self._root_locator).is_displayed())

    def send_message(self, to, subject, body):
        """Send an e-mail message from Guerrilla."""
        self.wait_for_page_to_load()
        sleep(0.5)
        to_box = self.find_element(*self._to_field_locator)
        to_box.click()
        to_box.clear()
        to_box.send_keys(to)
        subject_box = self.find_element(*self._subject_field_locator)
        subject_box.click()
        subject_box.clear()
        subject_box.send_keys(subject)
        body_box = self.find_element(*self._body_field_locator)
        body_box.click()
        body_box.clear()
        body_box.send_keys(body)
        self.find_element(*self._send_button_locator).click()
        sleep(1.0)
        return GuerrillaMail(self.selenium)


class RestMail(object):
    """RestMail API for non-interactive e-mail testing."""

    MAIL_URL = 'http://restmail.net/mail/{username}'

    def __init__(self, username):
        """Initialize a mailbox."""
        self._inbox = []
        self._username = username
        self._address = username + '@restmail.net'

    @property
    def user(self):
        """Return the box username."""
        return self._username

    @property
    def address(self):
        """Return the full email address."""
        return self._address

    @property
    def inbox(self):
        """Return the e-mail messages.

        Returns:
            The object list representing the inbox that may
            be empty if get_mail or wait_for_mail has not
            been called.

        """
        return self._inbox

    def get_mail(self):
        """Get email for a dynamic user.

        Returns:
            A list of Emails received for a particular user

        """
        messages = requests.get(self.MAIL_URL.format(username=self._username))
        self._inbox = [self.Email(message) for message in messages.json()]
        return self._inbox

    def wait_for_mail(self, max_time=60.0, pause_time=0.25):
        """Poll until mail is received but doesn't exceed max_time seconds.

        Args:
            max_time: maximum time to wait for emails
            pause_time: time between polling requests

        Returns:
            A list of Emails received for a particular user

        Raises:
            Timeout: after waiting the max time, no emails were received

        """
        timer = 0.0
        while timer <= (max_time / pause_time):
            self.get_mail()
            if self._inbox:
                return self._inbox
            timer = timer + pause_time
            sleep(pause_time)
        from requests.exceptions import Timeout
        raise Timeout('Mail not received in {time} seconds'
                      .format(time=max_time))

    @property
    def size(self):
        """Return the number of messages in the inbox."""
        return self._inbox.__len__

    def empty(self):
        """Delete all message in the inbox."""
        requests.delete(self.MAIL_URL.format(username=self._username))

    class Email(object):
        """E-mail message structure.

        Attributes:
            _html: HTML-formatted message body
            _text: plain text message body
            _headers: dict of email message headers
            _subject: email message subject
            _references: a list of additional message references
            _id: an internal message ID code
            _reply: a list of expected reply to email addresses
            _priority: message priority as indicated by the sender
            _from: a list of email message senders
            _to: a list of email message recipients
            _date: string-formed date and time when sent
            _received: string-formed date and time when received
            _received_at: string-formed date and time when received
            _excerpt: a blurb using the message body or the subject

        """

        def __init__(self, package):
            """Read possible RestMail fields."""
            self._html = self._pull_data('html', package, '')
            self._text = self._pull_data('text', package, '')
            self._headers = self._pull_data('headers', package, {})
            self._subject = self._pull_data('subject', package, '')
            self._references = self._pull_data('references', package, [])
            self._id = self._pull_data('messageId', package, '')
            self._reply = self._pull_data('inReplyTo', package, [])
            self._priority = self._pull_data('priority', package, '')
            self._from = self._pull_data('from', package, [])
            self._to = self._pull_data('to', package, [])
            self._date = self._pull_data('date', package, '')
            self._received = self._pull_data('receivedDate', package, '')
            self._received_at = self._pull_data('receivedAt', package, '')
            self._excerpt = (
                self._text if self._text else (
                    self._subject
                )
            )

        def _pull_data(self, field, package, default):
            """Pull data from the JSON package."""
            return package[field] if field in package else default

        @property
        def html(self):
            """Return the HTML formatted message body."""
            return self._html

        @property
        def text(self):
            """Return the unformatted message body."""
            return self._text

        @property
        def excerpt(self):
            """Return an excerpt from the HTML, text, or subject fields."""
            return self._excerpt

        @property
        def headers(self):
            """Return a dict of email headers."""
            return self._headers

        @property
        def subject(self):
            """Return the message subject."""
            return self._subject

        @property
        def id(self):
            """Return the message ID."""
            return self._id

        @property
        def priority(self):
            """Return the message priority."""
            return self._priority

        @property
        def sender(self):
            """Return the sender."""
            return self._from

        @property
        def recipients(self):
            """Return the list of recipients."""
            return self._to

        @property
        def date(self):
            """Return the UTC message date and time."""
            return self._date

        @property
        def received_on(self):
            """Return the message receive date."""
            return self._received

        @property
        def received_at(self):
            """Return the message receive time."""
            return self._received_at

        @property
        def has_pin(self):
            """Return True if a pin string is in the body excerpt."""
            return bool(PIN_MATCHER.search(self._excerpt))

        @property
        def pin(self):
            """Return the numeric pin."""
            if self.has_pin:
                return (PIN_MATCHER.search(self._excerpt).group())[-6:]
            raise EmailVerificationError('No pin found')

        @property
        def has_link(self):
            """Return True if a confirmation URL is in the excerpt."""
            return bool(URL_MATCHER.search(self._excerpt))

        @property
        def confirmation_link(self):
            """Access the confirmation URL link."""
            if self.has_link:
                return URL_MATCHER.search(self._excerpt).group()
            raise EmailVerificationError('No confirmation link found')

        def confirm_email(self):
            """Access the confirmation link."""
            send = requests.get(self.confirmation_link)
            if not send.status_code == requests.codes.ok:
                raise EmailVerificationError(
                    f'Email not confirmed. ({send.status_code})')

        @property
        def has_reset(self):
            """Return True if a password reset URL is in the excerpt."""
            return bool(RESET_MATCHER.search(self._excerpt))

        @property
        def reset_link(self):
            """Access the password reset URL link."""
            if self.has_reset:
                return RESET_MATCHER.search(self._excerpt).group()
            raise EmailVerificationError('No password reset link found')

        def submit_reset(self):
            """Access the reset link."""
            send = requests.get(self.reset_link)
            if not send.status_code == requests.codes.ok:
                raise EmailVerificationError(
                    'Reset link not successful. ({code})'
                    .format(code=send.status_code))


class SendMail(object):
    """Send an email through Gmail."""

    def __init__(self, username, password, host, port, timeout=10):
        """Initialize an email sender."""
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.timeout = timeout

    @contextmanager
    def _sender(self):
        """Start a relay for Gmail."""
        smtp_server = smtplib.SMTP(self.host, self.port, self.timeout)
        smtp_server.set_debuglevel(True)
        try:
            smtp_server.ehlo_or_helo_if_needed()
            smtp_server.starttls()
            smtp_server.ehlo(name='automated-qa.openstax.org')
            smtp_server.login(self.username, self.password)
            yield smtp_server
        finally:
            smtp_server.quit()
        sleep(3.0)

    def send_mail(self, recipients, sender, subject, message):
        """Send an email through Gmail."""
        with self._sender() as smtp:
            msg = MIMEText(message)
            msg['From'] = format_address(sender)
            msg['To'] = format_address(recipients)
            msg['Subject'] = subject
            smtp.send_message(msg=msg)


class EmailVerificationError(Exception):
    """General e-mail registration exception."""

    pass
