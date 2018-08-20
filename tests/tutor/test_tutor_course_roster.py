"""Test the Tutor teacher course roster functions."""

from tests.markers import nondestructive, skip_test, test_case, tutor


@test_case('')
@skip_test(reason='Script not written')
@tutor
def test_edit_student_id(tutor_base_url, selenium, teacher):
    """Test teacher to edit student ID."""
    # GIVEN: A logged in teacher user
    # AND: has a existing course
    # AND: has at least one student

    # WHEN: Select a Tutor course
    # AND: Click "course roster"
    # AND: Edit student ID by clicking on the little
    # pencil sign near student id

    # THEN: the student's id is edited

    # WHEN: The user resets the student's id

    # THEN: The student's id is reset


@test_case('')
@skip_test(reason='Script not written')
@tutor
def test_change_student_section(tutor_base_url, selenium, teacher):
    """Test teacher to change a student's enrolled section."""
    # GIVEN: Logged into tutor as a teacher
    # AND: has a existing course
    # AND: has at least one student
    # AND: has two or more sections

    # WHEN: Select a Tutor course
    # AND: Click "course roster"
    # AND: Choose a student, click "change section"

    # THEN: the student's section is changed

    # WHEN: The user resets the student's section

    # THEN: The student's section is reset


@test_case('')
@skip_test(reason='Script not written')
@tutor
def test_drop_a_student(tutor_base_url, selenium, teacher):
    """Test teacher to drop a student."""
    # GIVEN: Logged into tutor as a teacher
    # AND: has a existing course
    # AND: has at least one student

    # WHEN: Select a Tutor course
    # AND: Click "course roster"
    # AND: Click "drop" next to a students' name

    # THEN: the student should be removed from students' name
    #       list and appear in dropped student section


@test_case('')
@skip_test(reason='Script not written')
@tutor
def test_readd_dropped_student(tutor_base_url, selenium, teacher):
    """Test teacher to readd a dropped student."""
    # GIVEN: Logged into tutor as a teacher
    # AND: has a existing course
    # AND: has at least one dropped student

    # WHEN: Select a Tutor course
    # AND: Click "course roster"
    # AND: Click "add back to active roster"
    # next to a dropped student's name

    # THEN: student should be removed from "dropped student" section
    #       and appear back at the student name list


@test_case('')
@skip_test(reason='Script not written')
@tutor
def test_remove_instructor(tutor_base_url, selenium, teacher):
    """Test teacher to remove an instructor."""
    # GIVEN: Logged into tutor as a teacher
    # AND: has a existing course
    # AND: has another instruction

    # WHEN: Select a Tutor course
    # AND: Click "course roster"
    # AND: Click "remove" next to another instructor's name

    # THEN: a remove button should appear


@test_case('')
@skip_test(reason='Script not written')
@tutor
def test_remove_oneself_from_instructor(tutor_base_url, selenium, teacher):
    """Test teacher to remove oneself from instructor."""
    # GIVEN: Logged into tutor as a teacher
    # AND: has a existing course

    # WHEN: Select a Tutor course
    # AND: Click "course roster"
    # AND: Click "remove" next to the name of the teacher itself

    # THEN: a remove button with the message "If user remove
    #       User's self from the course user will be redirected
    #       to the dashboard." should appeared


@test_case('')
@skip_test(reason='Script not written')
@tutor
def test_add_a_new_section(tutor_base_url, selenium, teacher):
    """Add a new section in course roster."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: User is at the "Course Roster" page

    # WHEN: Click "add a section"
    # AND: Enter a section name, click enter

    # THEN: A new section should appear


@test_case('')
@skip_test(reason='Script not written')
@tutor
def test_add_a_new_instructor(tutor_base_url, selenium, teacher):
    """Add a new instruction in course roster."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: User is at the "Course Roster" page

    # WHEN: Click "add a new instructor"
    # AND: Add instructor name, click enter

    # THEN: A url link that instructor could use to join this course is shown


@test_case('')
@skip_test(reason='Script not written')
@tutor
def test_rename_a_section(tutor_base_url, selenium, teacher):
    """Rename a section in course roster."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: User is at the "Course Roster" page

    # WHEN: Click "rename"
    # AND: Type in new name, click enter

    # THEN: Section is renamed


@test_case('')
@skip_test(reason='Script not written')
@tutor
def test_delete_a_section(tutor_base_url, selenium, teacher):
    """Delete a section in course roster."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: User is at the "Course Roster" page

    # WHEN: Click "delete section"
    # AND: Click "yes"

    # THEN: the section is deleted


@test_case('')
@skip_test(reason='Script not written')
@nondestructive
@tutor
def test_cancel_delete_a_section(tutor_base_url, selenium, teacher):
    """Cancel deleting a section in course roster."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: User is at the "Course Roster" page

    # WHEN: Click "delete a section"
    # AND: Click "cancel"

    # THEN: The section should not be deleted


@test_case('')
@skip_test(reason='Script not written')
@nondestructive
@tutor
def test_cancel_renaming_a_section(tutor_base_url, selenium, teacher):
    """Cancel renaming a section in course roster."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: User is at the "Course Roster" page

    # WHEN: Click "rename a section"
    # AND: Click "cancel"

    # THEN: The section name should not change
