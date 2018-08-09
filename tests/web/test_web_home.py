"""Tests for the OpenStax home webpage."""

import pytest

from pages.web.home import WebHome as Home
from tests.markers import expected_failure, nondestructive, test_case, web


@test_case()
@web
@expected_failure
def test_top_navigation_bar_present(web_base_url, selenium):
    """Test if the top navigation bar is present."""
    # GIVEN: On the OpenStax homepage
    page = Home(selenium, web_base_url).open()

    # THEN: Page with navigation bar with about us,
    # supporters, blog, give, help, Rice logo is displayed    
    assert (page.header.is_header_displayed()), 'Header is not displayed'



@test_case()
@web
@expected_failure
def test_top_navigation_bar(web_base_url, selenium):
    """Test if the top navigation bar is working."""
    # GIVEN: On the OpenStax homepage
    # WHEN: On top of the page, click About us.
    # THEN: User is taken to the About us page
    page = Home(selenium, web_base_url).open()
    # method for click "about us" goes in web_base model for header
    page.header.click_about_us()
    assert ('about' in page.current_url), 'Header does not work properly'



@test_case()
@web
@expected_failure
def test_supporter_button(web_base_url, selenium):
    """Test if the supporter button is working."""
    # GIVEN: On the OpenStax homepage
    # WHEN: On top of the page, click Supporters.
    # THEN: User is taken to the Supporters page
    page = Home(selenium, web_base_url).open()
    # method for click supporter button goes in web_base model for header
    page.header.click_supporter()
    assert ('foundation' in page.current_url), 'Header does not work properly'


@test_case()
@web
@expected_failure
def test_blog_button(web_base_url, selenium):
    """Test if the blog button is working."""
    # GIVEN: On the OpenStax homepage
    # WHEN: On top of the page, click Supporters.
    # THEN: User is taken to the Supporters page
    page = Home(selenium, web_base_url).open()
    # method for click blog goes in web_base model for header
    page.header.click_blog()
    assert ('blog' in page.current_url), 'Header does not work properly'


@test_case()
@web
@expected_failure
def test_give(web_base_url, selenium):
    """Test if the nav bar is present when screen size reduced."""
    # GIVEN: On the OpenStax homepage
    # WHEN: On top of the page, click on Give button
    # THEN: User is taken to the Give page
    page = Home(selenium, web_base_url).open()
    # method for click give goes in web_base model for header
    page.header.click_give()
    assert ('give' in page.current_url), 'Header does not work properly'


@test_case()
@web
@expected_failure
def test_help(web_base_url, selenium):
    """Test if the nav bar is present when screen size is maxed."""
    # GIVEN: On the OpenStax homepage
    # WHEN: On top of the page, find the top navigation bar
    # AND: Click on help button
    # THEN: User is taken to the Help page
    page = Home(selenium, web_base_url).open()
    # method for click help goes in web_base model for header
    page.header.click_help()
    assert ('help' in page.current_url), 'Header does not work properly'


@test_case()
@web
@expected_failure
def test_rice_logo_on_nav(web_base_url, selenium):
    """Test if rice logo link works on nav bar."""
    # GIVEN: On the OpenStax homepage
    # WHEN: On top of the page, click Rice logo
    # THEN: User is taken to the Rice home page
    page = Home(selenium, web_base_url).open()
    # method for click rice icon goes in web_base model
    page.click_rice()
    assert ('rice' in page.current_url), 'Rice logo does not work properly'


@test_case()
@web
@expected_failure
def test_nav_components(web_base_url, selenium):
    """Test if the nav bar is visible and contains all the components."""
    # GIVEN: On the OpenStax homepage
    # THEN: Page with white navigation bar with Openstax logo with statement
    # "Access. The future of education.", Subjects,
    # Technology, Our Impact, Login is loaded
    page = Home(selenium, web_base_url).open()
    # method for check 'Our Impact' goes in web_base model
    assert (page.is_impact_displayed()), 'Nav components is not displayed'


