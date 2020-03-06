"""Test the partners page."""

from pages.web.home import WebHome
from tests.markers import nondestructive, skip_test, test_case, web
from utils.utilities import Utility
from utils.web import TechProviders, Web


@skip_test(reason='partner tech scout replacement page')
@test_case('C210443')
@nondestructive
@web
def test_the_openstax_ally_logo_is_available(web_base_url, selenium):
    """An OpenStax Ally is identified by the Ally logo."""
    # GIVEN: a user viewing the partners page
    home = WebHome(selenium, web_base_url).open()
    partners = home.web_nav.technology.view_partners()

    # WHEN:

    # THEN: the OpenStax Ally logo is displayed
    assert(partners.is_displayed())
    assert(partners.logo.is_displayed())
    assert(Utility.is_image_visible(selenium, image=partners.logo))


@skip_test(reason='partner tech scout replacement page')
@test_case('C210444', 'C210445')
@nondestructive
@web
def test_able_to_filter_partners_by_category(web_base_url, selenium):
    """The user may filter partners using a drop down menu."""
    # GIVEN: a user viewing the partners page
    # AND:  the screen width is greater than the tablet view
    #       or less than the table view
    home = WebHome(selenium, web_base_url).open()
    partners = home.web_nav.technology.view_partners()
    for width in [Web.FULL, Web.TABLET]:
        if width != Web.FULL:
            partners.resize_window(width=width)

        # WHEN: they click on the "Filter by:" drop down menu
        # AND:  select the "View All" menu option
        partners.filter_by(Web.VIEW_ALL)

        # THEN: all partner logos are displayed
        for company in partners.companies:
            assert(company.name in TechProviders.tech_list)

        for option in Web.FILTERS:
            # WHEN: they click on the "Filter by:" drop down menu
            # AND:  select a subject menu option
            partners.filter_by(option)

            # THEN: that subject's partners are displayed
            # AND:  partners that do not support that subject's
            #       books are not displayed
            for company in partners.companies:
                assert(company.name in TechProviders.tech_list)


@skip_test(reason='partner tech scout replacement page')
@test_case('C210446')
@nondestructive
@web
def test_selecting_a_partner_logo_scrolls_to_the_partner_summary(
        web_base_url, selenium):
    """Clicking a partner logo scrolls the page to the partner summary."""
    # GIVEN: a user viewing the partners page
    home = WebHome(selenium, web_base_url).open()
    partners = home.web_nav.technology.view_partners()
    logo = partners.companies[Utility.random(end=len(partners.companies) - 1)]
    summary = partners.summary_by_name(logo.name)

    # WHEN: they click on a partner logo
    logo.view()

    # THEN: the page scrolls until the partner summary is displayed
    # AND:  the summary contains a partner description
    # AND:  supported subjects or books
    # AND:  a "Return to top" link
    assert(Utility.in_viewport(selenium,
                               element=summary.header,
                               ignore_bottom=True))
    assert(summary.description)
    if summary.name != TechProviders.OPEN_TEXTBOOK_NETWORK:
        # the partner supports one or more OpenStax titles/subjects
        assert(summary.availability)
    assert(summary.return_to_top_link)

    # WHEN: they click on the "Return to top" link
    summary.return_to_top()

    # THEN: the partner filter list is displayed
    assert(Utility.in_viewport(selenium, element=logo.logo))


@skip_test(reason='partner tech scout replacement page')
@test_case('C210447')
@nondestructive
@web
def test_supported_topics_link_to_the_subjects_page_or_a_book_details_page(
        web_base_url, selenium):
    """Clicking a supported content link loads the subject or book details."""
    # GIVEN: a user viewing the partners page
    home = WebHome(selenium, web_base_url).open()
    partners = home.web_nav.technology.view_partners()
    logo = partners.companies[Utility.random(end=len(partners.companies) - 1)]
    summary = partners.summary_by_name(logo.name)

    # WHEN: they view a partner summary
    logo.view()

    # THEN: "full catalog of content." links to the subjects
    #       page, "mathematics titles" links to the math
    #       subject page, or a collection of book titles
    #       linking to the respective book details page
    name = summary.name
    if name in TechProviders.full_catalog:
        assert(summary.availability[0]
               .get_attribute('href').endswith('/subjects')), \
            '{0} not linked to the Subjects page.'.format(name)
    elif name in TechProviders.math_titles:
        assert(summary.availability[0]
               .get_attribute('href').endswith('/math')), \
            '{0} not linked to the Subject math page.'.format(name)
    elif name in TechProviders.no_titles:
        assert(not summary.availability)
    else:
        assert(summary.availability), \
            '{0} missing resource availability'.format(name)
        for option in summary.availability:
            assert('/details' in option.get_attribute('href')), \
                '{0} not using "/details"'.format(option.text)
