"""The OpenStax Tutor Beta automation smoke tests.

These cover a wide range of features to satisfy end-to-end
testing for high priority areas.
"""

from datetime import datetime, timedelta
from typing import Union

from autochomsky import chomsky

from pages.tutor.enrollment import Enrollment, Terms
from pages.tutor.home import TutorHome
from pages.tutor.task import Homework
from tests.markers import nondestructive, test_case, tutor
from utils import bookterm
from utils.email import RestMail
from utils.tutor import States, Tutor
from utils.utilities import Actions, Card, Utility


@test_case('C485035')
@tutor
def test_create_and_clone_a_course(tutor_base_url, selenium, teacher):
    """Test creating and cloning courses."""
    # SETUP:
    book = Tutor.BOOKS[Utility.random(0, len(Tutor.BOOKS) - 1)]
    # term = Tutor.TERMS[Utility.random(0, len(Tutor.TERMS) - 1)]
    term = Tutor.TERMS[Utility.random(0, 1)]
    today = datetime.now()
    course_name = (f"{book} Auto-{today.year}{today.month:02}{today.day:02}"
                   f" ({Utility.random_hex(6)})")
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
        f"{first_name}.{last_name}.{Utility.random_hex(4)}".lower())
    email.empty()
    password = Utility.random_hex(8)
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

    sign_up = enrollment.get_started()

    privacy = sign_up.sign_up(
        first=first_name,
        last=last_name,
        email=email,
        password=password,
        page=Terms,
        base_url=tutor_base_url)

    identification = privacy.i_agree()
    identification.student_id = student_id
    buy_access = identification._continue()

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
    chapters = 1

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
    # Patch: select one chapter because of the switch to baked books added
    #        a slew of unnumbered sections at the end of each chapter making
    #        section selection more difficult
    group = assignment.add_readings_by(chapters=chapters)

    # THEN:  the selected readings should be displayed under the currently
    #        selected table
    sections_selected = [section.number
                         for section
                         in assignment.reading_list
                         if section.number]
    assert(len(group) == chapters)
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
    open_and_due = homework.open_and_due
    if not isinstance(open_and_due, list):
        due_on = homework.open_and_due.due_date.get_attribute('value')
    else:
        due_on = (homework.open_and_due[0]
                  .open_to_close.due_date.get_attribute('value'))
    assert(due_on == date.strftime("%m/%d/%Y")), \
        f'The due date ({due_on}) does not match the expected date ({date})'

    # WHEN:  they fill out the assignment name and description, select a 'Show
    #        feedback' option, and click the '+ Select Problems' button
    # AND:   select 1 chapter and click the 'Show Problems' button
    # AND:   select 1-3 assessments from each available section
    homework.name = assignment_name
    homework.description = description
    homework.feedback = feedback

    problem_selector = homework.add_assessments_by(chapters=1)

    options_selected = 0
    for section in problem_selector.sections:
        for exercise in Utility.sample(section.assessments,
                                       questions_per_section):
            exercise.add_question()
            options_selected += 1

    # THEN:  the 'My Selections' shows the total number of assessments
    #        selected, which will equal or exceed the options selected due to
    #        multi-part questions
    assert(problem_selector.toolbar.my_selections >= options_selected), \
        f'My Selections must be equal or greater than the selections'

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


@test_case('C485051')
@tutor
def test_assignment_creation_event(tutor_base_url, selenium, store):
    """Test publishing each assignment type.

    Start a new event from the assignment menu, switch it to individual section
    assignment, then publish it.

    """
    # SETUP:
    test_data = store.get('C485051')
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
    assignment_name = f'Auto Event - {Utility.random_hex(5)}'
    description = f'Assignment description for {assignment_name}'
    today = datetime.now()
    two_days_from_today = today + timedelta(days=2)
    dates_and_times = {
        '1st': (today + timedelta(days=1), today + timedelta(days=2)),
        '2nd': (today + timedelta(days=2), today + timedelta(days=3)),
        '3rd': (today + timedelta(days=3), today + timedelta(days=4)), }

    # GIVEN: a Tutor teacher viewing their course calendar
    home = TutorHome(selenium, tutor_base_url).open()
    courses = home.log_in(user, password)
    calendar = courses.go_to_course(course_name)

    # WHEN:  they open the 'Add Assignment' taskbar
    # AND:   click the 'Add Event' link
    # AND:   fill out the event name and description, click the radio button
    #        to the right of 'Individual Sections', set the open dates to
    #        today +1, +2, ..., and the due dates to today +2, +3, ..., and
    #        click the 'Publish' button
    if not calendar.sidebar.is_open:
        calendar.banner.add_assignment()

    assignment = calendar.sidebar.add_event()

    assignment.name = assignment_name
    assignment.description = description
    assignment.set_assignment_dates(dates_and_times)
    calendar = assignment.publish()

    # THEN:  the course calendar is displayed
    # AND:   the event name is displayed on the first due date box
    assert(calendar.is_displayed())
    assert('month' in calendar.location)

    assert(assignment_name in calendar.assignments(by_name=True)), \
        f'"{assignment_name}" not found'
    assert(assignment_name in calendar.assignments_on(two_days_from_today,
                                                      by_name=True)), (
        f'"{assignment_name}" not on the first expected due date '
        f'({two_days_from_today.strftime("%m/%d/%Y")})')


