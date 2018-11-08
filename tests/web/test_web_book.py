"""Test the books webpage."""

import pytest
import requests
from selenium.common.exceptions import NoSuchElementException

from pages.accounts.home import AccountsHome
from pages.accounts.signup import Signup
from pages.web.book import Book
from pages.web.errata import ErrataForm
from pages.web.home import WebHome
from tests.markers import accounts, nondestructive, skip_if_headless  # NOQA
from tests.markers import test_case, web  # NOQA
from utils.email import RestMail
from utils.utilities import Utility
from utils.web import Library, Web


@test_case('C210348', 'C210349')
@nondestructive
@web
def test_for_book_details_and_user_resource_pages(web_base_url, selenium):
    """Test that the book details page is available."""
    # GIVEN: a user viewing the subjects page
    home = WebHome(selenium, web_base_url).open()
    subjects = home.web_nav.subjects.view_all()

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
    home.open()
    subjects = home.web_nav.subjects.view_all()
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
    home = WebHome(selenium, web_base_url).open()
    subjects = home.web_nav.subjects.view_all()
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
    home = WebHome(selenium, web_base_url).open()
    subjects = home.web_nav.subjects.view_all()
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
@skip_if_headless
@web
def test_details_pdf_is_downloadable(web_base_url, selenium):
    """Test that the PDF of a book may be downloaded."""
    # GIVEN: a user viewing the book details page
    home = WebHome(selenium, web_base_url).open()
    subjects = home.web_nav.subjects.view_all()
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
    home = WebHome(selenium, web_base_url).open()
    subjects = home.web_nav.subjects.view_all()
    book = subjects.select_random_book(_from=Library.PRINT_COPY)
    import logging
    logging.debug(str(book))

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
    home = WebHome(selenium, web_base_url)
    home.resize_window(width=600)
    home.open()
    home.web_nav.meta.toggle_menu()
    subjects = home.web_nav.subjects.view_all()
    book = subjects.select_random_book(_from=Library.PRINT_COPY)

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
    home = WebHome(selenium, web_base_url).open()
    subjects = home.web_nav.subjects.view_all()
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
    home = WebHome(selenium, web_base_url).open()
    subjects = home.web_nav.subjects.view_all()
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
    home = WebHome(selenium, web_base_url).open()
    subjects = home.web_nav.subjects.view_all()
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
    home = WebHome(selenium, web_base_url).open()
    subjects = home.web_nav.subjects.view_all()
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
    home = WebHome(selenium, web_base_url).open()
    subjects = home.web_nav.subjects.view_all()
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


@test_case('C210360')
@nondestructive
@web
def test_the_book_details_pane(web_base_url, selenium):
    """Test for the presence of a summary, authors, publish date and ISBN."""
    # GIVEN: a user viewing the book details page
    home = WebHome(selenium, web_base_url).open()
    subjects = home.web_nav.subjects.view_all()
    book = subjects.select_random_book(_from=Library.OPENSTAX)

    # WHEN:

    # THEN: a book "Summary" is present
    # AND:  one or more "Senior Contributing Authors" may be present
    # AND:  one or more "Contributing Authors" may be present
    # AND:  a publish date is present
    # AND:  one or more ISBN numbers is present
    # AND:  a license is present
    assert(book.details.is_displayed())
    assert(len(book.details.summary) > 10)
    if book.details.has_senior_authors:
        assert(book.details.senior_authors)
    if book.details.has_nonsenior_authors:
        assert(book.details.nonsenior_authors)
    assert(book.details.published_on)
    assert(book.details.print_isbns and book.details.digital_isbns)
    if book.sidebar.ibooks:
        assert(book.details.ibook_isbns)
    assert(book.details.license)

    # WHEN: the screen is reduced to 600 pixels
    # AND:  they click on the "Book details" bar
    book.resize_window(width=600)
    book.details.toggle()

    # THEN: the summary is displayed
    assert(len(book.details.summary) > 10)

    # WHEN: they click on the "Authors" bar
    book.details.authors.toggle()

    # THEN: one or more "Senior Contributing Authors" may be present
    # AND:  one or more "Contributing Authors" may be present
    assert(book.details.authors.senior_authors)
    if book.details.authors.has_nonsenior_authors:
        assert(book.details.authors.nonsenior_authors)

    # WHEN: they click on the "Product details" bar
    book.details.product_details.toggle()

    # THEN: one or more ISBN numbers is present
    # AND:  a license is present
    assert(book.details.product_details.print_isbns and
           book.details.product_details.digital_isbns)
    if book.phone.ibooks:
        assert(book.details.product_details.ibook_isbns)
    assert(book.details.product_details.license)


