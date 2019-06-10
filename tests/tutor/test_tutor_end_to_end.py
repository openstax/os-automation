"""The OpenStax Tutor Beta automation smoke tests.

These cover a wide range of features to satisfy end-to-end
testing for high priority areas.
"""

from datetime import datetime, timedelta
from time import sleep

from pages.tutor.home import TutorHome
from tests.markers import nondestructive, skip_test, test_case, tutor
from utils.tutor import Tutor
from utils.utilities import Utility


@test_case('C485035')
@tutor
def test_create_and_clone_a_course(tutor_base_url, selenium, teacher):
    """Test creating and cloning courses."""
    book = Tutor.BOOKS[Utility.random(0, len(Tutor.BOOKS) - 1)]
    term = Tutor.TERMS[Utility.random(0, len(Tutor.TERMS) - 1)]
    today = datetime.now()
    course_name = f"{book} Auto-{today.year}{today.month:02}{today.day:02}"
    timezone = Tutor.TIMEZONE[Utility.random(0, len(Tutor.TIMEZONE) - 1)]
    total_sections = Utility.random(1, 4)
    estimated_students = Utility.random(1, 500)
    event_name = f"Event_{today.year}{today.month:02}{today.day:02}"
    opens_on = (today + timedelta(days=1)).strftime("%m/%d/%Y")
    closes_on = (today + timedelta(days=2)).strftime("%m/%d/%Y")

    # GIVEN: a verified Tutor instructor viewing their dashboard
    home = TutorHome(selenium, tutor_base_url).open()
    courses = home.log_in(*teacher)

    # WHEN:  they click on the 'CREATE A COURSE' tile
    # AND:   select a course book and click the 'Continue' button
    # AND:   select a course term and click the 'Continue' button
    # AND:   select 'Create a new course' and click the 'Continue' button
    # AND:   enter a name for the course, selects a time zone for the course,
    #        and click the 'Continue' button
    # AND:   enter the number of course sections, estimated number of students,
    #        and click the 'Continue' button
    # AND:   click through any training wheel modals
    sleep(0.1)
    new_course = courses.create_a_course()
    new_course.course.select_by_title(book)
    new_course.next()
    new_course.term.select_by_term(term)
    new_course.next()
    if new_course.clone_possible:
        new_course.new_or_clone.create_a_new_course()
        new_course.next()
    new_course.name.name = course_name
    new_course.name.timezone = timezone
    new_course.next()
    new_course.details.sections = total_sections
    new_course.details.students = estimated_students
    calendar = new_course.next()
    calendar.clear_training_wheels()

    # THEN:  the instructor calendar is displayed for the new course
    assert(calendar.is_displayed()), \
        f'Calendar not displayed; at "{calendar.location}"'

    # WHEN:  an event is published to the course
    # AND:   the user returns to the courses page
    # AND:   clicks the 'Copy this course' button on the course tile for the
    #        recently created course
    # AND:   select a course term and click the 'Continue' button
    # AND:   enter a name for the course, selects a time zone for the course,
    #        and click the 'Continue' button
    # AND:   enter the number of course sections, estimated number of students,
    #        and click the 'Continue' button
    # AND:   click through any training wheel modals
    calendar.add_assignment(
        assignment=Tutor.EVENT,
        name=event_name,
        description="assignment clone test",
        open_on=opens_on,
        due_on=closes_on,
        action=Tutor.PUBLISH
    )
    dashboard = calendar.nav.menu.view_my_courses()
    selection = dashboard.current_courses.select_course_by_name(course_name)
    clone_course = selection.course_clone()
    clone_course.term.term = term
    clone_course.next()
    clone_course.name.name = course_name + " Clone"
    clone_course.name.timezone = timezone
    clone_course.next()
    clone_course.details.sections = total_sections
    clone_course.details.students = estimated_students
    calendar = clone_course.next()
    calendar.clear_training_wheels()

    # THEN:  the instructor calendar is displayed for the new course
    assert(calendar.is_displayed()), \
        f'Calendar not displayed; at "{calendar.location}"'

    # WHEN:  the 'Add Assignment' bar is opened
    if not calendar.sidebar.is_open:
        calendar.banner.add_assignment()

    # THEN:  the event assignment name from the original course is displayed
    assert(event_name in [assignment.title
                          for assignment
                          in calendar.sidebar.copied_assignments])


