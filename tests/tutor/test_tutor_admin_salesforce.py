"""Test of admin console salesforce page."""

from tests.markers import expected_failure, nondestructive, test_case, tutor


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_set_salesforce_user(tutor_base_url, selenium, admin):
    """Test admin to set salesforce user."""
    # GIVEN: logged in as admin
    # AND: At the Salesforce page

    # WHEN: In the dropdown click on ""Setup""
    # AND: Click on ""Set Salesforce User""

    # THEN: Salesforce website login page is loaded


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_edit_settings(tutor_base_url, selenium, admin):
    """Test admin to edit settings."""
    # GIVEN: logged in as admin
    # AND: At the Salesforce page

    # WHEN: In the drop down click on ""Settings""
    # AND: Edit one or more fields in settings
    # AND: Click ""Save All""

    # THEN: Settings is successfully updated


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_update_salesforce(tutor_base_url, selenium, admin):
    """Test admin to update salesforce."""
    # GIVEN: logged in as admin
    # AND: At the Salesforce page

    # WHEN: In the dropdown click on ""Actions""
    # AND: Click on ""Update Salesforce""

    # THEN: Salesforce is updated.
