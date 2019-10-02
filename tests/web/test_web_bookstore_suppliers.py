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
    assert(subjects.is_displayed()), 'Subjects page not displayed'
    assert('subjects' in subjects.location), \
        '"subjects" not in the current URL'


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
        message='OpenStax ISBN PDF',
        driver=selenium)

    # THEN: the file is downloaded
    assert(isbn_pdf_passed), 'The PDF download URL failed'


@test_case('C210468')
@nondestructive
@web
def test_there_are_three_book_fulfillment_companies(web_base_url, selenium):
    """Three fulfillment companies are available for bookstore orders."""
    # GIVEN: a user viewing the bookstore page
    home = WebHome(selenium, web_base_url).open()
    suppliers = home.quotes.get(Web.BOOKSTORE_SUPPLIERS).click()

    # WHEN: they test the "Order from MBS" button
    mbs_passed = Utility.test_url_and_warn(
        link=suppliers.fulfillment[Web.MBS_TEXTBOOK].button,
        message='MBS Textbook Exchange',
        driver=selenium)

    # THEN: the MBS Textbook Exchange site is verified
    assert(mbs_passed), 'Failed to verify MBS Textbook Exchange'

    # WHEN: they the "Order from TriLiteral" button
    triliteral_passed = Utility.test_url_and_warn(
        link=suppliers.fulfillment[Web.TRILITERAL].button,
        message='TriLiteral',
        driver=selenium)

    # THEN: the TriLiteral site is verified
    assert(triliteral_passed), 'Failed to verify TriLiteral'

    # WHEN: they test the "Order from Vretta" button
    vretta_passed = Utility.test_url_and_warn(
        link=suppliers.fulfillment[Web.VRETTA].button,
        message='indiCo',
        driver=selenium)

    # THEN: the Vretta site is verified
    assert(vretta_passed), 'Failed to verify Vretta'


@test_case('C210469')
@nondestructive
@web
def test_there_are_three_book_publishers(web_base_url, selenium):
    """Three book publishing companies are available for bookstore orders."""
    # GIVEN: a user viewing the bookstore page
    home = WebHome(selenium, web_base_url).open()
    suppliers = home.quotes.get(Web.BOOKSTORE_SUPPLIERS).click()

    # WHEN: they test the "Order from XanEdu" button
    xanedu_passed = Utility.test_url_and_warn(
        link=suppliers.publishers[Web.XANEDU].button,
        message='XanEdu',
        driver=selenium)

    # THEN: the XanEdu site is verified
    assert(xanedu_passed), 'Failed to verify XanEdu'

    # WHEN: they test the "Order from LAD" button
    lad_passed = Utility.test_url_and_warn(
        link=suppliers.publishers[Web.LAD_CUSTOM].button,
        message='LAD Custom Publishing',
        driver=selenium)

    # THEN: the LAD Custom Publishing site is verified
    assert(lad_passed), 'Failed to verify LAD Custom Publishing'

    # WHEN: they test the "Order from Montezuma" button
    montezuma_passed = Utility.test_url_and_warn(
        link=suppliers.publishers[Web.MONTEZUMA].button,
        message='Montezuma Publishing',
        driver=selenium)

    # THEN: the Montezuma Publishing site is verified
    assert(montezuma_passed), 'Failed to verify Montezuma Publishing'
