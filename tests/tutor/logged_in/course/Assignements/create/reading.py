"""Test case for tutor reading assignment as teacher."""

from tests.markers import expected_failure, test_case, tutor


@test_case('')
@expected_failure
@tutor
def test_add_reading(tutor_base_url, selenium, teacher):
    """Test the adding reading assignment."""
    # GIVEN: Logged into Tutor as a teacher

    # AND: Has an existing course

    # WHEN: The user clicks on one of the courses

    # AND:  Click on a date on the dashboard

    # AND: Click "add reading"

    # AND: Fill in all the required fields

    # AND: Click "Publish"

    # THEN: Dashboard of that course is successfully loaded and the
    # reading assignment is visible on the calendar


@test_case('')
@expected_failure
@tutor
def test_adding_reading_draft(tutor_base_url, selenium, teacher):
    """Test adding the reading draft to dashboard."""
    # GIVEN: Logged into Tutor as a teacher

    # AND: Has an existing course

    # WHEN: The user clicks on one of the courses

    # AND:  Click on a date on the dashboard

    # AND: Click "add reading"

    # AND: Fill in all the required fields

    # AND: Click "Save as draft"

    # THEN: Dashboard of that course is successfully loaded

    # AND the reading assignment draft is visible on the calendar


@test_case('')
@expected_failure
@tutor
def test_edit_published_reading(tutor_base_url, selenium, teacher):
    """Test editting the published reading."""
    # GIVEN: Logged into Tutor as a teacher

    # AND: Has an existing course

    # AND: Has a publish reading

    # WHEN: The user clicks on the course

    # AND: Click on the published reading

    # AND: Edit one of the required fields

    # AND: Click "Publish"

    # THEN: Dashboard of that course is successfully loaded and the
    # reading assignment with edits is visible on the calendar


@test_case('')
@expected_failure
@tutor
def test_publish_reading_draft(tutor_base_url, selenium, teacher):
    """Test editting the reading draft and publish."""
    # GIVEN: Logged into Tutor as a teacher

    # AND: Has an existing course

    # AND: Has a reading draft

    # WHEN: The user clicks on the course

    # AND: Click on the reading draft on calendar

    # AND: Edit one of the required fields

    # AND: Click "Publish"

    # THEN: Dashboard of that course is successfully loaded and
    # the reading assignment with edits is visible on the calendar


@test_case('')
@expected_failure
@tutor
def test_cancel_reading_edits(tutor_base_url, selenium, teacher):
    """Test cancelling reading assignments edits."""
    # GIVEN: Logged into Tutor as a teacher

    # AND: Has an existing course

    # AND: Has a publish reading

    # WHEN: The user clicks on the course

    # AND: Click on the published reading on calendar

    # AND: Edit the required fields

    # AND: Click "Cancel"

    # THEN: The changes made on the reading assignment is not saved


@test_case('')
@expected_failure
@tutor
def test_cancel_reading_draft(tutor_base_url, selenium, teacher):
    """Test cancelling reading draft edits."""
    # GIVEN: Logged into Tutor as a teacher

    # AND: Has an existing course

    # AND: Has a reading draft

    # WHEN:  The user clicks on the course

    # AND: Click on the reading draft

    # AND: Edit the required fields

    # AND: Click "Cancel"

    # THEN: The changes made on the reading draft is not saved


@test_case('')
@expected_failure
@tutor
def test_delete_published_reading(tutor_base_url, selenium, teacher):
    """Test the deleting the published reading."""
    # GIVEN: Logged into Tutor as a teacher

    # AND: Has an existing course

    # AND: Has a publish reading

    # WHEN: The user clicks on the course

    # AND: Click on the reading

    # AND: Click "Delete"

    # THEN: The reading is deleted.


@test_case('')
@expected_failure
@tutor
def test_delete_reading_draft(tutor_base_url, selenium, teacher):
    """Test deleting the reading draft."""
    # GIVEN: Logged into Tutor as a teacher

    # AND: Has an existing course

    # AND: Has a reading draft

    # WHEN:  The user clicks on the course

    # AND: Click on the reading draft

    # AND: Click "Delete"

    # THEN: The reading draft is deleted.


@test_case('')
@expected_failure
@tutor
def test_see_what_student_see(tutor_base_url, selenium, teacher):
    """Test the see what student see button."""
    # GIVEN: Logged into Tutor as a teacher

    # AND: Has an existing course

    # AND: Has a reading or homework assignment

    # WHEN: The user goes to a homework/reading assignment

    # AND: Edit it

    # THEN: "see what students see" button should be available