@test_case('C485039')
@tutor
def test_student_task_reading_assignment(tutor_base_url, selenium, store):
    """Test a student working a reading assignment.

    While working the assignment free response answer validation,
    highlighting, and annotation will also be checked.

    """
    # SETUP:
    test_data = store.get('C485039')
    if '-dev.' in tutor_base_url:
        enrollment_url = test_data.get('enrollment_url_dev')
    elif '-qa.' in tutor_base_url:
        enrollment_url = test_data.get('enrollment_url_qa')
    elif '-staging.' in tutor_base_url:
        enrollment_url = test_data.get('enrollment_url_staging')
    elif 'tutor.' in tutor_base_url:
        enrollment_url = test_data.get('enrollment_url_prod')
    else:
        enrollment_url = test_data.get('enrollment_url_unique')
    _, first_name, last_name, suffix = Utility.random_name()
    email = RestMail(
        f"{first_name}.{last_name}.{Utility.random_hex(3)}".lower())
    email.empty()
    password = Utility.random_hex(8)
    student_id = Utility.random(100000000, 999999999)
    assignment_name = test_data.get('assignment_name')
    highlight_length = Utility.random(-20, 20) * 5 + 5
    highlight_length = highlight_length if abs(highlight_length) > 30 else 30
    annotation_length = (
        Utility.random(-15, 15) * 10 + 5,
        Utility.random(-2, 2) * 33 + 20)
    annotation_text = chomsky()
    random_string = 'abcdefghijklmnopqrstuvwxyz      '
    options = len(random_string)
    free_response_giberish = ''
    for _ in range(30):
        free_response_giberish += random_string[Utility.random(0, options - 1)]
    book = bookterm.CollegePhysics()

    # GIVEN: a Tutor student enrolled in a course with a reading assignment
    selenium.get(enrollment_url)
    enrollment = Enrollment(selenium, tutor_base_url)
    sign_up = enrollment.get_started()
    privacy = sign_up.sign_up(
        first=first_name,
        last=last_name,
        email=email,
        password=password,
        page=Terms,
        base_url=tutor_base_url)
    identification = privacy.i_agree()
    identification.student_id = student_id
    course_page = identification._continue()
    course_page.clear_training_wheels()
    course_page.wait_for_assignments()
    course_page.clear_training_wheels()
    if assignment_name not in course_page.assignment_names:
        course_page.view_all_past_work()
        course_page.clear_training_wheels()

    # WHEN:  they click on the assignment name
    reading = course_page.select_assignment(assignment_name)
    reading.clear_training_wheels()

    # THEN:  the first task step is displayed
    assert(reading.is_displayed())
    assert('step/1' in reading.location), (
        f"Not at the reading's ({assignment_name}) " +
        f"first step: {reading.location}")

    # WHEN:  they select a section of text
    # AND:   click the highlighter icon
    if not Utility.is_browser(selenium, 'safari'):
        Utility.scroll_to(selenium,
                          element=reading.body.paragraphs[0],
                          shift=-150)
        (Actions(selenium)
            .move_to_element(reading.body.paragraphs[0])
            .move_by_offset(-30, -30)
            .click_and_hold()
            .move_by_offset(highlight_length, 0)
            .release()
            .perform())
    else:
        Utility.scroll_to(selenium, element=reading.body.paragraphs[0])
        (Actions(selenium)
            .move_by_offset(200, 30)
            .click_and_hold()
            .move_by_offset(0, 30)
            .release()
            .perform())

    reading.highlight()

    # THEN:  a text highlight in included
    assert(len(reading.content_highlights) == 1), \
        'No highlights found on the page'

    # WHEN:  they select a different section of text
    # AND:   click the speech bubble icon
    # AND:   enter text in the annotation box and click the check mark button
    if not Utility.is_browser(selenium, 'safari'):
        Utility.scroll_to(selenium,
                          element=reading.body.paragraphs[1],
                          shift=-150)
        (Actions(selenium)
            .move_to_element(reading.body.paragraphs[1])
            .move_by_offset(-30, -30)
            .click_and_hold()
            .move_by_offset(*annotation_length)
            .release()
            .perform())
    else:
        (Actions(selenium)
            .move_by_offset(0, 100)
            .click_and_hold()
            .move_by_offset(45, 10)
            .release()
            .perform())

    annotation = reading.annotate()

    annotation.text = annotation_text
    reading = annotation.save()

    # THEN:  a text highlight is included
    # AND:   a speech bubble icon is displayed to the right of the highlight
    assert(len(reading.content_highlights) == 2), (
        f'{len(reading.content_highlights)} highlight(s) found on the page')

    assert(reading.sidebar_buttons), \
        f'No annotation text bubbles found in the sidebar'

    # WHEN:  they click the highlight summary icon
    Utility.scroll_top(selenium)
    note_summary = reading.highlights()

    # THEN:  the highlight and the annotation are displayed
    assert(note_summary.is_displayed())
    assert(len(note_summary.notes) == 2)

    # WHEN:  they click the highlight summary icon
    # AND:   advance through the assignment until a two-step question is
    #        reached
    # AND:   enter random text in the text area and click the 'Answer' button
    Utility.scroll_top(selenium)
    reading = reading.highlights()

    while not reading.body.is_free_response:
        if reading.body.next_page_available:
            reading = reading.body.next_page()
        elif reading.body.is_multiple_choice:
            reading.body.pane.random_answer()
            reading.body.pane.answer()
            reading.body.pane._continue()
        else:
            reading = reading.body.next_page()

    reading.body.pane.free_response = free_response_giberish
    reading.body.pane.answer()

    # THEN:  the answer verification flags the answer
    assert(reading.body.pane.nudge), (
        'Response verification message not displayed for '
        f'"{free_response_giberish}"')

    # WHEN:  they enter new text is in the text area and click the 'Re-answer'
    #        button
    reading.body.pane.free_response = (
        book.get_term(reading.body.pane.chapter_section)[1])
    reading.body.pane.reanswer()

    # THEN:  the multiple choice answers are displayed
    assert(reading.body.is_multiple_choice), \
        'Multiple choice answer options not found'

    # WHEN:  they proceed through the rest of the assignment reaching the 'You
    #        are done.' step
    # AND:   click the milestones icon
    reading.body.pane.random_answer()
    reading.body.pane.answer()
    reading.body.pane._continue()
    while not reading.body.assignment_complete:
        if reading.body.next_page_available:
            reading = reading.body.next_page()
        elif reading.body.is_multiple_choice:
            reading.body.pane.random_answer()
            reading.body.pane.answer()
        elif reading.body.is_free_response:
            reading.body.pane.free_response = (
                book.get_term(reading.body.pane.chapter_section)[1])
            reading.body.pane.answer()
        else:
            reading = reading.body.next_page()

    milestones = reading.milestones()

    # THEN:  the milestones are displayed
    # AND:   there is a card for each step
    assert(milestones.is_displayed()), \
        'Milestone overlay not displayed'

    assert(milestones.milestones), \
        'No milestone cards found'

    # WHEN:  they click the milestones icon
    reading = milestones.close()

    # THEN:  the milestones overlay is closed
    assert(not milestones.is_displayed()), \
        'Milestone overlay is still displayed'

    # WHEN:  they click the 'Back to Dashboard' button
    this_week = reading.body.back_to_dashboard()
    this_week.reload()  # force a fresh to get any new dashboard data
    if assignment_name not in this_week.assignment_names:
        this_week.view_all_past_work()

    # THEN:  the 'THIS WEEK' dashboard is displayed
    # AND:   the reading assignment progress is 'Complete'
    assert(this_week.is_displayed()), \
        'Not viewing the student work dashboard'

    finished_assignment = this_week.assignment_bar(assignment_name)
    assert(finished_assignment.progress == 'Complete'), (
        f'Progress incorrect for {assignment_name}: '
        f'"{finished_assignment.progress}"')