@test_case('C210361')
@nondestructive
@web
def test_current_book_editions_have_an_errata_section(web_base_url, selenium):
    """Test that the current edition of a book has an errata section."""
    # GIVEN: a user viewing the subjects page
    home = WebHome(selenium, web_base_url).open()
    subjects = home.web_nav.subjects.view_all()

    # WHEN: they click a current edition book tile
    book = subjects.select_random_book(_from=Library.CURRENT)

    # THEN: the book details page is displayed
    # AND:  an errata section is present
    assert(book.is_displayed())
    assert(book.details.errata_text)


@test_case('C210362')
@nondestructive
@web
def test_an_old_version_does_not_have_errata(web_base_url, selenium):
    """Test that the current edition of a book has an errata section."""
    # GIVEN: a user viewing the subjects page
    home = WebHome(selenium, web_base_url).open()
    subjects = home.web_nav.subjects.view_all()

    # WHEN: they click a current edition book tile
    book = subjects.select_random_book(_from=Library.SUPERSEDED)

    # THEN: the book details page is displayed
    # AND:  an errata section is present
    assert(book.is_displayed())
    with pytest.raises(NoSuchElementException):
        book.details.errata_text


@test_case('C210363')
@nondestructive
@web
def test_users_may_view_the_current_list_of_errata_for_a_book(
        web_base_url, selenium):
    """Test any user may view the current errata list for a current book."""
    # GIVEN: a user viewing a current edition book details page
    # AND:   are not logged into the website
    home = WebHome(selenium, web_base_url).open()
    subjects = home.web_nav.subjects.view_all()
    book = subjects.select_random_book(_from=Library.OPENSTAX,
                                       filter_current=True)
    book_title = book.title

    # WHEN: they click the "Errata list" button
    errata = book.details.view_errata()

    # THEN: an errata list for the book is displayed
    assert(errata.is_displayed())
    assert('errata/?book' in errata.location)
    assert(book_title in errata.title)

    # WHEN: they return to the book details page
    # AND:  reduce the screen to 600 pixels
    # AND:  click on the "Report errata" bar
    # AND:  click on the "Errata list" button
    errata.back()
    book.resize_window(width=600)
    errata = book.phone.errata.view_errata()

    # THEN: an errata list for the book is displayed
    assert(errata.is_displayed())
    assert('errata/?book' in errata.location)
    assert(book_title in errata.title)


@test_case('C210364')
@nondestructive
@web
def test_logged_in_users_may_view_the_errata_submission_form(
        web_base_url, selenium, teacher):
    """Test a logged in user may view the errata submission form."""
    # GIVEN: a user viewing a current edition book details page
    # AND:   are logged into the website
    home = WebHome(selenium, web_base_url).open()
    home.web_nav.login.log_in(*teacher, destination=WebHome, url=web_base_url)
    home.web_nav.login.training_wheel.close_modal()
    subjects = home.web_nav.subjects.view_all()
    book = subjects.select_random_book(_from=Library.OPENSTAX,
                                       filter_current=True)
    book_title = book.title

    # WHEN: they click on the "Suggest a correction" button
    errata_form = book.details.submit_errata()

    # THEN: the errata form is displayed
    # AND:  the subject is prefilled in
    assert(errata_form.is_displayed())
    assert(errata_form.subject == book_title)

    # WHEN: they return to the book details page
    # AND:  reduce the screen to 600 pixels
    # AND:  click on the "Report errata" bar
    # AND:  click on the "Suggest a correction" button
    errata_form.back()
    book.resize_window(width=600)
    book.phone.errata.toggle()
    errata_form = book.phone.errata.submit_errata()

    # THEN: the errata form is displayed
    # AND:  the subject is prefilled in
    assert(errata_form.is_displayed())
    assert(errata_form.subject == book_title)