@skip_test
@test_case('C485036')
@tutor
def test_edit_course_settings_and_manage_course_students(
        tutor_base_url, selenium, teacher):
    """Test course settings and student management."""
    # GIVEN: a Tutor teacher viewing their course calendar

    # WHEN:  they select 'Course Settings' from the 'Menu'

    # THEN:  the 'Course settings' page is displayed
    # AND:   an enrollment URL is displayed for each course section

    # WHEN:  they click on the pencil icon to the right of the course name
    # AND:   edit the course name in the 'Rename Course' pop up box and click
    #        the 'Rename' button

    # THEN:  the course name is changed

    # WHEN:  they click on the 'DATES AND TIME' tab
    # AND:   click on the pencil icon to the right of the time zone
    # AND:   select a timezone radio button and click the 'Save' button

    # THEN:  the timezone is changed

    # WHEN:  they select 'Course Roster' from the 'Menu'

    # THEN:  the 'Course roster' page is displayed

    # WHEN:  they click on the '+ Add Instructor' link

    # THEN:  the instructor enrollment URL is displayed in a pop up box

    # WHEN:  they click on the 'x'
    # AND:   click on the 'Add Section' link
    # AND:   enter a section name and click the 'Add' button

    # THEN:  the section is added

    # WHEN:  they click on the 'Rename' link
    # AND:   enter a section name and click the 'Rename' button

    # THEN:  the section name is changed

    # WHEN:  they click on the pencil icon in the 'Student ID' column
    # AND:   enter an ID and send the tab key

    # THEN:  the ID is changed

    # WHEN:  they click the 'Change Section' link for a student
    # AND:   select a different section

    # THEN:  the student is moved to the selected section

    # WHEN:  they click the 'Drop' link for a student
    # AND:   click the 'Drop' button

    # THEN:  the student is moved to the 'Dropped Students' list

    # WHEN:  they click the 'Add Back to Active Roster` link for a student
    # AND:   click the 'Add <student name>?' button

    # THEN:  the student is moved to the active roster


@skip_test
@test_case('C485037')
@nondestructive
@tutor
def test_course_registration_and_initial_assignment_creation_timing(
        tutor_base_url, selenium):
    """Test student enrollment and initial assignment creation time."""
    # GIVEN: a user viewing the Tutor home page

    # WHEN:  they go to the student enrollment URL
    # AND:   click the 'Get started' button
    # AND:   sign up for an account
    # AND:   enter the student ID and click the 'Continue' button
    # AND:   click the 'I agree' button
    # IF:    using a production-based instance
    #  THEN: click the 'Try free for 14 days' button
    #  ELSE: fill out the purchase form address, city, state, zip code,
    #        credit  card  number, expiration date, CVV code, billing zip
    #        code, and click the 'Purchase' button
    # AND:   click the 'Access your course' button
    # AND:   click through any training wheel modals

    # THEN:  the current week dashboard is displayed

    # WHEN:  the loading spinner goes away

    # THEN:  assignments are populated in 'THIS WEEK' and/or 'ALL PAST WORK'


@skip_test
@test_case('C485038')
@tutor
def test_assignment_creation_readings(tutor_base_url, selenium):
    """Test publishing a reading.

    Start a new reading from the assignment menu, publish it, edit it and
    rename it.

    """
    # GIVEN: a Tutor teacher viewing their course calendar

    # WHEN:  they open the 'Add Assignment' taskbar
    # AND:   click on the 'Add Reading' link
    # AND:   fill out the assignment name and description, set the open date
    #        to today, set the open time to now, set the due date to tomorrow,
    #        set the due time to 12:00 pm, and click on the '+ Add Readings'
    #        button
    # AND:   select a chapter or 2+ individual sections and click the 'Add
    #        Readings' button

    # THEN:  the selected readings should be displayed under the currently
    #        selected table

    # WHEN:  they click the 'Publish' button

    # THEN:  the course calendar is displayed
    # AND:   the new reading name is displayed on tomorrow's date box

    # WHEN:  they click the reading name and then click 'View Assignment'
    #        button
    # AND:   enter a new assignment name and click the 'Save' button

    # THEN:  the course calendar is displayed
    # AND:   the modified reading name is displayed on tomorrow's date box


