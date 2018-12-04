"""Test the interest form."""

import pytest

from pages.web.book import Book
from pages.web.home import WebHome
from pages.web.interest import Interest, InterestConfirmation
from tests.markers import nondestructive, skip_test, smoke_test, test_case, web
from utils.email import RestMail
from utils.utilities import Utility
from utils.web import Library, Web


@test_case('C210508')
@nondestructive
@web
def test_the_interest_form_loads(web_base_url, selenium):
    """Test the interest form loads."""
    # GIVEN: a user and a web browser
    interest = Interest(selenium, web_base_url)

    # WHEN: they go to the interest form
    interest.open()

    # THEN: the form is displayed
    assert(interest.is_displayed())
    assert('interest' in interest.location)


@test_case('C210509')
@nondestructive
@web
def test_the_interest_form_links_to_the_adoption_form(web_base_url, selenium):
    """Test a user viewing the interest form can go to the adoption form."""
    # GIVEN: a user viewing the interest page
    interest = Interest(selenium, web_base_url).open()

    # WHEN: they click on the "Let us know!" link
    adoption = interest.go_to_adoption()

    # THEN: the adoption page is displayed
    assert(adoption.is_displayed())
    assert('adoption' in adoption.location)


@test_case('C210510')
@nondestructive
@web
def test_students_do_not_need_to_fill_out_the_form(web_base_url, selenium):
    """Test students are informed they do not need to fill out the form."""
    # GIVEN: a user viewing the interest page
    interest = Interest(selenium, web_base_url).open()

    # WHEN: they select "Student" from the drop down menu
    interest.form.select(Web.STUDENT)

    # THEN: a message "Students don't need to fill..." is displayed
    message = (
        "Students don't need to fill out any forms to use our books. "
        "Access them free now!")
    assert(interest.form.student_message == message), \
        'Student menu option not selected or message not displayed'

    # WHEN: they go to the home page
    # AND:  select all subjects
    # AND:  click on a book
    # AND:  click on the "Sign up to learn more"
    # AND:  select "Student" from the drop down menu
    # AND:  click on the "GO BACK" button
    home = WebHome(selenium, web_base_url).open()
    subjects = home.web_nav.subjects.view_all()
    book = subjects.select_random_book()
    book_title = book.title
    interest = book.is_interested()
    interest.form.select(Web.STUDENT)
    interest.form.go_back(destination=Book)

    # THEN: the book page is displayed
    assert(book.is_displayed() and book.title == book_title)


@test_case('C210511')
@web
def test_non_students_may_fill_out_the_form(web_base_url, selenium):
    """Test non-students may fill out and submit the interest form.

    Salesforce verification of the form is not tested.
    """
    # GIVEN: a user viewing the interest page
    user_type = Web.USERS[Utility.random(1, len(Web.USERS) - 1)]
    _, first_name, last_name, _ = Utility.random_name()
    email = RestMail(
        '{first}.{last}.{rand}'
        .format(first=first_name, last=last_name, rand=Utility.random_hex(6))
        .lower())
    phone = Utility.random_phone(713, False)
    school = 'Automation'
    books = Library().random_book(Utility.random(start=5, end=5))
    students = Utility.random(Web.STUDENT_MIN)
    from utils.web import TechProviders
    tech_providers = TechProviders.get_tech(Utility.random(0, 3))
    if TechProviders.OTHER in tech_providers:
        other = 'Another product provider'
    else:
        other = None
    interest = Interest(selenium, web_base_url).open()

    # WHEN: they select a non-Student role from the drop down menu
    # AND:  fill out the contact form fields
    # AND:  click on the "Next" button
    # AND:  select a book subject
    # AND:  enter a number of students
    # AND:  select zero to three partner options
    # AND:  select zero to eight "How did you hear?" options
    # AND:  click on the "Next" button
    # AND:  select zero or more technology options
    # AND:  click on the "Submit" button
    confirmation = interest.submit_interest(
        user_type=user_type,
        first=first_name,
        last=last_name,
        email=email.address,
        phone=phone,
        school=school,
        books=books,
        students=students,
        additional_resources=Web.resources(),
        heard_on=Web.heard_by(),
        tech_providers=tech_providers,
        other_provider=other)

    # THEN: the interest confirmation page is displayed
    assert(confirmation.is_displayed())
    assert('confirmation' in confirmation.location)


@test_case('C210512')
@nondestructive
@web
def test_a_book_is_preselected_when_a_book_details_interest_link_is_used(
        web_base_url, selenium):
    """Test the book is already selected when passed in the URL."""
    # GIVEN: a user viewing a book page
    user_type = Web.USERS[Utility.random(1, len(Web.USERS) - 1)]
    _, first_name, last_name, _ = Utility.random_name()
    email = RestMail(
        '{first}.{last}.{rand}'
        .format(first=first_name, last=last_name, rand=Utility.random_hex(6))
        .lower())
    phone = Utility.random_phone(713, False)
    school = 'Automation'
    book, short, full, detail_append = Library().get_name_set()
    books = [short]
    students = ''
    book_details = Book(selenium, web_base_url, book_name=detail_append).open()
    interest = book_details.is_interested()

    # WHEN: they click on the "Sign up to learn more" link
    # AND:  select a non-Student role from the drop down menu
    # AND:  fill out the contact form fields
    # AND:  click on the "Next" button
    with pytest.raises(AssertionError) as error:
        interest.submit_interest(
            user_type=user_type,
            first=first_name,
            last=last_name,
            email=email.address,
            phone=phone,
            school=school,
            books=books,
            students=students,
            additional_resources=Web.resources(),
            heard_on=Web.heard_by())

    selection = interest.form.selection
    # THEN: the book is selected
    assert(short in selection), (
        '{book} not in the current selection ({selection})'
        .format(book=short, selection=selection))
    assert('Using error' in Utility.get_error_information(error)), \
        'No book is preselected'