@test_case('C210365')
@nondestructive
@web
def test_non_logged_in_users_are_directed_to_log_in_to_view_the_errata_form(
        web_base_url, selenium, teacher):
    """Test non-logged in users trying to view the form are asked to log in."""
    # GIVEN: a user viewing a current edition book details page
    # AND:   have a valid login and password
    # AND:   are not logged into the website
    home = WebHome(selenium, web_base_url).open()
    subjects = home.web_nav.subjects.view_all()
    book = subjects.select_random_book(_from=Library.OPENSTAX,
                                       filter_current=True)
    book_title = book.title
    book_errata = book.details.errata_append

    # WHEN: they click on the "Suggest a correction" button
    accounts = book.details.submit_errata()

    # THEN: the Accounts login page is displayed
    assert(accounts.is_displayed())
    assert('accounts' in accounts.location)

    # WHEN: they log into Accounts
    errata_form = accounts.service_log_in(
        *teacher,
        destination=ErrataForm, url=web_base_url, book=book_errata)

    # THEN: the errata form is displayed
    # AND:  the subject is prefilled in
    assert(errata_form.is_displayed())
    assert(errata_form.subject == book_title)


@test_case('C210366')
@nondestructive
@web
def test_non_logged_in_users_on_mobile_are_directed_to_log_in_for_errata_form(
        web_base_url, selenium, teacher):
    """Test non-logged in users on mobile trying to view the form."""
    # GIVEN: a user viewing a current edition book details page
    # AND:  have a valid login and password
    # AND:  are not logged into the website
    # AND:  the screen width is 600 pixels
    home = WebHome(selenium, web_base_url)
    home.resize_window(width=600)
    home.open()
    home.web_nav.meta.toggle_menu()
    subjects = home.web_nav.subjects.view_all()
    book = subjects.select_random_book(_from=Library.OPENSTAX,
                                       filter_current=True)
    book_title = book.title
    book_errata = book.phone.errata.errata_append

    # WHEN: they click on the "Report errata" bar
    # AND:  click on the "Suggest a correction" button
    book.phone.errata.toggle()
    accounts = book.phone.errata.submit_errata()

    # THEN: the Accounts login page is displayed
    assert(accounts.is_displayed())
    assert('accounts' in accounts.location)

    # WHEN: they log into Accounts
    errata_form = accounts.service_log_in(
        *teacher,
        destination=ErrataForm, url=web_base_url, book=book_errata)

    # THEN: the errata form is displayed
    # AND:  the subject is prefilled in
    assert(errata_form.is_displayed())
    assert(errata_form.subject == book_title)


@test_case('C210367')
@nondestructive
@web
def test_teachers_are_asked_to_sign_up_to_access_locked_content(
        web_base_url, selenium):
    """Test users are directed to sign up to access locked resources."""
    # GIVEN: a user viewing the book details page
    # AND:  are not logged into the website
    # AND:  the book has instructor resources
    home = WebHome(selenium, web_base_url).open()
    subjects = home.web_nav.subjects.view_all()
    book = subjects.select_random_book(_from=Library.HAS_I_LOCK)

    # WHEN: they click on the "Sign up" link
    book.select_tab(Web.INSTRUCTOR_RESOURCES)
    accounts = book.instructor.sign_up()

    # THEN: the Accounts sign up page is displayed
    assert(accounts.is_displayed())
    assert('accounts' in accounts.location)


