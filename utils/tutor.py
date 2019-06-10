"""OpenStax Tutor Beta globals."""

from selenium.common.exceptions import WebDriverException


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


class Tutor(object):
    """Tutor shared variables."""

    # Assignment

    DUE_AT = 'only after due date/time passes'
    IMMEDIATE = 'instantly after the student answers each question'

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
