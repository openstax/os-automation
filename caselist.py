"""Test case from 1 ~ 88 for tutor page."""

from tests.markers import accounts, test_case


@test_case('')
@accounts
def test_tutor_home_page(tutor_base_url, selenium):
    """Test the tutor home page."""
    # GIVEN: A web browser

    # WHEN: Go to the Tutor home page

    # THEN: The Tutor home page loads


@test_case('')
@accounts
def test_sales_force_support_page(tutor_base_url, selenium):
    """Test the salesforce support page."""
    # GIVEN: The Tutor home page

    # WHEN: The user clicks "Help" link in the header

    # THEN: The Salesforce Tutor support page loads


@test_case('')
@accounts
def test_accounts_log_in_page(tutor_base_url, selenium):
    """Test the accounts log in page."""
    # GIVEN: The Tutor home page

    # WHEN: The user clicks "LOG IN" button

    # THEN: The Accounts log in page loads

    # AND: "tutor" is in the URL


@test_case('')
@accounts
def test_crest_rice_home_page(tutor_base_url, selenium):
    """Test the rice home page using crest."""
    # GIVEN: The Tutor home page

    # WHEN: The user clicks the Rice logo

    # THEN: The Rice home page loads


@test_case('')
@accounts
def test_footer_rice_home_page(tutor_base_url, selenium):
    """Test the rice home page using footer."""
    # GIVEN: The Tutor home page

    # WHEN: The user clicks "Rice University"

    # THEN: The Rice home page


@test_case('')
@accounts
def test_tutor_term_page(tutor_base_url, selenium):
    """Test the tutor term page."""
    # GIVEN: The Tutor home page

    # WHEN: The user clicks "Terms" link

    # THEN: The Terms page loads


@test_case('')
@accounts
def test_tutor_payment_page(tutor_base_url, selenium, student):
    """Test the tutor payment page."""
    # GIVEN: Tutor page logged in as a student

    # WHEN: The user clicks on the "Menu"

    # AND: The user clicks on the "Manage payments" menu item

    # THEN: The Payment Management page loads


@test_case('')
@accounts
def test_tutor_invoice_page(tutor_base_url, selenium, student):
    """Test the tutor invoice page."""
    # GIVEN: Tutor page logged in as a student

    # WHEN: The user clicks on "Manage payments"

    # AND: The user clicks "Invoice" of any one of the transactions

    # THEN: A page of the detailed invoice loads


@test_case('')
@accounts
def test_tutor_dashboard_page(tutor_base_url, selenium, student):
    """Test the tutor dashboard page."""
    # GIVEN: The Tutor page logged in as a student

    # AND: The student has enrolled in a course

    # WHEN: The user clicks on a enrolled Tutor course card

    # THEN: The Dashboard page for that course loads


@test_case('')
@accounts
def test_bypass_course_picker_page(tutor_base_url, selenium, student):
    """Test the tutor bypassing the course picker page."""
    # GIVEN: The Tutor home page logged in as a student

    # AND: The user has only one enrolled course

    # WHEN: The user logs in

    # THEN: The Dashboard page for the enrolled course loads


@test_case('')
@accounts
def test_open_reading_assignment_page(tutor_base_url, selenium, student):
    """Test the tutor open reading assignment page."""
    # GIVEN: The Tutor home page logged as a student

    # AND: The student Has enrolled in a course

    # AND: The student has an open reading assignment in that course

    # WHEN: The user clicks on the reading assignment

    # THEN: The Reading page for a specific chapter loads


@test_case('')
@accounts
def test_reading_questions(tutor_base_url, selenium, student):
    """Test the reading questions."""
    # GIVEN: Logged into Tutor as a student

    # AND: Has enrolled in a course

    # AND: Has an open reading assignment

    # WHEN: The user clicks on the reading assignment

    # AND: The user continues through the assignment

    # THEN: The review questions load

    # AND: The student is able to submit answers for all questions


@test_case('')
@accounts
def test_textbook_from_quiz(tutor_base_url, selenium, student):
    """Test the corresponding section of textbook from quiz."""
    # GIVEN: Logged into Tutor as a student

    # AND: Has enrolled in a course

    # AND: Has an open reading assignment

    # WHEN: The user clicks on the reading assignment

    # AND: The user goes to an assessment

    # AND: The user clicks the "Comes from <section name>" link

    # THEN: The corresponding section of the textbook loads