@test_case('C485040')
@tutor
def test_student_task_homework_assignment(tutor_base_url, selenium, store):
    """Test a student working a homework assignment.

    This will include standard two-step, standard multiple choice and
    multi-part assessments.

    """
    # SETUP:
    test_data = store.get('C485040')
    if '-dev.' in tutor_base_url:
        enrollment_url = test_data.get('enrollment_url_dev')
        assignment_url = test_data.get('assignment_url_dev')
    elif '-qa.' in tutor_base_url:
        enrollment_url = test_data.get('enrollment_url_qa')
        assignment_url = test_data.get('assignment_url_qa')
    elif '-staging.' in tutor_base_url:
        enrollment_url = test_data.get('enrollment_url_staging')
        assignment_url = test_data.get('assignment_url_staging')
    elif 'tutor.' in tutor_base_url:
        enrollment_url = test_data.get('enrollment_url_prod')
        assignment_url = test_data.get('assignment_url_prod')
    else:
        enrollment_url = test_data.get('enrollment_url_unique')
        assignment_url = test_data.get('assignment_url_unique')
    _, first_name, last_name, suffix = Utility.random_name()
    email = RestMail(
        f"{first_name}.{last_name}.{Utility.random_hex(5)}".lower())
    email.empty()
    password = Utility.random_hex(8)
    student_id = Utility.random(100000000, 999999999)
    assignment_name = test_data.get('assignment_name')
    book = bookterm.CollegePhysics()

    # GIVEN: a Tutor student enrolled in a course with a homework assignment
    selenium.get(enrollment_url)
    enrollment = Enrollment(selenium, tutor_base_url)
    sign_up = enrollment.get_started()
    privacy = sign_up.sign_up(
        first=first_name,
        last=last_name,
        email=email,
        password=password,
        page=Terms,
        base_url=tutor_base_url)
    identification = privacy.i_agree()
    identification.student_id = student_id
    course_page = identification._continue()
    course_page.clear_training_wheels()
    course_page.wait_for_assignments()
    course_page.clear_training_wheels()

    # WHEN:  they follow the assignment URL
    # AND:   work the free response assessment
    # AND:   work the multiple choice-only assessment
    # AND:   work the multi-part assessment
    # AND:   work each remaining step
    # AND:   click the 'Back to Dashboard' button
    selenium.get(assignment_url)
    homework = Homework(selenium, tutor_base_url)
    homework.clear_training_wheels()

    # answer the standard, two-step assessment
    if homework.body.is_two_step_intro:
        # move beyond the intersticial card, if it appears for the student
        homework.body._continue()
    free_response = homework.body.pane
    free_response.free_response = (
        book.get_term(free_response.chapter_section)[1])
    free_response.answer()
    multiple_choice = homework.body.pane
    multiple_choice.random_answer()
    multiple_choice.answer()
    multiple_choice._continue()

    # answer the multiple choice assessment
    multiple_choice_only = homework.body.pane
    multiple_choice_only.random_answer()
    multiple_choice_only.answer()
    multiple_choice_only._continue()

    # answer each question of the multipart assessment
    multipart = homework.body.pane
    questions = len(multipart.questions)
    for index, question in enumerate(multipart.questions):
        not_last_question = index + 1 < questions
        if question.is_multiple_choice:
            question.random_answer()
            question.answer()
            question._continue(not_last_question)
        elif question.has_correct_answer:
            question._continue(not_last_question)
        elif question.is_free_response:
            question.free_response = (
                book.get_term(question.body.pane.chapter_section)[1])
            question.answer()
            question.random_answer()
            question.answer()
            question._continue(not_last_question)

    # continue through the rest of the assignment
    while not homework.body.assignment_complete:
        if homework.body.is_interstitial or homework.body.has_correct_answer:
            homework.body._continue()
        elif homework.body.is_multiple_choice:
            homework.body.pane.random_answer()
            homework.body.pane.answer()
            homework.body.pane._continue()
        elif homework.body.is_free_response:
            homework.body.pane.free_response = (
                book.get_term(homework.body.pane.chapter_section)[1])
            homework.body.pane.answer()
            homework.body.pane.random_answer()
            homework.body.pane.answer()
            homework.body.pane._continue()

    this_week = homework.body.back_to_dashboard()
    this_week.reload()  # force a fresh to get any new dashboard data
    if assignment_name not in this_week.assignment_names:
        this_week.view_all_past_work()
        # clear the late icon pop up
        this_week.clear_training_wheels()

    # THEN:  the student dashboard is displayed
    # AND:   the homework assignment progress is 'N/N answered' or 'X/Y
    #        correct'
    assert(this_week.is_displayed()), \
        'Not viewing the student work dashboard'

    progress = this_week.assignment_bar(assignment_name).progress
    assert(' correct' in progress or ' answered' in progress), (
        f'Progress incorrect for {assignment_name}: '
        f'"{progress}"')


