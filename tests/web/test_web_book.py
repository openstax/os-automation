"""Test the books webpage."""

import requests

from pages.web.subjects import Subjects
from tests.markers import nondestructive, test_case, web
from utils.web import Library, Web


@test_case('C210348', 'C210349')
@nondestructive
@web
def test_for_book_details_and_user_resource_pages(web_base_url, selenium):
    """Test that the book details page is available."""
    # GIVEN: a user viewing the subjects page
    subjects = Subjects(selenium, web_base_url).open()

    # WHEN: they select a standard book tile
    book = subjects.select_random_book()

    # THEN: the book details page loads
    # AND:  the "Book details" tab is available
    # AND:  "Instructor resources" and "Student resources" tabs are available
    assert('details' in book.location)
    assert(book.details.is_displayed())
    assert(book.tabs[Web.INSTRUCTOR_RESOURCES].is_displayed())
    assert(book.tabs[Web.STUDENT_RESOURCES].is_displayed())

    # WHEN: they select a Polish book tile
    subjects.open()
    book = subjects.select_random_book(_from=Library.POLISH)

    # THEN: the book details page loads
    # AND:  the "Book details" tab is available
    # AND:  "Instructor resources" and "Student resources" tabs are not
    #       available
    assert('details' in book.location)
    assert(book.details.is_displayed())
    assert(len(book.tabs) == 1)


@test_case('C210350')
@nondestructive
@web
def test_the_availability_of_the_table_of_contents(web_base_url, selenium):
    """Test a book ToC is available."""
    # GIVEN: a user viewing the book details page
    subjects = Subjects(selenium, web_base_url).open()
    book = subjects.select_random_book()
    book_title = book.title

    # WHEN: they click on the "Table of contents" link
    book.sidebar.view_table_of_contents()

    # THEN: the table of contents pane is displayed
    assert(book.table_of_contents.is_displayed())

    # WHEN: they click on the "View online" button
    webview = book.table_of_contents.view_online()

    # THEN: the webview version of the book is loaded in a new tab
    assert('cnx' in webview.location)
    assert(book_title == webview.title), (
        'Not viewing the correct book: "{book}" != "{web}"'
        .format(book=book_title, web=webview.title))

    # WHEN: they close the new tab
    # AND:  switch back to the original tab
    # AND:  click on the "X"
    webview.close_tab()
    book.table_of_contents.close()

    # THEN: the table of contents pane is closed
    assert(not book.table_of_contents.is_displayed()), \
        'The table of contents is still visible.'

    # WHEN: the screen width is reduced to 600 pixels
    # AND:  click on the "Table of contents" toggle
    book.resize_window(width=600)
    book.table_of_contents.toggle()

    # THEN: the table of contents pane is displayed
    assert(book.table_of_contents.is_displayed())

    # WHEN: they click on the "Table of contents" link
    book.table_of_contents.toggle()

    # THEN: the table of contents pane is closed
    assert(not book.table_of_contents.is_displayed())


@test_case('C210351')
@nondestructive
@web
def test_webview_for_a_book_is_avaialble(web_base_url, selenium):
    """Test that the Webview of a book is available."""
    # GIVEN: a user viewing the book details page
    subjects = Subjects(selenium, web_base_url).open()
    book = subjects.select_random_book(_from=Library.ALL_BOOKS)
    book_title = book.title

    # WHEN: they click on the "View online" link
    webview = book.sidebar.view_online()

    # THEN: the webview version of the book is loaded in a new tab
    assert(webview.is_displayed())
    assert('cnx' in webview.location)
    assert(book_title == webview.title)

    # WHEN: they close the new tab
    # AND:  switch back to the original tab
    webview.close_tab()

    # THEN: the book details page is displayed
    assert(book.is_displayed())
    assert('openstax.org' in selenium.current_url)


@test_case('C210352')
@nondestructive
@web
def test_details_pdf_is_downloadable(web_base_url, selenium):
    """Test that the PDF of a book may be downloaded."""
    # GIVEN: a user viewing the book details page
    subjects = Subjects(selenium, web_base_url).open()
    book = subjects.select_random_book(_from=Library.ALL_BOOKS)

    # WHEN: they click on the "Download a PDF" link
    url = book.sidebar.pdf_url
    status = requests.head(url)
    book.sidebar.download_pdf()

    # THEN: the book PDF download begins
    assert(selenium.current_url == url)
    assert(status.status_code == requests.codes.ok)


@test_case('C210353')
@nondestructive
@web
def test_links_to_purchase_a_print_copy(web_base_url, selenium):
    """Test that links are provided to purchase a book print copy."""
    # GIVEN: a user viewing the book details page
    subjects = Subjects(selenium, web_base_url).open()
    book = subjects.select_random_book()

    # WHEN: they click on the "Order a print copy" link
    # AND:  click on the "Order on Amazon" button
    book_order = book.sidebar.view_book_order_options()
    amazon = book_order.boxes[Web.INDIVIDUAL].select()

    # THEN: the book order page on Amazon is loaded in a new tab
    assert(amazon.is_displayed())
    assert('amazon' in amazon.location)

    # WHEN: they close the new tab
    # AND:  switch back to the original tab
    amazon.close_tab()

    # THEN: the book details page is displayed
    assert(book.is_displayed())

    # WHEN: they click on the "Order a print copy" link
    # AND:  click on the "Order options" button
    book_order = book.sidebar.view_book_order_options()
    bookstores = book_order.boxes[Web.BOOKSTORES].select()

    # THEN: the bookstore page is displayed
    assert(bookstores.is_displayed())
    assert('bookstore-suppliers' in bookstores.location)


