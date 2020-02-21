"""Accounts helper."""

from typing import Tuple

from selenium.common.exceptions import WebDriverException

from utils.utilities import Utility

Name = Tuple[str, str, str, str]
Selector = Tuple[str, str]


class Accounts(object):
    """Accounts shared variables."""

    accounts_old = True

    ASCENDING = 'ASC'
    DESCENDING = 'DESC'

    FIRST_NAME = 'first_name'
    ID = 'id'
    LAST_NAME = 'last_name'
    ROLE = 'role'
    USERNAME = 'username'

    # Select menu options
    COLLEGE = 'College'
    CONFIRMED = 'Confirmed faculty'
    NO_INFO = 'No faculty info'
    OTHER = 'Other school type'
    PENDING = 'Pending faculty'
    REJECTED = 'Rejected faculty'
    UNKNOWN = 'Unknown school type'

    STUDENT = 'Student'
    INSTRUCTOR = 'Instructor'
    ADMINISTRATOR = 'Administrator'
    LIBRARIAN = 'Librarian'
    DESIGNER = 'Instructional Designer'
    OTHER = 'Other'

    FACEBOOK = 'facebook'
    GOOGLE = 'google'
    GUERRILLA_MAIL = 'guerrilla'
    RESTMAIL = 'restmail'

    TITLE = 0
    FIRST = 1
    LAST = 2
    SUFFIX = 3

    ADOPTED = 'Fully adopted and using it as the primary textbook'
    RECOMMENDED = 'Recommending the book – my students buy a different book'
    INTEREST = 'Interested in using OpenStax in the future'
    NOT_USING = 'Not using openstax'

    USE = [ADOPTED, RECOMMENDED, INTEREST]

    @classmethod
    def randomized_use(cls):
        """Return a random book use."""
        return Accounts.USE[Utility.random(0, len(Accounts.USE) - 1)]

    SUBJECTS = [
        ('algebra_and_trigonometry', 'Algebra and Trigonometry'),
        ('american_government', 'American Government'),
        ('anatomy_physiology', 'Anatomy & Physiology'),
        ('astronomy', 'Astronomy'),
        ('biology', 'Biology'),
        ('ap_bio', 'AP Biology'),
        ('calculus', 'Calculus'),
        ('chemistry', 'Chemistry'),
        ('chem_atoms_first', 'Chemistry: Atoms First'),
        ('college_algebra', 'College Algebra'),
        ('college_physics_algebra_', 'College Physics'),
        ('concepts_of_bio_non_majors', 'Concepts of Biology'),
        ('elementary_algebra', 'Elementary Algebra'),
        ('intermediate_algebra', 'Intermediate Algebra'),
        ('introduction_to_sociology', 'Introduction to Sociology 2e'),
        ('introductory_statistics', 'Introductory Statistics'),
        ('business_statistics', 'Introductory Business Statistics'),
        ('microbiology', 'Microbiology'),
        ('prealgebra', 'Prealgebra'),
        ('precalc', 'Precalculus'),
        ('economics', 'Principles of Economics'),
        ('macro_econ', 'Principles of Macroeconomics'),
        ('ap_macro_econ', 'AP Macro Econ'),
        ('micro_econ', 'Principles of Microeconomics'),
        ('ap_micro_econ', 'AP Micro Econ'),
        ('psychology', 'Psychology'),
        ('ap_physics', 'AP Physics'),
        ('us_history', 'U.S. History'),
        ('university_physics_calc_', 'University Physics')
    ]

    @classmethod
    def get_book_code(cls, book_title):
        """Return the short code for a book title."""
        for code, title in Accounts.SUBJECTS:
            if title == book_title:
                return code


class AccountsException(WebDriverException):
    """A generic exception for Accounts."""

    pass
