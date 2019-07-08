"""The OpenStax Tutor Beta automation smoke tests.

These cover a wide range of features to satisfy end-to-end
testing for high priority areas.
"""

from datetime import datetime, timedelta

from pages.tutor.enrollment import Enrollment, StudentID
from pages.tutor.home import TutorHome
from tests.markers import nondestructive, test_case, tutor
from utils.email import RestMail
from utils.tutor import States, Tutor
from utils.utilities import Card, Utility


@test_case('C485035')
@tutor
def test_create_and_clone_a_course(tutor_base_url, selenium, teacher):
    """Test creating and cloning courses."""
    # SETUP:
    book = Tutor.BOOKS[Utility.random(0, len(Tutor.BOOKS) - 1)]
    term = Tutor.TERMS[Utility.random(0, len(Tutor.TERMS) - 1)]
    today = datetime.now()
    course_name = f"{book} Auto-{today.year}{today.month:02}{today.day:02}"
    timezone = Tutor.TIMEZONE[Utility.random(0, len(Tutor.TIMEZONE) - 1)]
    total_sections = Utility.random(1, 4)
    estimated_students = Utility.random(1, 500)
    event_name = f"Event_{today.year}{today.month:02}{today.day:02}"

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
        assign_to={Tutor.ALL: Tutor.RANDOM, },
        action=Tutor.PUBLISH
    )

    dashboard = calendar.nav.menu.view_my_courses()

    selection = dashboard.current_courses.get_course_tile(course_name)
    clone_course = selection.copy_this_course()

    clone_course.term.select_by_term(term)
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


