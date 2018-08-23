"""Test case for external assignment interaction and activities."""

from tests.markers import skip_test, test_case, tutor


@test_case('C208517')
@skip_test(reason='Script not written')
@tutor
def test_external_assignment_page(tutor_base_url, selenium, student):
    """Test the external assignment."""
    # GIVEN: Logged on Tutor as a student
    # AND: Has enrolled in a course
    # AND: Has a external assignment

    # WHEN: The user clicks on the external assignment from the dashboard

    # THEN: User should be presented with details of the external assignment


@test_case('C208518')
@skip_test(reason='Script not written')
@tutor
def test_external_assignment_direction(tutor_base_url, selenium, student):
    """Test the external assignment direction."""
    # GIVEN: Logged on Tutor as a student
    # AND: Has enrolled in a course
    # AND: Has a external assignment

    # WHEN: The user clicks on the external assignment from the dashboard
    # AND: The user points to the info icon

    # THEN: User is presented with the directions for the assignment


@test_case('C208519')
@skip_test(reason='Script not written')
@tutor
def test_external_assignment_under_tab(tutor_base_url, selenium, student):
    """Test the external assignment through the tab on dashboard."""
    # GIVEN: Logged into Tutor as a student
    # AND: Has enrolled in a course
    # AND:  Has an external assignement

    # WHEN: The user clicks on an external assignment under the tab "This Week"
    #       on the dashboard
    # AND: The user clicks on the link to the external assignment

    # THEN: External assignment page loads


@test_case('C208520')
@skip_test(reason='Script not written')
@tutor
def test_external_assignment_instruction(tutor_base_url, selenium, student):
    """Test the external assignment instructions."""
    # GIVEN: Logged into Tutor as a student
    # AND: Has enrolled in a course
    # AND: Has an external assignement

    # WHEN: The user clicks on an external assignment

    # THEN: The external assignment link and instructions are shown


@test_case('C208521')
@skip_test(reason='Script not written')
@tutor
def test_clicked_external_assignment(tutor_base_url, selenium, student):
    """Test the link of external assignment."""
    # GIVEN: Logged into Tutor as a student
    # AND: Has enrolled in a course
    # AND: Has an external assignement

    # WHEN: The user clicks on the link to the external assignment
    # AND: The user closes the assignement tab
    # AND: The user clicks "Back to Dashboard"

    # THEN: The assignment is marked as "clicked" on the dashboard
