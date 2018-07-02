"""Tests the book webpage."""

from tests.markers import expected_failure, nondestructive, test_case, web


@test_case('')
@expected_failure
@nondestructive
@web
def test_all_subjects(web_base_url, selenium):
    """Tests ability to view all books."""
    # GIVEN: On the subjects page
    # WHEN: Click "All"
    # THEN: All textbooks are displayed


@test_case('')
@expected_failure
@nondestructive
@web
def test_science(web_base_url, selenium):
    """Tests ability to view science books."""
    # GIVEN: On the subjects page
    # WHEN: Click "Science"
    # THEN: All science textbooks should be displayed


@test_case('')
@expected_failure
@nondestructive
@web
def test_math(web_base_url, selenium):
    """Tests ability to view math books."""
    # GIVEN: On the subjects page
    # WHEN: Click "Math"
    # THEN: All math textbooks should be displayed


@test_case('')
@expected_failure
@nondestructive
@web
def test_humanities(web_base_url, selenium):
    """Tests ability to view humanities books."""
    # GIVEN: On the subjects page
    # WHEN: Click "Humanities"
    # THEN: All humanities textbooks should be displayed


@test_case('')
@expected_failure
@nondestructive
@web
def test_social_sciences(web_base_url, selenium):
    """Tests ability to view social sciences books."""
    # GIVEN: On the subjects page
    # WHEN: Click "Social Sciences"
    # THEN: All social sciences textbooks should be displayed


@test_case('')
@expected_failure
@nondestructive
@web
def test_ap(web_base_url, selenium):
    """Tests ability to view AP books."""
    # GIVEN: On the subjects page
    # WHEN: Click "AP"
    # THEN: All AP textbooks should be displayed