@test_case('C210354')
@nondestructive
@web
def test_mobile_links_to_purchase_a_print_copy(web_base_url, selenium):
    """Test that the mobile links are provided to purchase a book."""
    # GIVEN: a user viewing the book details page
    # AND:  the screen is 600 pixel or fewer wide
    subjects = Subjects(selenium, web_base_url)
    subjects.resize_window(width=600)
    subjects.open()
    book = subjects.select_random_book()

    # WHEN: they click on the "Order a print copy" link
    # AND:  click on the "Order on Amazon" button
    book_order = book.phone.view_book_order_options()
    amazon = book_order.boxes[Web.INDIVIDUAL].select()

    # THEN: the book order page on Amazon is loaded in a new tab
    assert(amazon.is_displayed())
    assert('amazon' in amazon.location)

    # WHEN: they close the new tab
    # AND:  switch back to the original tab
    amazon.close_tab()

    # THEN: the book details page is displayed
    assert(book.is_displayed())

    # WHEN: they click on the "Order a print copy" link
    # AND:  click on the "Order options" button
    book_order = book.phone.view_book_order_options()
    bookstores = book_order.boxes[Web.BOOKSTORES].select()

    # THEN: the indiCo programs page is displayed
    assert(bookstores.is_displayed())
    assert('bookstore-suppliers' in bookstores.location)


@test_case('C210355')
@nondestructive
@web
def test_bookshare_availability(web_base_url, selenium):
    """Test that Bookshare copies are available."""
    # GIVEN: a user viewing the book details page
    subjects = Subjects(selenium, web_base_url).open()
    book = subjects.select_random_book(_from=Library.BOOKSHARE)

    # WHEN: they click on the "Bookshare" link
    bookshare = book.sidebar.view_bookshare()

    # THEN: the Bookshare book page is loaded in a new tab
    assert(bookshare.is_displayed())
    assert('bookshare' in bookshare.location)

    # WHEN: they close the new tab
    # AND:  switch back to the original tab
    bookshare.close_tab()

    # THEN: the book details page is displayed
    assert(book.is_displayed())


@test_case('C210356')
@nondestructive
@web
def test_ibook_availability(web_base_url, selenium):
    """Test that iBook copies are available."""
    # GIVEN: a user viewing the book details page
    subjects = Subjects(selenium, web_base_url).open()
    book = subjects.select_random_book(_from=Library.ITUNES)

    ibooks = len(book.sidebar.ibooks)
    for part in range(ibooks):
        # WHEN: they click on the "Download on iBooks" link
        itunes = book.sidebar.view_ibook(part)

        # THEN: the iTunes book page is loaded in a new tab
        assert(itunes.is_displayed())
        assert('itunes' in itunes.location)

        # WHEN: they close the new tab
        # AND:  switch back to the original tab
        itunes.close_tab()

        # THEN: the book details page is displayed
        assert(book.is_displayed())


@test_case('C210357')
@nondestructive
@web
def test_kindle_availability(web_base_url, selenium):
    """Test that Amazon Kindle copies are available."""
    # GIVEN: a user viewing the book details page
    subjects = Subjects(selenium, web_base_url).open()
    book = subjects.select_random_book(_from=Library.KINDLE)

    # WHEN: they click on the "Download for Kindle" link
    kindle = book.sidebar.view_kindle()

    # THEN: the eTextbook order page on Amazon is loaded in a new tab
    assert(kindle.is_displayed())
    assert('amazon' in kindle.location)

    # WHEN: they close the new tab
    # AND:  switch back to the original tab
    kindle.close_tab()

    # THEN: the book details page is displayed
    assert(book.is_displayed())


@test_case('C210358')
@nondestructive
@web
def test_page_links_to_the_interest_form(web_base_url, selenium):
    """Test the interest form link."""
    # GIVEN: a user viewing the book details page
    subjects = Subjects(selenium, web_base_url).open()
    book = subjects.select_random_book(_from=Library.OPENSTAX)

    # WHEN: they click on the "Sign up to learn more" link
    library = Library()
    passed_title = library.get(book.title, Library.INTEREST)
    interest = book.is_interested()

    # THEN: the interest form is displayed
    # AND:  the book title is passed in the URL
    assert(interest.is_displayed())
    assert('interest' in interest.location)
    assert(passed_title in interest.location)


@test_case('C210359')
@nondestructive
@web
def test_page_links_to_the_adoption_form(web_base_url, selenium):
    """Test the adoption form link."""
    # GIVEN: a user viewing the book details page
    subjects = Subjects(selenium, web_base_url).open()
    book = subjects.select_random_book(_from=Library.OPENSTAX)

    # WHEN: they click on the "Using this book? Let us know." link
    library = Library()
    passed_title = library.get(book.title, Library.ADOPTION)
    adoption = book.is_using()

    # THEN: the adoption form is displayed
    # AND:  the book title is passed in the URL
    assert(adoption.is_displayed())
    assert('adoption' in adoption.location)
    assert(passed_title in adoption.location)
