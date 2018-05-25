"""Break the signup process out of the base."""
from selenium.webdriver.common.by import By

from pages.accounts.base import AccountsBase


class Signup(AccountsBase):
    """Signup process."""

    URL_TEMPLATE = '/signup'

    _signup_role_locator = (By.ID, 'signup_role')
    _signup_role_options_locator = (By.CSS_SELECTOR, '#signup_role option')
    _signup_email_locator = (By.ID, 'signup_email')
    _next_button_locator = (By.CSS_SELECTOR, '[type=submit]')
    _log_in_locator = (By.CSS_SELECTOR, '.footer a')

    def account_signup(self, email, password, _type='student', **kwargs):
        """Single signup entry point.

        Sign up a new user. Social, Random, and Name are mutually exclusive.

        Args:
            email (str): An accessible e-mail address
            password (str): A user password
            _type (:obj:`str`, optional): New user account type -
                student, instructor, administrator, librarian,
                instructional designer, other
                default: student
            **kwargs: Arbitrary keyword arguments
                'news': (bool) checked or unchecked
                    default: True
                'name': user name fields
                    [title (str), first_name (str),
                     last_name (str), suffix(str)]
                'social': (str): Use a social login -
                    facebook, google
                'phone': (str) instructor phone number
                'school': (str) school name
                'students': (int) number of course students
                'webpage': (str) web URL for an individual
                'subjects': ([str]) list of subject interest -
                    accounting, algebra_and_trigonometry, american_government,
                    anatomy_physiology, astronomy, biology, calculus,
                    chemistry, chem_atoms_first, college_algebra,
                    college_physics_algebra, concepts_of_bio_non_majors,
                    introduction_to_sociology, introductory_statistics,
                    microbiology, pre_algebra, precalc, economics, macro_econ,
                    ap_macro_econ, micro_econ, ap_micro_econ, psychology,
                    ap_physics, us_history, university_physics_calc, not_listed

        Return:
            page.accounts.Profile: new user profile page
        """
        if _type == 'student':
            get_news = kwargs.get('news') if 'news' in kwargs else True
            if 'social' in kwargs:
                return self._student_signup_social(
                    social=kwargs.get('social'),
                    email=email,
                    password=password,
                    news=get_news)
            return self._student_signup(
                name=kwargs.get('name'),
                email=email,
                password=password,
                news=get_news)
        if 'social' in kwargs:
            return self._elevated_signup_social(
                _type=_type,
                email=email,
                password=password,
                kwargs=kwargs)
        return self._elevated_signup(
            _type=_type,
            email=email,
            password=password,
            kwargs=kwargs)

    def _student_signup(self, name, email, password, news):
        """Student signup."""
        return EmailVerification(self.driver)

    def _student_signup_social(self, social, email, password, news):
        """Student signup using social media."""
        return StandardProfile(self.driver)

    def _elevated_signup(self, _type, email, password, **kwargs):
        """Non-student signup."""
        return SocialProfile(self.driver)

    def _elevated_signup_social(self, _type, email, password, **kwargs):
        """Non-student signup using social media."""
        return Facebook(self.driver)


class EmailVerification(Signup):
    """Verify the signup e-mail."""

    URL_TEMPLATE = '/verfy_email'


class Password(Signup):
    """Set the initial user password."""

    URL_TEMPLATE = '/password'


class StandardProfile(Signup):
    """Setup the initial profile."""

    URL_TEMPLATE = '/profile'


class SocialProfile(Signup):
    """Setup a social profile."""

    URL_TEMPLATE = '/social'


class Facebook(SocialProfile):
    """Use a Facebook profile."""


class Goggle(SocialProfile):
    """Use a Google profile."""