@test_case('')
@accounts
def test_dashboard_from_assignment_page(tutor_base_url, selenium, student):
    """Test the back to dashboard from reading assignment."""
    # GIVEN: Logged into Tutor as a student

    # AND: Has enrolled in a course

    # AND: Has an open reading assignment

    # WHEN: The user finishes the reading

    # AND: The user clicks on the "Back to Dashboard" button

    # THEN: The student's dashboard for that course loads


@test_case('')
@accounts
def test_assignment_review_page(tutor_base_url, selenium, student):
    """Test the tutor assignment review."""
    # GIVEN: Logged into Tutor as a student

    # AND: Enrolled in a course

    # AND: Has a reading assignment

    # WHEN: The user clicks on the reading assignment

    # AND: The user clicks on the "Continue" button

    # THEN: The corresponding reading assignment review loads


@test_case('')
@accounts
def test_spaced_practice_assessment(tutor_base_url, selenium, student):
    """Test the spaced practice assessment."""
    # GIVEN: Logged into Tutor as a student

    # AND: Enrolled in a course

    # AND: Has a reading assignment

    # AND: Has done at least three assignments before

    # WHEN: The user clicks on the reading assignment

    # AND: The user continues on the reading assignment

    # THEN: A Spaced Practice assessment is assigned


@test_case('')
@accounts
def test_personalized_assessment(tutor_base_url, selenium, student):
    """Test the personalized assessment."""
    # GIVEN: Logged into Tutor as a student

    # AND: Enrolled in a course

    # AND: Has a reading assignment

    # WHEN: The user clicks on the reading assignment

    # AND: The user goes through readings and click "Continue" button

    # THEN: A Personalized assessment  is assigned


@test_case('')
@accounts
def test_assignment_done_pop_up(tutor_base_url, selenium, student):
    """Test the pop up for  # WHEN assignment is finished."""
    # GIVEN: Logged into Tutor as a student

    # AND: Enrolled in a course

    # AND: Has a reading assignment

    # WHEN: The user click on the reading assignment

    # AND: The user completes the assignment

    # THEN: The user is shown "User are done"


@test_case('')
@accounts
def test_complete_reading(tutor_base_url, selenium, student):
    """Test that complete reading assignment is shown on dashboard."""
    # GIVEN: Logged into Tutor as a student

    # AND: Has enrolled in a course

    # AND: Has an open reading assignment

    # WHEN: The user selected the reading assignment

    # AND: The user works the assignment

    # AND: The user clicks "Back to Dashboard" button

    # THEN: The Dashboard page for that course loads

    # AND: The reading is marked "completed" on the dashboard


@test_case('')
@accounts
def test_homework_submit_button(tutor_base_url, selenium, student):
    """Test the homework submit button."""
    # GIVEN: Logged into Tutor as a student

    # AND: Has enrolled in a course

    # AND: Has an open homework assignment

    # WHEN: The user clicks on homework assignment

    # AND: The user clicks one of the answer choices

    # THEN: The selected answer is light blue

    # AND: The submit button is orange


@test_case('')
@accounts
def test_correct_answer(tutor_base_url, selenium, student):
    """Test the correct answer on the homework assignment."""
    # GIVEN: Logged into Tutor as a student

    # AND: Has enrolled in a course

    # AND: Has an open homework assignment

    # WHEN: The user clicks an answer from the answer choice

    # AND: The user clicks the submit button

    # THEN: The correct answer is highlighted in red


@test_case('')
@accounts
def test_assignment_error_page(tutor_base_url, selenium, student):
    """Test the tutor assignment error page."""
    # GIVEN: Logged into Tutor as a student

    # AND: Has enrolled in a course

    # AND: Has an open homework assignment

    # WHEN: The user clicks the Report An Error button on the right
    # bottom corner

    # THEN: Taken to the error report page


@test_case('')
@accounts
def test_assignment_from_link(tutor_base_url, selenium, student):
    """Test the tutor assignment comes from link."""
    # GIVEN: Logged into Tutor as a student

    # AND: Has enrolled in a course

    # AND: Has an open homework assignment

    # WHEN: The user clicks on the "Comes from" link

    # THEN: Taken to specific textbook page corresponding to problem


@test_case('')
@accounts
def test_dashboard_from_homework(tutor_base_url, selenium, student):
    """Test the back to dashboard button."""
    # GIVEN: Logged into Tutor as a student

    # AND: Has enrolled in a course

    # AND: Has an open homework assignment

    # WHEN: The user finishes the homework

    # AND: The user clicks on the "Back to Dashboard" button

    # THEN: The Dashboard page for that course loads


