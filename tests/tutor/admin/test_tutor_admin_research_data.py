"""Test of admin console research data page."""

from tests.markers import nondestructive, skip_test, test_case, tutor


@test_case('C208734')
@skip_test(reason='Script not written')
@nondestructive
@tutor
def test_export_research_data(tutor_base_url, selenium, admin):
    """Export research data to Box."""
    # GIVEN: a user logged in as an administrative user
    # AND: viewing the admin console Research Data page

    # WHEN: a "From:" date is selected
    # AND: a "To:" date is selected
    # AND: "Include Tutor" is checked
    # AND: "Include Concept Coach" is not checked
    # AND: the "Export Data" button is clicked

    # THEN: the data export is successfully sent to Box