@test_case('C485036')
@tutor
def test_edit_course_settings_and_manage_course_students(
        tutor_base_url, selenium, store):
    """Test course settings and student management."""
    # SETUP:
    test_data = store.get('C485036')
    user = test_data.get('username')
    if '-dev.' in tutor_base_url:
        password = test_data.get('password_dev')
    elif '-qa.' in tutor_base_url:
        password = test_data.get('password_qa')
    elif '-staging.' in tutor_base_url:
        password = test_data.get('password_staging')
    elif 'tutor.' in tutor_base_url:
        password = test_data.get('password_prod')
    else:
        password = test_data.get('password_unique')
    course_name = test_data.get('course_name')
    new_course_name = course_name + ' modified'
    new_timezone = Tutor.TIMEZONE[Utility.random(0, len(Tutor.TIMEZONE) - 1)]
    new_section_name = Utility.random_hex(8)
    edited_section_name = Utility.random_hex(12)
    new_student_id = Utility.random_hex(10, lower=True)

    # GIVEN: a Tutor teacher viewing their course calendar
    home = TutorHome(selenium, tutor_base_url).open()
    courses = home.log_in(user, password)
    calendar = courses.go_to_course(course_name)

    # WHEN:  they select 'Course Settings' from the 'Menu'
    settings = calendar.nav.menu.view_the_course_settings()

    # THEN:  the 'Course settings' page is displayed
    # AND:   an enrollment URL is displayed for each course section
    assert(settings.is_displayed)
    assert('settings' in settings.location)

    for section in settings.content.sections:
        assert(section.enrollment_url), \
            f'No enrollment URL found for section "{section.name}"'

    # WHEN:  they click on the pencil icon to the right of the course name
    # AND:   edit the course name in the 'Rename Course' pop up box and click
    #        the 'Rename' button
    rename = settings.edit_course_name()

    rename.name = new_course_name
    rename.rename()

    # THEN:  the course name is changed
    name = settings.course_name
    assert(name == new_course_name), \
        f'Course name ({name}) not changed to "{new_course_name}"'

    # reset the course name
    rename = settings.edit_course_name()
    rename.name = course_name
    rename.rename()

    # WHEN:  they click on the 'DATES AND TIME' tab
    # AND:   click on the pencil icon to the right of the time zone
    # AND:   select a timezone radio button and click the 'Save' button
    dates_and_times = settings.dates_and_time()

    timezone = dates_and_times.edit_timezone()

    timezone.select_timezone(new_timezone)
    timezone.save()

    # THEN:  the timezone is changed
    zone = dates_and_times.timezone
    assert(zone == new_timezone), \
        f'Timezone ({zone}) not changed to "{new_timezone}"'

    # reset the timezone
    timezone = dates_and_times.edit_timezone()
    timezone.select_timezone()
    timezone.save()

    # WHEN:  they select 'Course Roster' from the 'Menu'
    course_roster = settings.nav.menu.view_the_course_roster()

    # THEN:  the 'Course roster' page is displayed
    assert(course_roster.is_displayed)
    assert('roster' in course_roster.location)

    # WHEN:  they click on the '+ Add Instructor' link
    add_instructor = course_roster.instructors.add_instructor()

    # THEN:  the instructor enrollment URL is displayed in a pop up box
    assert(add_instructor.url), 'Instructor registration URL not available'

    # WHEN:  they click on the 'x'
    # AND:   click on the 'Add Section' link, enter a section name and click
    #        the 'Add' button
    add_instructor.close()

    course_roster.roster.add_section(new_section_name)

    # THEN:  the section is added
    assert(new_section_name in [section.name
                                for section
                                in course_roster.roster.sections]), \
        f'Section "{new_section_name}" not found'

    # WHEN:  they click on the 'Rename' link enter a section name and click
    #        the 'Rename' button
    course_roster.roster.select_section(new_section_name)
    course_roster.roster.rename_section(edited_section_name)

    # THEN:  the section name is changed
    assert(edited_section_name in [section.name
                                   for section
                                   in course_roster.roster.sections]), \
        f'Section "{edited_section_name}" not found'

    # reset the section list
    course_roster.roster.delete_section()

    # WHEN:  they click on the pencil icon in the 'Student ID' column enter an
    #        ID and send the tab key
    students = course_roster.roster.students
    student = students[Utility.random(0, len(students) - 1)]
    student_name = student.name
    student_id = student.student_id
    current_section = course_roster.roster.current_section
    other_sections = [section.name
                      for section
                      in course_roster.roster.sections
                      if section.name != edited_section_name]
    other_sections.remove(current_section)
    new_section = other_sections[Utility.random(0, len(other_sections) - 1)]
    student.student_id = new_student_id

    # THEN:  the ID is changed
    new_id = student.student_id
    assert(new_id == new_student_id), (
        f'ID for student {student_name} not changed ' +
        f'({new_id} != {new_student_id})')

    # reset the ID
    student.student_id = student_id

    # WHEN:  they click the 'Change Section' link for a student select a
    #        different section
    # AND:   view the selected section
    student.change_section(new_section)

    course_roster.roster.select_section(new_section)

    # THEN:  the student is moved to the selected section
    assert(student_name in [student.name
                            for student
                            in course_roster.roster.students]), \
        f"{student_name} ({student_id}) not found in period {new_section}"

    # move the student back to their original section
    ([student
      for student
      in course_roster.roster.students
      if student.name == student_name and student.student_id == student_id]
     [0].change_section(current_section))
    course_roster.roster.select_section(current_section)

    # WHEN:  they click the 'Drop' link for a student and click the 'Drop'
    #        button
    students = course_roster.roster.students
    student = students[Utility.random(0, len(students) - 1)]
    student_name = student.name
    student_id = student.student_id
    student.drop()

    # THEN:  the student is moved to the 'Dropped Students' list
    assert(student_name in [student.name
                            for student
                            in course_roster.roster.dropped_students]), \
        f"{student_name} ({student_id}) not found in the dropped students list"

    # WHEN:  they click the 'Add Back to Active Roster` link for a student and
    #        click the 'Add <student name>?' button
    ([student
      for student
      in course_roster.roster.dropped_students
      if student.name == student_name and student.student_id == student_id]
     [0].add_back_to_active_roster())

    # THEN:  the student is moved to the active roster
    assert(student_name in [student.name
                            for student
                            in course_roster.roster.students]), \
        f"{student_name} ({student_id}) not found in the active students list"


