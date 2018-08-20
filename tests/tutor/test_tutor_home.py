"""Test the Tutor home page."""

from pages.tutor.home import TutorHome as Home
from tests.markers import expected_failure, nondestructive  # NOQA
from tests.markers import skip_test, test_case, tutor


@test_case('')
@nondestructive
@tutor
def test_open_home_page(tutor_base_url, selenium):
    """Test opening the Tutor home page."""
    page = Home(selenium, tutor_base_url).open()
    assert('tutor' in page.driver.current_url), 'Not at a Tutor page'


@test_case('')
@skip_test(reason='Script not written')
@nondestructive
@tutor
def test_tutor_home_page(tutor_base_url, selenium):
    """Test the tutor home page."""
    # GIVEN: A web browser

    # WHEN: Go to the Tutor home page

    # THEN: The Tutor home page loads


@test_case('')
@skip_test(reason='Script not written')
@nondestructive
@tutor
def test_sales_force_support_page(tutor_base_url, selenium):
    """Test the salesforce support page."""
    # GIVEN: The Tutor home page

    # WHEN: The user clicks "Help" link in the header

    # THEN: The Salesforce Tutor support page loads


@test_case('')
@skip_test(reason='Script not written')
@nondestructive
@tutor
def test_accounts_log_in_page(tutor_base_url, selenium):
    """Test the accounts log in page."""
    # GIVEN: The Tutor home page

    # WHEN: The user clicks "LOG IN" button

    # THEN: The Accounts log in page loads
    # AND: "tutor" is in the URL


@test_case('')
@skip_test(reason='Script not written')
@nondestructive
@tutor
def test_crest_rice_home_page(tutor_base_url, selenium):
    """Test the rice home page using crest."""
    # GIVEN: The Tutor home page

    # WHEN: The user clicks the Rice logo

    # THEN: The Rice home page loads


@test_case('')
@skip_test(reason='Script not written')
@nondestructive
@tutor
def test_footer_rice_home_page(tutor_base_url, selenium):
    """Test the rice home page using footer."""
    # GIVEN: The Tutor home page

    # WHEN: The user clicks "Rice University"

    # THEN: The Rice home page


@test_case('')
@skip_test(reason='Script not written')
@nondestructive
@tutor
def test_tutor_term_page(tutor_base_url, selenium):
    """Test the tutor term page."""
    # GIVEN: The Tutor home page

    # WHEN: The user clicks "Terms" link

    # THEN: The Terms page loads
