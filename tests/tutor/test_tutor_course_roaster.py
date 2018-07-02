"""Test of teacher on course roaster."""

from tests.markers import expected_failure, nondestructive, test_case, tutor


@expected_failure
@nondestructive
@test_case('')
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


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_change_student_section(tutor_base_url, selenium, teacher):
    """Test teacher to change a student's enrolled section."""
    # GIVEN: Logged into tutor as a teacher
    # AND: has a existing course
    # AND: has at least one student
    # AND: has two or more sections
    # AND: Select a Tutor course
    # AND: Click "course roster"

    # WHEN: Choose a student, click ""change section""

    # THEN: the student's section is changed

    # WHEN: The user resets the student's section

    # THEN: The student's section is reset


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_drop_a_student(tutor_base_url, selenium, teacher):
    """Test teacher to drop a student."""
    # GIVEN: Logged into tutor as a teacher
    # AND: has a existing course
    # AND: has at least one student
    # AND: Select a Tutor course
    # AND: Click "course roster"

    # WHEN: Click ""drop"" next to a students' name

    # THEN: the student should be removed from students' name
    # list and appear in dropped student section


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_readd_dropped_student(tutor_base_url, selenium, teacher):
    """Test teacher to readd a dropped student."""
    # GIVEN: Logged into tutor as a teacher
    # AND: has a existing course
    # AND: has at least one dropped student
    # AND: Select a Tutor course
    # AND: Click "course roster"

    # WHEN: Click ""add back to active roster""
    # next to a dropped student's name

    # THEN: student should be removed from "dropped student" section
    # and appear back at the student name list


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_remove_instructor(tutor_base_url, selenium, teacher):
    """Test teacher to remove an instructor."""
    # GIVEN: Logged into tutor as a teacher
    # AND: has a existing course
    # AND: has another instruction
    # AND: Select a Tutor course
    # AND: Click "course roster"

    # WHEN: Click ""remove"" next to another instructor's name

    # THEN: a remove button should appear


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_remove_oneself_from_instructor(tutor_base_url, selenium, teacher):
    """Test teacher to remove oneself from instructor."""
    # GIVEN: Logged into tutor as a teacher
    # AND: has a existing course
    # AND: Select a Tutor course
    # AND: Click "course roster"

    # WHEN: Click ""remove"" next to the name of the teacher itself

    # THEN: a remove button with the message "If user remove
    # User's self from the course user will be redirected to the dashboard."
    # should appeared