@test_case('C485037')
@tutor
def test_course_registration_and_initial_assignment_creation_timing(
        tutor_base_url, selenium, store):
    """Test student enrollment and initial assignment creation time."""
    # SETUP:
    test_data = store.get('C485037')
    enrollment_url = test_data.get('enrollment_url')
    if '-dev.' in tutor_base_url:
        enrollment_url = test_data.get('enrollment_url_dev')
        production_payments = False
    elif '-qa.' in tutor_base_url:
        enrollment_url = test_data.get('enrollment_url_qa')
        production_payments = False
    elif '-staging.' in tutor_base_url:
        enrollment_url = test_data.get('enrollment_url_staging')
        production_payments = True
    elif 'tutor.' in tutor_base_url:
        enrollment_url = test_data.get('enrollment_url_prod')
        production_payments = True
    else:
        enrollment_url = test_data.get('enrollment_url_unique')
        production_payments = True
    _, first_name, last_name, suffix = Utility.random_name()
    email = RestMail(
        f"{first_name}.{last_name}.{Utility.random_hex(3)}".lower())
    email.empty()
    password = Utility.random_hex(8)
    school = 'Automation'
    student_id = Utility.random(100000000, 999999999)
    home_address = Utility.random_address()
    max_time_to_wait = 10  # minutes
    expected_assignments = ['Reading Creation', 'Homework Creation',
                            'External Creation', 'Event Creation']

    # GIVEN: a user viewing the Tutor home page
    TutorHome(selenium, tutor_base_url).open()

    # WHEN:  they go to the student enrollment URL
    # AND:   click the 'Get started' button
    # AND:   sign up for an account
    # AND:   enter the student ID and click the 'Continue' button
    # AND:   click the 'I agree' button
    # IF:    using a production-based Payments instance (Prod/Staging/Unique)
    #  THEN: click the 'Try free for 14 days' button
    #  ELSE: fill out the purchase form address, city, state, zip code,
    #        credit  card  number, expiration date, CVV code, billing zip
    #        code, and click the 'Purchase' button
    # AND:   click the 'Access your course' button
    # AND:   click through any training wheel modals
    selenium.get(enrollment_url)
    enrollment = Enrollment(selenium, tutor_base_url)

    signup = enrollment.get_started()

    signup.account_signup(
        destination=tutor_base_url,
        email=email.address,
        name=['', first_name, last_name, suffix],
        password=password,
        school=school,
        tutor=True)

    identification = StudentID(selenium, tutor_base_url)
    identification.student_id = student_id
    privacy = identification._continue()

    buy_access = privacy.i_agree()

    if production_payments:
        free_trial = buy_access.try_free()
        course_page = free_trial.access_your_course()
    else:
        credit_card = Card().generic()
        expiration = datetime.now() + timedelta(
            weeks=Utility.random(0, 5 * 52))  # exp between today and 5 years
        purchase = buy_access.buy_access_now()
        purchase.address = home_address[Tutor.ADDRESS]
        purchase.city = home_address[Tutor.CITY]
        purchase.state = States.from_abbreviation(home_address[Tutor.STATE])
        purchase.mailing_zip = home_address[Tutor.ZIP]
        purchase.card_number = credit_card.get('number')
        purchase.expiration_date = expiration.strftime("%m/%y")
        purchase.cvv = credit_card.get('cvv')
        purchase.billing_zip_code = home_address[Tutor.ZIP]
        confirmation = purchase.purchase()
        course_page = confirmation.access_your_course()

    course_page.clear_training_wheels()

    # THEN:  the current week dashboard is displayed
    assert(course_page.is_displayed)

    # WHEN:  the loading spinner goes away
    assignments_made = course_page.wait_for_assignments(max_time_to_wait)

    # THEN:  assignments are populated in 'THIS WEEK' and/or 'ALL PAST WORK'
    assert(assignments_made), \
        f'Assignment creation still pending after {max_time_to_wait} minutes'
    assignments = course_page.assignment_names
    new_assignments = expected_assignments.copy()
    for assignment in assignments:
        if assignment in new_assignments:
            new_assignments.remove(assignment)
    if new_assignments:
        # there are still assignments; look in past assignments
        course_page.view_all_past_work()
        assignments = course_page.assignment_names
        for assignment in assignments:
            if assignment in new_assignments:
                new_assignments.remove(assignment)
    assert(not new_assignments), \
        f'Not all assignments found: {new_assignments}'


