"""Test the FAQ page."""

from pages.web.home import WebHome
from tests.markers import nondestructive, smoke_test, test_case, web


@test_case('C210433')
@smoke_test
@nondestructive
@web
def test_users_with_unanswered_questions_are_directed_to_the_support_site(
        web_base_url, selenium):
    """Test each topic consists of a question and an associated answer."""
    # GIVEN: a user viewing the FAQ page
    home = WebHome(selenium, web_base_url).open()
    about = home.web_nav.openstax.view_about_us()
    faq = about.who_we_are.go_to_faq()

    # WHEN: they click on the "support page" link
    salesforce = faq.visit_support()

    # THEN: the support page is displayed in a new tab
    assert(salesforce.is_displayed())
    assert('force.com' in salesforce.location)


@test_case('C210434')
@nondestructive
@web
def test_each_topic_has_a_question_and_an_answer(web_base_url, selenium):
    """Test each topic consists of a question and an associated answer."""
    # GIVEN: a user viewing the FAQ page
    home = WebHome(selenium, web_base_url).open()
    about = home.web_nav.openstax.view_about_us()
    faq = about.who_we_are.go_to_faq()

    for question in faq.questions:
        # WHEN: they click on a question
        question.toggle()

        # THEN: the answer is displayed
        assert(question.question)
        assert(question.answer)
        assert(question.answer_is_visible)

        # WHEN: they click on the question again
        question.toggle()

        # THEN: the answer is hidden
        assert(not question.answer_is_visible)
