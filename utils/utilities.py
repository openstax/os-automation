"""Helper functions for OpenStax Pages."""

from http.client import responses
from platform import system
from random import randint
from time import sleep
from warnings import warn

import requests
from faker import Faker
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, StaleElementReferenceException, TimeoutException, WebDriverException  # NOQA
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.support.color import Color
from selenium.webdriver.support.ui import Select, WebDriverWait

JAVASCRIPT_CLICK = 'arguments[0].click()'
OPEN_TAB = 'window.open();'
SCROLL_INTO_VIEW = 'arguments[0].scrollIntoView();'
SHIFT_VIEW_BY = 'window.scrollBy(0, arguments[0])'

JQUERY = 'https://code.jquery.com/jquery-3.3.1.slim.min.js'
WAIT_FOR_IMAGE = ('https://cdnjs.cloudflare.com/ajax/libs/'
                  'jquery.waitforimages/1.5.0/jquery.waitforimages.min.js')

STATE_PROV = [
    ('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'),
    ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'),
    ('CT', 'Connecticut'), ('DE', 'Delaware'), ('FL', 'Florida'),
    ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'),
    ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'),
    ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'),
    ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'),
    ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MO', 'Missouri'),
    ('MS', 'Mississippi'), ('MT', 'Montana'), ('NE', 'Nebraska'),
    ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'),
    ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'),
    ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'),
    ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'),
    ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'),
    ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'),
    ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'),
    ('WY', 'Wyoming'), ('AS', 'American Samoa'),
    ('DC', 'District of Columbia'), ('FM', 'Federated States of Micronesia'),
    ('GU', 'Guam'), ('MP', 'Northern Mariana Islands'), ('PW', 'Palau'),
    ('PR', 'Puerto Rico'), ('VI', 'Virgin Islands'),
    ('AA', 'Armed Forces Americas'), ('AE', 'Armed Forces Europe'),
    ('AP', 'Armed Forces Pacific'), ('AB', 'Alberta'),
    ('BC', 'British Columbia'), ('MB', 'Manitoba'), ('NB', 'New Brunswick'),
    ('NF', 'Newfoundland'), ('NT', 'Northwest Territories'),
    ('NS', 'Nova Scotia'), ('ON', 'Ontario'), ('PE', 'Prince Edward Island'),
    ('PQ', 'Province du Quebec'), ('SK', 'Saskatchewan'),
    ('YT', 'Yukon Territory')
]


