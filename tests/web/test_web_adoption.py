"""Test the adoption form."""

from pages.web.adoption import Adoption
from pages.web.home import WebHome
from tests.markers import nondestructive, test_case, web
from utils.web import Web


@test_case('C210385')
@nondestructive
@web
def test_adoption_form_loads(web_base_url, selenium):
    """Test the form loading."""
    # GIVEN: a user viewing the adoption page
    adoption = Adoption(selenium, web_base_url).open()

    # WHEN:

    # THEN: the form is displayed
    assert(adoption.loaded)


@test_case('C210386')
@nondestructive
@web
def test_adoption_form_links_to_the_interest_form(web_base_url, selenium):
    """Test the cross-form link."""
    # GIVEN: a user viewing the adoption page
    adoption = Adoption(selenium, web_base_url).open()

    # WHEN: they click on the "interest form" link
    interest = adoption.go_to_interest()

    # THEN: the interest page is displayed
    assert(interest.loaded)


@test_case('C210387')
@nondestructive
@web
def test_students_do_not_need_to_fill_out_the_adoption_form(
        web_base_url, selenium):
    """Test when students try to fill out the adoption form."""
    # GIVEN: a user viewing the adoption page
    adoption = Adoption(selenium, web_base_url).open()

    # WHEN: they access the adoption form
    # AND:  select "Student" from the drop down menu
    adoption.form.select(Web.STUDENT)

    # THEN: a message "Students don't need to fill..." is displayed
    message = (
        "Students don't need to fill out any forms to use our books. "
        "Access them free now!")
    assert(adoption.form.student_message == message), \
        'Student menu option not selected or message not displayed'

    # WHEN: they go to the home page
    # AND:  select all subjects
    # AND:  click on a book
    # AND:  click on the "Using this book? Let us know."
    # AND:  select "Student" from the drop down menu
    # AND:  click on the "GO BACK" button
    home = WebHome(selenium, web_base_url).open()
    subjects = home.web_nav.subjects.view_all()
    book = subjects.select_random_book()
    book_title = book.title
    adoption = book.is_using()
    adoption.form.select(Web.STUDENT)
    book = adoption.form.go_back()

    # THEN: the book page is displayed
    assert(book.loaded and book.title == book_title)
