"""Test of admin console ecosystem page."""

from tests.markers import expected_failure, nondestructive, test_case, tutor


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_download_book_manifest(tutor_base_url, selenium, admin):
    """Test admin to download book manifest."""
    # GIVEN: logged in as admin

    # WHEN: Go to Tutor admin console
    # AND: Click on ""Content"" in the navbar
    # AND: In the drop down click on ""Ecosystems""
    # AND: Click the ""Download Manifest"" next to a book

    # THEN: The book manifest is downloaded


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_save_comment(tutor_base_url, selenium, admin):
    """Test admin to save a comment."""
    # GIVEN: logged in as admin

    # WHEN: Go to Tutor admin console
    # AND: Click on ""Content"" in the navbar
    # AND: In the drop down click on ""Ecosystems""
    # AND: Choose a book and write a comment
    # AND: Click ""Save""

    # THEN: Comment is successfully saved.


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_view_book_archive(tutor_base_url, selenium, admin):
    """Test admin to view book archive."""
    # GIVEN: logged in as admin

    # WHEN: Go to Tutor admin console
    # AND: Click on ""Content"" in the navbar
    # AND: In the drop down click on ""Ecosystems""
    # AND: Click on ""Archive""

    # THEN: User is taken to the archive page for the selected book.