@test_case('C210513')
@nondestructive
@web
def test_interest_form_identity_fields_are_required(web_base_url, selenium):
    """Test interest form identity input fields are required."""
    # GIVEN: a user viewing the interest page
    user_type = Web.USERS[Utility.random(1, len(Web.USERS) - 1)]
    interest = Interest(selenium, web_base_url).open()

    # WHEN: they select a non-Student role from the drop
    #       down menu
    # AND:  click on the "Next" button
    with pytest.raises(AssertionError) as error:
        interest.submit_interest(
            user_type=user_type,
            first='',
            last='',
            email='',
            phone='',
            school='',
            books='',
            students='',
            additional_resources=None,
            heard_on='')

    # THEN: the contact form fields are shaded red
    # AND:  "Please fill out this field." is below each
    #       contact form field input box
    browser = selenium.capabilities.get('browserName').lower()
    expected_error = (
        ': {browser_front}ill out this field'
        .format(browser_front='F' if browser == 'safari' else 'Please f'))
    data_issues = Utility.get_error_information(error)
    first = ('first_name' + expected_error) in data_issues
    last = ('last_name' + expected_error) in data_issues
    email = ('email' + expected_error) in data_issues
    phone = ('phone' + expected_error) in data_issues
    school = ('school' + expected_error) in data_issues
    assert(first and last and email and phone and school), (
        'Errors not all shown:\n{errors}\n'.format(errors=data_issues)
        ('{first} {last} {email} {phone} {school}'
         .format(first=first, last=last, email=email, school=school)))


@skip_test(reason='Not written')
@test_case('C210514')
@nondestructive
@web
def test_interest_form_school_name_auto_complete(web_base_url, selenium):
    """Test typing characters in the school name filters the school list."""
    # GIVEN: a user viewing the interest page

    # WHEN: they select a non-Student role from the drop down menu
    # AND:  enter at least two letters in the "School name" input box

    # THEN: suggested institutions with the string are displayed

    # WHEN: one or more letters are appended

    # THEN: the suggestion list is filtered further


@test_case('C210515')
@nondestructive
@web
def test_able_to_submit_a_new_institution_name(web_base_url, selenium):
    """Test a user may submit a new school name not in the list."""
    # GIVEN: a user viewing the interest page

    # WHEN: they select a non-Student role from the drop down menu
    # AND:  fill out the contact form fields
    # AND:  enter a random string in the "School name" field
    # AND:  click on the "Next" button

    # THEN: the textbook selection list is displayed


@test_case('C210516')
@nondestructive
@web
def test_interest_form_requires_at_least_one_book_selection(
        web_base_url, selenium):
    """Test at least one book must be selected before submitting the form."""
    # GIVEN: a user viewing the interest page
    user_type = Web.USERS[Utility.random(1, len(Web.USERS) - 1)]
    _, first_name, last_name, _ = Utility.random_name()
    email = RestMail(
        '{first}.{last}.{rand}'
        .format(first=first_name, last=last_name, rand=Utility.random_hex(6))
        .lower())
    phone = Utility.random_phone(713, False)
    school = 'Automation'
    interest = Interest(selenium, web_base_url).open()

    # WHEN: they select a non-Student role from the drop down menu
    # AND:  fill out the contact form fields
    # AND:  click on the "Next" button
    # AND:  click on the "Next" button
    with pytest.raises(AssertionError) as error:
        interest.submit_interest(
            user_type=user_type,
            first=first_name,
            last=last_name,
            email=email.address,
            phone=phone,
            school=school,
            books=[],
            students='',
            additional_resources=None,
            heard_on=None)

    # THEN: the textbook selection list is still displayed
    # AND:  an error message "Please select at least one book" is displayed
    assert('Please select at least one book'
           in Utility.get_error_information(error)), (
        'The book error was not displayed')


@skip_test(reason='Salesforce API not written')
@test_case('C210517')
@web
def test_all_fields_are_sent_to_a_salesforce_lead(web_base_url, selenium):
    """Test all interest form fields are sent to one Salesforce lead."""
    # GIVEN: a user viewing the interest page

    # WHEN: they fill out the interest form
    # AND:  submit the form

    # THEN: the form data is present in an interest lead in Salesforce


@skip_test(reason='Salesforce API not written')
@test_case('C210518')
@smoke_test
@web
def test_multiple_book_selection_generates_one_lead(web_base_url, selenium):
    """Test selecting multiple books generates one Salesforce lead."""
    # GIVEN: a user viewing the interest page

    # WHEN: they fill out the interest form
    # AND:  select two or more books
    # AND:  submit the form

    # THEN: one interest lead is sent to Salesforce


@test_case('C210519')
@web
def test_post_form_submission_text_and_link(web_base_url, selenium):
    """Test the interest form confirmation page."""
    # GIVEN: a user viewing the interest confirmation page
    confirmation = InterestConfirmation(selenium, web_base_url).open()

    # WHEN: they click on the "Back to the books" button
    subjects = confirmation.back_to_books()

    # THEN: the subjects page is displayed
    assert(subjects.is_displayed())
    assert('subjects' in subjects.location)