@test_case('')
@accounts
def test_previous_question(tutor_base_url, selenium, student):
    """Test the previous question icon."""
    # GIVEN: Logged into Tutor as a student

    # AND: Has enrolled in a course

    # AND: Has an open homework assignment

    # AND: Has answered an assessment

    # WHEN: The user selects the homework assignment

    # AND: The user clicks on the previous question icon

    # THEN: The user is taken to the previous question

    # AND: The assessment is answered


@test_case('')
@accounts
def test_navigate_question(tutor_base_url, selenium, student):
    """Test the breadcrub of questions."""
    # GIVEN: Logged into Tutor as a student

    # AND: Has enrolled in a course

    # AND: Has an open homework assignment

    # WHEN: The user clicks one of the section performance bars
    # from the dashboard

    # AND: The user clicks on a breadcrumb

    # THEN: Taken to the specific question that the user clicked on


@test_case('')
@accounts
def test_user_performance_bar(tutor_base_url, selenium, student):
    """Test the user performance bar."""
    # GIVEN: Logged into Tutor as a studnet

    # AND: Has enrolled in a course

    # WHEN: The user clicks on a enrolled course

    # AND: The user clicks on the user performance bars

    # THEN: The header bar, containing the course name, OpenStax logo,
    # and user menu link are visible.


@test_case('')
@accounts
def test_performance_bar_question(tutor_base_url, selenium, student):
    """Test the performance bar questions."""
    # GIVEN: Logged into Tutor as a student

    # AND: Has enrolled in a course

    # WHEN: The user clicks on a enrolled course

    # AND: The user clicks one of the section performance
    # bars from the dashboard

    # AND: If there is a text box, input text

    # THEN: "Answer" button can be clicked


@test_case('')
@accounts
def test_performance_bar_answer(tutor_base_url, selenium, student):
    """Test the performance bar answers."""
    # GIVEN: Logged into Tutor as a student

    # AND: Has enrolled in a course

    # WHEN: The user clicks on a enrolled course

    # AND: The user clicks one of the section performance bars
    # from the dashboard

    # AND: If there is a text box, the user input text

    # AND: The user clicks the 'Answer' button

    # THEN: Text box disappears and the multiple choice answer appear


@test_case('')
@accounts
def test_performance_bar_submit(tutor_base_url, selenium, student):
    """Test the performance bar submit button."""
    # GIVEN: Logged on Tutor as a student

    # AND: Has enrolled in a course

    # WHEN: The user clicks on one of the section of the performance bars

    # AND: The user filled out the text box and click on a multiple
    # choice answer

    # THEN: User should be able to click the submit button


@test_case('')
@accounts
def test_performance_bar_assessment(tutor_base_url, selenium, student):
    """Test the performance bar assessment."""
    # GIVEN: Logged on Tutor as a student

    # AND: Has enrolled in a course

    # WHEN: The user clicks on one of the section of the performance
    # bars

    # AND: The user Filled out the text box and click on a multiple
    # choice answer

    # AND: The user clicks on submit button

    # THEN: The answer should be submited and user should be able to see
    # next question button


@test_case('')
@accounts
def test_performance_bar_feedback(tutor_base_url, selenium, student):
    """Test the performance bar feedback."""
    # GIVEN: Logged on Tutor as a student

    # AND: Has enrolled in a course

    # WHEN: The user clicks on one of the section of the performance bars

    # AND: The user filled out the text box and click on a multiple choice
    # answer

    # AND: The user submit the answer

    # THEN: The correct answer and feedback should appear


@test_case('')
@accounts
def test_performance_bar_breadcrumb(tutor_base_url, selenium, student):
    """Test the performance bar breadcrumb."""
    # GIVEN: Logged on Tutor as a student

    # AND: Has enrolled in a course

    # WHEN: The user clicks on one of the section of the performance bars

    # AND: The user filled out the text box

    # AND: The user clicks on a multiple choice answer

    # AND: The user submits the answer

    # THEN: Correctness for the completed question is visible in the breadcrumb


@test_case('')
@accounts
def test_external_assignment_page(tutor_base_url, selenium, student):
    """Test the external assignment."""
    # GIVEN: Logged on Tutor as a student

    # AND: Has enrolled in a course

    # AND: Has a external assignment

    # WHEN: The user clicks on the external assignment from the dashboard

    # THEN: User should be presented with details of the external assignment


