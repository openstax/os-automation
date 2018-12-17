"""Test the contact form."""

from autochomsky import chomsky

from pages.web.home import WebHome
from tests.markers import expected_failure, nondestructive, test_case, web
from utils.email import RestMail
from utils.utilities import Utility
from utils.web import Web


@expected_failure
@test_case('C210413', 'C210417')
@web
def test_a_user_may_submit_a_message(web_base_url, selenium):
    """A user may use the contact form to message OpenStax."""
    # GIVEN: a user viewing the contact form page
    topic = Web.TOPICS[Utility.random(end=len(Web.TOPICS) - 1)]
    _, first, last, _ = Utility.random_name()
    email = RestMail('{first}.{last}.{id}'
                     .format(first=first, last=last, id=Utility.random_hex(5))
                     .lower())
    message = chomsky(Utility.random(1, 3))
    home = WebHome(selenium, web_base_url).open()
    contact = home.footer.directory.go_to_the_contact_form()

    # WHEN: they select a question topic from the drop down
    #       menu
    # AND:  enter a name
    # AND:  enter an e-mail address
    # AND:  enter a message
    # AND:  click on the "Send" button
    contact.form.topic = topic
    contact.form.name = '{0} {1}'.format(first, last)
    contact.form.email = email.address
    contact.form.message = message
    confirmation = contact.form.send()

    # THEN: the contact confirmation page is displayed
    # AND:  a "Thank you for contacting OpenStax!" email is
    #       received
    assert(confirmation.is_displayed())
    assert('confirmation' in confirmation.location)

    # WHEN: they click on the "Check out our subjects" button
    subjects = confirmation.view_subjects()

    # THEN: the subjects page is displayed
    assert(subjects.is_displayed())
    assert('subjects' in subjects.location)


@test_case('C210414')
@nondestructive
@web
def test_all_contact_form_fields_are_required(web_base_url, selenium):
    """Test the contact form field verification."""
    # GIVEN: a user viewing the contact form page
    home = WebHome(selenium, web_base_url).open()
    contact = home.footer.directory.go_to_the_contact_form()

    # WHEN: they click "Send"
    contact.form.send()

    # THEN: "Please fill out this field." is displayed below
    #       each text input box
    fields = ['Name', 'Email', 'Message']
    error_text = ': {0}ill out this field{1}'.format(
        *(('F', '') if contact.is_safari else ('Please f', '.')))
    errors = contact.form.get_errors
    for field in fields:
        assert((field + error_text) in errors), \
            '{0} not in {1}'.format(field, str(error_text))


@test_case('C210415')
@nondestructive
@web
def test_the_openstax_mailing_address_is_displayed(web_base_url, selenium):
    """The OpenStax mailing address is displayed next to the contact form."""
    # GIVEN: a user viewing the contact form page
    home = WebHome(selenium, web_base_url).open()
    contact = home.footer.directory.go_to_the_contact_form()

    # WHEN:

    # THEN: the OpenStax mailing address is displayed
    assert(contact.address), 'The mailing address is not visible.'


@test_case('C210416')
@nondestructive
@web
def test_users_seeking_help_are_directed_to_the_support_page(
        web_base_url, selenium):
    """Users looking for help are directed to the Salesforce support pages."""
    # GIVEN: a user viewing the contact form page
    home = WebHome(selenium, web_base_url).open()
    contact = home.footer.directory.go_to_the_contact_form()

    # WHEN: they click on the "SUPPORT CENTER" link
    support = contact.visit_the_support_center()

    # THEN: the OpenStax Support page is displayed in a new tab
    assert(support.is_displayed())
    assert('force.com' in support.location)
