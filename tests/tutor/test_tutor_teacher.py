@test_case('')
@tutor
def test_edit_student_ID(tutor_base_url, selenium, teacher):
    """Test teacher to edit student ID."""
    # GIVEN: A logged in teacher user
    # AND: has a existing course
    # AND: has at least one student

    # WHEN: Select a Tutor course
    # AND: Click "course roster"
    # AND: Edit student ID by clicking on the little pencil sign near student id

    # THEN: the student's id is edited

    # WHEN: The user resets the student's id

    # THEN: The student's id is reset


@test_case('')
@tutor
def test_change_student_section(tutor_base_url, selenium, teacher):
    """Test teacher to change a student's enrolled section."""
    # GIVEN: Logged into tutor as a teacher
    # AND: has a existing course
    # AND: has at least one student
    # AND: has two or more sections

    # WHEN: Select a Tutor course
    # AND: Click ""course roster""
    # AND: Choose a student, click ""change section""

    # THEN: the student's section is changed

    # WHEN: The user resets the student's section

    # THEN: The student's section is reset


@test_case('')
@tutor
def test_drop_a_student(tutor_base_url, selenium, teacher):
    """Test teacher to drop a student."""
    # GIVEN: Logged into tutor as a teacher
    # AND: has a existing course
    # AND: has at least one student

    # WHEN: Select a Tutor course
    # AND: Click ""course roster""
    # AND: Click ""drop"" next to a students' name

    # THEN: the student should be removed from students' name list and appear in dropped student section


@test_case('')
@tutor
def test_readd_dropped_student(tutor_base_url, selenium, teacher):
    """Test teacher to readd a dropped student."""
    # GIVEN: Logged into tutor as a teacher
    # AND: has a existing course
    # AND: has at least one dropped student

    # WHEN: Select a Tutor course
    # AND: Click ""course roster""
    # AND: Click ""add back to active roster"" next to a dropped student's name

    # THEN: student should be removed from "dropped student" section and appear back at the student name list


@test_case('')
@tutor
def test_remove_instructor(tutor_base_url, selenium, teacher):
    """Test teacher to remove an instructor."""
    # GIVEN: Logged into tutor as a teacher
    # AND: has a existing course
    # AND: has another instruction

    # WHEN: Select a Tutor course
    # AND: Click ""course roster""
    # AND: Click ""remove"" next to another instructor's name

    # THEN: a remove button should appear


@test_case('')
@tutor
def test_remove_oneself_from_instructor(tutor_base_url, selenium, teacher):
    """Test teacher to remove oneself from instructor."""
    # GIVEN: Logged into tutor as a teacher
    # AND: has a existing course

    # WHEN: Select a Tutor course
    # AND: Click ""course roster""
    # AND: Click ""remove"" next to the name of the teacher itself

    # THEN: a remove button with the message "If user remove User's self from the course user
    # will be redirected to the dashboard." should appeared


@test_case('')
@tutor
def test_view_calendar(tutor_base_url, selenium, teacher):
    """Test teacher to view the calendar."""
    # GIVEN: A logged in teacher user
    # AND: has a existing course

    # WHEN: Select a Tutor course

    # THEN: The teacher is presented their calendar dashboard


@test_case('')
@tutor
def test_view_student_score_w_calendar_button(tutor_base_url, selenium, teacher):
    """Test teacher to view student score with calendar button."""
    # GIVEN: A logged in teacher user
    # AND: has a existing course

    # WHEN: Select a Tutor course
    # AND: Click "Student Scores"

    # THEN: the teacher is presented with their students' scores each section/period


@test_case('')
@tutor
def test_view_performance_forecast_w_calendar_button(tutor_base_url, selenium, teacher):
    """Test teacher to view performance forecast with calendar button."""
    # GIVEN: A logged in teacher user
    # AND: has a existing course

    # WHEN: Select a Tutor course
    # AND: Click "Performance Forecast"

    # THEN: the teacher is presented with performance forecast fot the sections


@test_case('')
@tutor
def test_view_reading_assignment_summary(tutor_base_url, selenium, teacher):
    """Test teacher to view a reading assignment summary."""
    # GIVEN: A logged in teacher user
    # AND: has a existing course
    # AND: has a reading assignment

    # WHEN: Select a Tutor course
    # AND: From the user calendar, click on a reading that is displayed

    # THEN: the teacher is presented with a summary of information about the reading


