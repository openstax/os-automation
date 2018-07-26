"""Test of admin console main page."""

from tests.markers import skip_test, nondestructive, test_case, tutor


@test_case('C208708')
@skip_test(reason='Script not written')
@nondestructive
@tutor
def test_navbar_elements_present(tutor_base_url, selenium, admin):
    """Verify admin console navbar elements are present."""
    # GIVEN: Logged in as admin
    # AND: At the Tutor admin console

    # WHEN:

    # THEN: User is able to see the navbar with the following elements:
    #       "Tutor Admin Console", "Course Organization", "Content",
    #       "Legal", "Stats", "Users", "Job", "Payments", "Research Data",
    #       "Salesforce", "System Setting".
