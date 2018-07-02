"""Tests for the OpenStax home webpage."""

from tests.markers import expected_failure, nondestructive, test_case, web


@test_case()
@web
@expected_failure
def test_top_navigation_bar_present(web_base_url, selenium):
    """Test if the top navigation bar is present."""
    # GIVEN: On the OpenStax homepage
    # THEN: Page with navigation bar with about us,
    # supporters, blog, give, help, Rice logo is displayed


@test_case()
@web
@expected_failure
def test_top_navigation_bar(web_base_url, selenium):
    """Test if the top navigation bar is working."""
    # GIVEN: On the OpenStax homepage
    # WHEN: On top of the page, click About us.
    # THEN: User is taken to the About us page


@test_case()
@web
@expected_failure
def test_supporter_button(web_base_url, selenium):
    """Test if the supporter button is working."""
    # GIVEN: On the OpenStax homepage
    # WHEN: On top of the page, click Supporters.
    # THEN: User is taken to the Supporters page


@test_case()
@web
@expected_failure
def test_blog_button(web_base_url, selenium):
    """Test if the blog button is working."""
    # GIVEN: On the OpenStax homepage
    # WHEN: On top of the page, click Supporters.
    # THEN: User is taken to the Supporters page


@test_case()
@web
@expected_failure
def test_nav_bar_when_reduced(web_base_url, selenium):
    """Test if the nav bar is present when screen size reduced."""
    # GIVEN: On the OpenStax homepage
    # WHEN: On top of the page, click on Give button
    # THEN: User is taken to the Give page


@test_case()
@web
@expected_failure
def test_nav_bar_when_maxed(web_base_url, selenium):
    """Test if the nav bar is present when screen size is maxed."""
    # GIVEN: On the OpenStax homepage
    # WHEN: On top of the page, find the top navigation bar
    # AND: Click on help button
    # THEN: User is taken to the Help page


@test_case()
@web
@expected_failure
def test_rice_logo_on_nav(web_base_url, selenium):
    """Test if rice logo link works on nav bar."""
    # GIVEN: On the OpenStax homepage
    # WHEN: On top of the page, click Rice logo
    # THEN: User is taken to the Rice home page


@test_case()
@web
@expected_failure
def test_nav_components(web_base_url, selenium):
    """Test if the nav bar is visible and contains all the components."""
    # GIVEN: On the OpenStax homepage
    # THEN: Page with white navigation bar with Openstax logo with statement
    # "Access. The future of education.", Subjects,
    # Technology, Our Impact, Login is loaded


@test_case()
@web
@expected_failure
def test_subject_tech_drop_down_list(web_base_url, selenium):
    """Test if hovering over subjects or tech creates a drop down list."""
    # GIVEN: On the OpenStax homepage
    # WHEN: Decrease the screen size
    # THEN: OpenStax navigation bar goes to the top of the page, and
    # all components are invisible except the Openstax logo on the left
    # side and a list logo on the right side.


@test_case()
@web
@expected_failure
def test_nav_bar_present_other_page(web_base_url, selenium):
    """Test if nav bar is present on page other than home page."""
    # GIVEN: On the OpenStax homepage
    # WHEN: Go to bottom of the page where it says "OpenStax Partners"
    # AND: Click on the partners
    # THEN: Partners page is loaded
    # AND: OpenStax navigation bar with Openstax logo on the top of the page
    # is displayed


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


@test_case()
@web
@expected_failure
def test_nav_bar_within_website(web_base_url, selenium):
    """Test if the nav bar stays within website."""
    # GIVEN: On the OpenStax homepage
    # WHEN: Go to books
    # THEN: Navigation bar on the home page is displayed, and also on the
    # books page.


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


@test_case()
@web
@expected_failure
def test_footer_adjust(web_base_url, selenium):
    """Test if footer adjusts properly as screen gets bigger."""
    # GIVEN: On the OpenStax homepage
    # WHEN: Go to Subjects page
    # AND: Go to Technology page
    # AND: Go to Sponsor page
    # THEN: In all the pages, on the bottom of the page, the footer with dark
    # background is visible.


@test_case()
@web
@expected_failure
def test_footer_all_page(web_base_url, selenium):
    """Test if footer is visible on all pages."""
    # GIVEN: On the OpenStax homepage
    # WHEN: Go to bottom of the page and click on
    # Terms of use in the footer with dark background
    # THEN:  Terms of use page is loaded.


@test_case()
@web
@expected_failure
def test_terms_of_use(web_base_url, selenium):
    """Test if terms of use link works."""
    # GIVEN: On the OpenStax homepage
    # WHEN: Go to bottom of the page and click on
    # Terms of use in the footer with dark background
    # THEN:  Terms of use page is loaded.


@test_case()
@web
@expected_failure
def test_accessiblity(web_base_url, selenium):
    """Test if accessiblity works properly."""
    # GIVEN: On the OpenStax homepage
    # WHEN: Go to bottom of the page and click on Accessibility
    # statement in the footer with dark background
    # THEN: Accessibility statement in the footer is displayed


@test_case()
@web
@expected_failure
def test_privacy_policy(web_base_url, selenium):
    """Test if privacy policy works properly."""
    # GIVEN: On the OpenStax homepage
    # WHEN: Go to bottom of the page and click on
    # privacy policy in the footer with dark background
    # THEN: Privacy page is displayed.


@test_case()
@web
@expected_failure
def test_open_source(web_base_url, selenium):
    """Test if open source works properly."""
    # GIVEN: On the OpenStax homepage
    # WHEN: Go to bottom of the page and
    # click on Open Source in the footer with dark background
    # THEN: Open Source page is loaded