@test_case('')
@tutor
def test_view_homework_assignment_summary(tutor_base_url, selenium, teacher):
    """Test teacher to view a homework assignment ."""
    # GIVEN: A logged in teacher user
    # AND: has a homework assignment

    # WHEN: Select a Tutor course
    # AND: From the user calendar, click on a homework assignment that is displayed"

    # THEN: The teacher is presented with a summary of the homework assignment.


@test_case('')
@tutor
def test_view_external_assignment_summary(tutor_base_url, selenium, teacher):
    """Test teacher to view an external assignment."""
    # GIVEN: A logged in teacher user
    # AND: has an external assignment

    # WHEN: Select a Tutor course
    # AND: From the user calendar, click on external assignment that is displayed""

    # THEN: The teacher is presented with a summary of the external assignment.


@test_case('')
@tutor
def test_view_event_summary(tutor_base_url, selenium, teacher):
    """Test teacher to view an event."""
    # GIVEN: A logged in teacher user
    # AND: has a existing course
    # AND: has a event

    # WHEN:  Select a Tutor course
    # AND: From the user calendar, click on an event that is displayed""

    # THEN: The teacher is presented with a summary of the selected event.


@test_case('')
@tutor
def test_open_reference_book_w_calendar_button(tutor_base_url, selenium, teacher):
    """Test teacher to open a reference book with calendar button."""
    # GIVEN: A logged in teacher user
    # AND: has a existing course

    # WHEN: Select a Tutor course
    # AND: Click on the 'Browse The Book' button on the user dashboard""

    # THEN: The teacher is presented with the book in a new tab


@test_case('')
@tutor
def test_return_to_course_picker(tutor_base_url, selenium, teacher):
    """Test teacher return to course picker by clicking logo."""
    # GIVEN: A logged in teacher user
    # AND: has a existing course

    # WHEN: Select a Tutor course
    # AND: Click on the OpenStax logo at the top of the page""

    # THEN: The teacher should be returned to a page displaying all of their courses.


@test_case('')
@tutor
def test_add_by_drag(tutor_base_url, selenium, teacher):
    """Test teacher to add assignments/readings/events by drag and drop."""
    # GIVEN: A logged in teacher user
    # AND: has a existing course

    # WHEN: Select a Tutor course
    # AND: Drag ""assignments/reading/external assignment/event"" from the left menu to a day on calendar""

    # THEN: The page for creating new assignment/reading/external assignment/event should open with the
    # due date already fill in as the day user dragged it to on calendar.


@test_case('')
@tutor
def test_add_assignment_to_past_day(tutor_base_url, selenium, teacher):
    """Test teacher to attempt to add and assignment to past day."""
    # GIVEN: A logged in teacher user
    # AND: has a existing course

    # WHEN: Select a Tutor course
    # AND: Click on a past day and drag assignments onto a past day""

    # THEN: User shouldn't be able to access past dates on calendar


@test_case('')
@tutor
def test_view_course_setting_w_menu(tutor_base_url, selenium, teacher):
    """Test teacher use the user drop bar menu to view course setting."""
    # GIVEN: A logged in teacher user
    # AND: has a existing course

    # WHEN: Select a Tutor course
    # AND: Click ""course setting"" in the menu""

    # THEN: User should be taken to the settings page


@test_case('')
@tutor
def test_view_course_roaster_w_menu(tutor_base_url, selenium, teacher):
    """Test teacher use user drop bar menu to view course roaster."""
    # GIVEN: A logged in teacher user
    # AND: has a existing course

    # WHEN: Select a Tutor course
    # AND: Click ""course roster"" from menu""

    # THEN: User should be taken to course roster page


@test_case('')
@tutor
def test_question_library(tutor_base_url, selenium, teacher):
    """Test if question library works under teacher."""
    # GIVEN: A logged in teacher user
    # AND: has a existing course

    # WHEN:  Select a Tutor course
    # AND: Click ""question library"" from the calendar"

    # THEN: user should be taken to the question library