class Utility(object):
    """Helper functions for various Pages actions."""

    HEX_DIGITS = '0123456789ABCDEF'

    @classmethod
    def clear_field(cls, driver, field=None, field_locator=None):
        """Clear the contents of text-type fields."""
        sleep(0.1)
        if not field:
            field = driver.find_element(*field_locator)
        if driver.name == 'chrome':
            field.clear()
        elif driver.name == 'firefox':
            special = Keys.COMMAND if system() == 'Darwin' else Keys.CONTROL
            ActionChains(driver) \
                .click(field) \
                .key_down(special) \
                .send_keys('a') \
                .key_up(special) \
                .send_keys(Keys.DELETE) \
                .perform()

    @classmethod
    def close_tab(cls, driver):
        """Close the current tab and switch to the other tab."""
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    @classmethod
    def compare_colors(cls, left, right):
        """Return True if two RGB color strings match."""
        return Color.from_string(left) == Color.from_string(right)

    @classmethod
    def fake_email(cls, first_name, surname, id=False):
        """Return a name-based fake email."""
        template = ('{first}.{second}.{random}@restmail.net')
        return template.format(
            first=first_name,
            second=surname,
            random=id if id else Utility.random_hex(6)
        ).lower()

    @classmethod
    def fast_multiselect(cls, driver, element_locator, labels):
        """Select menu multiselect options.

        Daniel Abel multiselect
        'https://sqa.stackexchange.com/questions/1355/
        what-is-the-correct-way-to-select-an-option-using-seleniums-
        python-webdriver#answer-2258'
        """
        menu = driver.find_element(*element_locator)
        Utility.scroll_to(driver, element=menu)
        select = Select(menu)
        for label in labels:
            select.select_by_visible_text(label)
        return select

    @classmethod
    def get_error_information(cls, error):
        """Break up an assertion error object."""
        short = str(error.getrepr(style='short'))
        info = short.split('AssertionError: ')[-1:][0]
        return info.replace("'", '').replace('{', '').replace('}', '')

    @classmethod
    def get_test_credit_card(cls, card=None, status=None):
        """Return a random card number and CVV for test transactions."""
        braintree = Card()
        _card = card if card else Status.VISA
        _status = status if status else Status.VALID
        test_cards = braintree.get_by(Status.STATUS, _status)
        test_cards = braintree.get_by(Status.TYPE, _card, test_cards)
        select = randint(0, len(test_cards) - 1)
        use_card = test_cards[select]
        return (use_card['number'], use_card['cvv'])

    @classmethod
    def has_children(cls, element):
        """Return True if a specific element has one or more children."""
        return len(element.find_elements('xpath', './*')) > 0

    @classmethod
    def has_height(cls, driver, locator):
        """Return True if the computed height isn't 'auto'."""
        auto = ('return window.getComputedStyle('
                'document.querySelector("{selector}")).height!="auto"'
                ).format(selector=locator)
        return driver.execute_script(auto)

    @classmethod
    def in_viewport(cls, driver, locator=None, element=None,
                    ignore_bottom=False, display_marks=True):
        """Return True if the element boundry completely lies in view."""
        LEFT, TOP, RIGHT, BOTTOM = range(4)
        target = element if element else driver.find_element(*locator)
        rect = driver.execute_script(
            'return arguments[0].getBoundingClientRect();', target)
        if display_marks:
            print('Rectangle: {0}'.format(rect))
        page_x_offset = driver.execute_script('return window.pageXOffset;')
        page_y_offset = driver.execute_script('return window.pageYOffset;')
        target_boundry = (
            rect.get('left') + page_x_offset,
            rect.get('top') + page_y_offset,
            rect.get('right') + page_x_offset,
            rect.get('bottom') + page_y_offset)
        window_width = driver.execute_script(
            'return document.documentElement.clientWidth;')
        window_height = driver.execute_script(
            'return document.documentElement.clientHeight;')
        page_boundry = (
            page_x_offset,
            page_y_offset,
            page_x_offset + window_width,
            page_y_offset + window_height)
        if display_marks:
            base = '{side} {result} - Element ({element}) {sign} Page ({page})'
            bottom = (
                'Bottom {result} - [Element ({element}) {sign} '
                'Page ({page})] or [Skip Bottom ({skip})]')
            print(base.format(
                side='Left', sign='>=', page=page_boundry[LEFT],
                result=target_boundry[LEFT] >= page_boundry[LEFT],
                element=target_boundry[LEFT]))
            print(base.format(
                side='Top', sign='>=', page=page_boundry[TOP],
                result=target_boundry[TOP] >= page_boundry[TOP],
                element=target_boundry[TOP]))
            print(base.format(
                side='Right', sign='<=', page=page_boundry[RIGHT],
                result=target_boundry[RIGHT] <= page_boundry[RIGHT],
                element=target_boundry[RIGHT]))
            print(bottom.format(
                sign='<=', page=page_boundry[BOTTOM],
                result=(
                    target_boundry[BOTTOM] <= page_boundry[BOTTOM] or
                    ignore_bottom),
                element=target_boundry[BOTTOM], skip=ignore_bottom))
        return (
            target_boundry[LEFT] >= page_boundry[LEFT] and
            target_boundry[TOP] >= page_boundry[TOP] and
            target_boundry[RIGHT] <= page_boundry[RIGHT] and
            (target_boundry[BOTTOM] <= page_boundry[BOTTOM] or
             ignore_bottom))

    @classmethod
    def is_image_visible(cls, driver, image=None, locator=None):
        """Return True if an image is rendered."""
        if image:
            image_group = image if isinstance(image, list) else [image]
        else:
            image_group = driver.find_elements(*locator)
            auto = ('return window.getComputedStyle('
                    'arguments[0]).height!="auto"')
            image_group = list(filter(
                lambda img: driver.execute_script(auto, img),
                image_group))
        ie = 'internet explorer'
        from selenium.webdriver import Ie
        if (isinstance(driver, Ie) or
                driver.capabilities.get('browserName') == ie):
            script = 'return arguments[0].complete'
        else:
            script = (
                'return ((typeof arguments[0].naturalWidth)!="undefined")')
        from functools import reduce
        map_list = (list(map(
            lambda img: driver.execute_script(script, img), image_group)))
        return reduce(lambda img, group: img and group, map_list, True)

    @classmethod
    def load_background_images(cls, driver, locator):
        """Inject a script to wait for background image downloads.

        Return True when complete so it can be used in loaded methods.
        """
        inject = (
            r'''
            ;(function() {
                var head = document.getElementsByTagName("head")[0];
                var jquery = document.createElement("script");
                jquery.src = "JQUERY_STRING";
                jquery.onload = function() {
                    var $ = window.jQuery;
                    var head = document.getElementsByTagName("head")[0];
                    var image = document.createElement("script");
                    image.src = "IMAGE_STRING";
                    image.type = "text/javascript";
                    head.appendChild(image);
                    $("SELECTOR").waitForImages().done(
                        function() { return true; });
                };
                head.appendChild(jquery);
            });
            return true;
            '''
            .replace('JQUERY_STRING', JQUERY)
            .replace('IMAGE_STRING', WAIT_FOR_IMAGE)
            .replace('SELECTOR', locator[1])
        )
        return driver.execute_script(inject)

    @classmethod
    def new_tab(cls, driver):
        """Open another browser tab."""
        driver.execute_script(OPEN_TAB)
        sleep(1)
        return driver.window_handles

    @classmethod
    def random(cls, start=0, end=100000):
        """Return a random integer from start to end."""
        if start >= end:
            return start
        return randint(start, end)

    @classmethod
    def random_address(cls, string=False):
        """Return a fake mailing address."""
        fake = Faker()
        address = ['', '', '', '']
        use_abrev = randint(0, 1)
        address[0] = fake.street_address()
        address[1] = fake.city()
        address[2] = STATE_PROV[randint(0, len(STATE_PROV) - 1)][use_abrev]
        address[3] = fake.postcode().split('-')[0]
        return address

    @classmethod
    def random_hex(cls, length=20, lower=False):
        """Return a random hex number of size length."""
        line = ''.join([Utility.HEX_DIGITS[randint(0, 0xF)]
                       for _ in range(length)])
        return line if not lower else line.lower()

    @classmethod
    def random_name(cls, is_male=None, is_female=None):
        """Generate a random name list for Accounts users."""
        fake = Faker()
        name = ['', '', '', '']
        if is_female:
            use_male_functions = False
        elif is_male:
            use_male_functions = True
        else:
            use_male_functions = randint(0, 2) == 0
        has_prefix = randint(0, 10) >= 6
        has_suffix = randint(0, 10) >= 8

        if has_prefix:
            name[0] = fake.prefix_male() if use_male_functions else \
                fake.prefix_female()
        name[1] = fake.first_name_male() if use_male_functions else \
            fake.first_name_female()
        name[2] = fake.last_name()
        if has_suffix:
            name[3] = fake.suffix_male() if use_male_functions else \
                fake.suffix_female()
        return name

    @classmethod
    def random_phone(cls, area_code=713, number_only=True):
        """Return a random phone number."""
        template = ('{area}5550{local}' if number_only else
                    '({area}) 555-0{local}')
        return template.format(area=area_code, local=randint(100, 199))

    @classmethod
    def random_set(cls, group, size=1):
        """Return a unique set from a list."""
        if size <= 0:
            return []
        if size >= len(group):
            return group
        new_set = []
        while len(new_set) < size:
            selected = group[Utility.random(0, len(group) - 1)]
            if selected not in new_set:
                new_set.append(selected)
        return new_set

    @classmethod
    def safari_exception_click(cls, driver, locator=None, element=None,
                               force_js_click=False):
        """Click on elements which cause Safari 500 errors."""
        element = element if element else driver.find_element(*locator)
        Utility.scroll_to(driver=driver, element=element, shift=-80)
        sleep(0.5)
        try:
            if force_js_click:
                raise WebDriverException('Bypassing the driver-defined click')
            element.click()
        except WebDriverException:
            for _ in range(10):
                try:
                    driver.execute_script(JAVASCRIPT_CLICK, element)
                    break
                except ElementClickInterceptedException:  # Firefox issues
                    sleep(1.0)
                except NoSuchElementException:  # Safari issues
                    if locator:
                        element = driver.find_element(*locator)
                except StaleElementReferenceException:  # Chrome and Firefox
                    if locator:
                        element = driver.find_element(*locator)

    @classmethod
    def scroll_bottom(cls, driver):
        """Scroll to the bottom of the browser screen."""
        driver.execute_script(
            'window.scrollTo(0, document.body.scrollHeight);')
        sleep(0.75)

    @classmethod
    def scroll_to(
            cls, driver, element_locator=None, element=None, shift=0):
        """Scroll the screen to the element.

        Args:
            driver (webdriver): the selenium browser object
            element_locator (Tuple(str, str)): a By selector and locator
            element (WebElement): a specific element
            shift (int): adjust the page vertically by a set number of pixels
                > 0 scrolls down, < 0 scrolls up

        """
        target = element if element else driver.find_element(*element_locator)
        driver.execute_script(SCROLL_INTO_VIEW, target)
        if shift != 0:
            driver.execute_script(SHIFT_VIEW_BY, shift)

    @classmethod
    def scroll_top(cls, driver):
        """Scroll to the top of the browser screen."""
        driver.execute_script('window.scrollTo(0, 0);')
        sleep(0.75)

    @classmethod
    def select(cls, driver, element_locator, label):
        """Select an Option from a menu."""
        return Utility.fast_multiselect(driver, element_locator, [label])

    @classmethod
    def selected_option(cls, driver, element_locator):
        """Return the currently selected option."""
        return Select(driver.find_element(*element_locator)) \
            .first_selected_option \
            .text

    @classmethod
    def switch_to(cls, driver, link_locator=None, element=None, action=None,
                  force_js_click=False):
        """Switch to the other window handle."""
        current = driver.current_window_handle
        data = None
        if not action:
            Utility.safari_exception_click(driver=driver,
                                           locator=link_locator,
                                           element=element,
                                           force_js_click=force_js_click)
        else:
            data = action()
        sleep(1)
        new_handle = 1 if current == driver.window_handles[0] else 0
        if len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[new_handle])
        if data:
            return data

    @classmethod
    def test_url_and_warn(cls, _head=True, code=None, url=None, link=None,
                          message='', driver=None):
        """Query a URL and return a warning if the code is not a success."""
        if driver:
            browser = driver.capabilities.get('browserName', '').lower()
        agent = {
            'chrome': {
                'User-Agent': (
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1)'
                    ' AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/70.0.3538.110 Safari/537.36'), },
            'firefox': {
                'User-Agent': (
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14;'
                    ' rv:64.0) Gecko/20100101 Firefox/64.0'), },
            'safari': {
                'User-Agent': (
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1)'
                    ' AppleWebKit/605.1.15 (KHTML, like Gecko)'
                    ' Version/12.0.1 Safari/605.1.15'), },
            '': {},
        }
        if link:
            url = link.get_attribute('href')
        test = requests.head(url) if _head \
            else requests.get(url, headers=agent.get(browser))
        code = test.status_code
        if code == 403 and _head:
            _head = False
            test = requests.get(url, headers=agent.get(browser))
            code = test.status_code
        if code == 503 or \
                'Error from cloudfront' in test.headers.get('X-Cache', ''):
            for _ in range(20):
                sleep(3)
                test = requests.head(url) if _head \
                    else requests.get(url, headers=agent.get(browser))
                code = test.status_code
                if code != 503:
                    break
        if code >= 400:
            # the test ran into a problem with the URL query
            status = ('<{code} {reason}>'
                      .format(code=code, reason=responses.get(code)))
            warn(UserWarning(
                '"{article}" returned a {status}'
                .format(article=message, status=status)))
            if 'Error from cloudfront' in test.headers.get('X-Cache', ''):
                return True
            return False
        return True

    @classmethod
    def wait_for_overlay(cls, driver, locator):
        """Wait for an overlay to clear making the target available."""
        WebDriverWait(driver, 15).until(
            expect.element_to_be_clickable(locator))
        sleep(1.0)

    @classmethod
    def wait_for_overlay_then(cls, target, time=10.0, interval=0.5):
        """Wait for an overlay to clear then performing the target action."""
        for _ in range(int(time / interval)):
            try:
                target()
                break
            except WebDriverException:
                sleep(interval)
        sleep(1.0)


