"""OpenStax Web globals."""

import re


class Web(object):
    """Website shared variables."""

    # RegEx matchers
    FILENAME_MATCHER = re.compile(r'url\([\w\-\:\/\.]*\)\;')

    # Web banner carousel options
    FREE_BOOKS_NO_CATCH = 0
    EDUCATION_OVER_PROFIT = 1
    ACADEMIC_FREEDOM = 2
    _29_BOOKS = 3

    # Quotes
    SUBSCRIBE = 0
    BOOK_QUALITY_RIGGS = 1
    BOOKSTORE_SUPPLIERS = 2

    # Matching strings
    ABOUT = 'about'
    BOOKSTORE = 'bookstore-suppliers'
    GIVE = 'give'
    IMPACT = 'impact'
    NEWSLETTER = 'www2.openstax.org'
    PARTNERS = 'partners'
    RESEARCH = 'research'
    SUBJECTS = 'subjects'
    TECHNOLOGY = 'technology'
    TUTOR = 'openstax-tutor'
    VIEW_ALL = 'View All'
    VIEW_MATH = 'Math'
    VIEW_SCIENCE = 'Science'
    VIEW_SOCIAL_SCIENCES = 'Social Sciences'
    VIEW_HUMANITIES = 'Humanities'
    VIEW_BUSINESS = 'Business'
    VIEW_AP = 'AP®'

    # User types
    STUDENT = 'Student'
    INSTRUCTOR = 'Instructor'
    ADMINISTRATOR = 'Administrator'
    LIBRARIAN = 'Librarian'
    DESIGNER = 'Instructional Designer'
    HOMESCHOOL = 'Homeschool Instructor'
    ADJUNCT = 'Adjunct Faculty'
    OTHER = 'Other'

    ACCESSIBILITY = [
        'Accessibility',
        'Web Accessibility',
        'Our progress',
        'Feedback',
        'Interactive Simulations',
        'User-Contributed Content'
    ]