@test_case('')
@tutor
def test_back_to_performance_forecast(tutor_base_url, selenium, teacher):
    """Test teacher to go back to performance forecast."""
    # GIVEN: A logged in teacher user
    # AND: has a existing course

    # WHEN: Select a Tutor course
    # AND: Go to ""performance forecast""
    # AND: Go to dashboard/question library""

    # THEN: back to performance forecast"" button should be present
    # AND: clicking ""back to performance forecast"" button should take user back to performance forecast page"


@test_case('')
@tutor
def test_back_to_scores(tutor_base_url, selenium, teacher):
    """Test teacher to go back to scores."""
    # GIVEN: A logged in teacher user
    # AND: has a existing course

    # WHEN: Select a Tutor course
    # AND: Go to student scores
    # AND: Go to dashboard/performance forecast/question library""

    # THEN: back to scores"" button should be present
    # AND: clicking ""back to scores"" button should take user back to scores"


@test_case('')
@tutor
def test_back_to_question_library(tutor_base_url, selenium, teacher):
    """Test teacher to go back to question library."""
    # GIVEN: A logged in teacher user
    # AND: has a existing course

    # WHEN: Go to question library
    # AND: Go to performance forecast/dashboard, ""back to question library"" button should be present
    # AND: Click on the ""back to question library""

    # THEN: User is taken back to question library page


@test_case('')
@tutor
def test_back_to_dashboard(tutor_base_url, selenium, teacher):
    """Test teacher to go back to dashboard."""
    # GIVEN: A logged in teacher user
    # AND: has a existing course

    # WHEN: go to performance forecast/question library, ""back to dashboard"" button should be present
    # AND: Click on the ""Back to dashboard"" button""

    # THEN: User is taken back to the dashboard


@test_case('')
@tutor
def test_accessibility_infor(tutor_base_url, selenium, teacher):
    """Test teacher to use accessibility info page."""
    # GIVEN: A logged in teacher user

    # WHEN: Click ""help""
    # AND: Click ""accessibility statement""

    # THEN: User is directed to accessibility info page


@test_case('')
@tutor
def test_online_support_form(tutor_base_url, selenium, teacher):
    """Test teacher to use online support form."""
    # GIVEN: A logged in teacher user

    # WHEN: Click ""help""
    # AND: Click ""chat with support""

    # THEN: User is tanekn to online support form


@test_case('')
@tutor
def test_training_wheels(tutor_base_url, selenium, teacher):
    """Test teacher to use training wheels on question library page."""
    # GIVEN: A logged in teacher user

    # WHEN: Click on the ""Question Library"" button from the user dashboard
    # AND: Click on ""Help"" dropdown menu

    # AND: A super training wheel appears on the page


@test_case('')
@tutor
def test_super_training_wheel(tutor_base_url, selenium, teacher):
    """Test under new teacher, super training wheel triggered automatically first visit ."""
    # GIVEN: logged in Tutor as new verified teacher

    # WHEN: Navigate to each of the following pages for the first time: My Courses,
    # Preview Course Dashboard, Question Library, Add Reading

    # THEN: Going to My Courses, Preview Course Dashboard, Question Library,
    # Add Reading should have training wheel triggered


@test_case('')
@tutor
def test_training_wheel_no_reappear(tutor_base_url, selenium, teacher):
    """Test training wheel doesn't reappear after teacher create a course."""
    # GIVEN: A logged in teacher user

    # WHEN: Check that the ""Create a Course"" training wheel pops up
    # AND: Navigate to another page
    # AND: Click back to the ""My Courses"" page

    # THEN: User is able to see "Create a Course" training wheel.


@test_case('')
@tutor
def test_active_super_training_wheels(tutor_base_url, selenium, teacher):
    """Test teacher to activate super training wheels."""
    # GIVEN: A logged in teacher user

    # WHEN: Click on bottom left corner of window

    # THEN: User is in spy mode(as indicated by a pi symbol).


@test_case('')
@tutor
def test_training_wheels_dashboard(tutor_base_url, selenium, teacher):
    """Test teacher to use training wheels for dashboard`."""
    # GIVEN: A logged in teacher user

    # WHEN: Click on a current course to navigate to Dashboard
    # AND: Activate Spy Mode
    # AND: Pop-up should show with the options ""View Tips Now"" and ""View Later""
    # AND:Click ""View Tips Now""

    # THEN: User should be taken through a training wheels tour detailing the creation of assignments,
    # the options at the top, the user dropdown options, and the navbar