class Card(object):
    """Fake card objects."""

    def __init__(self):
        """Retrieve card numbers from BTP."""
        import requests
        from bs4 import BeautifulSoup

        braintree = (
            'https://developers.braintreepayments.com/'
            'reference/general/testing/python'
        )
        section_list_selector = 'table:nth-of-type({position}) tbody tr'
        response = requests.get(braintree)
        if response.status_code != requests.codes.ok:
            response.raise_for_status()
        resp = BeautifulSoup(response.text, 'html.parser')
        self.options = []

        for card_status in range(Status.VALID, Status.OTHER + 1):
            for card in resp.select(
                    section_list_selector.format(position=card_status)):
                fields = card.select('td')
                card_processor = (Status.VISA
                                  if fields[0].text[0] == '4'
                                  else fields[1].text)
                if card_processor == Status.AMEX:
                    cvv = '{:04}'.format(randint(0, 9999))
                else:
                    cvv = '{:03}'.format(randint(0, 999))
                rest = fields[2].text if len(fields) > 2 else ''
                data = fields[1].text if card_status == Status.OTHER or  \
                    card_status == Status.TYPED else ''
                self.options.append({
                    'number': fields[0].text,
                    'cvv': cvv,
                    'type': card_processor,
                    'status': card_status,
                    'response': rest,
                    'data': data,
                })

    def get_by(self, field=None, state=None, use_list=None):
        """Return a subset of test cards with a specific type."""
        _field = field if field else Status.STATUS
        _state = state if state else Status.VALID
        _use_list = use_list if use_list else self.options
        return list(
            filter(
                lambda card: card[_field] == _state,
                _use_list
            )
        )


