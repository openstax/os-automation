"""Test the OpenStax Tutor Beta marketing page."""

from pages.web.home import WebHome
from tests.markers import accounts, nondestructive, skip_test, smoke_test, test_case, tutor, web  # NOQA
from utils.utilities import Utility


@test_case('C210490')
@smoke_test
@nondestructive
@tutor
@web
def test_tutor_users_may_access_their_course_from_the_marketing_page(
        tutor_base_url, web_base_url, selenium, teacher):
    """Current Tutor users may access their dashboard from the page."""
    # GIVEN: a user viewing the Tutor marketing page
    # AND:  logged into the site with a current Tutor user
    home = WebHome(selenium, web_base_url).open()
    home.web_nav.login.log_in(*teacher)
    tutor_marketing = home.web_nav.technology.view_tutor()

    # WHEN: they click on the "Access Your Course" button
    dashboard = tutor_marketing.introduction.access_your_course(tutor_base_url)

    # THEN: the Tutor dashboard for the user is displayed in a new tab
    assert(dashboard.is_displayed())
    assert('dashboard' in dashboard.location)


@test_case('C210491')
@nondestructive
@accounts
@web
def test_logged_out_users_are_sent_to_accounts_to_log_in_to_view_dashboard(
        accounts_base_url, web_base_url, selenium):
    """Logged out users are sent to Accounts to log in for their dashboard."""
    # GIVEN: a user viewing the Tutor marketing page
    # AND:  not logged into the site
    home = WebHome(selenium, web_base_url).open()
    tutor_marketing = home.web_nav.technology.view_tutor()

    # WHEN: they click on the "Access Your Course" button
    accounts = (tutor_marketing.introduction
                .access_your_course(accounts_base_url))

    # THEN: the Accounts log in page is displayed in a new tab
    assert(accounts.is_displayed())
    assert('login' in accounts.location)


@test_case('C210492')
@nondestructive
@web
def test_the_openstax_books_available_in_tutor_are_listed(
        web_base_url, selenium):
    """The OpenStax books available for use in Tutor are displayed."""
    # GIVEN: a user viewing the Tutor marketing page
    home = WebHome(selenium, web_base_url).open()
    tutor_marketing = home.web_nav.technology.view_tutor()

    # WHEN:

    # THEN: the introductory section lists "College
    #       Physics", "Biology 2e", and "Introduction to
    #       Sociology 2e"
    books = ['College Physics', 'Biology 2e', 'Introduction to Sociology 2e']
    introduction = tutor_marketing.introduction.description
    for book in books:
        assert(book in introduction), \
            '{book} no in the introduction.'.format(book=book)


@test_case('C210493')
@nondestructive
@web
def test_learn_more_scrolls_to_how_it_works(web_base_url, selenium):
    """The Learn More button scrolls down to the 'How it works' section."""
    # GIVEN: a user viewing the Tutor marketing page
    home = WebHome(selenium, web_base_url).open()
    tutor_marketing = home.web_nav.technology.view_tutor()

    # WHEN: they click on the "Learn More" button
    tutor_marketing.introduction.learn_more()

    # THEN: the screen scrolls down to the "How it works" section
    assert(Utility.in_viewport(
        selenium, element=tutor_marketing.how_it_works.subheading,
        display_marks=True)), \
        'Subheading not in the browser window'


@test_case('C210494')
@nondestructive
@web
def test_the_tutor_methodology_is_outlined(web_base_url, selenium):
    """The marketing page outlines the Tutor methodology."""
    # GIVEN: a user viewing the Tutor marketing page
    home = WebHome(selenium, web_base_url).open()
    tutor_marketing = home.web_nav.technology.view_tutor()

    # WHEN: they scroll down to the "How it works" section
    tutor_marketing.sidebar.view_how_it_works()

    # THEN: "low-cost", "easy-to-use", "professionally
    #       written", "peer-reviewed", "research-based",
    #       and "high-quality content" are in the description
    # AND:  the four primary tiles are shown ("Spaced
    #       practice", "Personalized questions", "Two-step
    #       questions", and "Low cost")
    themes = ['low-cost', 'easy-to-use', 'professionally written',
              'peer-reviewed', 'research-based', 'high-quality content']
    description = tutor_marketing.how_it_works.description
    for theme in themes:
        assert(theme in description)
    tiles = ['Spaced practice', 'Personalized questions', 'Two-step questions',
             'Low cost']
    assert(len(tiles) == len(tutor_marketing.how_it_works.boxes))
    for box in tutor_marketing.how_it_works.boxes:
        assert(box.title in tiles)