@test_case('')
@accounts
def test_external_assignment_direction(tutor_base_url, selenium, student):
    """Test the external assignment direction."""
    # GIVEN: Logged on Tutor as a student

    # AND: Has enrolled in a course

    # AND: Has a external assignment

    # WHEN: The user clicks on the external assignment from the dashboard

    # AND: The user points to the info icon

    # THEN: User is presented with the directions for the assignment


@test_case('')
@accounts
def test_external_assignment_under_tab(tutor_base_url, selenium, student):
    """Test the external assignment through the tab on dashboard."""
    # GIVEN: Logged into Tutor as a student

    # AND: Has enrolled in a course

    # AND:  Has an external assignement

    # WHEN: The user clicks on an external assignment under the tab "This Week"
    # on the dashboard

    # AND: The user clicks on the link to the external assignment

    # THEN: External assignment page loads


@test_case('')
@accounts
def test_external_assignment_instruction(tutor_base_url, selenium, student):
    """Test the external assignment instructions."""
    # GIVEN: Logged into Tutor as a student

    # AND: Has enrolled in a course

    # AND: Has an external assignement

    # WHEN: The user clicks on an external assignment

    # THEN: The external assignment link and instructions are shown


@test_case('')
@accounts
def test_external_assignment_to_dashboard(tutor_base_url, selenium, student):
    """Test the external assignment to dashboard button."""
    # GIVEN: Logged into Tutor as a student

    # AND: Has enrolled in a course

    # AND:  Has an external assignement

    # WHEN: The user clicks on an external assignment under the tab "This Week"
    # on the dashboard

    # AND: The user clicks on the link to the external assignment

    # AND: The user closes the assignement tab

    # AND: The user clicks "Back to Dashboard"

    # THEN: User is presented with the dashboard"


@test_case('')
@accounts
def test_clicked_external_assignment(tutor_base_url, selenium, student):
    """Test the link of external assignment."""
    # GIVEN: Logged into Tutor as a student

    # AND: Has enrolled in a course

    # AND:  Has an external assignement

    # WHEN: The user clicks on an external assignment under the tab "This Week"
    # on the dashboard

    # AND: The user clicks on the link to the external assignment

    # AND: The user closes the assignement tab

    # AND: The user clicks "Back to Dashboard"

    # THEN: The assignment is marked as "clicked" on the dashboard


@test_case('')
@accounts
def test_score_page(tutor_base_url, selenium, student):
    """Test the score page."""
    # GIVEN:  Logged into Tutor as a student

    # AND: Has enrolled in a class

    # WHEN: The user clicks on score

    # AND: The user clicks on view weight

    # THEN: New weight page pops up and loads


@test_case('')
@accounts
def test_average_section(tutor_base_url, selenium, student):
    """Test the average section of the homework assignment."""
    # GIVEN:  Logged into Tutor as a student

    # AND: Has enrolled in a class

    # AND: Has a homework assignment

    # WHEN: The user clicks on a homework assignment

    # AND: The user clicks on an answer

    # AND: The user clicks on the arrow next to the average

    # THEN: See the average section widen


@test_case('')
@accounts
def test_change_student_id(tutor_base_url, selenium, student):
    """Test the changing student id."""
    # GIVEN: Logged into Tutor as a student

    # AND: Has enrolled in a class

    # WHEN: The user clicks on "Change Student ID"

    # AND: The user enters new student id to the input box

    # THEN: User is able to change student section

    # AND: User is able to enter new digits to the student id


@test_case('')
@accounts
def test_change_id_to_dashboard(tutor_base_url, selenium, student):
    """Test student can go back to dashnoard from changing id page."""
    # GIVEN: Logged into Tutor as a student

    # AND: Has enrolled in a class

    # WHEN: The user goes into an enrolled class

    # AND: The user clicks on "Change Student ID"

    # AND: The user clicks on "Cancel"

    # THEN: Navigated back to the dashboard of the class


@test_case('')
@accounts
def test_save_student_id(tutor_base_url, selenium, student):
    """Test the changed student id is saved."""
    # GIVEN: Logged into Tutor as a student

    # AND: Has enrolled in a class

    # WHEN: The user goes into an enrolled class

    # AND: The user clicks on "Change Student ID"

    # AND: The user enter the new student id number

    # AND: The user clicks "Save"

    # THEN: Student ID saved and navigatde back to the dashboard


