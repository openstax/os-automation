"""Test of admin console courses page."""

from tests.markers import expected_failure, nondestructive, test_case, tutor


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_create_new_contract(tutor_base_url, selenium, admin):
    """Test admin to create a new contract."""
    # GIVEN: logged in as admin

    # WHEN: Go to Tutor admin console
    # AND: Click on ""Legal"" in the navbar
    # AND: In the drop down click on ""Terms""
    # AND: At the bottom of the page click ""New Contract""
    # AND: Fill out the required fields
    # AND: Click ""Create Contract""

    # THEN: A new contract is created and appears in the contracts list


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_edit_contract(tutor_base_url, selenium, admin):
    """Test admin to edit a contract."""
    # GIVEN: logged in as admin

    # WHEN: Go to Tutor admin console
    # AND: Click on ""Legal"" in the navbar
    # AND: In the drop down click on ""Terms""
    # AND: At the bottom of the page click ""Edit""
    # AND: Edit one or more fields
    # AND: Click ""Update Contract""

    # THEN: Contract is updated


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_delete_contract(tutor_base_url, selenium, admin):
    """Test admin to delete a contract."""
    # GIVEN: logged in as admin

    # WHEN: Go to Tutor admin console
    # AND: Click on ""Legal"" in the navbar
    # AND: In the drop down click on ""Terms""
    # AND: At the bottom of the page click ""Delete""
    # AND: Click ""Okay""

    # THEN: The selected contract is deleted and no longer appears in the list


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_view_contract(tutor_base_url, selenium, admin):
    """Test admin to view a contract."""
    # GIVEN: logged in as admin

    # WHEN: Go to Tutor admin console
    # AND: Click on ""Legal"" in the navbar
    # AND: In the drop down click on ""Terms""
    # AND: Click on one of the versions of one of the legal docs

    # THEN: Page containing the legal doc information is loaded


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_add_targeted_contract(tutor_base_url, selenium, admin):
    """Test admin to add targeted contract."""
    # GIVEN: logged in as admin

    # WHEN: Go to Tutor admin console
    # AND: Click on ""Legal"" in the navbar
    # AND: In the drop down click on ""Targeted Contract""
    # AND: Click on ""Add Targeted Contract""
    # AND: Fill in all necessary field
    # AND: Click ""Submit""

    # THEN: A new targeted contract is created.


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_edit_targeted_contract(tutor_base_url, selenium, admin):
    """Test admin to edit targeted contract."""
    # GIVEN: logged in as admin

    # WHEN: Go to Tutor admin console
    # AND: Click on ""Legal"" in the navbar
    # AND: In the drop down click on ""Targeted Contract""
    # AND: Click on ""Edit"" next to a contract

    # THEN: "User are unable to edit at this time. " message is loaded.


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_delete_targeted_contract(tutor_base_url, selenium, admin):
    """Test admin to delete targeted contract."""
    # GIVEN: logged in as admin

    # WHEN: Go to Tutor admin console
    # AND: Click on ""Legal"" in the navbar
    # AND: In the drop down click on ""Targeted Contract""
    # AND: Click on ""delete""

    # THEN: Contract is removed from the list of targeted contracts.
