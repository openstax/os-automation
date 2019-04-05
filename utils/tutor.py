"""OpenStax Tutor Beta globals."""

from selenium.common.exceptions import WebDriverException


class Tutor(object):
    """Tutor shared variables."""

    # Course Page

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


class TutorException(WebDriverException):
    """A generic exception for Tutor."""

    pass