@test_case('')
@accounts
def test_performance_forcast(tutor_base_url, selenium, student):
    """Test the performance forcast."""
    # GIVEN: Logged into Tutor as a student

    # AND: Has enrolled in a class

    # WHEN: The user clicks on the user menu in the upper right corner

    # AND: The user clicks on "Performance Forecast"

    # THEN:  Personal Performance Forecast is loaded


@test_case('')
@accounts
def test_performance_forcast_info_icon(tutor_base_url, selenium, student):
    """Test the performance forcast info icon."""
    # GIVEN: Logged into Tutor as a student

    # AND: Has enrolled in a class

    # WHEN: The user goes into an enrolled class

    # AND: The user clicks on the user menu in the upper right
    # corner of the page

    # AND: The user clicks on "Performance Forecast"

    # AND: The user hovers the cursor over the info icon that is next to the
    # "Performance Forecast" header

    # THEN: Page with Info icon showing an explanation of the data is loaded


@test_case('')
@accounts
def test_performance_color_key(tutor_base_url, selenium, student):
    """Test the performance color key."""
    # GIVEN: Logged into Tutor as a student

    # AND: Has enrolled in a class

    # WHEN: The user goes into an enrolled class

    # AND: The user clicks on the user menu in the upper right corner
    # of the page

    # AND: The user clicks on "Performance Forecast"

    # THEN: The performance color key is presented (next
    # to the 'Return to Dashboard' button)


@test_case('')
@accounts
def test_return_to_dashboard_button(tutor_base_url, selenium, student):
    """Test the return to dashboard button."""
    # GIVEN: Logged into Tutor as a student

    # AND: Has enrolled in a class

    # WHEN: The user goes into an enrolled class

    # THEN: Click on "Return To Dashboard"


@test_case('')
@accounts
def test_performance_forcast_with_zero_question(
        tutor_base_url, selenium, student):
    """Test the performance forcast with zero questions."""
    # GIVEN: Logged into Tutor as a student

    # AND: Has enrolled in a class

    # AND: Has not done many questions before

    # WHEN: The user clicks on the user menu in the upper right corner

    # AND: The user clicks on "Performance Forecast"

    # THEN: Presented with blank performance forecast with no section
    # breakdowns and the words "User haven't worked enough problems
    # for Tutor to predict User's weakest topics."


@test_case('')
@accounts
def test_performance_forcast_weak_area(tutor_base_url, selenium, student):
    """Test the weak area of the performance forcast."""
    # GIVEN: Logged into Tutor as a student

    # AND: Has enrolled in a class

    # AND: Has finished some assignments before

    # WHEN: The user goes into an enrolled class

    # AND: The user clicks on the user menu in the upper right
    # corner of the page

    # AND: The user clicks on "Performance Forecast"

    # THEN: The user is presented with up to four problematic sections
    # under My Weaker Areas


@test_case('')
@accounts
def test_performance_forcast_individual_section(
        tutor_base_url, selenium, student):
    """Test the individual sections of forcast."""
    # GIVEN: Logged into Tutor as a student

    # AND: Has enrolled in a class

    # WHEN: The user clicks on the user menu in the upper right corner

    # AND: The user clicks on "Performance Forecast"

    # AND: The user scrolls to Individual Chapters section

    # THEN: User is presented with chapters listed on top and their
    # sections below


@test_case('')
@accounts
def test_performance_forcast_chapter(tutor_base_url, selenium, student):
    """Test the performance forcast chapter bar."""
    # GIVEN: Logged into Tutor as a student

    # AND: Has enrolled in a class

    # WHEN: The user goes to the enrolled class

    # AND: The user clicks on the user menu in the upper right corner

    # AND: The user clicks on "Performance Forecast"

    # AND: The user scrolls to the Individual Chapters section

    # AND: The user clicks on a chapter bar

    # THEN: Page with up to five practice assessments for that
    # chapter is loaded


@test_case('')
@accounts
def test_performance_forcast_section_bar(tutor_base_url, selenium, student):
    """Test the performance forcast section bar."""
    # GIVEN: Logged into Tutor as a student

    # AND: Has enrolled in a class

    # WHEN: The user clicks on the user menu in the upper right corner

    # AND: The user clicks on "Performance Forecast"

    # AND: The user scrolls to the Individual Chapters section

    # AND: The user clicks on a section bar

    # THEN: User is presented with up to five practice assessments for
    # that section


