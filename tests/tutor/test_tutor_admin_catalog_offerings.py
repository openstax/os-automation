"""Test of admin console catalog offerings page."""

from tests.markers import expected_failure, nondestructive, test_case, tutor


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_add_to_catalog_offerings(tutor_base_url, selenium, admin):
    """Test admin to add to catalog offerings."""
    # GIVEN: logged in as admin
    # AND: At the Tutor course offerings

    # WHEN: Click the "Add Offerings" button
    # AND: Fill out the required fields
    # AND: Click the ""Save"" button

    # THEN: A new course is added to the course catalog with the
    # correct information.


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_edit_catalog(tutor_base_url, selenium, admin):
    """Test admin to edit catalog in catalog offereings."""
    # GIVEN: logged in as admin
    # AND: At the Catalog Offerings Page

    # WHEN: Change one or more of the fields
    # AND: Click save"

    # THEN: The course is updated with the changed fields
