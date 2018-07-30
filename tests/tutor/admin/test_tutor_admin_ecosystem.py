"""Test of admin console ecosystem page."""

from tests.markers import nondestructive, skip_test, test_case, tutor


@test_case('C208722')
@skip_test(reason='Script not written')
@nondestructive
@tutor
def test_download_a_book_manifest(tutor_base_url, selenium, admin):
    """Download an ecosystem manifest."""
    # GIVEN: a user logged in as an administrative user
    # AND: viewing the admin console Ecosystems page

    # WHEN: they click on the "Download Manifest" link in an ecosystem pane

    # THEN: the book manifest is downloaded


@test_case('C208723')
@skip_test(reason='Script not written')
@tutor
def test_save_an_ecosystem_comment(tutor_base_url, selenium, admin):
    """Save a comment to an existing ecosystem."""
    # GIVEN: a user logged in as an administrative user
    # AND: viewing the admin console Ecosystems page

    # WHEN: they choose a book and write a comment
    # AND: click the "Save" button

    # THEN: the comment is successfully saved


@test_case('C208724')
@skip_test(reason='Script not written')
@nondestructive
@tutor
def test_view_the_book_archive(tutor_base_url, selenium, admin):
    """View the book archive associated with an ecosystem."""
    # GIVEN: a user logged in as an administrative user
    # AND: viewing the admin console Ecosystems page

    # WHEN: they click on the "Archive" button

    # THEN: they are taken to the CNX Archive page for the selected book


@test_case('C208849')
@skip_test(reason='Not tested using automation')
@tutor
def test_import_a_new_version_of_an_ecosystem(tutor_base_url, selenium, admin):
    """Import a new version of a Tutor-formatted textbook."""
    # GIVEN: a user logged in as an administrative user
    # AND: viewing the admin console Ecosystems page

    # WHEN: they download a book manifest
    # AND: click the "Import a new Ecosystem" button
    # AND: select click the "Browse..." button
    # AND: select the manifest file from the local file system
    # AND: check the "Update book version" checkbox
    # AND: select the radio button next to
    #      "Discard exercise information (update numbers and versions)"
    # AND: click the "Import" button
    # AND: wait quite a while

    # THEN: the new version of the book ecosystem is import
    # AND: it is at the top of the ecosystem list
