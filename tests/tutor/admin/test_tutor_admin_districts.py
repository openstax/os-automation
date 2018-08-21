"""Test of admin console districts page."""

from tests.markers import skip_test, test_case, tutor


@test_case('C208718', 'C208719', 'C208720')
@skip_test(reason='Script not written')
@tutor
def test_managing_districts(tutor_base_url, selenium, admin):
    """Add, modify, than delete a new school district."""
    # GIVEN: a user logged in as an administrative user
    # AND: viewing the "Manage districts" page

    # WHEN: they click the "Add District" button
    # AND: fill out the district name
    # AND: click the "Save" button

    # THEN: the new district is added to the district list

    # WHEN: they click the "edit" button under Actions
    # AND: change the school district name
    # AND: click the "Save" button

    # THEN: the district is renamed

    # WHEN: they click the "delete" link under Actions of the "QA-ISD" district

    # THEN: an error "Cannot delete a district that has schools." is shown
    # AND: the district is not removed from the list

    # WHEN: they click the "delete" link under Actions of the new district

    # THEN: the district is deleted and removed from the list
