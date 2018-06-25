"""Test of admin console catalog offerings page."""

from tests.markers import expected_failure, nondestructive, test_case, tutor


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_add_to_catalog_offerings(tutor_base_url, selenium, admin):
    """Test admin to add to catalog offerings."""
    # GIVEN: logged in as admin

    # WHEN: Go to Tutor admin console
    # AND: Click on ""Course Organization""
    # AND: In the drop down click on ""Catalog Offerings""
    # AND: Click the ""Add Offerings"" button
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

    # WHEN: Go to Tutor admin console
    # AND: Click on ""Course Organization"" in the navbar
    # AND: On the drop down click on ""Catalog Offerings""
    # AND: On the side of a course listing click the ""Edit"" button
    # AND: Change one or more of the fields
    # AND: Click save"

    # THEN: The course is updated with the changed fields
