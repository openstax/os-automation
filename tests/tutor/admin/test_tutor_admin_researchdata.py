"""Test of admin console research data page."""

from tests.markers import expected_failure, nondestructive, test_case, tutor


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_export_data(tutor_base_url, selenium, admin):
    """Test admin to export data."""
    # GIVEN: logged in as admin
    # AND: At the Resarch Data Page

    # WHEN:: Choose two dates (Start and end)
    # AND: Click the ""Export"" button

    # THEN: Data is successfully exported from the start and end dates