@test_case('C210495')
@nondestructive
@web
def test_videos_and_images_show_the_student_experience(web_base_url, selenium):
    """The video carousel shows the student experience using Tutor."""
    # GIVEN: a user viewing the Tutor marketing page
    home = WebHome(selenium, web_base_url).open()
    tutor_marketing = home.web_nav.technology.view_tutor()
    tutor_marketing.sidebar.view_what_students_get()

    for option, _ in \
            enumerate(tutor_marketing.what_students_get.tutor.options):
        # WHEN: they click on the a tile
        tutor_marketing.what_students_get.tutor.view(option)

        # THEN: the image or video is prsented in the
        #       viewport
        description = tutor_marketing.what_students_get.tutor.description
        assert(tutor_marketing.what_students_get.tutor.media_ready), \
            '{0} was not ready'.format(description)


@test_case('C210496')
@nondestructive
@web
def test_current_features_and_future_plans_are_outlined(
        web_base_url, selenium):
    """Current and future plans for Tutor are outlined."""
    # GIVEN: a user viewing the Tutor marketing page
    home = WebHome(selenium, web_base_url).open()
    tutor_marketing = home.web_nav.technology.view_tutor()

    # WHEN: they scroll to the current and future plans
    #       section
    tutor_marketing.sidebar.view_feature_matrix()

    # THEN: available features are listed
    # AND:  "Ability to add own questions" is gray because
    #       it is a planned feature
    assert(tutor_marketing.features.features)
    assert(tutor_marketing.features.new_features)
    assert('Ability to add own questions'
           in tutor_marketing.features.planned_features)


@test_case('C210497')
@nondestructive
@web
def test_a_breakdown_of_the_student_fee_is_shown(web_base_url, selenium):
    """The student fee is broken down and explained."""
    # GIVEN: a user viewing the Tutor marketing page
    home = WebHome(selenium, web_base_url).open()
    tutor_marketing = home.web_nav.technology.view_tutor()

    # WHEN: they scroll to the $10 explanation section
    tutor_marketing.sidebar.view_where_money_goes()

    # THEN: the breakdown image is displayed
    assert(tutor_marketing.where_money_goes.breakdown_image.is_displayed())
    assert(Utility.is_image_visible(
        selenium, image=tutor_marketing.where_money_goes.breakdown_image))


@test_case('C210498')
@nondestructive
@web
def test_student_learning_research_is_discussed(web_base_url, selenium):
    """Student learning research is mentioned."""
    # GIVEN: a user viewing the Tutor marketing page
    home = WebHome(selenium, web_base_url).open()
    tutor_marketing = home.web_nav.technology.view_tutor()

    # WHEN: they scroll to the Behind the science section
    tutor_marketing.sidebar.view_science()

    # THEN: "researchers at Rice", "cognitive science", and
    #       "machine learning" are mentioned
    mentions = ['researchers at Rice', 'cognitive science', 'machine learning']
    for mention in mentions:
        assert(mention in tutor_marketing.science.description), \
            '{0} not found in the Science description'.format(mention)


@test_case('C210499')
@nondestructive
@web
def test_frequently_asked_questions_are_displayed(web_base_url, selenium):
    """Common Tutor questions are available."""
    # GIVEN: a user viewing the Tutor marketing page FAQ
    home = WebHome(selenium, web_base_url).open()
    tutor_marketing = home.web_nav.technology.view_tutor()
    tutor_marketing.sidebar.view_faq()

    for question in tutor_marketing.faq.questions:
        # WHEN: they click on a question
        question.toggle()

        # THEN: the answer is displayed
        assert(question.is_open), \
            'The answer for {0} is not visible'.format(question.question)
        assert(question.question)
        assert(question.answer)

        # WHEN: they click on the question
        question.toggle()

        # THEN: the answer is hidden
        assert(not question.is_open), \
            'The answer for {0} is still visible'.format(question.question)


@test_case('C210500')
@nondestructive
@web
def test_users_with_unanswered_questions_are_directed_to_the_support_page(
        web_base_url, selenium):
    """Users with additional questions are directed to the help page."""
    # GIVEN: a user viewing the Tutor marketing page FAQ
    home = WebHome(selenium, web_base_url).open()
    tutor_marketing = home.web_nav.technology.view_tutor()
    tutor_marketing.sidebar.view_faq()

    # WHEN: they click on the "Get more answers at our Support page" link
    salesforce = tutor_marketing.faq.view_support()

    # THEN: the support page is displayed in a new tab
    assert(salesforce.is_displayed())
    assert('force.com' in salesforce.location)


