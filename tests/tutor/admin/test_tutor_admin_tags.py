"""Test of admin console tags page."""

from tests.markers import nondestructive, skip_test, test_case, tutor


@test_case('C208721')
@skip_test(reason='Script not written')
@nondestructive
@tutor
def test_search_for_tags(tutor_base_url, selenium, admin):
    """Search for a valid tag and an invalid tag."""
    # GIVEN: a user logged in as an administrative user
    # AND: viewing the admin console Tags page

    # WHEN: they enter "aplo" in the "Search here" input
    # AND: click the "Search" button

    # THEN: there are search results containing "aplo"
    # AND: each entry may have a "Name" and "Edit" button
    # AND: the results are paginated

    # WHEN: they enter eight random hex digits
    # AND: click the "Search" button

    # THEN: the "No tags found." message is displayed