@test_case('')
@accounts
def test_performance_forcast_without_data(tutor_base_url, selenium, student):
    """Test the performance forcast individual section without enough data."""
    # GIVEN: Logged into Tutor as a student

    # AND: Has enrolled in a class

    # WHEN: The user clicks on the user menu in the upper right corner

    # AND: The user clicks on "Performance Forecast"

    # AND: The user scrolls to the Individual Chapters section

    # THEN: User is presented with the "Practice More To Get Forecast"
    # button under a section without enough data instead of a color bar


@test_case('')
@accounts
def test_performance_forcast_finished_assignment(
        tutor_base_url, selenium, student):
    """Test the performance forcast with finished assignment."""
    # GIVEN: Logged into Tutor as a student

    # AND: Has enrolled in a class

    # AND: Has finished an assignment

    # WHEN: Once an assignment is completed, the user clicks the
    # Performance Forecast

    # THEN: Performance forecast with the finished assignment updated is loaded


@test_case('')
@accounts
def test_payment_option(tutor_base_url, selenium, student):
    """Test the tutor payment option section."""
    # GIVEN: Logged into Tutor as a student

    # WHEN: The user goes to student enrollment url for a paid course

    # AND: The user agrees to Tutor Terms of Use and Privacy Policy

    # AND: From "Pay now or pay later" screen, the user click "Buy access now"

    # THEN: Payment screen -- with options for Free Trial and to Buy Access to
    # course now is loaded


@test_case('')
@accounts
def test_course_payment(tutor_base_url, selenium, student):
    """Test the process of making payment for a course."""
    # GIVEN: Logged into Tutor as a student

    # WHEN: The user goes to the url of a paid course

    # AND: The user sign Terms and Privacy policy

    # AND: On payment option page, click on "Buy access now"

    # AND: Fill out information correctly on Payment option page

    # THEN: Student gets confirmation that payment was accepted successfully,
    # and there should be an option to "Access User's Course"


@test_case('')
@accounts
def test_invalid__card_payment(tutor_base_url, selenium, student):
    """Test the tutor invalid payment methods."""
    # GIVEN: Logged into Tutor as a student with newly enrolled paid course

    # AND: Signed terms and Privacy policy

    # AND: Clicked "Buy access now"

    # WHEN: The user types in 1 to Credit card blank

    # AND: The user clicks purchase

    # THEN: Warning with "Invalid card number. Please check User's number and
    # try again." is loaded


@test_case('')
@accounts
def test_unfilled_purchase(tutor_base_url, selenium, student):
    """Test the tutor assignment review."""
    # GIVEN: Logged into Tutor as a student

    # AND: Being at the payment page

    # WHEN: The user clicks purchase directly

    # THEN: Multiple warning shows up


@test_case('')
@accounts
def test_join_trial_course(tutor_base_url, selenium, student):
    """Test the tutor 14 days trial."""
    # GIVEN: Logged into Tutor as a student with a expired trial course

    # WHEN: The user trying to get into the course from course picker

    # THEN: a screen confirming "User's free trial is activated," should pop up


@test_case('')
@accounts
def test_expired_course(tutor_base_url, selenium, student):
    """Test the expired course."""
    # GIVEN: Logged into Tutor as an student with a expired trial course

    # WHEN: The user clicks on the expired course

    # THEN: Modal pops up and student should be denied access to the course


@test_case('')
@accounts
def test_access_user_course(tutor_base_url, selenium, student):
    """Test the access user"s course button."""
    # GIVEN: Logged into Tutor as a student with a free trial course

    # WHEN: Get to screen confirming "User's free trial is activated,"

    # AND: The user clicks "Access User's course"

    # THEN: Brought to the course dashboard


@test_case('')
@accounts
def test_trial_course_access(tutor_base_url, selenium, student):
    """Test access to the trial course."""
    # GIVEN: Logged into Tutor as a student

    # AND: Enrolled in a class with 14 days trial mode

    # WHEN: The user navigates to a course while the 14 day grace period is
    # still in effect

    # THEN: Dashboard of that course is successfully loaded


@test_case('')
@accounts
def test_enrollment_url(tutor_base_url, selenium, student):
    """Test the enrollment url for the student and the teacher works."""
    # GIVEN:  Logged into Tutor as teacher that has paid course

    # AND: Has gotten enrollment url

    # AND: Log out of teacher account and log in as a student

    # WHEN: The user enters the enrollment url as a student

    # AND: Click past modal(optional)

    # AND: Agree to Terms and Privacy Policy

    # THEN: Student is enrolled in the course


