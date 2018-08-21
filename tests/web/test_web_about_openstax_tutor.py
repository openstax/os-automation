"""Tests the about OpenStax Tutor webpage."""

from tests.markers import nondestructive, skip_test, test_case, web


@test_case('')
@skip_test(reason='Script not written')
@nondestructive
@web
def test_view_about_tutor(web_base_url, selenium):
    """Tests ability to view about OpenStax tutor page."""
    # GIVEN: On the OpenStax homepage.

    # WHEN: Hover over "Technology".
    # AND: Click on "About OpenStax Tutor".

    # THEN: User is navigated to the about OpenStax tutor.


@test_case('')
@skip_test(reason='Script not written')
@nondestructive
@web
def test_scaling_about_tutor(web_base_url, selenium):
    """Tests ability to scale about OpenStax tutor page."""
    # GIVEN: On About OpenStax Tutor Page
    # WHEN: Change browser window size
    # THEN: All important elements present and scaled correctly
    # AND: All clickable elements still still usable


@test_case('')
@skip_test(reason='Script not written')
@nondestructive
@web
def test_access_your_course(web_base_url, selenium):
    """Tests ability access course."""
    # GIVEN: On About OpenStax Tutor Page
    # WHEN: Click on the button ACCESS YOUR COURSE
    # THEN: User will be redirected to tutor
    # AND: User will be shown a sign in page


@test_case('')
@skip_test(reason='Script not written')
@nondestructive
@web
def test_about_tutor_learn_more(web_base_url, selenium):
    """Tests about OpenStax tutor learn more button."""
    # GIVEN: On About OpenStax Tutor Page
    # WHEN: Click on Learn More
    # THEN: User should be auto scrolled to the How
    # does OpenStax Tutor Beta work section
    # AND: Footer should be visible where user should
    # see the options to get started or join a webinar section


@test_case('')
@skip_test(reason='Script not written')
@nondestructive
@web
def test_view_openstax_beta(web_base_url, selenium):
    """Tests ability to view OpenStax beta section of about tutor."""
    # GIVEN: On About OpenStax Tutor Page
    # WHEN: Scroll to the OpenStax Tutor Beta works section.
    # THEN: The following 4 icons are present in the order below:
    # "Spaced Practice", "Personalized questions",
    # "Two-step questions", "Low cost ($10 icon)"


@test_case('')
@skip_test(reason='Script not written')
@nondestructive
@web
def test_view_what_students_see(web_base_url, selenium):
    """Tests ability to view OpenStax beta section of about tutor."""
    # GIVEN: On About OpenStax Tutor Page
    # WHEN: Click through the tiles in what students see section
    # THEN:  The section should be present with proper content
    # AND: GIFs should automatically play
    # AND: Text under each screenshot
    # AND: Active tile has blue border


@test_case('')
@skip_test(reason='Script not written')
@nondestructive
@web
def test_view_current_future(web_base_url, selenium):
    """Tests ability to view current future plans section of about tutor."""
    # GIVEN: On About OpenStax Tutor Page
    # WHEN: Scroll to the section about current and future plans
    # THEN: The section should be present with proper content


@test_case('')
@skip_test(reason='Script not written')
@nondestructive
@web
def test_view_10dollars_toward(web_base_url, selenium):
    """Tests ability to view 10 dollar goes toward section of about tutor."""
    # GIVEN: On About OpenStax Tutor Page
    # WHEN: Scroll to the section explaining what the $10 goes towards
    # THEN: The section should be present with proper content


@test_case('')
@skip_test(reason='Script not written')
@nondestructive
@web
def test_view_faq_questions(web_base_url, selenium):
    """Tests ability to view faq questions section of about tutor."""
    # GIVEN: On About OpenStax Tutor Page
    # WHEN: Scroll to the FAQ section
    # AND: Click on the grey arrow icons
    # THEN: A question response should appear/disappear