@test_case('C485038')
@tutor
def test_assignment_creation_readings(tutor_base_url, selenium, store):
    """Test publishing a reading.

    Start a new reading from the assignment menu, publish, edit and rename it.

    """
    # SETUP:
    test_data = store.get('C485038')
    user = test_data.get('username')
    if '-dev.' in tutor_base_url:
        password = test_data.get('password_dev')
    elif '-qa.' in tutor_base_url:
        password = test_data.get('password_qa')
    elif '-staging.' in tutor_base_url:
        password = test_data.get('password_staging')
    elif 'tutor.' in tutor_base_url:
        password = test_data.get('password_prod')
    else:
        password = test_data.get('password_unique')
    course_name = test_data.get('course_name')
    assignment_name = f'Auto Reading - {Utility.random_hex(5)}'
    assignment_edit_name = assignment_name + ' (Edited)'
    description = f'Assignment description for {assignment_name}'
    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    dates_and_times = {Tutor.ALL: (today, (tomorrow, '1200p')), }
    chapters = [1, None][Utility.random(0, 1)]
    sections = Utility.random(2, 6)

    # GIVEN: a Tutor teacher viewing their course calendar
    home = TutorHome(selenium, tutor_base_url).open()
    courses = home.log_in(user, password)
    calendar = courses.go_to_course(course_name)

    # WHEN:  they open the 'Add Assignment' taskbar
    # AND:   click on the 'Add Reading' link
    # AND:   fill out the assignment name and description, set the open date
    #        to today, set the open time to now, set the due date to tomorrow,
    #        set the due time to 12:00 pm, and click on the '+ Add Readings'
    #        button
    # AND:   select a chapter or 2+ individual sections and click the 'Add
    #        Readings' button
    if not calendar.sidebar.is_open:
        calendar.banner.add_assignment()

    assignment = calendar.sidebar.add_reading()

    assignment.name = assignment_name
    assignment.description = description
    assignment.set_assignment_dates(dates_and_times)

    # Using the internal function to exercise both chapter and section options
    # either select 1 random chapter, or, when ``chapters == None``, select
    # between 2 and 6, inclusive, random, sequential book sections
    group = assignment.add_readings_by(chapters=chapters, sections=sections)

    # THEN:  the selected readings should be displayed under the currently
    #        selected table
    sections_selected = [section.number
                         for section
                         in assignment.reading_list]
    assert(len(group) == (chapters or sections))
    if chapters:
        chapter = group[0].split('.')[0]
        for section in sections_selected:
            assert(section.startswith(str(chapter))), \
                f'Section {section} not in chapter {chapter}'
    else:
        assert(len(group) == len(sections_selected))
        for section in sections_selected:
            assert(section in group), \
                f'Section {section} not in the requested list ({group})'

    # WHEN:  they click the 'Publish' button
    calendar = assignment.publish()

    # THEN:  the course calendar is displayed
    # AND:   the new reading name is displayed on tomorrow's date box
    assert(calendar.is_displayed())
    assert('month' in calendar.location)

    assert(assignment_name in calendar.assignments(by_name=True)), \
        f'"{assignment_name}" not found'
    assert(assignment_name in calendar.assignments_on(tomorrow,
                                                      by_name=True)), (
        f'"{assignment_name}" not on the expected due date '
        f'({tomorrow.strftime("%m/%d/%Y")})')

    # WHEN:  they click the reading name and then click 'View Assignment'
    #        button
    # AND:   enter a new assignment name and click the 'Save' button
    quick_look = calendar.assignment(name=assignment_name).edit()
    assignment_edit = quick_look.view_assignment()

    assignment_edit.name = assignment_edit_name
    calendar = assignment_edit.save()

    # THEN:  the course calendar is displayed
    # AND:   the modified reading name is displayed on tomorrow's date box
    assert(calendar.is_displayed())
    assert('month' in calendar.location)

    assert(assignment_edit_name in calendar.assignments(by_name=True)), \
        f'"{assignment_edit_name}" not found'
    assert(assignment_edit_name in calendar.assignments_on(tomorrow,
                                                           by_name=True)), (
        f'"{assignment_edit_name}" not on the expected due date ' +
        f'({tomorrow.strftime("%m/%d/%Y")})')


