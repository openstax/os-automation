"""Test the Tutor home page."""
import pytest
from pytest_testrail.plugin import pytestrail

from pages.tutor.home import TutorHome as Home


@pytestrail.case('')
@pytest.mark.nondestructive
def test_open_home_page(base_url, selenium):
    """Test opening the Tutor home page."""
    page = Home(selenium, base_url).open()
    assert('tutor' in page.driver.current_url), 'Not at a Tutor page'
