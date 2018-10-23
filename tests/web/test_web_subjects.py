"""Tests for the OpenStax Web subjects page."""

from pages.web.subjects import Subjects
from tests.markers import nondestructive, test_case, web


@test_case('C210343')
@nondestructive
@web
def test_the_subjects_page_loads(web_base_url, selenium):
    """Test if the OpenStax.org Subjects webpage loads."""
    # GIVEN: a web browser
    subjects = Subjects(selenium, web_base_url)

    # WHEN: a user opens the subjects webpage
    subjects.open()

    # THEN: the page loads
    assert(subjects.loaded), \
        '{page} did not load successfully'.format(page=web_base_url)


@test_case('C210344')
@nondestructive
@web
def test_able_to_filter_books_by_category(web_base_url, selenium):
    """Test a user's ability to filter books by category."""
    # GIVEN: a user viewing the subjects page
    subjects = Subjects(selenium, web_base_url).open()
    filter_list = [*(subjects.filters[1:])]
    subject_list = [
        subjects.math,
        subjects.science,
        subjects.social_sciences,
        subjects.humanities,
        subjects.business,
        subjects.ap
    ]

    for index in range(len(subject_list)):
        # WHEN: they click on a subject filter button
        filter_list[index].view_books()

        # THEN: that subject is displayed
        # AND:  the other subjects are not displayed
        assert(subject_list[index].is_visible)
        for other_index in range(len(subject_list)):
            if index != other_index:
                assert(not subject_list[other_index].is_visible), (
                    '{subject} not hidden'
                    .format(subject=subject_list[other_index].section))

    # WHEN: they click on the "View All" filter button
    subjects.filters[0].view_books()

    # THEN: all categories are displayed
    for subject in subject_list:
        assert(subject.is_visible), \
            '{subject} is not visible'.format(subject=subject.section)


@test_case('C210345')
@nondestructive
@web
def test_able_to_filter_books_by_category_using_the_drop_down_menu(
        web_base_url, selenium):
    """Test a user's ability to filter books by category using the menu."""
    # GIVEN: a user viewing the subjects page
    # AND:   the screen width is 960 pixels or less
    subjects = Subjects(selenium, web_base_url)
    subjects.resize_window(width=900)
    subjects.open()
    filter_list = [*(subjects.filters[1:])]
    subject_list = [
        subjects.math,
        subjects.science,
        subjects.social_sciences,
        subjects.humanities,
        subjects.business,
        subjects.ap
    ]

    for index in range(len(subject_list)):
        # WHEN: they click on the "Filter by:" drop down menu
        # AND:  select a subject menu option
        subjects.filter_toggle()
        filter_list[index].view_books()

        # THEN: that subject is displayed
        # AND:  the other subjects are not displayed
        assert(subject_list[index].is_visible)
        for other_index in range(len(subject_list)):
            if index != other_index:
                assert(not subject_list[other_index].is_visible), (
                    '{subject} not hidden'
                    .format(subject=subject_list[other_index].section))

    # WHEN: they click on the "Filter by:" drop down menu
    # AND:  select the "View All" menu option
    subjects.filter_toggle()
    subjects.filters[0].view_books()

    # THEN: all categories are displayed
    for subject in subject_list:
        assert(subject.is_visible), \
            '{subject} is not visible'.format(subject=subject.section)


@test_case('C210346')
@nondestructive
@web
def test_selecting_a_book_cover_opens_the_book_details_page(
        web_base_url, selenium):
    """Test clicking on a book cover opens the book's details page."""
    # GIVEN: a user viewing the subjects page
    subjects = Subjects(selenium, web_base_url).open()

    # WHEN: they click on a book cover
    book = subjects.select_random_book()

    # THEN: the book details page is displayed
    assert('details' in book.location)


@test_case('C210347')
@nondestructive
@web
def test_for_the_presence_of_the_book_production_overview_blurb(
        web_base_url, selenium):
    """Test for the presence of the textbook production overview."""
    # GIVEN: a user viewing the subjects page
    subjects = Subjects(selenium, web_base_url).open()

    # WHEN: they scroll to the "About Our Textbooks" section
    subjects.view_about_our_textbooks()

    # THEN: text blurbs describing the book production process are displayed
    assert('Expert Authors' in subjects.about[Subjects.AUTHORS].title and
           len(subjects.about[Subjects.AUTHORS].blurb) > 0)
    assert('Standard Scope and Sequence'
           in subjects.about[Subjects.SEQUENCE].title and
           len(subjects.about[Subjects.SEQUENCE].blurb) > 0)
    assert('Peer Reviewed' in subjects.about[Subjects.PEER_REVIEWED].title and
           len(subjects.about[Subjects.PEER_REVIEWED].blurb) > 0)
