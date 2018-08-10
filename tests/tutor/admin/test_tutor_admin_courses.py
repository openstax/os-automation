"""Test of admin console courses page."""

from tests.markers import nondestructive, skip_test, test_case, tutor


@test_case('C208712')
@skip_test(reason='Script not written')
@tutor
def test_edit_an_existing_course(tutor_base_url, selenium, admin):
    """Edit an existing course's settings."""
    # GIVEN: a user logged in as an administrative user
    # AND: at the Tutor admin console

    # WHEN: the admin clicks on "Course Organization"
    # AND: selects "Courses" from the drop down menu
    # AND: clicks the "Edit" button in a course entry
    # AND: changes the course fields
    # AND: clicks the "Save" button

    # THEN: the changes are saved

    # WHEN: the admin reverts the changes
    # AND: clicks the "Save" button

    # THEN: the course settings are restored


@test_case('C208711')
@skip_test(reason='Script not written')
@nondestructive
@tutor
def test_view_students_in_a_course(tutor_base_url, selenium, admin):
    """View the students enrolled in a course."""
    # GIVEN: a user logged in as an administrative user
    # AND: viewing the admin console Courses page

    # WHEN: the they click the "List Students" button

    # THEN: a list of all enrolled students is displayed


@test_case('C208713')
@skip_test(reason='Not tested using automation')
@tutor
def test_add_a_new_course(tutor_base_url, selenium, admin):
    """Administratively add add a new course."""
    # GIVEN: a user logged in as an administrative user
    # AND: viewing the admin console Courses page

    # WHEN: they click the "Add Course" button
    # AND: fill in the fields
    # AND: clicks the "Save" button

    # THEN: a new course is added
    # AND: the course is listed on the last Courses page


@test_case('')
@skip_test(reason='Script not written')
@tutor
def test_view_the_other_courses_tabs(tutor_base_url, selenium, admin):
    """View the incomplete and failed jobs tabs."""
    # GIVEN: a user logged in as an administrative user
    # AND: viewing the admin console Courses page

    # WHEN: they click the "Incomplete Bulk Ecosystem Update Jobs" link

    # THEN: the incomplete bulk update job log is displayed

    # WHEN: they click the "Failed Bulk Ecosystem Update Jobs" link
    # AND: click on a "Job ID"

    # THEN: the job name and error for the course is shown