@test_case('C210368')
@accounts
@web
def test_pending_instructors_see_access_pending_for_locked_resources(
        accounts_base_url, web_base_url, selenium, teacher):
    """Test pending instructors see 'Access pending' for locked resources."""
    # GIVEN: a user viewing the book details page
    # AND:  have an unverified instructor account
    # AND:  the book has locked instructor resources
    name = Utility.random_name()
    email = RestMail(
        '{first}.{last}.{tag}'
        .format(first=name[1], last=name[2], tag=Utility.random_hex(3))
        .lower()
    )
    email.empty()
    address = email.address
    password = teacher[1]
    accounts = AccountsHome(selenium, accounts_base_url).open()
    accounts.login.go_to_signup.account_signup(
        email=address, password=password, _type=Signup.INSTRUCTOR,
        provider=Signup.RESTMAIL, name=name, school='Automation',
        news=False, phone=Utility.random_phone(),
        webpage='https://openstax.org/', subjects=subject_list(2), students=10,
        use=Signup.ADOPTED)
    home = WebHome(selenium, web_base_url).open()
    subjects = home.web_nav.subjects.view_all()
    book = subjects.select_random_book(_from=Library.HAS_I_LOCK)

    # WHEN: they click on the "Instructor resources" tab
    book.select_tab(Web.INSTRUCTOR_RESOURCES)

    # THEN: locked resources show "Access pending"
    for option in book.instructor.resources:
        assert(option.status_message in Web.ACCESS_OK), (
            '{resource} ("{status}") not pending authorization or available'
            .format(resource=option.title, status=option.status_message))


@test_case('C210369')
@accounts
@web
def test_verified_instructors_may_access_locked_resources(
        accounts_base_url, web_base_url, selenium, teacher):
    """Test verified instructors may access locked resources."""
    # GIVEN: a user viewing the book details page
    # AND:  they have a valid instructor login and password
    # AND:  they are not logged into the website
    # AND:  the book has locked instructor resources
    home = WebHome(selenium, web_base_url).open()
    subjects = home.web_nav.subjects.view_all()
    book = subjects.select_random_book(_from=Library.HAS_I_LOCK)

    # WHEN: they click on the "Instructor resources" tab
    # AND:  click on the "Click here to unlock" link
    book.select_tab(Web.INSTRUCTOR_RESOURCES)
    options = book.instructor.resources_by_option(Web.LOCKED)
    assert(options)
    option = options[Utility.random(0, len(options) - 1)]
    option_title = option.title
    option.select()
    accounts = AccountsHome(selenium, accounts_base_url)

    # THEN: the Accounts login page is displayed
    assert(accounts.is_displayed())
    assert('login' in accounts.location)

    # WHEN: they log into Accounts
    accounts.service_log_in(*teacher, destination=Book, url=web_base_url)

    # THEN: the instructor resources tab on the book details page is displayed
    # AND:  the resource is no longer locked
    assert(book.instructor.is_displayed())
    option = book.instructor.resource_by_name(option_title)
    assert(not option.is_locked), \
        '{option} is still locked'.format(option=option.title)