@test_case('')
@tutor
def test_physics_stu_preview_vidz(tutor_base_url, selenium, teacher):
    """Test teacher to embed physics student preview videos."""
    # GIVEN: A logged in teacher user

    # WHEN: Navigate to a Physics class
    # AND: Click on the small video icon on the top navbar

    # Dashboard preview: https://usertu.be/IbYU5py9YP8
    # Physics HW: https://usertu.be/Ic2_9LYXY84
    # Physics Reading: https://usertu.be/tCocd4jCVCA


@test_case('')
@tutor
def test_soci_stu_preview_vidz(tutor_base_url, selenium, teacher):
    """Test teacher to embed sociology student preview videos."""
    # GIVEN: A logged in teacher user

    # WHEN:  Navigate to a Sociology class
    # AND: Click on the small video icon on the top navbar

    # THEN: User is taken to usertube videos with the following links:
    # Dashboard preview: https://usertu.be/IbYU5py9YP8
    # Soci HW: https://usertu.be/Ki-y2AywXlI
    # Soci Reading: https://usertu.be/GF05th84Bw8


@test_case('')
@tutor
def test_bio_stu_preview_vidz(tutor_base_url, selenium, teacher):
    """Test teacher to embed biology student preview videos."""
    # GIVEN: A logged in teacher user

    # WHEN: Navigate to a Biology class
    # AND: Click on the small video icon on the top navbar

    # THEN: User is taken to usertube videos embedded with the following links:
    # Dashboard preview: https://usertu.be/IbYU5py9YP8
    # Bio HW: https://usertu.be/kzvHLFsQDTM
    # Bio Reading: https://usertu.be/4neNaHRyTUw


@test_case('')
@tutor
def test_support_page(tutor_base_url, selenium, teacher):
    """Test teacher to go to OpenStax Support page."""
    # GIVEN: A logged in teacher user

    # WHEN: Click "help articles" from user menu

    # THEN: User is taken to openstax support page


@test_case('')
@tutor
def test_open_guide_new_tab(tutor_base_url, selenium, teacher):
    """Test teacher to open 'Best Practices Guide' in a new tab."""
    # GIVEN: A logged in teacher user

    # WHEN: Click "best practices" from user menu

    # THEN: User is taken to the best practices page


@test_case('')
@tutor
def test_nag_new_course(tutor_base_url, selenium, teacher):
    """Test 'Nag' teacher each time they create a new course."""
    # GIVEN: A logged in teacher user

    # WHEN: User creates a full Tutor course

    # THEN: User should see the Nag message pop up


@test_case('')
@tutor
def test_nag_second_login(tutor_base_url, selenium, teacher):
    """Test 'Nag' teachers upon their second login/session."""
    # GIVEN: logged in Tutor as a new verified teacher

    # WHEN: Create a full tutor course
    # AND: Mess around in course a bit
    # AND: Leave the course
    # AND: Return to the course

    # THEN: User should see the Nag message pop up


@test_case('')
@tutor
def test_nag_reappears(tutor_base_url, selenium, teacher):
    """Test 'Nag' reappears if user select 'I don't know yet' option."""
    # GIVEN: logged in Tutor as a new verified teacher

    # WHEN: Create full tutor course
    # AND: Answer with the ""I don't know yet"" option
    # AND: Log out from teacher
    # AND: Log back into teacher
    # AND: Click back on the same course user just made

    # THEN: User should see the Nag message pop up


@test_case('')
@tutor
def test_nag_not_pop_up(tutor_base_url, selenium, teacher):
    """Test 'nag' survey does not pop up when answering 'I won't be using it'."""
    # GIVEN: logged in Tutor as a new verified teacher

    # WHEN: Create full tutor course
    # AND: Answer the ""Nag"" with the ""I won't be using it"" option

    # THEN: The survey does not show up