@test_case()
@web
@expected_failure
def test_our_impact(web_base_url, selenium):
    """Test if our impact works properly on navbar."""
    # GIVEN: On the OpenStax homepage
    # WHEN: Find "Using OpenStax in User's course again this semester?"
    # and click "Let us know"
    # AND: Go to top of the page, and click "Our Impact"
    # on the OpenStax nav bar
    # THEN: Once clicking "Let us know", a different page is loaded,
    # and the navigation bar should still be visible.
    # AND: When clicking "Our Impact", impact page with information about
    # affiliated schools is loaded.
    page = Home(selenium, web_base_url).open()
    # method for click 'Our Impact' goes in web_base model
    page.click_impact()
    assert ('impact' in page.current_url), 'Our Impact does not work properly'


@test_case()
@web
@expected_failure
def test_drop_down_list_when_decreased(web_base_url, selenium):
    """Test if drop down list is working on decreased window size."""
    # GIVEN: On the OpenStax homepage
    # WHEN: Decrease the window size until some of
    # the OpenStax navigation bar disappears
    # AND: Click on the dropdown list on the right
    # side of the navigation bar
    # THEN: A screen pop up with components that
    # are originally in the navigation bar including
    # Subjects, Technology, Our Impact, Login is displayed
    page = Home(selenium, web_base_url).open()
    # method for decrease window size goes in web_base model
    page.decrease_size()
    # method for click drop down list goes in web_base model
    page.click_drop_down()
    # method for test if 'Subjects' is displayed goes in web-base 
    assert (page.subjects_displayed), 'Drop down list not working'


@test_case()
@web
@expected_failure
def test_footer_displayed(web_base_url, selenium):
    """Test if footer is properly displayed on homepage."""
    # GIVEN: On the OpenStax homepage
    # WHEN: Go to the bottom of the page where user
    # can see the footer with dark background
    # THEN: "Access. The future of education" is visible.
    # AND: Below, Licensing, Terms of Use, Privacy Policy,
    # Accessibility Statement,
    # Open Source Code, Contact Us, Press Kit, Newsletter is visible.
    # AND: Below, short introduction and information
    # about Rice and AP is visible.
    # AND: Below, Facebook, Twitter, and Linkedin's logos are visible.
    page = Home(selenium, web_base_url).open()
    assert (page.footer.is_footer_displayed), 'footer is not displayed'


@test_case()
@web
@expected_failure
def test_terms_of_use(web_base_url, selenium):
    """Test if terms of use link works."""
    # GIVEN: On the OpenStax homepage
    # WHEN: Go to bottom of the page and click on
    # Terms of use in the footer with dark background
    # THEN:  Terms of use page is loaded.
    page = Home(selenium, web_base_url).open()
    # method for clicking terms of use goes into web.base model footer
    page.footer.terms_of_use()
    assert ('tos' in page.current_url), 'terms of use is not displayed'


@test_case()
@web
@expected_failure
def test_accessiblity(web_base_url, selenium):
    """Test if accessiblity works properly."""
    # GIVEN: On the OpenStax homepage
    # WHEN: Go to bottom of the page and click on Accessibility
    # statement in the footer with dark background
    # THEN: Accessibility statement in the footer is displayed
    page = Home(selenium, web_base_url).open()
    # method for clicking accessiblity goes into web.base model footer
    page.footer.accessiblity()
    assert ('accessiblity' in page.current_url), 'accessiblity is not displayed'


@test_case()
@web
@expected_failure
def test_privacy_policy(web_base_url, selenium):
    """Test if privacy policy works properly."""
    # GIVEN: On the OpenStax homepage
    # WHEN: Go to bottom of the page and click on
    # privacy policy in the footer with dark background
    # THEN: Privacy page is displayed.
    page = Home(selenium, web_base_url).open()
    # method for clicking privacy goes into web.base model footer
    page.footer.privacy()
    assert ('privacy' in page.current_url), 'privacy is not displayed'