@test_case('C210411')
@nondestructive
@web
def test_verified_instructors_may_request_a_comped_ibook(
        web_base_url, selenium, teacher):
    """Test verified instructors may request a complimentary iBook copy."""
    # GIVEN: a user viewing the book details page
    # AND:  the book has comp copies available
    home = WebHome(selenium, web_base_url).open()
    subjects = home.web_nav.subjects.view_all()
    book = subjects.select_random_book(_from=Library.COMP_COPY)
    book.web_nav.login.log_in(*teacher, destination=Book, url=web_base_url)
    if book.web_nav.login.modal_displayed:
        book.web_nav.login.training_wheel.close_modal()

    # WHEN: they click on the "Instructor resources" tab
    # AND:  click on the "iBooks Comp Copy" tile
    book.select_tab(Web.INSTRUCTOR_RESOURCES)
    comp_copy = book.instructor.resource_by_name('iBooks Comp Copy').select()

    # THEN: the comp copy modal is displayed
    assert(comp_copy.is_displayed())

    # WHEN: they click "Request iBook"
    comp_copy.submit()

    # THEN: a "Please enter a number." pop up appears below
    #       the "How many students will be using <book>
    #       this semester?" input box
    assert(comp_copy.get_error() in
           ['Please enter a number.',
            'Please fill out this field.',
            'Fill out this field'])

    # WHEN: they click on the "Cancel" button
    comp_copy.cancel()

    # THEN: the comp copy modal is closed
    assert(not comp_copy.is_displayed())

    # WHEN: they click on the "iBooks Comp Copy" tile
    # AND:  click on the 'X' icon
    comp_copy = book.instructor.resource_by_name('iBooks Comp Copy').select()
    comp_copy.close()

    # THEN: the comp copy modal is closed
    assert(not comp_copy.is_displayed())

    # WHEN: they click on the "iBooks Comp Copy" tile
    # AND:  enter a zero or greater number in the input box
    # AND:  click on the "Request iBook" button
    comp_copy = book.instructor.resource_by_name('iBooks Comp Copy').select()
    comp_copy.students = Utility.random()
    comp_copy_receipt = comp_copy.submit()

    # THEN: "Your request was submitted!" is displayed
    assert('Your request was submitted!' in comp_copy_receipt.text)

    # WHEN: they click on the "Close" button
    comp_copy_receipt.close()

    # THEN: the comp copy modal is closed
    assert(not comp_copy_receipt.is_displayed())


@test_case('C210370')
@nondestructive
@web
def test_resources_have_a_title_description_and_access_type(
        web_base_url, selenium, teacher):
    """Test available resources have a title, description and access type."""
    # GIVEN: a user viewing the book details page
    # AND:  have a verified instructor account
    # AND:  are logged into the site
    # AND:  the book has instructor resources
    # AND:  the book has student resources
    home = WebHome(selenium, web_base_url).open()
    home.web_nav.login.log_in(*teacher, destination=WebHome, url=web_base_url)
    if home.web_nav.login.modal_displayed:
        home.web_nav.login.training_wheel.close_modal()
    subjects = home.web_nav.subjects.view_all()
    book = subjects.select_random_book(_from=Library.HAS_S_UNLOCK)

    # WHEN: they click on the "Instructor resources" tab
    book.select_tab(Web.INSTRUCTOR_RESOURCES)

    # THEN: each resource has a title
    # AND:  each resource has a description
    # AND:  each resource has an access type of "Go" to,
    #       "Download", "Access pending", "Request your
    #       complimentary iBooks download", or "Visit the
    #       Hub"
    for resource in book.instructor.resources_by_status(Web.ACCESS_OK):
        assert(resource.title)
        assert(resource.description)
        assert(resource.status_message in Web.ACCESS_OK)

    # WHEN: they click on the "Student resources" tab
    book.select_tab(Web.STUDENT_RESOURCES)

    # THEN: each resource has a title
    # AND:  each resource has a description
    # AND:  each resource has an access type of "Go" to or
    #       "Download"
    for resource in book.student.resources_by_status(Web.ACCESS_OK):
        assert(resource.title)
        assert(resource.description)
        assert(resource.status_message in Web.ACCESS_OK)

    # WHEN: the screen is reduced to 600 pixels
    book.resize_window(width=600)

    # THEN: the description is not displayed
    for resource in book.student.resources_by_status(Web.ACCESS_OK):
        assert(resource.title)
        assert(not resource.description)
        assert(resource.status_message in Web.ACCESS_OK)


def subject_list(size=1):
    """Return a list of subjects for an elevated signup."""
    subjects = len(Signup.SUBJECTS)
    if size > subjects:
        size = subjects
    book = ''
    group = []
    while len(group) < size:
        book = (Signup.SUBJECTS[Utility.random(0, subjects - 1)])[1]
        if book not in group:
            group.append(book)
    return group