@test_case('C485041')
@tutor
def test_student_task_practice(tutor_base_url, selenium, store):
    """Test a student working a practice question set.

    Practice a section and practice the student's weakest topics.

    """
    # SETUP:
    test_data = store.get('C485041')
    user = test_data.get('users')
    user = user[Utility.random(0, len(user) - 1)]
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
    book = bookterm.Biology2e()

    # GIVEN: a Tutor student enrolled in a course with at least one reading or
    #        homework
    home = TutorHome(selenium, tutor_base_url).open()
    courses = home.log_in(user, password)
    this_week = courses.go_to_course(course_name)
    this_week.clear_training_wheels()

    # WHEN:  they click the 'Practice more to get forecast' button or a
    #        forecast bar
    recent_topics = this_week.performance_sidebar.sections
    topic = Utility.random(0, len(recent_topics) - 1)
    section = recent_topics[topic]
    section_number = section.number
    section_title = section.title
    already_worked = int(section.worked.split()[0])
    practice = section.practice()

    # THEN:  a practice session with between 1 - 5 questions from the selected
    #        section is displayed
    url = practice.location
    assert('task' in url or 'practice' in url), \
        f'Practice session not started: {url}'
    title = practice.footer.title
    assert(title == 'Practice'), f'Wrong title found: {title}'
    assessments = practice.exercises
    assert(assessments >= 1 and assessments <= 5), \
        f'Wrong number of assessment breadcrumbs: {assessments}'
    assert(section_number in practice.section)
    assert(section_title in practice.section_title)

    # WHEN:  they answer all questions
    while not practice.body.assignment_complete:
        if practice.body.is_interstitial or practice.body.has_correct_answer:
            practice.body._continue()
        elif practice.body.is_multiple_choice:
            practice.body.pane.random_answer()
            practice.body.pane.answer()
            practice.body.pane._continue()
        elif practice.body.is_free_response:
            practice.body.pane.free_response = (
                book.get_term(practice.body.pane.chapter_section)[1])
            practice.body.pane.answer()
            practice.body.pane.random_answer()
            practice.body.pane.answer()
            practice.body.pane._continue()

    # THEN:  the 'You are done.' card is displayed
    assert('You are done.' in selenium.page_source)

    # WHEN:  they click the 'Back to Dashboard' button
    this_week = practice.body.back_to_dashboard()
    this_week.reload()
    this_week.clear_training_wheels()

    # THEN:  the student dashboard is displayed
    # AND:   the section shows the new total of question worked for the
    #        selected section
    assert(this_week.is_displayed()), \
        'Not viewing the student work dashboard'

    worked = [section.worked.split()[0]
              for section
              in this_week.performance_sidebar.sections
              if section.title == section_title][0]
    assert(worked == str(already_worked + assessments)), \
        f'Incorrect number of worked assessments for section {section_number}'

    # WHEN:  they click the 'Practice my weakest topics' button
    practice = this_week.performance_sidebar.practice_my_weakest_topics()

    # THEN:  a practice session with between 1 - 5 questions is displayed
    url = practice.location
    assert('task' in url or 'practice' in url), \
        f'Practice session not started: {url}'
    title = practice.footer.title
    assert(title == 'Practice'), f'Wrong title found: {title}'
    assessments = practice.exercises
    assert(assessments >= 1 and assessments <= 5), \
        f'Wrong number of assessment breadcrumbs: {assessments}'