@test_case()
@web
@expected_failure
def test_open_source(web_base_url, selenium):
    """Test if open source works properly."""
    # GIVEN: On the OpenStax homepage
    # WHEN: Go to bottom of the page and
    # click on Open Source in the footer with dark background
    # THEN: Open Source page is loaded
    page = Home(selenium, web_base_url).open()
    # method for clicking open source goes into web.base model footer
    page.footer.open_source()
    assert ('github' in page.current_url), 'opensource is not displayed'


@test_case()
@web
@expected_failure
def test_press_kit(web_base_url, selenium):
    """Test if the press kit works properly."""
    # GIVEN: On the OpenStax homepage
    # WHEN: Go to bottom of the page and click
    # on press kit in the footer with dark background
    # THEN: Press kit page is loaded
    page = Home(selenium, web_base_url).open()
    # method for clicking press kit goes into web.base model footer
    page.footer.press()
    assert ('press' in page.current_url), 'press kit is not displayed'


@test_case()
@web
@expected_failure
def test_newsletter(web_base_url, selenium):
    """Test if newsletter works properly."""
    # GIVEN: On the OpenStax homepage
    # WHEN: Go to bottom of the page and click on
    # newsletter in the footer with dark background
    # THEN: Newsletter of Openstax is loaded
    page = Home(selenium, web_base_url).open()
    # method for clicking press kit goes into web.base model footer
    page.footer.newsletter()
    assert ('www2' in page.current_url), 'Newsletter is not displayed'


@test_case()
@web
@expected_failure
def test_contact_hyperlink(web_base_url, selenium):
    """Test if contacy hyperlink works properly."""
    # GIVEN: On the OpenStax homepage
    # WHEN: Go to bottom of the page and click on
    # Contact us in the footer with dark background
    # THEN:  Openstax contact page is loaded.
    page = Home(selenium, web_base_url).open()
    # method for clicking contact us goes into web.base model
    page.footer.contact_us()
    assert ('contact' in page.current_url), 'Contact us is not displayed'
    


@test_case()
@web
@expected_failure
def test_facebook(web_base_url, selenium):
    """Test facebook link."""
    # GIVEN: On the OpenStax homepage
    # WHEN: Go to bottom of the page and click on Facebook
    # logo in the footer with dark background
    # THEN: OpenStax official facebook page is loaded
    page = Home(selenium, web_base_url).open()
    # method for clicking facebook goes into web.base model
    page.footer.facebook()
    assert ('facebook' in page.current_url), 'Facebook is not displayed'


@test_case()
@web
@expected_failure
def test_linkedin(web_base_url, selenium):
    """Test linkedin link."""
    # GIVEN: On the OpenStax homepage
    # WHEN: Go to bottom of the page and
    # click on Linkedin logo in the footer with dark background
    # THEN: Openstax official linkedin page is loaded
    page = Home(selenium, web_base_url).open()
    # method for clicking linkedin goes into web.base model
    page.footer.linkedin()
    assert ('link' in page.current_url), 'Linkedin is not displayed'


@test_case()
@web
@expected_failure
def test_twitter(web_base_url, selenium):
    """Test twitter link."""
    # GIVEN: On the OpenStax homepage
    # WHEN: Go to bottom of the page and click on
    # Twitter logo in the footer with dark background
    # THEN: OpenStax official Twitter page is loaded.
    page = Home(selenium, web_base_url).open()
    # method for clicking linkedin goes into web.base model
    page.footer.twitter()
    assert ('twitter' in page.current_url), 'twitter is not displayed'


@test_case()
@web
@expected_failure
def test_donation_banner(web_base_url, selenium):
    """Test the persence of donation banner."""
    # GIVEN: On the OpenStax homepage
    # WHEN: Reload the page 5 more times
    # THEN: The orange Give Now sticky is visible every time except the last


