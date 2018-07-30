"""Test the Tutor Manage schools page."""

from tests.markers import skip_test, test_case, tutor


@test_case('C208715', 'C208716', 'C208717')
@skip_test(reason='Script not written')
@tutor
def test_add_edit_and_delete_a_new_school(tutor_base_url, selenium, admin):
    """Add, edit and delete a new school organization."""
    # GIVEN: a user logged in as an administrative user
    # AND: viewing the admin console Manage schools page

    # WHEN: they click the "Add school" button
    # AND: enter a school or organization name
    # AND: select the "QA-ISD" district from the District drop down menu
    # AND: click the "Save" button

    # THEN: the new school is added to the school list
    # AND: the "The school has been created." alert is displayed

    # WHEN: they click the "Add school" button
    # AND: enter the same school or organization name
    # AND: select the "QA-ISD" district from the District drop down menu
    # AND: click the "Save" button

    # THEN: the "Name has already been taken" alert is displayed
    # AND: the page does not change

    # WHEN: they go back to the Manage schools page
    # AND: click the "edit" button under Actions for the added course
    # AND: change the school "Name"
    # AND: click the "Save" button

    # THEN: the school name is updated in the school list
    # AND: the "The school has been updated." alert is displayed

    # WHEN: they click the "delete" link under Actions for the added course
    # AND: click the "OK" button in the alert box

    # THEN: the school is removed from the school list
    # AND: the "The school has been deleted." alert is displayed

    # WHEN: they click the "delete" link under Actions for the "Automation"
    #       course in the "QA-ISD" District
    # AND: click the "OK" button in the alert box

    # THEN: the school is not removed from the school list
    # AND: the "Cannot delete a school that has courses." error is displayed