def valid_score(score: Union[str, int]) -> bool:
    """Return True if the score value is valid.

    .. note:

       for use in scores page tests

    :param score: the score to evaluate
    :type score: str or int
    :return: ``True`` if the score value is an expected string or a number
        between 0 and 100
    :rtype: bool

    """
    return (score == '---' or
            score == 'n/a' or
            (isinstance(score, int) and score >= 0 and score <= 100))


@test_case('C485042')
@tutor
def test_teacher_viewing_student_scores(tutor_base_url, selenium, store):
    """Test an instructor viewing the course scores page.

    Review the scores for a student;
    accept a student's late work;
    review an assignment;
    review student work.

    """
    # SETUP:
    test_data = store.get('C485042')
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
    invalid_weights = Utility.summed_list(length=3, total=100) + [50]
    valid_weights = Utility.summed_list(length=4, total=100)

    # GIVEN: a Tutor instructor with a course containing readings, homeworks,
    #        and/or external assignments with at least one student
    home = TutorHome(selenium, tutor_base_url).open()
    courses = home.log_in(user, password)
    calendar = courses.go_to_course(course_name)

    # WHEN:  they click on the 'Student Scores' button
    scores = calendar.banner.student_scores()

    # THEN:  the scores page is displayed
    # AND:   the course average, homework score average, homework progress
    #        average, reading score average, reading progress average, and
    #        each assignment are displayed
    assert(scores.is_displayed()), 'Scores page not displayed'
    assert('scores' in scores.location), 'Not viewing the scores page'

    course_average = scores.table.heading.course_average
    homework_score = scores.table.heading.homework_average_score
    homework_progress = scores.table.heading.homework_average_progress
    reading_score = scores.table.heading.reading_average_score
    reading_progress = scores.table.heading.reading_average_progress
    assert(valid_score(course_average)), \
        f'Invalid course average: {course_average}'
    assert(valid_score(homework_score)), \
        f'Invalid homework score average: {homework_score}'
    assert(valid_score(homework_progress)), \
        f'Invalid homework progress average: {homework_progress}'
    assert(valid_score(reading_score)), \
        f'Invalid reading score average: {reading_score}'
    assert(valid_score(reading_progress)), \
        f'Invalid reading progress average: {reading_progress}'
    assert(scores.table.heading.assignments), 'No assignment headers found'

    # WHEN:  they click the 'Set weights' link
    previous_course_average = course_average
    weights = scores.table.heading.set_weights()

    # THEN:  the score weights are displayed
    assert(weights.is_displayed()), 'Set weights modal not displayed'

    # WHEN:  they change the weights to not total 100%
    weights.set(invalid_weights)

    # THEN:  an information alert is displayed
    assert(not weights.weights_are_valid), \
        f'Weights ({invalid_weights}) not marked as invalid'

    # WHEN:  they click the 'Restore default' link
    weights.restore_default()

    # THEN:  the weights are 100%, 0%, 0%, and 0%, respectively
    assert(weights.homework_score == 100)
    assert(weights.homework_progress == 0)
    assert(weights.reading_score == 0)
    assert(weights.reading_progress == 0)

    # WHEN:  they change the weights to equal 100% and click the 'Save' button
    weights.set(valid_weights)
    weights.save()

    # THEN:  the wights modal is closed and the course average is updated
    assert(not scores.modal_open), 'Weights modal still open'
    assert(previous_course_average != scores.table.heading.course_average), \
        'Course average not updated'

    # WHEN:  they click an assignment 'Review' link
    # expand the window width to render all assignments instead of only the
    # ones that fit; at [width == 1024] (test default), only the most recent
    # assignment is in the HTML
    scores.table.heading.set_weights().restore_default().save()
    scores.resize_window(width=2300, height=1024)
    assignments = scores.table.heading.assignments
    assignment_type = ''
    while (assignment_type != Tutor.HOMEWORK and
           assignment_type != Tutor.READING):
        random = Utility.random(0, len(assignments) - 1)
        random_assignment = assignments[random]
        assignment_type = random_assignment.assignment_type
    assignment_name = random_assignment.name
    review = random_assignment.review_assignment()
    review.resize_window(width=1024, height=768)

    # THEN:  the assignment review is displayed
    assert(review.is_displayed()), 'Review page not displayed'
    assert('metrics' in review.location), 'Not at the assignment review page'

    # WHEN:  they go back to the scores page
    # AND:   click a student name
    scores = review.toolbar.back_to_scores()

    students = scores.table.students
    random_student = students[Utility.random(0, len(students) - 1)]
    student_name = random_student.name
    performance = random_student.performance_forecast()

    # THEN:  the student's performance forecast is displayed
    assert(performance.is_displayed()), 'Performance forecast not displayed'
    assert(student_name in selenium.page_source), \
        f"Not viewing {student_name}\'s performance forecast"

    # WHEN:  they click the 'Back to Scores' button
    # AND:   click a late work arrow
    # AND:   click the 'Accept late score' button
    scores = performance.back_to_scores()

    students = scores.table.students
    random_student = students[Utility.random(0, len(students) - 1)]
    scores.resize_window(width=2300, height=1024)
    assignments = [assignment
                   for assignment
                   in random_student.assignments
                   if assignment.has_late_work]
    random = Utility.random(0, len(assignments) - 1)
    random_assignment = assignments[random]
    assignment_score = random_assignment.score
    late_work = random_assignment.view_late_work_tooltip()

    late_work.accept_late_score()

    # THEN:  the assignment on time score is replaced by the late work score
    # note - there is one assignment for one student where the original and
    #        the late work are equal (38%)
    assert(assignment_score != random_assignment.score or (
           assignment_score == 38 and random_assignment.score == 38)), \
        "Score not updated"

    # WHEN:  they click the late work arrow
    # AND:   click the 'Use this score' button
    late_work = random_assignment.view_late_work_tooltip()

    late_work.use_this_score()

    # THEN:  the assignment late work score is replaced by the on time score
    assert(assignment_score == random_assignment.score), \
        f"{assignment_name}'s score did not revert"

    # WHEN:  they click the scores spreadsheet download icon
    review.resize_window(width=1024, height=768)
    scores.export()

    # THEN:  the spreadsheet is downloaded
    assert(scores.toast_seen), 'Export toast message not seen'


