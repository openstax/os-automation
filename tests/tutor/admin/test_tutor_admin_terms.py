"""Test of admin console courses page."""

from tests.markers import skip_test, test_case, tutor


@test_case('C208725', 'C208726', 'C208727')
@skip_test(reason='Script not written')
@tutor
def test_add_edit_and_delete_a_new_contract(tutor_base_url, selenium, admin):
    """Add, edit and delete a new terms or privacy contract."""
    # GIVEN: a user logged in as an administrative user
    # AND: viewing the admin console Contracts page

    # WHEN: they click the "New Contract" link
    # AND: fill out the name, title and content fields
    # AND: click "Create contract"

    # THEN: the new contract is created
    # AND: the Details view for the new contract is displayed

    # WHEN: they click the "Edit" link
    # AND: change the name, title and content fields
    # AND: click the "Update contract" button

    # THEN: the Details view for the contract is displayed
    # AND: the edits to the contract are displayed
    # AND: the "Contract updated." alert is displayed

    # WHEN: they click the "Delete" link

    # THEN: the contract is not displayed
    # AND: the "Contract deleted." alert is displayed


@test_case('C208728', 'C210279')
@skip_test(reason='Script not written')
@tutor
def test_view_a_contract_and_remove_a_signer(tutor_base_url, selenium, admin):
    """View a contract, the signatories and remove a signature."""
    # GIVEN: a user logged in as an administrative user
    # AND: viewing the admin console Contracts page

    # WHEN: they select a published contract

    # THEN: the Details view for the contract is displayed

    # WHEN: they click the "Signatures" link

    # THEN: a list of user profiles who have accepted the contract

    # WHEN: they click the "Terminate" link for a user profile
    # AND: click the "OK" button is the alert

    # THEN: the user is removed from the list of signatories
    # AND: the "Signature deleted." alert message is displayed


@test_case('C210276', 'C210277', 'C210278')
@skip_test(reason='Script not written')
@tutor
def test_add_edit_and_delete_a_new_targeted_contract(tutor_base_url,
                                                     selenium, admin):
    """Add, edit and delete a new targeted contract."""
    # GIVEN: a user logged in as an administrative user
    # AND: viewing the admin console Targeted Contracts page

    # WHEN: they click the "Add Targeted Contract" button
    # AND: select a contract name and target district
    # AND: mark the "Can Show Contents?" checkbox
    # AND: click the "Submit" button

    # THEN: the new contract is in the Targeted Contracts list
    # AND: the "The targeted contract has been created." alert message is
    #      displayed

    # WHEN: they click the "edit"
