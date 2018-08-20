"""Test of admin console salesforce page."""

from tests.markers import skip_test, test_case, tutor


@test_case('C208735')
@skip_test(reason='Not tested using automation')
@tutor
def test_tutor_salesforce_settings(tutor_base_url, selenium, admin):
    """Adjust salesforce settings."""
    # GIVEN: a user logged in as an administrative user
    # AND: viewing the admin console Salesforce Setup page

    # WHEN: they click the "Clear Salesforce User" button

    # THEN: there "is no Salesforce user" set

    # WHEN: they click the "Set Salesforce User" button
    # AND: log into Salesforce

    # THEN: the Salesforce user is set


@test_case('C210275')
@skip_test(reason='Not applicable to the current iteration of Tutor')
@tutor
def test_update_salesforce_stats(tutor_base_url, selenium, admin):
    """Update Salesforce statistics."""
    # GIVEN: a user logged in as an administrative user
    # AND: viewing the admin console Salesforce Actions page

    # WHEN: they click the "Update Salesforce" button

    # THEN: new course data is submitted to Salesforce