@test_case('C485043')
@nondestructive
@tutor
def test_student_viewing_student_scores(tutor_base_url, selenium, store):
    """Test a student viewing their scores page."""
    # SETUP:
    test_data = store.get('C485043')
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

    # GIVEN: a Tutor student with a reading, homework and external assignment
    home = TutorHome(selenium, tutor_base_url).open()
    courses = home.log_in(user, password)
    # select the course if the student ends up on the course picker
    if 'dashboard' in courses.location:
        course = courses.go_to_course(course_name)
    else:
        course = courses

    # WHEN:  they click on the 'Scores' link in the 'Menu'
    scores = course.nav.menu.view_student_scores()

    # THEN:  the scores page is displayed
    # AND:   a course average, homework score, homework progress, reading
    #        score, reading progress, and each assignment are displayed
    assert(scores.is_displayed())
    assert('scores' in scores.location)

    # WHEN:  they click the 'View weights' link
    weights = scores.table.heading.view_weights()
    homework_score = weights.homework_score
    homework_progress = weights.homework_progress
    reading_score = weights.reading_score
    reading_progress = weights.reading_progress
    combined = (homework_score + homework_progress +
                reading_score + reading_progress)

    # THEN:  the score weights are displayed
    assert(weights.is_displayed())
    assert(valid_score(homework_score)), \
        f'Invalid homework score value: {homework_score}'
    assert(valid_score(homework_progress)), \
        f'Invalid homework progress value: {homework_progress}'
    assert(valid_score(reading_score)), \
        f'Invalid reading score value: {reading_score}'
    assert(valid_score(reading_progress)), \
        f'Invalid reading progress value: {reading_progress}'
    assert(combined == 100), \
        f'Weights do not equal 100 ({combined})'

    # WHEN:  they click the 'Close' button
    weights.close()

    # THEN:  the weights modal is closed
    assert(not weights.is_displayed()), 'Weights are still visible'


