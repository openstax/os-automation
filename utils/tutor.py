"""OpenStax Tutor Beta globals."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Tuple, Union

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By

from utils.utilities import Utility

DateFormat = Union[Tuple[str, str], datetime]
FullDateTime = Tuple[DateFormat, DateFormat]
Webdriver = Union[webdriver.Chrome, webdriver.Firefox, webdriver.Safari]


class States(object):
    """Valid purchase form districts, states and territories."""

    ALABAMA = 'Alabama'
    ALASKA = 'Alaska'
    AMERICAN_SAMOA = 'American Samoa'
    ARIZONA = 'Arizona'
    ARKANSAS = 'Arkansas'
    CALIFORNIA = 'California'
    COLORADO = 'Colorado'
    CONNECTICUT = 'Connecticut'
    DELAWARE = 'Delaware'
    DISTRICT_OF_COLUMBIA = 'District Of Columbia'
    FLORIDA = 'Florida'
    GEORGIA = 'Georgia'
    GUAM = 'Guam'
    HAWAII = 'Hawaii'
    IDAHO = 'Idaho'
    ILLINOIS = 'Illinois'
    INDIANA = 'Indiana'
    IOWA = 'Iowa'
    KANSAS = 'Kansas'
    KENTUCKY = 'Kentucky'
    LOUISIANA = 'Louisiana'
    MAINE = 'Maine'
    MARYLAND = 'Maryland'
    MASSACHUSETTS = 'Massachusetts'
    MICHIGAN = 'Michigan'
    MINNESOTA = 'Minnesota'
    MISSISSIPPI = 'Mississippi'
    MISSOURI = 'Missouri'
    MONTANA = 'Montana'
    NEBRASKA = 'Nebraska'
    NEVADA = 'Nevada'
    NEW_HAMPSHIRE = 'New Hampshire'
    NEW_JERSEY = 'New Jersey'
    NEW_MEXICO = 'New Mexico'
    NEW_YORK = 'New York'
    NORTH_CAROLINA = 'North Carolina'
    NORTH_DAKOTA = 'North Dakota'
    NORTHERN_MARIANA_ISLANDS = 'Northern Mariana Islands'
    OHIO = 'Ohio'
    OKLAHOMA = 'Oklahoma'
    OREGON = 'Oregon'
    PENNSYLVANIA = 'Pennsylvania'
    PUERTO_RICO = 'Puerto Rico'
    RHODE_ISLAND = 'Rhode Island'
    SOUTH_CAROLINA = 'South Carolina'
    SOUTH_DAKOTA = 'South Dakota'
    TENNESSEE = 'Tennessee'
    TEXAS = 'Texas'
    UTAH = 'Utah'
    VERMONT = 'Vermont'
    VIRGIN_ISLANDS = 'Virgin Islands'
    VIRGINIA = 'Virginia'
    WASHINGTON = 'Washington'
    WEST_VIRGINIA = 'West Virginia'
    WISCONSIN = 'Wisconsin'
    WYOMING = 'Wyoming'

    abbreviation = {
        'AL': ALABAMA, 'AK': ALASKA, 'AS': AMERICAN_SAMOA, 'AZ': ARIZONA,
        'AR': ARKANSAS,
        'CA': CALIFORNIA, 'CO': COLORADO, 'CT': CONNECTICUT,
        'DE': DELAWARE, 'DC': DISTRICT_OF_COLUMBIA,
        'FL': FLORIDA,
        'GA': GEORGIA, 'GU': GUAM,
        'HI': HAWAII,
        'ID': IDAHO, 'IL': ILLINOIS, 'IN': INDIANA, 'IA': IOWA,
        'KS': KANSAS, 'KY': KENTUCKY,
        'LA': LOUISIANA,
        'ME': MAINE, 'MD': MARYLAND, 'MA': MASSACHUSETTS, 'MI': MICHIGAN,
        'MN': MINNESOTA, 'MS': MISSISSIPPI, 'MO': MISSOURI, 'MT': MONTANA,
        'NE': NEBRASKA, 'NV': NEVADA, 'NH': NEW_HAMPSHIRE, 'NJ': NEW_JERSEY,
        'NM': NEW_MEXICO, 'NY': NEW_YORK, 'NC': NORTH_CAROLINA,
        'ND': NORTH_DAKOTA, 'MP': NORTHERN_MARIANA_ISLANDS,
        'OH': OHIO, 'OK': OKLAHOMA, 'OR': OREGON,
        'PA': PENNSYLVANIA, 'PR': PUERTO_RICO,
        'RI': RHODE_ISLAND,
        'SC': SOUTH_CAROLINA, 'SD': SOUTH_DAKOTA,
        'TN': TENNESSEE, 'TX': TEXAS,
        'UT': UTAH,
        'VT': VERMONT, 'VI': VIRGIN_ISLANDS, 'VA': VIRGINIA,
        'WA': WASHINGTON, 'WV': WEST_VIRGINIA, 'WI': WISCONSIN, 'WY': WYOMING,
    }

    @classmethod
    def from_abbreviation(cls, abbreviation: str) -> str:
        """Return the full state name from its abbreviation.

        .. note:

            Return Texas if a non-OpenStax Tutor Beta available location is
            requested (ie Canadian provinces)

        :param str abbreviation: the 2-character abbreviation for the state or
            U.S. territory
        :return: the full name for the state or territory
        :rtype: str

        """
        if len(abbreviation) > 2:
            if abbreviation not in cls.abbreviation.values():
                return cls.TEXAS
            return abbreviation
        try:
            return cls.abbreviation[abbreviation]
        except KeyError:
            return cls.TEXAS


class Tutor(object):
    """Tutor shared variables."""

    # Assignment

    ALL = 'all'
    CANCEL = 'Cancel'
    DELETE = 'delete'
    DRAFT = 'Save as Draft'
    DUE_AT = 'only after due date/time passes'
    IMMEDIATE = 'instantly after the student answers each question'
    PUBLISH = 'Publish'
    RANDOM = 'random'
    SAVE = 'Save'
    STAGGER = 'stagger-dates'
    TODAY = 'today'

    # Calendar

    AFTER_TERM = 'after-term'
    BEFORE_TERM = 'before-term'
    IN_FUTURE = 'upcoming'
    IN_PAST = 'past'
    IN_TERM = 'in-term'
    TODAY = 'today'

    # Course Creation
    AP_BIOLOGY = 'Biology For AP® Courses'
    AP_PHYSICS = 'College Physics for AP® Courses'
    APUSH = 'AP® U.S. History'
    BIOLOGY = 'Biology 2e'
    PHYSICS = 'College Physics'
    SOCIOLOGY = 'Introduction to Sociology 2e'

    BOOKS = [BIOLOGY, PHYSICS, SOCIOLOGY]

    FALL = 'Fall'
    SPRING = 'Spring'
    SUMMER = 'Summer'
    WINTER = 'Winter'

    TERMS = [SPRING, SUMMER, FALL, WINTER]

    # Course Settings

    STUDENT_ACCESS = 0
    DATES_AND_TIME = 1

    START_DATE = 1
    END_DATE = 3

    ALASKA = 'Alaska'
    ARIZONA = 'Arizona'
    ATLANTIC = 'Atlantic Time (Canada)'
    CENTRAL_TIME = 'Central Time (US & Canada)'
    EASTERN_TIME = 'Eastern Time (US & Canada)'
    HAWAII = 'Hawaii'
    INDIANA = 'Indiana (East)'
    MOUNTAIN_TIME = 'Mountain Time (US & Canada)'
    PACIFIC_TIME = 'Pacific Time (US & Canada)'

    TIMEZONE = [HAWAII, ALASKA, PACIFIC_TIME, ARIZONA, MOUNTAIN_TIME,
                CENTRAL_TIME, EASTERN_TIME, INDIANA, ATLANTIC]

    # Course Page

    EMAIL = 'email'
    END_OF_COURSE = 'course-has-ended'
    STUDENT_ID = 'missing-student-id'
    SYSTEM = 'system'

    EVENT = 'event'
    EXTERNAL = 'external'
    HOMEWORK = 'homework'
    READING = 'reading'
    ASSIGNMENTS = [EVENT, EXTERNAL, HOMEWORK, READING]

    ON_TIME = 'On time'
    DUE_SOON = 'Due soon'
    LATE = 'Late'
    ACCEPTED_LATE = 'Late but accepted'

    LATE_COLOR = '#c2002f'
    ACCEPTED_COLOR = '#6f6f6f'

    # Dashboard

    BY_APPEARANCE = 'by appearance'
    BY_ID = 'by id'
    BY_SUBJECT = 'by subject'
    BY_TERM = 'by term'
    BY_TITLE = 'by title'
    BY_TYPE = 'by type'

    IS_PREVIEW = 'is preview'
    IS_TEACHER = 'is teacher'

    # Enrollment
    ADDRESS = 0
    CITY = 1
    STATE = 2
    ZIP = 3

    @classmethod
    def states(cls):
        """Return the district, state, and territory options.

        Any changes to `~utils.tutor.States` will always be reflected in
        :py:classmethod:`~utils.tutor.Tutor.states`.
        :py:method:`~inspect.getmembers` returns a list of name/value tuples.

        >>> States.ALABAMA in Tutor.states()
        True
        >>> 'Alabama' in Tutor.states()
        True
        >>> 'alabama' in Tutor.states()
        False

        :return: a list of state strings available to the course purchase page
        :rtype: list(str)

        """
        from inspect import getmembers, isroutine
        return list([
            state[1]
            for state
            in getmembers(States, lambda member: not(isroutine(member)))
            if not(state[0].startswith('__') and state[0].endswith('__'))])

    # Scores
    ASCENDING = 'is-ascending'
    DESCENDING = 'is-descending'
    NO_SORT = 'no sort'

    AS_NUMBER = 'number'
    AS_PERCENTAGE = 'percentage'

    # Tasks
    CORE = 'core assessment'
    CORRECT = 'correct answer'
    END_CARD = 'assignment complete'
    EXERCISE = 'exercise'
    INCORRECT = 'incorrect answer'
    NOT_A_QUESTION = 'not a question step'
    NOT_ANSWERED = 'assessment not answered'
    NOT_GRADED = 'not graded'
    PERSONALIZED = 'personalized assessment'
    REVIEW_CARD = 'review card step'
    SPACED_PRACTICE = 'spaced practice assessment'


class TutorException(WebDriverException):
    """A generic exception for Tutor."""

    pass


def to_date_time_string(to_format: Union[str, DateFormat]) -> Tuple[str, str]:
    """Split the date and time.

    :param to_format: the date or date/time to format
    :type to_format: str or tuple(str, str) or datetime
    :return: the date and time formatted as strings for a Tutor assignment
    :rtype: tuple(str, str)

    """
    # Handle plain date or date/time strings
    if isinstance(to_format, str):
        try:
            date, time = to_format.split()
        except ValueError:
            date = to_format
            time = ''
    # Split date/time string tuples
    elif isinstance(to_format, tuple):
        date, time = to_format
    # Format datetime entries
    elif isinstance(to_format, datetime):
        date, time = (
            to_format.strftime('%m/%d/%Y %I:%M%p')
            .lower()
            [:-1]
            .split())
    else:
        raise TutorException(f'Unknown date time format: "{to_format}"')

    # Fix some time prefixes that the form widget can't handle well
    if not time.startswith('01') and time.startswith('0'):
        time = time[1:]
    elif time.startswith('1:'):
        time = f'0{time}'

    return (date, time)


def get_date_times(driver: Webdriver,
                   option: Union[str, DateFormat, FullDateTime]) \
        -> Tuple[str]:
    """Return Tutor-ready date and time strings.

    Take various formats of dates and times for assignment open/due
    requirements and return Tutor ``send_key``-ready strings.

    :param option: the requested date/time option for a section
    :type option:
        str or
        tuple(str, str) or
        tuple(tuple(str, str), tuple(str, str)) or
        datetime or
        tuple(datetime, datetime)
    :return: the list of values (open date, open time, due date, due time); if
        a time is not needed the time field will be an empty string
    :rtype: tuple(str)

    """
    # Handle a random date in the future or today
    if option == Tutor.RANDOM:
        base_date = driver.find_element(
            By.CSS_SELECTOR,
            '.-assignment-open-date input:not([readonly])')
        _open = datetime.strptime(
            '{date} {time}'.format(
                date=base_date.get_attribute('value'),
                time='12:01 am'),
            '%m/%d/%Y %I:%M %p')
        _open = _open + timedelta(days=Utility.random(0, 7),
                                  minutes=Utility.random(0, 60 * 24 - 2))
        _due = _open + timedelta(days=Utility.random(1, 7),
                                 minutes=Utility.random(0, 60 * 24))
        option = (_open, _due)
    elif option == Tutor.TODAY:
        # open now
        option = datetime.now()

    # Change from a single option to open and due values
    if isinstance(option, datetime):
        open_on = option
        # Set a random end date if one wasn't included
        due_on = option + timedelta(days=Utility.random(1, 7))
    else:
        open_on, due_on = option

    open_on, open_at = to_date_time_string(open_on)
    due_on, due_at = to_date_time_string(due_on)

    return (open_on, open_at, due_on, due_at)
