"""Test of admin console jobs page."""

from tests.markers import expected_failure, nondestructive, test_case, tutor


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_view_jobs(tutor_base_url, selenium, admin):
    """Test admin to view jobs."""
    # GIVEN: logged in as admin
    # AND: At the Tutor Admin Console

    # WHEN: Go to the Jobs page

    # THEN: List of jobs are loaded. Jobs can be filtered for
    # more specific searches.