@test_case('')
@accounts
def test_free_trial_nag(tutor_base_url, selenium, student):
    """Test the tutor assignment review."""
    # GIVEN: Logged into Tutor as a student

    # AND: Enrolled in a class with 14 days trial mode

    # WHEN:  The user goes to course with free trial

    # THEN: Free Trial Nag Includes a count-down on days left


@test_case('')
@accounts
def test_full_access_to_trial(tutor_base_url, selenium, student):
    """Test the full trial payment from trial."""
    # GIVEN: Logged into Tutor as a student

    # AND: Enrolled in a class with 14 days trial mode

    # WHEN: The user goes to course with free trial

    # AND: Click on the "Get Access" button of the nag banner

    # THEN: User is taken to the payments page


@test_case('')
@accounts
def test_free_trial_tag_disappear(tutor_base_url, selenium, student):
    """Test the free trial tag disappearing."""
    # GIVEN: Logged into Tutor as a student

    # AND: Enrolled in a class with 14 days trial mode

    # WHEN: The user pay for the course

    # AND: Refresh page

    # THEN: Free trial tag no longer there


@test_case('')
@accounts
def test_not_payed_course_skip_payment(tutor_base_url, selenium, student):
    """Test that course not payed skips the payment section."""
    # GIVEN:  Logged into tutor as a student

    # WHEN: The user goes throught the enrollment process

    # AND: Put student id

    # THEN: Student account page is loaded


@test_case('')
@accounts
def test_buy_free_trial(tutor_base_url, selenium, student):
    """Test buying a course from free trial."""
    # GIVEN: Logged into Tutor as a student

    # AND: Enrolled in a class with 14 days trial mode

    # WHEN: The user clicks "Pay Now"

    # AND: Enter credit card and other information

    # AND: Complete the payment

    # THEN: Free trial tag no longer there


@test_case('')
@accounts
def test_teacher_dashboard(tutor_base_url, selenium, teacher):
    """Test the teacher dashboard."""
    # GIVEN: Logged into Tutor as a teacher

    # WHEN: The user logs in as teacher

    # THEN: On the dashboard can see their all existing course's card with
    # information


@test_case('')
@accounts
def test_preview_course(tutor_base_url, selenium, teacher):
    """Test the preview course section."""
    # GIVEN: Logged into Tutor as a teacher

    # WHEN: The user goes to the course picker page

    # THEN: Preview courses are present


@test_case('')
@accounts
def test_copy_course_page(tutor_base_url, selenium, teacher):
    """Test the copy course page."""
    # GIVEN: Logged into Tutor as a teacher

    # AND: Has an existing course

    # WHEN: The user hovers over a course card

    # AND: Click "copy this course" button

    # THEN: User should be taken to the copy course page


@test_case('')
@accounts
def test_roster_period_page(tutor_base_url, selenium, teacher):
    """Test the roster period in preview course."""
    # GIVEN: Logged into Tutor as a teacher

    # AND: Has a preview course

    # WHEN: The user goes to the preview course

    # AND: Open the user menu

    # AND: Click on "Course Settings and Roster"

    # AND: Click on each period tabs shown

    # THEN:  Page with period with at least 3 students per section
    # is loaded


@test_case('')
@accounts
def test_preview_calendar(tutor_base_url, selenium, teacher):
    """Test the preview course calendar's assignment samples."""
    # GIVEN: Logged into Tutor as a teacher

    # AND: Has a preview course

    # WHEN: The user goes to a preview course

    # THEN: From the calendar, the user should be able see sample
    # assignments and readings


@test_case('')
@accounts
def test_add_reading(tutor_base_url, selenium, teacher):
    """Test the adding reading assignment."""
    # GIVEN: Logged into Tutor as a teacher

    # AND: Has an existing course

    # WHEN: The user clicks on one of the courses

    # AND:  Click on a date on the dashboard

    # AND: Click "add reading"

    # AND: Fill in all the required fields

    # AND: Click "Publish"

    # THEN: Dashboard of that course is successfully loaded and the
    # reading assignment is visible on the calendar


@test_case('')
@accounts
def test_adding_reading_draft(tutor_base_url, selenium, teacher):
    """Test adding the reading draft to dashboard."""
    # GIVEN: Logged into Tutor as a teacher

    # AND: Has an existing course

    # WHEN: The user clicks on one of the courses

    # AND:  Click on a date on the dashboard

    # AND: Click "add reading"

    # AND: Fill in all the required fields

    # AND: Click "Save as draft"

    # THEN: Dashboard of that course is successfully loaded

    # AND the reading assignment draft is visible on the calendar


