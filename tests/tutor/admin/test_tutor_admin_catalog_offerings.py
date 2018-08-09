"""Test of admin console catalog offerings page."""

from tests.markers import skip_test, nondestructive, test_case, tutor


@test_case('C208709')
@skip_test(reason='Script not written')
@nondestructive
@tutor
def test_add_to_catalog_offerings(tutor_base_url, selenium, admin):
    """Test admin to add to catalog offerings."""
    # GIVEN: logged in as admin
    # AND: At the Tutor admin console

    # WHEN: Click the ""Add Offerings"" button
    # AND: Fill out the required fields
    # AND: Click the "Cancel" link

    # THEN: Course offerings are unchanged


@test_case('C208710')
@skip_test(reason='Script not written')
@nondestructive
@tutor
def test_edit_catalog(tutor_base_url, selenium, admin):
    """Test admin to edit catalog in catalog offereings."""
    # GIVEN: logged in as admin
    # AND: At the Catalog Offerings Page

    # WHEN: Change one or more of the fields
    # AND: Click the "Cancel" link

    # THEN: The course offering is unchanged
