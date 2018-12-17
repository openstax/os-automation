"""Test the bookstore suppliers page."""

from pages.web.home import WebHome
from tests.markers import nondestructive, test_case, web
from utils.utilities import Utility
from utils.web import Web


@test_case('C210466')
@nondestructive
@web
def test_users_are_directed_to_the_subjects_page(web_base_url, selenium):
    """Instructors and students are directed to the Subjects page."""
    # GIVEN: a user viewing the bookstore page
    home = WebHome(selenium, web_base_url).open()
    suppliers = home.quotes.get(Web.BOOKSTORE_SUPPLIERS).click()

    # WHEN: they click on the "Subjects page" link
    subjects = suppliers.view_subjects()

    # THEN: the subjects page is displayed
    assert(subjects.is_displayed())
    assert('subjects' in subjects.location)


@test_case('C210467')
@nondestructive
@web
def test_book_suppliers_has_a_pdf_of_openstax_isbn_numbers(
        web_base_url, selenium):
    """A PDF of OpenStax ISBNs is available."""
    # GIVEN: a user viewing the bookstore page
    home = WebHome(selenium, web_base_url).open()
    suppliers = home.quotes.get(Web.BOOKSTORE_SUPPLIERS).click()

    # WHEN: they click on the "Download a list of ISBN
    #       numbers" button
    isbn_pdf_passed = Utility.test_url_and_warn(
        link=suppliers.isbn_list,
        message='OpenStax ISBN PDF')

    # THEN: the file is downloaded
    assert(isbn_pdf_passed)


@test_case('C210468')
@nondestructive
@web
def test_there_are_three_book_fulfillment_companies(web_base_url, selenium):
    """Three fulfillment companies are available for bookstore orders."""
    # GIVEN: a user viewing the bookstore page
    home = WebHome(selenium, web_base_url).open()
    suppliers = home.quotes.get(Web.BOOKSTORE_SUPPLIERS).click()

    # WHEN: they test the "Order from IndiCo" button
    # THEN: the indiCo site is verified
    indico_passed = Utility.test_url_and_warn(
        link=suppliers.fulfillment[Web.INDICO].button,
        message='indiCo')

    # WHEN: they test the "Order from MBS" button
    # THEN: the MBS Textbook Exchange site is verified
    mbs_passed = Utility.test_url_and_warn(
        link=suppliers.fulfillment[Web.MBS_TEXTBOOK].button,
        message='MBS Textbook Exchange')

    # WHEN: they the "Order from TriLiteral" button
    # THEN: the TriLiteral site is verified
    triliteral_passed = Utility.test_url_and_warn(
        link=suppliers.fulfillment[Web.TRILITERAL].button,
        message='TriLiteral')

    assert(indico_passed and mbs_passed and triliteral_passed)


@test_case('C210469')
@nondestructive
@web
def test_there_are_three_book_publishers(web_base_url, selenium):
    """Three book publishing companies are available for bookstore orders."""
    # GIVEN: a user viewing the bookstore page
    home = WebHome(selenium, web_base_url).open()
    suppliers = home.quotes.get(Web.BOOKSTORE_SUPPLIERS).click()

    # WHEN: they test the "Order from XanEdu" button
    # THEN: the XanEdu site is verified
    xanedu_passed = Utility.test_url_and_warn(
        link=suppliers.publishers[Web.XANEDU].button,
        message='XanEdu')

    # WHEN: they test the "Order from LAD" button
    # THEN: the LAD Custom Publishing site is verified
    lad_passed = Utility.test_url_and_warn(
        link=suppliers.publishers[Web.LAD_CUSTOM].button,
        message='LAD Custom Publishing')

    # WHEN: they test the "Order from Montezuma" button
    # THEN: the Montezuma Publishing site is verified
    montezuma_passed = Utility.test_url_and_warn(
        link=suppliers.publishers[Web.MONTEZUMA].button,
        message='Montezuma Publishing')

    assert(xanedu_passed and lad_passed and montezuma_passed)
