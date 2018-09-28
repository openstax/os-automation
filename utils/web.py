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
    NO_FILTER = 'View All'
    PARTNERS = 'partners'
    RESEARCH = 'research'
    SUBJECTS = 'subjects'
    TECHNOLOGY = 'technology'
    TUTOR = 'openstax-tutor'

    # Menus
    VIEW_ALL = 'All'
    VIEW_MATH = 'Math'
    VIEW_SCIENCE = 'Science'
    VIEW_SOCIAL_SCIENCES = 'Social Sciences'
    VIEW_HUMANITIES = 'Humanities'
    VIEW_BUSINESS = 'Business'
    VIEW_AP = 'AP®'
    VIEW_TECHNOLOGY = 'Technology Options'
    VIEW_TUTOR = 'About OpenStax Tutor'
    VIEW_PARTNERS = 'OpenStax Partners'
    VIEW_ABOUT_US = 'About Us'
    VIEW_TEAM = 'Team'
    VIEW_RESEARCH = 'Research'

    # User types
    STUDENT = 'Student'
    INSTRUCTOR = 'Instructor'
    ADMINISTRATOR = 'Administrator'
    LIBRARIAN = 'Librarian'
    DESIGNER = 'Instructional Designer'
    HOMESCHOOL = 'Homeschool Instructor'
    ADJUNCT = 'Adjunct Faculty'
    OTHER = 'Other'

    # Expected lists
    ACCESSIBILITY = [
        'Accessibility',
        'Web Accessibility',
        'Our progress',
        'Feedback',
        'Interactive Simulations',
        'User-Contributed Content'
    ]
    URL_APPENDS = [
        'math',
        'science',
        'social-sciences',
        'humanities',
        'business',
        'ap'
    ]
    FILTERS = [
        VIEW_MATH,
        VIEW_SCIENCE,
        VIEW_SOCIAL_SCIENCES,
        VIEW_HUMANITIES,
        VIEW_BUSINESS,
        VIEW_AP
    ]
    MENU_SUBJECTS = [
        VIEW_ALL,
        *FILTERS
    ]
    MENU_TECHNOLOGY = [
        VIEW_TECHNOLOGY,
        VIEW_TUTOR,
        VIEW_PARTNERS
    ]
    MENU_WHAT_WE_DO = [
        VIEW_ABOUT_US,
        VIEW_TEAM,
        VIEW_RESEARCH
    ]
