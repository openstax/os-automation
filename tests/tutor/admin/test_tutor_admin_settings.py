"""Test the Tutor system settings."""

from tests.markers import skip_test, test_case, tutor


@test_case('C208736')
@skip_test(reason='Script not written')
@tutor
def test_tutor_admin_settings(tutor_base_url, selenium, admin):
    """Adjust Tutor system settings."""
    # GIVEN: an administrator logged in
    # AND: viewing the admin console settings page

    # WHEN: they edit the fields
    # AND: click the "Save All" button

    # TODO: clarify the fields available for edit

    # THEN: the settings are updated

    # WHEN: they edit the fields back to their original values
    # AND: click the "Save All" button

    # THEN: the settings are reverted
