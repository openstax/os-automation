"""Test the Tutor teacher question library functions."""

from tests.markers import expected_failure, nondestructive, test_case, tutor


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_review_all_questions(tutor_base_url, selenium, teacher):
    """View questions in question library."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: Click "Question Library" from the user menu
    # AND: Select a section or chapter
    # AND: Click "Show Questions"

    # THEN: The user is presented with all the questions for the chapter


@expected_failure
@test_case('')
@tutor
def test_exclude_certain_questions(tutor_base_url, selenium, teacher):
    """Exclude certain questions in question library."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: Click "Question Library" from the user menu
    # AND: Select a section or chapter
    # AND: Click "Show Questions"
    # AND: Hover over the desired question and click "Exclude question"

    # THEN: Question is excluded


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_switch_between_reading_and_homework_questions(
        tutor_base_url, selenium, teacher):
    """Switch to view reading and homework questions in question library."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: Click "Question Library" from the user menu
    # AND: Select a section or chapter
    # AND: Click "Show Questions"
    # AND: Click on the "Reading" tab

    # THEN: Exercises that are only for Reading appear


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_question_library_pinned_tab(tutor_base_url, selenium, teacher):
    """Check the pinned tab to the top of the screen in question library."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: Click "Question Library" from the user menu
    # AND: Select a section or chapter
    # AND: Click "Show Questions"
    # AND: Scroll down

    # THEN: Tabs are pinned to the top of the screen when scrolled


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_browse_corresponding_chapter_in_the_book(tutor_base_url, selenium,
                                                  teacher):
    """Browse questions of a certain chapter in question library."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: Click "menu"
    # AND: Click "question library"
    # AND: Click "browse this chapter"

    # THEN: content of the chapter user choose is displayed


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_section_in_question_library(tutor_base_url, selenium, teacher):
    """Jump between chapters with breadcrumbs in question library."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: Click "menu"
    # AND: Click "question library"
    # AND: Choose a section besides the intro chapter
    # AND: Choose sections from top left side of page

    # THEN: When a subchapter number is clicked on, the book shows the content
    # of the subchapter user've chosen"


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_go_to_question_details(tutor_base_url, selenium, teacher):
    """Go to question details page in question library."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: Click "menu"
    # AND: Click "question library"
    # AND: Click on a chapter besides intro
    # AND: Click "question details"

    # THEN: Question details page are shown


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_report_errata_about_questions(tutor_base_url, selenium, teacher):
    """Report a errata for a question in question library."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: Click "Question Library" from the user menu
    # AND: Select a section or chapter
    # AND: Click "Show Questions"
    # AND: Hover over the desired question and click "Question details"
    # AND: Click "Report an error"

    # THEN: A new tab with the assessment errata form appears
    # AND: The assessment ID is already filled in


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_preview_feedback(tutor_base_url, selenium, teacher):
    """Preview feedback for a question in question library."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: Click "menu"
    # AND: Click "question library"
    # AND: Click on a chapter besides intro
    # AND: Click "question details"
    # AND: Click "preview feedback"

    # THEN: Feedback of the question is shown"


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_switch_between_questions(tutor_base_url, selenium, teacher):
    """Switch between questions using arrows in question library."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: Click "menu"
    # AND: Click "question library"
    # AND: Click on a chapter besides intro
    # AND: Click "question details"
    # AND: Click the right arrow

    # THEN: User should be navigated to the next question


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_go_to_card_view(tutor_base_url, selenium, teacher):
    """Switch to card view in question library."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: Click "menu"
    # AND: Click "question library"
    # AND: Click on a chapter besides intro
    # AND: Click "question details"
    # AND: Click "back to card view"

    # THEN: The questions now displays in card view


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_errata_with_empty_fields(tutor_base_url, selenium, teacher):
    """Attempt to suggest a correction without filling in required fields."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: Click "menu"
    # AND: Click "question library"
    # AND: Click on a chapter besides intro
    # AND: Click "question details"
    # AND: Click "suggest an error"
    # AND: Do not fill out the required fields, click "submit"

    # THEN: Could not submit the form
    # AND: User is prompted to fill out the required field


@expected_failure
@test_case('')
@tutor
def test_exclude_a_question(tutor_base_url, selenium, teacher):
    """Exclude a question in question details in question library."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: Click "menu"
    # AND: Click "question library"
    # AND: Click on a chapter besides intro
    # AND: Click "question details"
    # AND: Click "exclude question"

    # THEN: The chosen question is excluded

