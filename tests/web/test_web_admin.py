"""Tests the admin page."""

from tests.markers import skip_test, test_case, web


@test_case('')
@skip_test(reason='Script not written')
@web
def test_edit_higher_ed_page(web_base_url, seleniumm, admin):
    """Tests ability to edit higher education page."""
    # GIVEN: Logged into the website content management system as a admin
    # AND: On the Higher Eduacation page
    # WHEN: Edit some of the content
    # AND: Click "Save Draft"
    # THEN: The content edited on the cms
    # will show up on the higher education page


@test_case('')
@skip_test(reason='Script not written')
@web
def test_edit_partner_page(web_base_url, seleniumm, admin):
    """Tests ability to edit partner page."""
    # GIVEN: Logged into the website content management system as a admin
    # AND: On the Partner page
    # WHEN: Edit some of the content
    # AND: Click "Save Draft"
    # THEN: The content edited on the cms will show up on the partner page


@test_case('')
@skip_test(reason='Script not written')
@web
def test_edit_support_page(web_base_url, seleniumm, admin):
    """Tests ability to edit support page."""
    # GIVEN: Logged into the website content management system as a admin
    # AND: On the Support page
    # WHEN: Edit some of the content
    # AND: Click "Save Draft"
    # THEN: The content edited on the cms will show up on the support page


@test_case('')
@skip_test(reason='Script not written')
@web
def test_edit_publish_date(web_base_url, seleniumm, admin):
    """Tests ability to edit support page."""
    # GIVEN: Logged into the website content management system as a admin
    # AND: On a textbook page
    # WHEN: Edit Publish Date field
    # AND: Click "Save Draft"
    # THEN: Books publish date is updated on the website


@test_case('')
@skip_test(reason='Script not written')
@web
def test_edit_book_name(web_base_url, seleniumm, admin):
    """Tests ability to edit book name."""
    # GIVEN: Logged into the website content management system as a admin
    # AND: On a textbook page
    # WHEN: Edit SalesForce Name and SalesForce Abbreviation fields
    # AND: Click "Save Draft"
    # THEN: Book titles show up properly in the drop down of forms