@test_case()
@web
@expected_failure
def test_banner(web_base_url, selenium):
    """Test if banner is present."""
    # GIVEN: On the OpenStax homepage
    # WHEN: On the OpenStax homepage
    # THEN: Banner is visible and should switch every few seconds
    page = Home(selenium, web_base_url).open()
    # method for banner goes into web.base model
    assert (page.banner()), 'banner is not displayed'


@test_case()
@web
@expected_failure
def test_quotes(web_base_url, selenium):
    """Test if quotes by prof are present."""
    # GIVEN: On the OpenStax homepage
    # WHEN: On the OpenStax homepage
    # THEN: Homepage displays a quote from one of our textbook heroes
    page = Home(selenium, web_base_url).open()
    # method for quotes goes into web.base model
    assert (page.quote()), 'quote is not displayed'


@test_case()
@web
@expected_failure
def test_suscribe_form(web_base_url, selenium):
    """Test if suscribe form is present."""
    # GIVEN: On the OpenStax homepage
    # WHEN: On the OpenStax homepage
    # THEN: Users is able to access the subscribe form from the homepage.
    # AND: Clicking on "Subscribe" takes them to the renewal form.
    page = Home(selenium, web_base_url).open()
    # method for clicking subscribe goes into web.base model
    page.suscribe()
    assert ('www2' in page.current_url), 'suscribe is not displayed'


@test_case()
@web
@expected_failure
def test_renewal(web_base_url, selenium):
    """Test if renewal form is present."""
    # GIVEN: On the OpenStax homepage
    # WHEN: On the OpenStax homepage
    # THEN: Faculty is able to access the renewal form from the homepage.
    # AND: Clicking on Let Us Know takes them to the renewal form
    page = Home(selenium, web_base_url).open()
    # method for clicking let us know goes into web.base model
    page.let_us_know()
    assert ('adopt' in page.current_url), 'renewal is not displayed'
=======


@test_case()
@web
@expected_failure
def test_homepage_reduced(web_base_url, selenium):
    """Test if homepage is displayed on reduced screen size."""
    # GIVEN: On the OpenStax homepage
    # WHEN: Reduce screen size
    # THEN: All elements are present on the reduced size


@test_case()
@web
@expected_failure
def test_hamburger_menu(web_base_url, selenium):
    """Test if hamburger menu is present on reduced screen size."""
    # GIVEN: On the OpenStax homepage
    # WHEN: Reduce screen size
    # THEN: The header collapses into a hamburger menu


@test_case()
@web
@expected_failure
def test_contact_us(web_base_url, selenium):
    """Test if contact us page is visible."""
    # GIVEN: On the OpenStax homepage
    # WHEN: Go to bottom of the page and
    # click on contact us in the footer with dark background
    # THEN: Contact page is loaded.


@test_case()
@web
@expected_failure
def test_info_send_when_not_filled(web_base_url, selenium):
    """Test if info is sent when not all info is filled."""
    # GIVEN: On the OpenStax homepage
    # WHEN: Go to bottom of the page and
    # click on contact us in the footer with dark background
    # AND: Click orange send button
    # THEN: The message should not send
    # AND: String "Please fill out this field" should be displayed where the
    # input boxes are empty
    page = Home(selenium, web_base_url).open()
    # go to contact us page is done in web.base
    page.contact_us()
    # clicking send goes in web.base
    page.click_send()
    # please fill out this page's display method is on web.base
    assert (page.fill_out_prompt), "the prompt does not show"


@test_case()
@web
@expected_failure
def test_alpha(web_base_url, selenium):
    """Test entering an alpha character takes user to the first item."""
    # GIVEN: On the OpenStax homepage
    # WHEN: Click Give link/ Give banner
    # AND: Select a donation amount and click the donate button
    # AND: Type an alpha key when in the country or state drop down
    # THEN: First state or country that starts with the letter they typed is
    # displayed.
    page = Home(selenium, web_base_url).open()
    # click give goes in web.base
    page.give()
    # enter donation amount goes in web.base
    page.enter_amount()
    # click donate goes in web.base
    page.click_donate()
    # entering "c" is done in web.base
    page.enter_c()
    # checking display of cambodia in web.base
    assert (page.cambodia_displayed()), "alpha does not work well "


