"""Test the Tutor home page."""

from pages.tutor.home import TutorHome as Home
from tests.markers import nondestructive, test_case, tutor


@test_case('')
@nondestructive
@tutor
def test_open_home_page(tutor_base_url, selenium):
    """Test opening the Tutor home page."""
    page = Home(selenium, tutor_base_url).open()
    assert('tutor' in page.driver.current_url), 'Not at a Tutor page'