@test_case('C485044')
@nondestructive
@tutor
def test_teacher_viewing_the_course_performance_forecast(
        tutor_base_url, selenium, store):
    """Test an instructor viewing the course performance forecast."""
    # SETUP:
    test_data = store.get('C485044')
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
    sections = test_data.get('sections')

    # GIVEN: a Tutor instructor with a course containing readings, homeworks,
    #        and/or external assignments with at least one student
    home = TutorHome(selenium, tutor_base_url).open()
    courses = home.log_in(user, password)
    calendar = courses.go_to_course(course_name)

    # WHEN:  they click on the 'Performance Forecast' button
    performance = calendar.banner.performance_forecast()

    # THEN:  the performance forecast is displayed
    # AND:   each course section tab is available
    # AND:   weaker areas and each chapter are displayed
    # AND:   each chapter and section displayed show a progress bar or 'Not
    #        enough exercises completed' message
    assert(performance.is_displayed())
    assert('guide' in performance.location)

    assert(len(performance.section_tabs) == sections), \
        'Expected {course_sections} sections, found {sections}'.format(
            course_sections=sections,
            sections=[section.name for section in performance.section_tabs])

    assert(not performance.no_data), 'No course performance found'
    assert(performance.forecast.weakest.lack_data or
           performance.forecast.weakest.sections), \
        'Weaker Areas pane not found'

    for chapter in performance.forecast.chapters:
        assert(chapter.chapter.number)
        assert(chapter.chapter.title)
        assert(chapter.chapter.progress)
        assert(chapter.chapter.count)
        for section in chapter.sections:
            assert(section.number)
            assert(section.title)
            assert(section.progress)
            assert(section.count)


