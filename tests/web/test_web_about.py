"""Tests for the OpenStax Web About Us page."""

from pages.web.about import AboutUs
from tests.markers import nondestructive, test_case, web
from utils.utilities import Utility

CARDS = 6
FIRST, SECOND, THIRD, FOURTH, FIFTH, SIXTH = range(CARDS)


@test_case('C210378')
@nondestructive
@web
def test_the_about_us_panels_load(web_base_url, selenium):
    """Test for the presence of the About Us sections."""
    # GIVEN: a user viewing the about page
    about = AboutUs(selenium, web_base_url).open()

    # WHEN:

    # THEN: the "Who we are" section is displayed
    # AND:  the "What we do" section is displayed
    # AND:  the "Where we're going" section is displayed
    # AND:  the stats map is displayed
    assert(about.who_we_are.is_displayed()), \
        '"Who we are" section not found'

    assert(about.what_we_do.is_displayed()), \
        '"What we do" section not found'

    assert(about.where_were_going.is_displayed()), \
        '"Where we\'re going" section not found'

    assert(about.content_map.is_displayed()), 'Map not found'


@test_case('C210379')
@nondestructive
@web
def test_who_we_are_links(web_base_url, selenium):
    """Test the links within the Who we are panel."""
    # GIVEN: a user viewing the about page
    about = AboutUs(selenium, web_base_url).open()

    # WHEN: they click on the "philanthropic foundations" link
    foundations = about.who_we_are.go_to_foundations()

    # THEN: the foundations page is displayed
    assert(foundations.is_displayed()), 'Foundations page not displayed'

    # WHEN: they return to the about page
    # AND:  click on the "educational resource companies" link
    about.open()

    resources = about.who_we_are.go_to_resources()

    # THEN: the partners page is displayed
    assert(resources.is_displayed()), \
        'Educational resources page not displayed'

    # WHEN: they return to the about page
    # AND:  click on the "FAQ page" link
    about.open()

    faq = about.who_we_are.go_to_faq()

    # THEN: the faq page is displayed
    assert(faq.is_displayed()), 'FAQ page not displayed'


@test_case('C210380')
@nondestructive
@web
def test_what_we_do_links(web_base_url, selenium):
    """Test the links within the What we do panel."""
    # GIVEN: a user viewing the about page
    about = AboutUs(selenium, web_base_url).open()

    # WHEN: they click on the "current library" link
    subjects = about.what_we_do.go_to_library()

    # THEN: the subjects page is displayed
    assert(subjects.is_displayed())

    # WHEN: they return to the about page
    # AND:  click on the "OpenStax Tutor Beta" link
    about.open()

    tutor_marketing = about.what_we_do.go_to_tutor_marketing()

    # THEN: the Tutor marketing page is displayed
    assert(tutor_marketing.is_displayed())


@test_case('C210381')
@nondestructive
@web
def test_what_we_do_information_cards(web_base_url, selenium):
    """Test the information cards in the What we do panel."""
    # GIVEN: a user viewing the about page
    about = AboutUs(selenium, web_base_url).open()

    # WHEN: they scroll to the "What we do" cards
    Utility.scroll_to(selenium, element=about.what_we_do.root)

    # THEN: four information cards are displayed
    assert(len(about.what_we_do.cards) == CARDS), \
        f'Expected {CARDS} cards, found {len(about.what_we_do.cards)}'

    # WHEN: they click on the first card
    subjects = about.what_we_do.cards[FIRST].click()

    # THEN: the subjects page is displayed
    assert(subjects.is_displayed()), \
        f'{selenium.current_url} is not the Subjects page'

    # WHEN: they return to the about page
    # AND:  click on the second card
    about.open()

    research = about.what_we_do.cards[SECOND].click()

    # THEN: the research page is displayed
    assert(research.is_displayed()), \
        f'{selenium.current_url} is not the Research page'

    # WHEN: they return to the about page
    # AND:  click on the third card
    about.open()

    institutional_partners = about.what_we_do.cards[THIRD].click()

    # THEN: the Tutor marketing page is displayed
    assert(institutional_partners.is_displayed()), \
        f'{selenium.current_url} is not the institutional partners page'

    # WHEN: they return to the about page
    # AND:  click on the fourth card
    about.open()

    partners = about.what_we_do.cards[FOURTH].click()

    # THEN: the partners page is displayed
    assert(partners.is_displayed()), \
        f'{selenium.current_url} is not the Partners page'

    # WHEN: they return to the about page
    # AND:  click on the fifth card
    about.open()

    tutor_marketing = about.what_we_do.cards[FIFTH].click()

    # THEN: the Tutor marketing page is displayed
    assert(tutor_marketing.is_displayed()), \
        f'{selenium.current_url} is not the Tutor marketing page'

    # WHEN: they return to the about page
    # AND:  click on the sixth card
    about.open()

    rover = about.what_we_do.cards[SIXTH].click()

    # THEN: the Rover marketing page is displayed
    assert(rover.is_displayed()), \
        f'{selenium.current_url} is not the Rover marketing page'


@test_case('C210382')
@nondestructive
@web
def test_where_were_going_links(web_base_url, selenium):
    """Test the links within the Where we're going panel."""
    # GIVEN: a user viewing the about page
    about = AboutUs(selenium, web_base_url).open()

    # WHEN: they click on the "improving student learning" link
    tutor_marketing = about.where_were_going.go_to_student_learning()

    # THEN: the Tutor marketing page is displayed
    assert(tutor_marketing.is_displayed()), \
        'Tutor marketing page not displayed'

    # WHEN: they return to the about page
    # AND:  click on the "research in learning science" link
    about.open()

    research = about.where_were_going.go_to_research()

    # THEN: the research page is displayed
    assert(research.is_displayed()), 'Research page not displayed'