@test_case()
@web
@expected_failure
def test_donation_fields(web_base_url, selenium):
    """Test if donation field is required."""
    # GIVEN: On the OpenStax homepage
    # WHEN: Click on the give link
    # AND: Select price user'd like to donate and click the donate button
    # AND: Fill out required fields
    # THEN: User should be able to submit the form
    # by filling out the entire form minus title
    page = Home(selenium, web_base_url).open()
    # click give goes in web.base
    page.give()
    # enter donation amount goes in web.base
    page.enter_amount()
    # click donate goes in web.base
    page.click_donate()
    # fill everything except title goes in web.base
    page.fill_form_except_title()
    # submit goes in web.base
    assert (page.submit_suscess()), "unable to submit the form"


@test_case()
@web
@expected_failure
def test_navigate_to_all_subjects(web_base_url, selenium):
    """Test if user could navigate to all subjects from home."""
    # GIVEN: On the OpenStax homepage
    # WHEN: Click "Subject" on the top right to open the drop down menu
    # AND: Click "All"
    # THEN: All textbooks -- math, science, humanities, AP, etc. is displayed
    page = Home(selenium, web_base_url).open()
    page.go_all()
    assert ("subjects" in page.current_url), "not at the all subjects page"


@test_case()
@web
@expected_failure
def test_navigate_to_ap_subjects(web_base_url, selenium):
    """Test if user could navigate to ap subjects from home."""
    # GIVEN: On the OpenStax homepage
    # WHEN: Click "Subject" on the top right to open the drop down menu
    # AND: Click "AP"
    # THEN: ap textbooks are displayed
    page = Home(selenium, web_base_url).open()
    page.go_ap()
    assert ("AP" in page.current_url), "not at the AP page"


@test_case()
@web
@expected_failure
def test_navigate_to_math_subjects(web_base_url, selenium):
    """Test if user could navigate to math subjects from home."""
    # GIVEN: On the OpenStax homepage
    # WHEN: Click "Subject" on the top right to open the drop down menu
    # AND: Click "Math"
    # THEN: math textbooks are displayed
    page = Home(selenium, web_base_url).open()
    page.go_math()
    assert ("math" in page.current_url), "not at the math page"


@test_case()
@web
@expected_failure
def test_navigate_to_soci_subjects(web_base_url, selenium):
    """Test if user could navigate to all subjects from home."""
    # GIVEN: On the OpenStax homepage
    # WHEN: Click "Subject" on the top right to open the drop down menu
    # AND: Click "Social Science"
    # THEN: Soci textbooks are displayed
    page = Home(selenium, web_base_url).open()
    page.go_soci()
    assert ("social" in page.current_url), "not at the soci page"


@test_case()
@web
@expected_failure
def test_navigate_to_humanities_subjects(web_base_url, selenium):
    """Test if user could navigate to all subjects from home."""
    # GIVEN: On the OpenStax homepage
    # WHEN: Click "Subject" on the top right to open the drop down menu
    # AND: Click "Humanites"
    # THEN:  Humanites textbooks are displayed
    page = Home(selenium, web_base_url).open()
    page.go_huma()
    assert ("humanities" in page.current_url), "not at the humanities page"


@test_case()
@web
@expected_failure
def test_navigate_to_science_subjects(web_base_url, selenium):
    """Test if user could navigate to all subjects from home."""
    # GIVEN: On the OpenStax homepage
    # WHEN: Click "Subject" on the top right to open the drop down menu
    # AND: Click "Science"
    # THEN: Sciences textbooks displayed
    page = Home(selenium, web_base_url).open()
    page.go_sci()
    assert ("science" in page.current_url), "not at the science page"
