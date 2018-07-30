"""Test the admin console Jobs page."""

from tests.markers import nondestructive, skip_test, test_case, tutor


@test_case('C210272')
@skip_test(reason='Script not written')
@nondestructive
@tutor
def test_view_jobs(tutor_base_url, selenium, admin):
    """Test admin to view jobs."""
    # GIVEN: a user logged in as an administrative user
    # AND: viewing the admin console Jobs page

    # WHEN: they click on a job ID

    # THEN: the job name, progress, and four date/times are shown