class Status(object):
    """Card states."""

    STATUS = 'status'
    VALID = 2
    NO_VERIFY = 3
    TYPED = 4
    OTHER = 5

    TYPE = 'type'
    AMEX = 'American Express'
    DINERS = 'Diners Club'
    DISCOVER = 'Discover'
    JCB = 'JCB'
    MAESTRO = 'Maestro'
    MC = 'Mastercard'
    VISA = 'Visa'

    RESPONSE = 'response'
    DECLINED = 'processor declined'
    FAILED = 'failed (3000)'


def go_to_(destination):
    """Follow a destination link and wait for the page to load."""
    return go_to_external_(destination)


def go_to_external_(destination, url=None):
    """Follow an external destination link repeatedly waiting for page load."""
    if url:
        for _ in range(2):
            try:
                destination.wait_for_page_to_load()
                return destination
            except TimeoutException:
                destination.driver.get(url)
                sleep(1)
    try:
        destination.wait_for_page_to_load()
        return destination
    except TimeoutException:
        raise TimeoutException('{0} did not load ({1})'
                               .format(type(destination).__name__, url))


class Actions(ActionChains):
    """Add a javascript retrieval action and a data return perform."""

    def get_js_data(self, css_selector=None, data_type=None, expected=None,
                    element=None, new_script=None):
        """Trigger a style lookup."""
        if element:
            self._actions.append(
                lambda: self.data_read(element=element,
                                       data_type=data_type,
                                       expected=expected))
        elif new_script:
            self._actions.append(
                lambda: self.data_read(new_script=new_script,
                                       element=element,
                                       expected=expected))
        else:
            self._actions.append(
                lambda: self.data_read(css_selector=css_selector,
                                       data_type=data_type,
                                       expected=expected))
        result = None
        if self._driver.w3c:
            try:
                self.w3c_actions.perform()
            except TypeError:
                pass
            if element:
                result = self.data_read(element=element,
                                        data_type=data_type,
                                        expected=expected)
            elif new_script:
                result = self.data_read(new_script=new_script,
                                        element=element,
                                        expected=expected)
            else:
                result = self.data_read(css_selector=css_selector,
                                        data_type=data_type,
                                        expected=expected)
        else:
            for action in self._actions:
                result = action()
        sleep(1)
        return result

    def data_read(self, css_selector=None, data_type=None, expected=None,
                  element=None, new_script=None):
        """Compare the script return to an expected value."""
        if new_script:
            script = new_script
        elif element:
            script = (
                'return window.getComputedStyle(arguments[0])["{data_type}"]'
            ).format(data_type=data_type)
        else:
            script = (
                'return window.getComputedStyle(document.querySelector'
                '("{selector}"))["{data_type}"]'
            ).format(selector=css_selector, data_type=data_type)
        val = self._driver.execute_script(script, element)
        print(val, expected, val == expected)
        return [val == expected, val, expected]

    def wait(self, seconds: float):
        """Sleep for a specified number of seconds within an ActionChain."""
        self._actions.append(lambda: sleep(seconds))
        return self
