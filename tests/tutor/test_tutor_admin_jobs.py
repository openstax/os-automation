"""Test of admin console jobs page."""

from tests.markers import expected_failure, nondestructive, test_case, tutor


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_view_jobs(tutor_base_url, selenium, admin):
    """Test admin to view jobs."""
    # GIVEN: logged in as admin

    # WHEN: Go to Tutor admin console
    # AND: Click on ""Jobs"" in the navbar

    # THEN: List of jobs are loaded. Jobs can be filtered for
    # more specific searches.