@test_case('')
@accounts
def test_edit_published_reading(tutor_base_url, selenium, teacher):
    """Test editting the published reading."""
    # GIVEN: Logged into Tutor as a teacher

    # AND: Has an existing course

    # AND: Has a publish reading

    # WHEN: The user clicks on the course

    # AND: Click on the published reading

    # AND: Edit one of the required fields

    # AND: Click "Publish"

    # THEN: Dashboard of that course is successfully loaded and the
    # reading assignment with edits is visible on the calendar


@test_case('')
@accounts
def test_publish_reading_draft(tutor_base_url, selenium, teacher):
    """Test editting the reading draft and publish."""
    # GIVEN: Logged into Tutor as a teacher

    # AND: Has an existing course

    # AND: Has a reading draft

    # WHEN: The user clicks on the course

    # AND: Click on the reading draft on calendar

    # AND: Edit one of the required fields

    # AND: Click "Publish"

    # THEN: Dashboard of that course is successfully loaded and
    # the reading assignment with edits is visible on the calendar


@test_case('')
@accounts
def test_cancel_reading_edits(tutor_base_url, selenium, teacher):
    """Test cancelling reading assignments edits."""
    # GIVEN: Logged into Tutor as a teacher

    # AND: Has an existing course

    # AND: Has a publish reading

    # WHEN: The user clicks on the course

    # AND: Click on the published reading on calendar

    # AND: Edit the required fields

    # AND: Click "Cancel"

    # THEN: The changes made on the reading assignment is not saved


@test_case('')
@accounts
def test_cancel_reading_draft(tutor_base_url, selenium, teacher):
    """Test cancelling reading draft edits."""
    # GIVEN: Logged into Tutor as a teacher

    # AND: Has an existing course

    # AND: Has a reading draft

    # WHEN:  The user clicks on the course

    # AND: Click on the reading draft

    # AND: Edit the required fields

    # AND: Click "Cancel"

    # THEN: The changes made on the reading draft is not saved


@test_case('')
@accounts
def test_delete_published_reading(tutor_base_url, selenium, teacher):
    """Test the deleting the published reading."""
    # GIVEN: Logged into Tutor as a teacher

    # AND: Has an existing course

    # AND: Has a publish reading

    # WHEN: The user clicks on the course

    # AND: Click on the reading

    # AND: Click "Delete"

    # THEN: The reading is deleted.


@test_case('')
@accounts
def test_delete_reading_draft(tutor_base_url, selenium, teacher):
    """Test deleting the reading draft."""
    # GIVEN: Logged into Tutor as a teacher

    # AND: Has an existing course

    # AND: Has a reading draft

    # WHEN:  The user clicks on the course

    # AND: Click on the reading draft

    # AND: Click "Delete"

    # THEN: The reading draft is deleted.


@test_case('')
@accounts
def test_see_what_student_see(tutor_base_url, selenium, teacher):
    """Test the see what student see button."""
    # GIVEN: Logged into Tutor as a teacher

    # AND: Has an existing course

    # AND: Has a reading or homework assignment

    # WHEN: The user goes to a homework/reading assignment

    # AND: Edit it

    # THEN: "see what students see" button should be available


@test_case('')
@accounts
def test_add_homework(tutor_base_url, selenium, teacher):
    """Test adding homework to a course."""
    # GIVEN: Logged into Tutor as a teacher

    # AND: Has an existing couse

    # WHEN: The user clicks on a date on the dashboard

    # AND: Click "add homework"

    # AND: Fill in all the required fields

    # THEN:  Click "Publish" button


@test_case('')
@accounts
def test_add_homework_draft(tutor_base_url, selenium, teacher):
    """Test addomg homework draft to a course."""
    # GIVEN: Logged into Tutor as a teacher

    # AND: Has an existing course

    # WHEN: The user clicks on a date on the dashboard, then click
    # "Add Homework"

    # AND: Fill in all the required fields

    # AND: Click "Save as Draft"

    # THEN: HW draft should be visible on the calendar


@test_case('')
@accounts
def test_publish_existing_unopened_homework(tutor_base_url, selenium, teacher):
    """Test publishing existing unopened homework."""
    # GIVEN: Logged into Tutor as a teacher

    # AND: Has an existing course

    # WHEN: The user goes to a course with unopened homework

    # AND: Click on an unopened hw

    # AND: Change all the required fields

    # AND: Click “publish"

    # THEN: User is taken back to the Calender

    # AND: The edits should be saved
