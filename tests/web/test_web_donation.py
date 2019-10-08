"""Test the OpenStax Website donation form.

This assumes TouchNet's payment side is functioning.
"""

from pages.web.home import WebHome
from tests.markers import nondestructive, test_case, web
from utils.utilities import Utility
from utils.web import Web


@test_case('C210421', 'C210422')
@nondestructive
@web
def test_the_preform_amount_is_passed_to_the_donation_form(
        web_base_url, selenium):
    """The preform sets the dollar donation amount in the full form."""
    # SETUP:
    title, first, last, suffix = Utility.random_name()
    email = Utility.fake_email(first, last)
    phone = Utility.random_phone(number_only=Utility.random(0, 1) == 1)
    phone_type = ['Work', 'Home', 'Cell', 'Fax'][Utility.random(0, 3)]
    street, city, state, zip_code = Utility.random_address()
    country = 'US'
    amount = Web.DOLLAR_OPTIONS[
        Utility.random(end=len(Web.DOLLAR_OPTIONS) - 2)]

    # GIVEN: a user viewing the give page
    home = WebHome(selenium, web_base_url).open()
    give = home.openstax_nav.view_donation_options()

    # WHEN: they select a set dollar option
    # AND:  click on the "donate!" button
    give.form.boxes = amount

    donation = give.form.donate()

    # THEN: the "Donation Amount" shows the same amount
    assert(donation.is_displayed()), 'Donation page not displayed'
    assert('form' in donation.location), 'Donation form not available'
    assert(amount == donation.current_amount), \
        f'{amount} expected, found {donation.current_amount}'

    # WHEN: they go back to the give page
    # AND:  enter a random amount (5 or greater)
    # AND:  click on the "donate!" button
    home = WebHome(selenium, web_base_url).open()
    if home.is_safari:
        home.reload()
    give = home.openstax_nav.view_donation_options()

    amount = Utility.random(start=Web.MIN_DONATION)
    give.form.other = amount

    donation = give.form.donate()

    # THEN: the "Donation Amount" shows the same amount
    assert(amount == donation.current_amount), \
        f'{amount} expected, found {donation.current_amount}'

    # WHEN: they fill out the donar input boxes
    # AND:  click on the "Continue" button
    if title:
        donation.title = title
    donation.first = first
    donation.last = last
    if suffix:
        donation.suffix = suffix
    donation.email = email
    donation.phone = phone
    donation.phone_type = phone_type
    donation.address = street
    donation.city = city
    donation.state = state
    donation.zip_code = zip_code
    donation.country = country

    donation.submit()

    # THEN: TouchNet's payment page is displayed
    assert('ebank' in donation.location or 'touchnet' in donation.location), \
        f'Not at TouchNet ({donation.location})'


@test_case('C210423')
@nondestructive
@web
def test_most_form_fields_are_required(web_base_url, selenium):
    """Most of the full form fields are required."""
    # GIVEN: a user viewing the give page
    home = WebHome(selenium, web_base_url).open()
    give = home.openstax_nav.view_donation_options()

    # WHEN: they click on the "donate!" button
    # AND:  click on the "Continue" button
    donation = give.form.donate()

    donation.submit()

    # THEN: "Please fill out this field." appears below
    #       "First Name", "Last Name", "Email", "Phone",
    #       "Phone Type", "Address", "City", and "Zip Code"
    # AND:  "Please select an item in the list." appears
    #       below "State" and "Country"
    errors = donation.get_errors()
    check_phrase = '{0}ill out this field{1}'.format(
        'F' if donation.is_safari else 'Please f',
        '' if donation.is_safari else '.')
    check_menu = '{0}elect an item in the list{1}'.format(
        'S' if donation.is_safari else 'Please s',
        '' if donation.is_safari else '.')

    inputs = ['First Name', 'Last Name', 'Email', 'Phone',
              'Phone Type', 'Address', 'City', 'Zip']
    for field in inputs:
        assert(f'{field}: {check_phrase}' in errors), \
            f'{field}: "{check_phrase}" not found in the error list'

    menus = ['State', 'Country']
    for field in menus:
        assert(f'{field}: {check_menu}' in errors), \
            f'{field}: "{check_menu}" not found in the error list'


@test_case('C210424')
@nondestructive
@web
def test_other_donation_methods_are_outlined(web_base_url, selenium):
    """Non-form donation mentods are discussed."""
    # GIVEN: a user viewing the give page
    home = WebHome(selenium, web_base_url).open()
    give = home.openstax_nav.view_donation_options()

    # WHEN:

    # THEN: sections for checks, gift matching, and other
    #       options are listed
    expected = ['Check', 'Amplify Your Donation With Matching Gifts',
                'Other Donation Options', 'We appreciate your support!']
    for option in give.options:
        assert(option.title in expected), \
            f'Unknown donation method: "{option.title}"'


@test_case('C210425')
@nondestructive
@web
def test_users_with_questions_are_directed_to_the_contact_form(
        web_base_url, selenium):
    """Donation questions are referred to the contact form."""
    # GIVEN: a user viewing the give page
    home = WebHome(selenium, web_base_url).open()
    give = home.openstax_nav.view_donation_options()

    # WHEN: they click on the "CONTACT US FOR HELP WITH YOUR
    #       GIFT" button
    contact = give.contact_us()

    # THEN: the contact form is diplayed
    # AND:  the subject is preset to "Donations"
    assert(contact.is_displayed()), 'Contact page not displayed'
    assert('contact' in contact.location), \
        f'Not viewing the contact page ({contact.location})'

    assert('Donations' in contact.location), \
        f'"Donations" expected in the URL ({contact.location})'
    assert('Donations' in contact.form.topic), \
        f'"Donations" not found in the form topic: {contact.form.topic}'
