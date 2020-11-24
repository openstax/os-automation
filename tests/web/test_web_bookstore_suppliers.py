"""Test the bookstore suppliers page."""

from pages.web.home import WebHome
from tests.markers import nondestructive, test_case, web
from utils.utilities import Utility


@test_case('C210466')
@nondestructive
@web
def test_users_are_directed_to_the_subjects_page(web_base_url, selenium):
    """Instructors and students are directed to the Subjects page."""
    # GIVEN: a user viewing the bookstore page
    home = WebHome(selenium, web_base_url).open()
    suppliers = home.openstax_nav.view_bookstores()

    # WHEN: they click on the "Subjects page" link
    subjects = suppliers.subjects_page()

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
    suppliers = home.openstax_nav.view_bookstores()

    for price_list in suppliers.price_lists:
        # WHEN: they click on the "View" button for each price list
        country = price_list.country
        list_pdf_passed = Utility.test_url_and_warn(
            url=price_list.url,
            message=f'{country} retail price list PDF',
            driver=selenium)

        # THEN: the file is downloaded
        assert(list_pdf_passed), f'the {country} PDF download URL failed'


@test_case('C210468')
@nondestructive
@web
def test_there_is_one_preferred_book_fulfillment_company(
        web_base_url, selenium):
    """One book fulfillment company is listed as preferred."""
    # GIVEN: a user viewing the bookstore page
    home = WebHome(selenium, web_base_url).open()
    suppliers = home.openstax_nav.view_bookstores()

    # WHEN:

    # THEN: one company is listed as the 'preferred provider'
    assert(suppliers.preferred_provider), 'preferred provider not found'
    assert(suppliers.preferred_provider.name == 'XanEdu'), \
        f'wrong provider listed ({suppliers.preferred_provider.name})'

    # WHEN: they click the 'Order from XanEdu' button
    xanedu_passed = Utility.test_url_and_warn(
        url=suppliers.preferred_provider.url,
        message='XanEdu',
        driver=selenium)

    # THEN: the preferred provider site is available
    assert(xanedu_passed), 'failed to verify XanEdu'


@test_case('C210469')
@nondestructive
@web
def test_there_are_four_additional_provider_options(web_base_url, selenium):
    """Four additional companies are available for bookstore orders."""
    # GIVEN: a user viewing the bookstore page
    home = WebHome(selenium, web_base_url).open()
    suppliers = home.openstax_nav.view_bookstores()

    # WHEN:

    # THEN: there are four additional book purchase options
    providers = [provider.name for provider in suppliers.other_providers]
    assert(len(providers) == 4), \
        f'unexpected number of providers ({", ".join(providers)})'

    for provider in suppliers.other_providers:
        # WHEN: they test the "Order from <provider>" button
        provider_passed = Utility.test_url_and_warn(
            url=provider.url, message=provider.name, driver=selenium)

        # THEN: the provider site is verified as working
        assert(provider_passed), f'failed to verify {provider.name}'