@skip_test
@test_case('C485049')
@tutor
def test_assignment_creation_homework(tutor_base_url, selenium):
    """Test publishing each assignment type.

    Start a new homework from the calendar date, save it as a draft, then
    publish it.

    """
    # GIVEN: a Tutor teacher viewing their course calendar

    # WHEN:  they click on an available date box on the calendar
    # AND:   click on the 'Add Homework' link

    # THEN:  the due date should match the selected date box

    # WHEN:  they fill out the assignment name and description, select a 'Show
    #        feedback' option, and click the '+ Select Problems' button
    # AND:   select 2-3 non-introductory sections and click the 'Show
    #        Problems' button

    # THEN:  the selected section buttons are displayed in the secondary
    #        toolbar

    # WHEN:  they select 1-3 assessments from each available section

    # THEN:  the 'My Selections' shows the total number of assessments selected

    # WHEN:  they click on the 'Next' button
    # AND:   click on the 'Save as Draft' button

    # THEN:  the course calendar is displayed
    # AND:   the new homework name is displayed on the selected date box and
    #        is prefixed with 'draft'

    # WHEN:  they click on the homework name
    # AND:   click the 'Publish' button

    # THEN:  the course calendar is displayed
    # AND:   the homework name is displayed on the selected date box and is
    #        not prefixed with 'draft'


@skip_test
@test_case('C485050')
@tutor
def test_assignment_creation_external(tutor_base_url, selenium):
    """Test publishing each assignment type.

    Start a new external assignment by drag-and-drop onto the calendar date,
    publish it, then delete it.

    """
    # GIVEN: a Tutor teacher viewing their course calendar

    # WHEN:  they open the 'Add Assignment' taskbar
    # AND:   click and drap the 'Add External Assignment' bar onto an
    #        available date box on the calendar

    # THEN:  the due date should match the selected date box

    # WHEN:  they fill out the assignment name, description, and assignment
    #        URL, and click the 'Publish' button

    # THEN:  the course calendar is displayed
    # AND:   the new external assignment name is displayed on the selected
    #        date box

    # WHEN:  they click on the assignment name
    # AND:   click the 'Edit Assignment' button

    # THEN:  the 'Edit External Assignment' window is displayed

    # WHEN:  they click the 'Delete' button and click the 'Delete' button in
    #        the pop up

    # THEN:  the course calendar is displayed
    # AND:   the external assignment name is no longer displayed on the
    #        selected date box


@skip_test
@test_case('C485051')
@tutor
def test_assignment_creation_event(tutor_base_url, selenium):
    """Test publishing each assignment type.

    Start a new event from the assignment menu, switch it to individual section
    assignment, then publish it.

    """
    # GIVEN: a Tutor teacher viewing their course calendar

    # WHEN:  they open the 'Add Assignment' taskbar
    # AND:   click the 'Add Event' link
    # AND:   fill out the event name and description, click the radio button
    #        to the right of 'Individual Sections', set the open dates to
    #        today +1, +2, ..., and the due dates to today +2, +3, ..., and
    #        click the 'Publish' button

    # THEN:  the course calendar is displayed
    # AND:   the event name is displayed on the first due date box


@skip_test
@test_case('C485039')
@tutor
def test_student_task_reading_assignment(tutor_base_url, selenium):
    """Test a student working a reading assignment.

    While working the assignment, free response answer validation,
    highlighting, and annotation will also be checked.

    """
    # GIVEN: a Tutor student enrolled in a course with a reading assignment

    # WHEN:  they click on the assignment name

    # THEN:  the first task step is displayed

    # WHEN:  they select a section of text
    # AND:   click the highlighter icon

    # THEN:  a text highlight in included

    # WHEN:  they select a different section of text
    # AND:   click the speech bubble icon
    # AND:   enter text in the annotation box and click the check mark button

    # THEN:  a text highlight is included
    # AND:   a speech bubble icon is displayed to the right of the highlight

    # WHEN:  they click the highlight summary icon

    # THEN:  the highlight and the annotation are displayed

    # WHEN:  they click the highlight summary icon
    # AND:   advance through the assignment unti a two-step question is reached
    # AND:   enter random text in the text area and click the 'Answer' button

    # THEN:  the answer verification flags the answer

    # WHEN:  they enter new text is in the text area and click the 'Re-answer'
    #        button

    # THEN:  the multiple choice answers are displayed

    # WHEN:  they proceed through the rest of the assignment reaching the 'You
    #        are done.' step
    # AND:   click the milestones icon

    # THEN:  the milestones are displayed
    # AND:   there is a card for each step

    # WHEN:  they click the milestones icon
    # AND:   click the 'Back to Dashboard' button

    # THEN:  the 'THIS WEEK' dashboard is displayed
    # AND:   the reading assignment progress is 'Complete'


@skip_test
@test_case('C485040')
@tutor
def test_student_task_homework_assignment(tutor_base_url, selenium):
    """Test a student working a homework assignment.

    This will include standard two-step, standard multiple choice and
    multi-part assessments.

    """
    # GIVEN: a Tutor student enrolled in a course with a homework assignment

    # WHEN:  they click on the assignment name
    # AND:   work each step
    # AND:   click the 'Back to Dashboard' button

    # THEN:  the student dashboard is displayed
    # AND:   the homework assignment progress is 'N/N answered' or 'X/Y
    #        correct'