@test_case('C485049')
@tutor
def test_assignment_creation_homework(tutor_base_url, selenium, store):
    """Test publishing each assignment type.

    Start a new homework from the calendar date, save it as a draft, then
    publish it.

    """
    # SETUP:
    test_data = store.get('C485049')
    user = test_data.get('username')
    if '-dev.' in tutor_base_url:
        password = test_data.get('password_dev')
    elif '-qa.' in tutor_base_url:
        password = test_data.get('password_qa')
    elif '-staging.' in tutor_base_url:
        password = test_data.get('password_staging')
    elif 'tutor.' in tutor_base_url:
        password = test_data.get('password_prod')
    else:
        password = test_data.get('password_unique')
    course_name = test_data.get('course_name')
    assignment_name = f'Auto Homework - {Utility.random_hex(5)}'
    description = f'Assignment description for {assignment_name}'
    feedback = [Tutor.DUE_AT, Tutor.IMMEDIATE][Utility.random(0, 1)]
    sections = Utility.random(2, 3)
    questions_per_section = Utility.random(1, 3)

    # GIVEN: a Tutor teacher viewing their course calendar
    home = TutorHome(selenium, tutor_base_url).open()
    courses = home.log_in(user, password)
    calendar = courses.go_to_course(course_name)

    # WHEN:  they click on an available date box on the calendar
    # AND:   click on the 'Add Homework' link
    days = [day
            for day
            in calendar.calendar.days
            if day.tense != Tutor.IN_PAST]
    day = days[Utility.random(0, len(days) - 1)]
    date = day.date

    homework = day.add_assignment(Tutor.HOMEWORK)

    # THEN:  the due date should match the selected date box
    due_on = homework.open_and_due.due_date.get_attribute('value')
    assert(due_on == date.strftime("%m/%d/%Y")), \
        f'The due date ({due_on}) does not match the expected date ({date})'

    # WHEN:  they fill out the assignment name and description, select a 'Show
    #        feedback' option, and click the '+ Select Problems' button
    # AND:   select 2-3 sections and click the 'Show Problems' button
    homework.name = assignment_name
    homework.description = description
    homework.feedback = feedback

    problem_selector = homework.add_assessments_by(sections=sections)

    # THEN:  the selected section buttons are displayed in the secondary
    #        toolbar
    selected_sections = problem_selector.toolbar.sections
    assert(len(selected_sections) == sections), (
        'Section selections ({0}) do not match expectation ({1})'
        .format([section.number for section in selected_sections],
                sections))

    # WHEN:  they select 1-3 assessments from each available section
    options_selected = 0
    for section in problem_selector.sections:
        for exercise in Utility.sample(section.assessments,
                                       questions_per_section):
            exercise.add_question()
            options_selected += 1

    # THEN:  the 'My Selections' shows the total number of assessments selected
    assert(problem_selector.toolbar.my_selections == options_selected), \
        f'My Selections does not match the actual assessment selections'

    # WHEN:  they click on the 'Next' button
    # AND:   click on the 'Save as Draft' button
    homework = problem_selector.toolbar.next()

    calendar = homework.save_as_draft()

    # THEN:  the course calendar is displayed
    # AND:   the new homework name is displayed on the selected date box and
    #        is prefixed with 'draft'
    assert(calendar.is_displayed())
    assert('month' in calendar.location)

    assert(assignment_name in calendar.assignments(by_name=True)), \
        f'"{assignment_name}" not found'
    assert(assignment_name in calendar.assignments_on(date, by_name=True)), (
        '"{name}" not on the expected due date ({date})'
        .format(name=assignment_name, date=date.strftime("%m/%d/%Y")))

    # WHEN:  they click on the homework name
    # AND:   click the 'Publish' button
    assignment_edit = calendar.assignment(name=assignment_name).edit()

    calendar = assignment_edit.publish()

    # THEN:  the course calendar is displayed
    # AND:   the homework name is displayed on the selected date box and is
    #        not prefixed with 'draft'
    assert(calendar.is_displayed())
    assert('month' in calendar.location)

    assert(assignment_name in calendar.assignments(by_name=True)), \
        f'"{assignment_name}" not found'
    assert(assignment_name in calendar.assignments_on(date, by_name=True)), (
        '"{name}" not on the expected due date ({date})'
        .format(name=assignment_name, date=date.strftime("%m/%d/%Y")))
    assert(not calendar.assignment(assignment_name).is_draft), \
        f'"{assignment_name}" is still a draft assignment'


