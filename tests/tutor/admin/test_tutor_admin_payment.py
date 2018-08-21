"""Test of admin console courses page."""

from tests.markers import nondestructive, skip_test, test_case, tutor


@test_case('C210273')
@skip_test(reason='Script not written')
@nondestructive
@tutor
def test_extend_payment_due_dates_available(tutor_base_url, selenium, admin):
    """Test extending payment due dates.

    No extension is enabled - only the availability to
    perform the action is verified.
    """
    # GIVEN: a user logged in as an administrative user
    # AND: viewing the admin console Payments page

    # WHEN:

    # THEN: the "Extend Payment Due Dates" button is available
