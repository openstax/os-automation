"""Test the technology page."""

from pages.web.home import WebHome
from tests.markers import accounts, nondestructive, smoke_test  # NOQA
from tests.markers import test_case, tutor, web  # NOQA
from utils.utilities import Utility
from utils.web import Library, Web


@test_case('C210460')
@nondestructive
@web
def test_the_technology_summary_links_to_the_page_steps(
        web_base_url, selenium):
    """Test the anchor link in the summary moves to the page steps."""
    # GIVEN: a user viewing the technology page
    home = WebHome(selenium, web_base_url).open()
    technology = home.web_nav.technology.view_technology()

    # WHEN: they click on the "LEARN MORE" button
    technology.learn_more()

    # THEN: the resource selector is displayed
    assert(Utility.in_viewport(selenium,
                               element=technology.resources.title_box)), \
        'Book selection pull down menu not in the browser window'


@test_case('C210461')
@smoke_test
@nondestructive
@web
def test_able_to_view_instructor_resources_for_a_book(web_base_url, selenium):
    """Test select a book and click the view resources link."""
    # GIVEN: a user viewing the technology page
    home = WebHome(selenium, web_base_url).open()
    technology = home.web_nav.technology.view_technology()

    # WHEN: they select a book from the book drop down menu
    # AND:  click on the "View free instructor resources" link
    book = Library().random_book(full_name=True)
    technology.learn_more()
    technology.resources.select_book(book)
    details = technology.resources.view_instructor_resources()

    # THEN: the instructor resources section of the book
    #       details page is displayed in a new tab
    assert(details.is_displayed())
    assert(book in selenium.page_source)
    assert(details.tabs[Web.INSTRUCTOR_RESOURCES].is_displayed())


@test_case('C210462')
@smoke_test
@nondestructive
@web
def test_able_to_view_technology_options_for_a_book(web_base_url, selenium):
    """Test select a book and click the technology options link."""
    # GIVEN: a user viewing the technology page
    home = WebHome(selenium, web_base_url).open()
    technology = home.web_nav.technology.view_technology()

    # WHEN: they select a book from the book drop down menu
    # AND:  click on the "View technology options" link
    book = Library().random_book(full_name=True)
    technology.learn_more()
    technology.resources.select_book(book)
    details = technology.resources.view_technology_options()

    # THEN: the partner tools on the instructor resources
    #       section of the book details page is displayed
    #       in a new tab
    assert(details.is_displayed())
    assert(book in selenium.page_source)
    assert(details.tabs[Web.INSTRUCTOR_RESOURCES].is_displayed())
    assert(Utility.in_viewport(selenium,
                               element=details.instructor.tech_options)), \
        'Tech options not in the browser window'


@test_case('C210463')
@nondestructive
@web
def test_the_learn_more_button_loads_the_tutor_marketing_page_how_it_works(
        web_base_url, selenium):
    """Test clicking the Tutor 'Learn more' button loads the marketing page."""
    # GIVEN: a user viewing the technology page
    home = WebHome(selenium, web_base_url).open()
    technology = home.web_nav.technology.view_technology()

    # WHEN: they click on the "Learn more" button in the
    #       Tutor section
    marketing = technology.tutor.learn_more()

    # THEN: the "How it works" section on the Tutor
    #       marketing page is displayed
    assert(marketing.is_displayed())
    assert(Utility.in_viewport(selenium,
                               element=marketing.how_it_works.subheading)), \
        'Subheading not in the browser window'


@test_case('C210464')
@nondestructive
@tutor
@web
def test_the_go_to_tutor_button_loads_the_users_tutor_dashboard(
        tutor_base_url, web_base_url, selenium, teacher):
    """Test clicking the 'Go to OpenStax Tutor' button loads the dashboard."""
    # GIVEN: a user viewing the technology page
    # AND:  logged into the site with a Tutor user's
    #       account
    home = WebHome(selenium, web_base_url).open()
    home.web_nav.login.log_in(*teacher, destination=WebHome, url=web_base_url)
    home.web_nav.login.training_wheel.close_modal()
    technology = home.web_nav.technology.view_technology()

    # WHEN: they click on the "Go to OpenStax Tutor" button
    dashboard = technology.tutor.go_to_openstax_tutor(tutor_base_url)

    # THEN: the user's Tutor dashboard is displayed
    assert(dashboard.is_displayed())
    assert('dashboard' in dashboard.location)


@test_case('C210465')
@nondestructive
@accounts
@web
def test_the_go_to_tutor_button_loads_accounts_for_users_who_are_not_logged_in(
        accounts_base_url, web_base_url, selenium):
    """Test the 'Go to OpenStax Tutor' button opens Accounts."""
    # GIVEN: a user viewing the technology page
    # AND:  not logged into the site
    home = WebHome(selenium, web_base_url).open()
    technology = home.web_nav.technology.view_technology()

    # WHEN: they click on the "Go to OpenStax Tutor" button
    accounts = technology.tutor.go_to_openstax_tutor(accounts_base_url)

    # THEN: the Accounts log in page is displayed
    assert(accounts.is_displayed())
    assert('login' in accounts.location)