@test_case('C485050')
@tutor
def test_assignment_creation_external(tutor_base_url, selenium, store):
    """Test publishing each assignment type.

    Start a new external assignment by drag-and-drop onto the calendar date,
    publish it, then delete it.

    """
    # SETUP:
    test_data = store.get('C485050')
    user = test_data.get('username')
    if '-dev.' in tutor_base_url:
        password = test_data.get('password_dev')
    elif '-qa.' in tutor_base_url:
        password = test_data.get('password_qa')
    elif '-staging.' in tutor_base_url:
        password = test_data.get('password_staging')
    elif 'tutor.' in tutor_base_url:
        password = test_data.get('password_prod')
    else:
        password = test_data.get('password_unique')
    course_name = test_data.get('course_name')
    assignment_name = f'Auto External - {Utility.random_hex(5)}'
    description = f'Assignment description for {assignment_name}'
    assignment_url = tutor_base_url

    # GIVEN: a Tutor teacher viewing their course calendar
    home = TutorHome(selenium, tutor_base_url).open()
    courses = home.log_in(user, password)
    calendar = courses.go_to_course(course_name)

    # WHEN:  they open the 'Add Assignment' taskbar
    if not calendar.sidebar.is_open:
        calendar.banner.add_assignment()

    ''' Bypass the drag-and-drop method as it cannot be accurately reproduced
        in Tutor; click on the bar instead leaving the drag-and-drop to manual
        testing.
    # AND:   click and drap the 'Add External Assignment' bar onto an
    #        available date box on the calendar '''

    days = [day
            for day
            in calendar.calendar.days
            if day.tense == Tutor.IN_FUTURE]
    day = days[Utility.random(0, len(days) - 1)]
    date = day.date

    external = day.add_assignment(Tutor.EXTERNAL)

    # THEN:  the due date should match the selected date box
    due_on = external.open_and_due.due_date.get_attribute('value')
    assert(due_on == date.strftime("%m/%d/%Y")), \
        f'The due date ({due_on}) does not match the expected date ({date})'

    # WHEN:  they fill out the assignment name, description, and assignment
    #        URL, and click the 'Publish' button
    external.name = assignment_name
    external.description = description
    external.assignment_url = assignment_url
    calendar = external.publish()

    # THEN:  the course calendar is displayed
    # AND:   the new external assignment name is displayed on the selected
    #        date box
    assert(calendar.is_displayed())
    assert('month' in calendar.location)

    assert(assignment_name in calendar.assignments(by_name=True)), \
        f'"{assignment_name}" not found'
    assert(assignment_name in calendar.assignments_on(date, by_name=True)), (
        '"{name}" not on the expected due date ({date})'
        .format(name=assignment_name, date=date.strftime("%m/%d/%Y")))

    # WHEN:  they click on the assignment name
    # AND:   click the 'Edit Assignment' button
    quick_look = calendar.assignment(name=assignment_name).edit()
    external = quick_look.view_assignment()

    # THEN:  the 'Edit External Assignment' window is displayed
    assert('external' in external.location)

    # WHEN:  they click the 'Delete' button and click the 'Delete' button in
    #        the pop up
    calendar = external.delete(confirm=True)

    # THEN:  the course calendar is displayed
    # AND:   the external assignment name is no longer displayed on the
    #        selected date box
    assert(calendar.is_displayed())
    assert('month' in calendar.location)

    assert(assignment_name not in calendar.assignments(by_name=True)), \
        f'"{assignment_name}" still on the calendar'


'''@test_case('C485051')
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

    import time
    time.sleep(5)
    assert(False), '*** Reached Test End ***'''


'''@test_case('C485039')
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

    import time
    time.sleep(5)
    assert(False), '*** Reached Test End ***'''


'''@test_case('C485040')
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

    import time
    time.sleep(5)
    assert(False), '*** Reached Test End ***'''


'''@test_case('C485041')
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

    import time
    time.sleep(5)
    assert(False), '*** Reached Test End ***'''


'''@test_case('C485042')
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

    import time
    time.sleep(5)
    assert(False), '*** Reached Test End ***'''


'''@test_case('C485043')
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

    import time
    time.sleep(5)
    assert(False), '*** Reached Test End ***'''


'''@test_case('C485044')
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

    import time
    time.sleep(5)
    assert(False), '*** Reached Test End ***'''


'''@test_case('C485045')
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

    import time
    time.sleep(5)
    assert(False), '*** Reached Test End ***'''
