"""Test the legal / intellectual property FAQ."""

from pages.web.home import WebHome
from tests.markers import nondestructive, test_case, web
from utils.utilities import Utility


@test_case('C210435', 'C210436')
@nondestructive
@web
def test_each_intellectual_property_question_has_an_answer(
        web_base_url, selenium):
    """Each topic consists of a question and an associated answer."""
    # GIVEN: a user viewing the legal page
    home = WebHome(selenium, web_base_url).open()
    license = home.footer.directory.licensing()

    # WHEN:

    # THEN: each question is followed by an answer
    for question in license.questions:
        assert(question.question)
        assert(question.answer)

    # WHEN: they click on the "Creative Commons" link

    # THEN: the Creative Commons website is available
    Utility.test_url_and_warn(link=license.creative_commons,
                              message='Creative Commons',
                              driver=selenium)

    # WHEN: they click on the "Attribution license" link

    # THEN: the "Attribution 4.0 International" license
    #       overview is available
    Utility.test_url_and_warn(link=license.attribution_license,
                              message='CC BY 4.0 license',
                              driver=selenium)