@test_case()
@web
@expected_failure
def test_press_kit(web_base_url, selenium):
    """Test if the press kit works properly."""
    # GIVEN: On the OpenStax homepage
    # WHEN: Go to bottom of the page and click
    # on press kit in the footer with dark background
    # THEN: Press kit page is loaded


@test_case()
@web
@expected_failure
def test_newsletter(web_base_url, selenium):
    """Test if newsletter works properly."""
    # GIVEN: On the OpenStax homepage
    # WHEN: Go to bottom of the page and click on
    # newsletter in the footer with dark background
    # THEN: Newsletter of Openstax is loaded


@test_case()
@web
@expected_failure
def test_contact_hyperlink(web_base_url, selenium):
    """Test if contacy hyperlink works properly."""
    # GIVEN: On the OpenStax homepage
    # WHEN: Go to bottom of the page and click on
    # Contact us in the footer with dark background
    # THEN:  Openstax contact page is loaded.


@test_case()
@web
@expected_failure
def test_facebook(web_base_url, selenium):
    """Test facebook link."""
    # GIVEN: On the OpenStax homepage
    # WHEN: Go to bottom of the page and click on Facebook
    # logo in the footer with dark background
    # THEN: OpenStax official facebook page is loaded


@test_case()
@web
@expected_failure
def test_linkedin(web_base_url, selenium):
    """Test linkedin link."""
    # GIVEN: On the OpenStax homepage
    # WHEN: Go to bottom of the page and
    # click on Linkedin logo in the footer with dark background
    # THEN: Openstax official linkedin page is loaded


@test_case()
@web
@expected_failure
def test_twitter(web_base_url, selenium):
    """Test twitter link."""
    # GIVEN: On the OpenStax homepage
    # WHEN: Go to bottom of the page and click on
    # Twitter logo in the footer with dark background
    # THEN: OpenStax official Twitter page is loaded.


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


@test_case()
@web
@expected_failure
def test_quotes(web_base_url, selenium):
    """Test if quotes by prof are present."""
    # GIVEN: On the OpenStax homepage
    # WHEN: On the OpenStax homepage
    # THEN: Homepage displays a quote from one of our textbook heroes


@test_case()
@web
@expected_failure
def test_suscribe_form(web_base_url, selenium):
    """Test if suscribe form is present."""
    # GIVEN: On the OpenStax homepage
    # WHEN: On the OpenStax homepage
    # THEN: Users is able to access the subscribe form from the homepage.
    # AND: Clicking on "Subscribe" takes them to the renewal form.


@test_case()
@web
@expected_failure
def test_renewal(web_base_url, selenium):
    """Test if renewal form is present."""
    # GIVEN: On the OpenStax homepage
    # WHEN: On the OpenStax homepage
    # THEN: Faculty is able to access the renewal form from the homepage.
    # AND: Clicking on Let Us Know takes them to the renewal form


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
def test_navigate_to_all_subjects(web_base_url, selenium):
    """Test if user could navigate to all subjects from home."""
    # GIVEN: On the OpenStax homepage
    # WHEN: Click "Subject" on the top right to open the drop down menu
    # AND: Click "All"
    # THEN: All textbooks -- math, science, humanities, AP, etc. is displayed


@test_case()
@web
@expected_failure
def test_navigate_to_ap_subjects(web_base_url, selenium):
    """Test if user could navigate to ap subjects from home."""
    # GIVEN: On the OpenStax homepage
    # WHEN: Click "Subject" on the top right to open the drop down menu
    # AND: Click "AP"
    # THEN: ap textbooks are displayed


@test_case()
@web
@expected_failure
def test_navigate_to_math_subjects(web_base_url, selenium):
    """Test if user could navigate to math subjects from home."""
    # GIVEN: On the OpenStax homepage
    # WHEN: Click "Subject" on the top right to open the drop down menu
    # AND: Click "Math"
    # THEN: math textbooks are displayed


@test_case()
@web
@expected_failure
def test_navigate_to_soci_subjects(web_base_url, selenium):
    """Test if user could navigate to all subjects from home."""
    # GIVEN: On the OpenStax homepage
    # WHEN: Click "Subject" on the top right to open the drop down menu
    # AND: Click "Social Science"
    # THEN: Soci textbooks are displayed


@test_case()
@web
@expected_failure
def test_navigate_to_humanities_subjects(web_base_url, selenium):
    """Test if user could navigate to all subjects from home."""
    # GIVEN: On the OpenStax homepage
    # WHEN: Click "Subject" on the top right to open the drop down menu
    # AND: Click "Humanites"
    # THEN:  Humanites textbooks are displayed


@test_case()
@web
@expected_failure
def test_navigate_to_science_subjects(web_base_url, selenium):
    """Test if user could navigate to all subjects from home."""
    # GIVEN: On the OpenStax homepage
    # WHEN: Click "Subject" on the top right to open the drop down menu
    # AND: Click "Science"
    # THEN: Sciences textbooks displayed


@test_case()
@web
@expected_failure
def test_explore_subjects(web_base_url, selenium):
    """Test if the explore all subjects button works properly."""
    # GIVEN: On the OpenStax homepage
    # WHEN:  Click "Explore All subjects"
    # THEN: Textbooks of all subjects should be displayed


@test_case('')
@expected_failure
@nondestructive
@web
def test_view_home(web_base_url, selenium):
    """Tests ability view homepage from other pages."""
    # GIVEN: On the OpenStax homepage.

    # WHEN: Click "About Us".
    # AND: Click the OpenStax logo on the upper left corner.

    # THEN: On homepage.
