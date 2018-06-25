"""Test of admin console districts page."""

from tests.markers import expected_failure, nondestructive, test_case, tutor


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_add_district(tutor_base_url, selenium, admin):
    """Test admin to add district."""
    # GIVEN: logged in as admin

    # WHEN: Go to Tutor admin console
    # AND: Click on ""Course Organization""
    # AND: In the drop down click on ""District""
    # AND: Click the ""Add District"" button
    # AND: Fill out the required fields
    # AND: Click the ""Save"" button

    # THEN: The new district is added to the list of districts.


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_edit_district(tutor_base_url, selenium, admin):
    """Test admin to edit district."""
    # GIVEN: logged in as admin

    # WHEN: Go to Tutor admin console
    # AND: Click on ""Course Organization""
    # AND: In the drop down click on ""District""
    # AND: Click the ""Edit District"" button
    # AND: Edit the field
    # AND: Click the ""Save"" button

    # THEN: The edited district is correctly updated.


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_delete_district(tutor_base_url, selenium, admin):
    """Test admin to delete district."""
    # GIVEN: logged in as admin

    # WHEN: Go to Tutor admin console
    # AND: Click on ""Course Organization""
    # AND: In the drop down click on ""District""
    # AND: Click the ""delete"" button

    # THEN: District is deleted if it has no schools.
    # If the district contains schools it is not deleted.