@test_case('C485045')
@tutor
def test_student_viewing_their_performance_forecast(
        tutor_base_url, selenium, store):
    """Test a student using their performance forecast.

    View the performance forecast;
    practice a chapter.

    """
    # SETUP:
    test_data = store.get('C485045')
    user = test_data.get('users')
    user = user[Utility.random(0, len(user) - 1)]
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
    book = bookterm.Biology2e()

    # GIVEN: a Tutor student enrolled in a course with at least one completed
    #        reading or homework
    home = TutorHome(selenium, tutor_base_url).open()
    courses = home.log_in(user, password)
    this_week = courses.go_to_course(course_name)
    this_week.clear_training_wheels()

    # WHEN:  they click the 'Performance Forecast' link in the 'Menu'
    performance = this_week.nav.menu.view_the_performance_forecast()

    # THEN:  the performance forecast is displayed
    # AND:   each chapter and section displayed show a progress bar or 'Not
    #        enough exercises completed' message
    assert(performance.is_displayed()), \
        'Not viewing the student performance forecast'
    assert('guide' in performance.location)

    for chapter in performance.forecast.chapters:
        assert(chapter.chapter.number)
        assert(chapter.chapter.title)
        assert(chapter.chapter.progress)
        assert(chapter.chapter.count)
        for section in chapter.sections:
            assert(section.number)
            assert(section.title)
            assert(section.progress)
            assert(section.count)

    # WHEN:  they click a chapter progress bar or chapter 'Pracitce more to
    #        get forecast' button
    options = performance.forecast.chapters
    practice = options[Utility.random(0, len(options) - 1)].chapter.practice()

    # THEN:  a practice session is loaded for the selected chapter
    url = practice.location
    assert('task' in url or 'practice' in url), \
        f'Practice session not started: {url}'
    title = practice.footer.title
    assert(title == 'Practice'), f'Wrong title found: {title}'
    assessments = practice.exercises
    assert(assessments >= 1 and assessments <= 5), \
        f'Wrong number of assessment breadcrumbs: {assessments}'

    # WHEN:  they answer all questions
    while not practice.body.assignment_complete:
        if practice.body.is_interstitial or practice.body.has_correct_answer:
            practice.body._continue()
        elif practice.body.is_multiple_choice:
            practice.body.pane.random_answer()
            practice.body.pane.answer()
            practice.body.pane._continue()
        elif practice.body.is_free_response:
            practice.body.pane.free_response = (
                book.get_term(practice.body.pane.chapter_section)[1])
            practice.body.pane.answer()
            practice.body.pane.random_answer()
            practice.body.pane.answer()
            practice.body.pane._continue()

    # THEN:  the 'You are done.' card is displayed
    assert('You are done.' in selenium.page_source)

    # WHEN:  they click the 'Back to Performance Forecast' button
    performance = practice.body.back_to_performance_forecast()
    performance.reload()
    performance.clear_training_wheels()

    # THEN:  the student dashboard is displayed
    assert(performance.is_displayed()), \
        'Not viewing the student performance forecast'
    assert('guide' in performance.location)
