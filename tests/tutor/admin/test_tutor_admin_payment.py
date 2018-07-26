"""Test of admin console courses page."""

from tests.markers import expected_failure, nondestructive, test_case, tutor


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_extend_payment(tutor_base_url, selenium, admin):
    """Test admin to extend payment due dates."""
    # GIVEN: logged in as admin
    # AND: At the payments page

    # WHEN: Click on ""Extend Payment Due Dates""

    # THEN: Payment due dates are extended.