@test_case('C210501')
@nondestructive
@web
def test_clicking_the_get_started_button_takes_instructors_to_their_dashboard(
        web_base_url, selenium, teacher):
    """Current Tutor instructors clicking 'Get started' are taken to Tutor."""
    # GIVEN: a user viewing the Tutor marketing page
    # AND:   logged in to the site with a verified
    #        instructor account
    home = WebHome(selenium, web_base_url).open()
    home.web_nav.login.log_in(*teacher)
    tutor_marketing = home.web_nav.technology.view_tutor()

    # WHEN: they click the "Get started" button in the
    #       "Pioneer a new way of teaching and learning"
    #       section
    tutor_marketing.sidebar.view_learn_more()
    tutor = tutor_marketing.learn_more.get_started()

    # THEN: the Tutor dashboard for the instructor is
    #       displayed in a new tab
    assert(tutor.is_displayed())
    assert('dashboard' in tutor.location)


@test_case('C210502')
@nondestructive
@web
def test_interested_users_may_view_the_upcoming_webinar_schedule(
        web_base_url, selenium):
    """Test interested users may view the Tutor webinar schedule blog entry."""
    # GIVEN: a user viewing the Tutor marketing page
    home = WebHome(selenium, web_base_url).open()
    tutor_marketing = home.web_nav.technology.view_tutor()

    # WHEN: they click on the "Join a webinar" button in
    #       the "Pioneer a new way of teaching and
    #       learning" section
    tutor_marketing.sidebar.view_learn_more()
    blog = tutor_marketing.learn_more.join_a_webinar()

    # THEN: the upcoming webinar blog entry is displayed
    assert(blog.is_displayed())
    assert('webinar' in blog.location)


@test_case('C210503', 'C210504')
@nondestructive
@web
def test_the_sidebar_links_to_each_page_section(web_base_url, selenium):
    """Test the side nav bar links to each id'ed section."""
    # GIVEN: a user viewing the Tutor marketing page
    home = WebHome(selenium, web_base_url).open()
    tutor_marketing = home.web_nav.technology.view_tutor()

    # WHEN: they scroll down
    tutor_marketing.introduction.learn_more()

    for index, dot in enumerate(tutor_marketing.sidebar.nav):
        # AND: click on the nav dot
        tutor_marketing.sidebar.select(dot)

        # THEN: the page scrolls to the corresponding section
        # AND:  the dot is selected
        assert(Utility.in_viewport(
            driver=selenium,
            element=tutor_marketing.sections[index].section,
            display_marks=True)), \
            '"{0}" not in the browser window'.format(
                tutor_marketing.sections[index].heading)


@skip_test(reason='Safari action chains are broken')
@test_case('C210505')
@nondestructive
@web
def test_the_exclamation_point_alert_icon(web_base_url, selenium):
    """Test the Tutor availability alert icon."""
    # GIVEN: a user viewing the Tutor marketing page
    home = WebHome(selenium, web_base_url).open()
    tutor_marketing = home.web_nav.technology.view_tutor()

    # WHEN: the cursor hovers over the "!" icon

    # THEN: a pop up message shows "OpenStax Tutor Beta is
    #       not available for high school or international
    #       courses at this time."
    assert(tutor_marketing)


@test_case('C210506')
@nondestructive
@web
def test_the_pinned_tutor_and_webinar_buttons(web_base_url, selenium):
    """Test the pinned 'Get Started' and 'Join a Webinar' buttons."""
    # GIVEN: a user viewing the Tutor marketing page
    home = WebHome(selenium, web_base_url).open()
    tutor_marketing = home.web_nav.technology.view_tutor()

    # WHEN: the browser is scrolled to the top of the page
    Utility.scroll_top(selenium)

    # THEN: the "Get Started" and "Join A Webinar" pinned
    #       buttons are not displayed
    assert(not tutor_marketing.marketing_footer.is_visible)

    # WHEN: the browser scrolls down
    # AND:  stops scrolling before reaching the bottom
    tutor_marketing.sidebar.view_how_it_works()

    # THEN: the "Get Started" and "Join A Webinar" pinned
    #       buttons are displayed
    assert(tutor_marketing.marketing_footer.is_visible)

    # WHEN: the browser scrolls down to the bottom of the
    #       page
    Utility.scroll_bottom(selenium)

    # THEN: the "Get Started" and "Join A Webinar" pinned
    #       buttons are not displayed
    assert(not tutor_marketing.marketing_footer.is_visible)


@test_case('C210507')
@nondestructive
@web
def test_mobile_users_do_not_see_the_veritcal_navbar(web_base_url, selenium):
    """Users viewing the marketing page do not see the shortcut bar."""
    # GIVEN: a user viewing the Tutor marketing page
    # AND:  the browser window is 600 pixels wide
    home = WebHome(selenium, web_base_url)
    home.resize_window(width=600)
    home.open()
    home.web_nav.meta.toggle_menu()
    home.web_nav.technology.open()
    tutor_marketing = home.web_nav.technology.view_tutor()

    # WHEN:

    # THEN: the veritcal nav is not displayed
    assert(not tutor_marketing.sidebar.is_displayed())