@test_case('')
@tutor
def test_nag_not_reappear(tutor_base_url, selenium, teacher):
    """Test 'Nag' doesn't reappear if user don't select 'I don't know yet' option."""
    # GIVEN: logged in Tutor as a new verified teacher

    # WHEN:  Create full tutor course
    # AND: Answer with any option BUT the ""I don't know yet"" option
    # AND: Log out from teacher
    # AND: Log back into teacher
    # AND: Click back on the same course user just made

    # THEN: The "Nag" should not pop back up


@test_case('')
@tutor
def test_nag_in_preview_course_second(tutor_base_url, selenium, teacher):
    """Test 'Nag' in preview course - every 2nd assignment."""
    # GIVEN: logged in as a teacher account that doesn't already have any courses

    # WHEN: Go to Preview Course
    # AND: Make 2 assignments (HW, reading, or external)

    # THEN: Upon making the 2nd assignment, a Nag should pop up saying "Remember -- this is just a preview course!"
    # and encouraging the user to "Create a Course"


@test_case('')
@tutor
def test_nag_in_preview_course_expires(tutor_base_url, selenium, teacher):
    """Test 'Nag' in preview course - preview expires."""
    # GIVEN: logged in as a teacher account that doesn't already have any courses

    # WHEN: Navigate to preview course
    # AND: Get course number/title
    # AND: Login as admin on separate browser
    # AND: Go to dropdown > Admin > Course Organization > Courses
    # AND: Search for and click on the specific preview course that user found above (distinguishing by course no.)
    # AND: Click to edit
    # AND: Change the End Date to be soon (~1 or 2 min)
    # AND: Navigate back to teacher account
    # AND: Refresh after the new course End Date has passed

    # THEN: Nag should show up urging Tutor Adoption and saying "Preview Course has expired"


@test_case('')
@tutor
def test_nag_in_preview_course_launching(tutor_base_url, selenium, teacher):
    """Test 'Nag' in preview course - stop after launching full course."""
    # GIVEN: A logged in teacher user

    # WHEN: Navigate to Preview Course

    # THEN: the user should not see any "Create a Course" button on the Navbar, nor any tutor adoption nags


@test_case('')
@tutor
def test_nag_in_preview_course_create(tutor_base_url, selenium, teacher):
    """Test 'Nag' in preview course - create a course button."""
    # GIVEN: A logged in teacher user

    # WHEN: Navigate to preview course

    # THEN: User should see "Create a Course" button on the Navbar at the top


@test_case('')
@tutor
def test_setup_nag_appear(tutor_base_url, selenium, teacher):
    """Test teacher to setup now 'nag' appearing on first initialization of preview course."""
    # GIVEN: A verified instructor account made at least 4 hours before the test is conducted

    # WHEN: Four hours after the instructor account was created, click on a preview course

    # THEN: User should see A "Nag" encouraging teachers to create their own course


@test_case('')
@tutor
def test_pop_up_for_unverified_instructor(tutor_base_url, selenium, teacher):
    """Test modal popup for unverified instructor signing up for new tutor account."""
    # GIVEN:  Be at the Tutor page

    # WHEN: Log into unverified teacher account

    # THEN: User should not see the Key value prop/product differentiators on the My Courses
    # page for an unverified teacher


@test_case('')
@tutor
def test_pop_up_for_verified_instructor(tutor_base_url, selenium, teacher):
    """Test modal popup for verified instructor signing up for new tutor account."""
    # GIVEN:  Be at the Tutor page

    # WHEN: Log into verified teacher account

    # THEN: User should see the Key value prop/product differentiators on the My Courses
    # page for a verified teacher


@test_case('')
@tutor
def test_term_appearance_new(tutor_base_url, selenium, teacher):
    """Test terms/PP appearance for onboarding | new instructor."""
    # GIVEN:  Be at the Tutor page

    # WHEN: Log into verified teacher account
    # AND: Pick a course

    # THEN: In that course, the instructor is shown terms
    # AND:Once agreed, the instructor is taken to the course dashboard.


@test_case('')
@tutor
def test_term_appearance_exist(tutor_base_url, selenium, teacher):
    """Test terms/PP appearance for onboarding | existing instructor."""
    # GIVEN: Having changed the terms of a particular course as admin

    # WHEN: Log in as teacher and go to that course page.
    # AND: Enters a course.

    # THEN: the teacher is shown the terms when they changed.