@skip_test
@test_case('C485041')
@tutor
def test_student_task_practice(tutor_base_url, selenium):
    """Test a student working a practice question set.

    Practice a section and practice the student's weakest topics.

    """
    # GIVEN: a Tutor student enrolled in a course with at least one reading or
    #        homework

    # WHEN:  they click the 'Practice more to get forecast' button or a
    #        forecast bar

    # THEN:  a practice session with between 1 - 5 questions from the selected
    #        section is displayed

    # WHEN:  they answer all questions

    # THEN:  the 'You are done.' card is displayed

    # WHEN:  they click the 'Back to Dashboard' button

    # THEN:  the student dashboard is displayed
    # AND:   the section shows the new total of question worked for the
    #        selected section

    # WHEN:  they click the 'Practice my weakest topics' button

    # THEN:  a practice session with between 1 - 5 questions is displayed


@skip_test
@test_case('C485042')
@tutor
def test_teacher_viewing_student_scores(tutor_base_url, selenium, teacher):
    """Test an instructor viewing the course scores page.

    Review the scores for a student;
    accept a student's late work;
    review an assignment;
    review student work.

    """
    # GIVEN: a Tutor instructor with a course containing readings, homeworks,
    #        and/or external assignments with at least one student

    # WHEN:  they click on the 'Student Scores' button

    # THEN:  the scores page is displayed
    # AND:   the course average, homework score average, homework progress
    #        average, reading score average, reading progress average, and
    #        each assignment are displayed

    # WHEN:  they click the 'Set weights' link

    # THEN:  the score weights are displayed

    # WHEN:  they change the weights to not total 100%

    # THEN:  an information alert is displayed

    # WHEN:  they click the 'Restore default' link

    # THEN:  the weights are 100%, 0%, 0%, and 0%, respectively

    # WHEN:  they change the weights to equal 100% and click the 'Save' button

    # THEN:  the wights modal is closed and the course average is updated

    # WHEN:  they click an assignment 'Review' link

    # THEN:  the assignment review is displayed

    # WHEN:  they go back to the scores page
    # AND:   click a student name

    # THEN:  the student's performance forecast is displayed

    # WHEN:  they click the 'Back to Scores' button
    # AND:   click a late work arrow
    # AND:   click the 'Accept late score' button

    # THEN:  the assignment on time score is replaced by the late work score

    # WHEN:  they click the late work arrow
    # AND:   click the 'Use this score' button

    # THEN:  the assignment late work score is replaced by the on time score

    # WHEN:  they click the scores spreadsheet download icon

    # THEN:  the spreadsheet is downloaded


@skip_test
@test_case('C485043')
@nondestructive
@tutor
def test_student_viewing_student_scores(tutor_base_url, selenium, student):
    """Test a student viewing their scores page."""
    # GIVEN: a Tutor student with a reading, homework and external assignment

    # WHEN:  they click on the 'Scores' link in the 'Menu'

    # THEN:  the scores page is displayed
    # AND:   a course average, homework score, homework progress, reading
    #        score, reading progress, and each assignment are displayed

    # WHEN:  they click the 'View weights' link

    # THEN:  the score weights are displayed

    # WHEN:  they click the 'Close' button

    # THEN:  the weights modal is closed


@skip_test
@test_case('C485044')
@nondestructive
@tutor
def test_teacher_viewing_the_course_performance_forecast(
        tutor_base_url, selenium, teacher):
    """Test an instructor viewing the course performance forecast."""
    # GIVEN: a Tutor instructor with a course containing readings, homeworks,
    #        and/or external assignments with at least one student

    # WHEN:  they click on the 'Performance Forecast' button

    # THEN:  the performance forecast is displayed
    # AND:   each course section tab is available
    # AND:   weaker areas and each chapter are displayed
    # AND:   each chapter and section displayed show a progress bar or 'Not
    #        enough exercises completed' message


@skip_test
@test_case('C485045')
@tutor
def test_student_viewing_their_performance_forecast(
        tutor_base_url, selenium, student):
    """Test a student using their performance forecast.

    View the performance forecast;
    practice a chapter.

    """
    # GIVEN: a Tutor student enrolled in a course with at least one completed
    #        reading or homework

    # WHEN:  they click the 'Performance Forecast' link in the 'Menu'

    # THEN:  the performance forecast is displayed

    # WHEN:  they click a chapter progress bar or chapter 'Pracitce more to
    #        get forecast' button

    # THEN:  a practice session is loaded for the selected chapter
