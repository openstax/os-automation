"""Test of admin console courses page."""

from tests.markers import expected_failure, nondestructive, test_case, tutor


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_edit_course(tutor_base_url, selenium, admin):
    """Test admin to edit course."""
    # GIVEN: logged in as admin
    
    # AND: At the Course Page

    # WHEN: Next to a course click on a the ""Edit"" button
    
    # AND: Change one or more of the course fields

    # AND: Click the ""Save"" button

    # THEN: The course is edited and the changes are correctly updated


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_add_course_to_incomplete(tutor_base_url, selenium, admin):
    """Test admin to add course to incomplete ecosystem."""
    # GIVEN: logged in as admin
    # AND: At the Courses Page

    # WHEN: Click the ""Incomplete Bulk Ecosystem Update Jobs""
    
    # AND: Click ""Add Course""

    # AND: Fill in necessary fields
    
    # AND: Click "Save"

    # THEN: A new course is added to the Incomplete Bulk Ecosystem.


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_add_course_to_failed(tutor_base_url, selenium, admin):
    """Test admin to add course to failed ecosystem."""
    # GIVEN: logged in as admin
    # AND: At the Courses Page

    # WHEN: Click the ""Failed Bulk Ecosystem Update Jobs""
    # AND: Click ""Add Course""
    # AND: Fill in necessary fields
    # AND: Click ""Save""

    # THEN: A new course is added to the Failed Bulk Ecosystem.
