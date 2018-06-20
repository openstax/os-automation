@test_case('')
@tutor
def test_navbar_elements_present(tutor_base_url, selenium, admin):
    """Test admin console navbar elements present."""
    # GIVEN: logged in as admin

    # WHEN: Click on menu in the navbar
    # AND: Click on admin in the menu dropdown
    # AND: User will be taken to the admin console

    # THEN: User is able to see the navbar with the following elements:
    # "Tutor Admin Console", "Course Organization", "Content", "Legal", "Stats",
    # "Users", "Job", "Payments", "Research Data", "Salesforce", "System Setting".


@test_case('')
@tutor
def test_add_to_catalog_offereings(tutor_base_url, selenium, admin):
    """Test admin to add to catalog offerings."""
    # GIVEN: logged in as admin

    # WHEN: Go to Tutor admin console
    # AND: Click on ""Course Organization""
    # AND: In the drop down click on ""Catalog Offerings""
    # AND: Click the ""Add Offerings"" button
    # AND: Fill out the required fields
    # AND: Click the ""Save"" button

    # THEN: A new course is added to the course catalog with the correct information.


@test_case('')
@tutor
def test_edit_catalog(tutor_base_url, selenium, admin):
    """Test admin to edit catalog in catalog offereings."""
    # GIVEN: logged in as admin

    # WHEN: Go to Tutor admin console
    # AND: Click on ""Course Organization"" in the navbar
    # AND: On the drop down click on ""Catalog Offerings""
    # AND: On the side of a course listing click the ""Edit"" button
    # AND: Change one or more of the fields
    # AND: Click save"

    # THEN: The course is updated with the changed fields


@test_case('')
@tutor
def test_view_student(tutor_base_url, selenium, admin):
    """Test to view students in a course."""
    # GIVEN: logged in as admin

    # WHEN: Go to Tutor admin console
    # AND: Click on ""Course Organization""
    # AND: In the drop down click on ""Courses""
    # AND: Click the ""List Students"" button next to one of the courses

    # THEN: A list of students in the course is displayed


@test_case('')
@tutor
def test_edit_course(tutor_base_url, selenium, admin):
    """Test admin to edit course."""
    # GIVEN: logged in as admin

    # WHEN: Go to Tutor admin console
    # AND: Click on ""Course Organization""
    # AND: In the drop down click on ""Courses""
    # AND: Next to a course click on a the ""Edit"" button
    # AND: Change one or more of the course fields
    # AND: Click the ""Save"" button

    # THEN: The course is edited and the changes are correctly updated


@test_case('')
@tutor
def test_add_course_to_incomplete(tutor_base_url, selenium, admin):
    """Test admin to add course to incomplete ecosystem."""
    # GIVEN: logged in as admin

    # WHEN: Go to Tutor admin console
    # AND: Click on ""Course Organization""
    # AND: In the drop down click on ""Courses""
    # AND: Click the ""Incomplete Bulk Ecosystem Update Jobs""
    # AND: Click ""Add Course""
    # AND: Fill in necessary fields
    # AND: Click ""Save""

    # THEN: A new course is added to the Incomplete Bulk Ecosystem.


@test_case('')
@tutor
def test_add_course_to_failed(tutor_base_url, selenium, admin):
    """Test admin to add course to failed ecosystem."""
    # GIVEN: logged in as admin

    # WHEN:  Go to Tutor admin console
    # AND: Click on ""Course Organization""
    # AND:  In the drop down click on ""Courses""
    # AND: Click the ""Failed Bulk Ecosystem Update Jobs""
    # AND: Click ""Add Course""
    # AND: Fill in necessary fields
    # AND: Click ""Save""

    # THEN: A new course is added to the Failed Bulk Ecosystem.


@test_case('')
@tutor
def test_add_school(tutor_base_url, selenium, admin):
    """Test admin to add a school."""
    # GIVEN: logged in as admin

    # WHEN: Go to Tutor admin console
    # AND: Click on ""Course Organization""
    # 3. In the drop down click on ""Schools""
    # AND: Click the ""Add School"" button
    # AND: Fill out the required fields
    # AND: Click the ""Save"" button

    # THEN: The new school is added to schools list


@test_case('')
@tutor
def test_edit_school(tutor_base_url, selenium, admin):
    """Test admin to edit a school."""
    # GIVEN: logged in as admin

    # WHEN: Go to Tutor admin console
    # AND: Click on ""Course Organization"" in the navbar
    # AND: In the drop down click on ""Schools""
    # AND: Click the edit button next to a school
    # AND: Update one or more fields
    # AND: Click the ""Save"" button

    # THEN: The edited school is correctly updated


@test_case('')
@tutor
def test_delete_schoole(tutor_base_url, selenium, admin):
    """Test admin to delete a school."""
    # GIVEN: logged in as admin

    # WHEN: Go to Tutor admin console
    # AND: Click on ""Course Organization"" in the navbar
    # AND: In the drop down click on ""Schools""
    # AND: Next to a school click the ""Delete"" button
    # AND: Click ""Okay""

    # THEN: The deleted school is removed from the list of schools


@test_case('')
@tutor
def test_add_district(tutor_base_url, selenium, admin):
    """Test admin to add district."""
    # GIVEN: logged in as admin

    # WHEN: Go to Tutor admin console
    # AND: Click on ""Course Organization""
    # AND: In the drop down click on ""District""
    # AND: Click the ""Add District"" button
    # AND: Fill out the required fields
    # AND: Click the ""Save"" button

    # THEN: The new district is added to the list of districts.


@test_case('')
@tutor
def test_edit_district(tutor_base_url, selenium, admin):
    """Test admin to edit district."""
    # GIVEN: logged in as admin

    # WHEN: Go to Tutor admin console
    # AND: Click on ""Course Organization""
    # AND: In the drop down click on ""District""
    # AND: Click the ""Edit District"" button
    # AND: Edit the field
    # AND: Click the ""Save"" button

    # THEN: The edited district is correctly updated.


@test_case('')
@tutor
def test_delete_district(tutor_base_url, selenium, admin):
    """Test admin to delete district."""
    # GIVEN: logged in as admin

    # WHEN: Go to Tutor admin console
    # AND: Click on ""Course Organization""
    # AND: In the drop down click on ""District""
    # AND: Click the ""delete"" button

    # THEN: District is deleted if it has no schools. If the district contains schools it is not deleted.


@test_case('')
@tutor
def test_tag_searching(tutor_base_url, selenium, admin):
    """Test tag searching correctly searches."""
    # GIVEN: logged in as admin

    # WHEN: Go to Tutor admin console
    # AND: Click on ""Content"" in the navbar
    # AND: In the dropdown click on ""Tags""
    # AND: In the search bar enter a random word
    # AND: Click the ""Search"" button

    # THEN: Tags related to the entered word is correctly found and displayed


@test_case('')
@tutor
def test_download_book_manifest(tutor_base_url, selenium, admin):
    """Test admin to download book manifest."""
    # GIVEN: logged in as admin

    # WHEN: Go to Tutor admin console
    # AND: Click on ""Content"" in the navbar
    # AND: In the drop down click on ""Ecosystems""
    # AND: Click the ""Download Manifest"" next to a book

    # THEN: The book manifest is downloaded


@test_case('')
@tutor
def test_save_comment(tutor_base_url, selenium, admin):
    """Test admin to save a comment."""
    # GIVEN: logged in as admin

    # WHEN: Go to Tutor admin console
    # AND: Click on ""Content"" in the navbar
    # AND: In the drop down click on ""Ecosystems""
    # AND: Choose a book and write a comment
    # AND: Click ""Save""

    # THEN: Comment is successfully saved.


@test_case('')
@tutor
def test_view_book_archive(tutor_base_url, selenium, admin):
    """Test admin to view book archive."""
    # GIVEN: logged in as admin

    # WHEN: Go to Tutor admin console
    # AND: Click on ""Content"" in the navbar
    # AND: In the drop down click on ""Ecosystems""
    # AND: Click on ""Archive""

    # THEN: User is taken to the archive page for the selected book.


@test_case('')
@tutor
def test_create_new_contract(tutor_base_url, selenium, admin):
    """Test admin to create a new contract."""
    # GIVEN: logged in as admin

    # WHEN: Go to Tutor admin console
    # AND: Click on ""Legal"" in the navbar
    # AND: In the drop down click on ""Terms""
    # AND: At the bottom of the page click ""New Contract""
    # AND: Fill out the required fields
    # AND: Click ""Create Contract""

    # THEN: A new contract is created and appears in the contracts list


@test_case('')
@tutor
def test_edit_contract(tutor_base_url, selenium, admin):
    """Test admin to edit a contract."""
    # GIVEN: logged in as admin

    # WHEN: Go to Tutor admin console
    # AND: Click on ""Legal"" in the navbar
    # AND: In the drop down click on ""Terms""
    # AND: At the bottom of the page click ""Edit""
    # AND: Edit one or more fields
    # AND: Click ""Update Contract""

    # THEN: Contract is updated


@test_case('')
@tutor
def test_delete_contract(tutor_base_url, selenium, admin):
    """Test admin to delete a contract."""
    # GIVEN: logged in as admin

    # WHEN: Go to Tutor admin console
    # AND: Click on ""Legal"" in the navbar
    # AND: In the drop down click on ""Terms""
    # AND: At the bottom of the page click ""Delete""
    # AND: Click ""Okay""

    # THEN: The selected contract is deleted and no longer appears in the list


@test_case('')
@tutor
def test_view_contract(tutor_base_url, selenium, admin):
    """Test admin to view a contract."""
    # GIVEN: logged in as admin

    # WHEN: Go to Tutor admin console
    # AND: Click on ""Legal"" in the navbar
    # AND: In the drop down click on ""Terms""
    # AND: Click on one of the versions of one of the legal docs

    # THEN: Page containing the legal doc information is loaded


@test_case('')
@tutor
def test_add_targeted_contract(tutor_base_url, selenium, admin):
    """Test admin to add targeted contract."""
    # GIVEN: logged in as admin

    # WHEN: Go to Tutor admin console
    # AND: Click on ""Legal"" in the navbar
    # AND: In the drop down click on ""Targeted Contract""
    # AND: Click on ""Add Targeted Contract""
    # AND: Fill in all necessary field
    # AND: Click ""Submit""

    # THEN: A new targeted contract is created.


@test_case('')
@tutor
def test_edit_targeted_contract(tutor_base_url, selenium, admin):
    """Test admin to edit targeted contract."""
    # GIVEN: logged in as admin

    # WHEN: Go to Tutor admin console
    # AND: Click on ""Legal"" in the navbar
    # AND: In the drop down click on ""Targeted Contract""
    # AND: Click on ""Edit"" next to a contract

    # THEN: "User are unable to edit at this time. " message is loaded.


@test_case('')
@tutor
def test_delete_targeted_contract(tutor_base_url, selenium, admin):
    """Test admin to delete targeted contract."""
    # GIVEN: logged in as admin

    # WHEN: Go to Tutor admin console
    # AND: Click on ""Legal"" in the navbar
    # AND: In the drop down click on ""Targeted Contract""
    # AND: Click on ""delete""

    # THEN: Contract is removed from the list of targeted contracts.


@test_case('')
@tutor
def test_view_user_list(tutor_base_url, selenium, admin):
    """Test admin to view user list."""
    # GIVEN: logged in as admin

    # WHEN: Go to Tutor admin console
    # AND: Click on ""Users"" in the navbar

    # THEN: A list of users is displayed with a search bar that allows an admin to find specific users


@test_case('')
@tutor
def test_view_user_info(tutor_base_url, selenium, admin):
    """Test admin to view user info."""
    # GIVEN: logged in as admin

    # WHEN: Go to Tutor admin console
    # AND: Click on ""Users"" in the navbar
    # AND: Click on the ""Info"" button

    # THEN: User is taken to a page containing user info.


@test_case('')
@tutor
def test_view_jobs(tutor_base_url, selenium, admin):
    """Test admin to view jobs."""
    # GIVEN: logged in as admin

    # WHEN: Go to Tutor admin console
    # AND: Click on ""Jobs"" in the navbar

    # THEN: List of jobs are loaded. Jobs can be filtered for more specific searches.


@test_case('')
@tutor
def test_extend_payment(tutor_base_url, selenium, admin):
    """Test admin to extend payment due dates."""
    # GIVEN: logged in as admin

    # WHEN: Go to Tutor admin console
    # AND: Click on ""Payments"" in the navbar
    # AND: Click on ""Extend Payment Due Dates""

    # THEN: Payment due dates are extended.


@test_case('')
@tutor
def test_export_data(tutor_base_url, selenium, admin):
    """Test admin to export data."""
    # GIVEN: logged in as admin

    # WHEN:  Go to Tutor admin console
    # AND: Click on ""Research Data"" in the navbar
    # AND: Choose two dates (Start and end)
    # AND: Click the ""Export"" button

    # THEN: Data is successfully exported from the start and end dates


@test_case('')
@tutor
def test_set_salesforce_user(tutor_base_url, selenium, admin):
    """Test admin to set salesforce user."""
    # GIVEN: logged in as admin

    # WHEN: Go to Tutor admin console
    # AND: Click on ""Salesforce"" in the navbar
    # AND: In the dropdown click on ""Setup""
    # AND: Click on ""Set Salesforce User""

    # THEN: Salesforce website login page is loaded


@test_case('')
@tutor
def test_edit_settings(tutor_base_url, selenium, admin):
    """Test admin to edit settings."""
    # GIVEN: logged in as admin

    # WHEN: Go to Tutor admin console
    # AND: Click on ""System Settings"" in the navbar
    # AND: In the drop down click on ""Settings""
    # AND: Edit one or more fields in settings
    # AND: Click ""Save All""

    # THEN: Settings is successfully updated


@test_case('')
@tutor
def test_view_course_stats(tutor_base_url, selenium, admin):
    """Test admin to view course stats."""
    # GIVEN: logged in as admin

    # WHEN: Go to Tutor admin console
    # AND: Click on ""Stats"" in the navbar
    # AND: In the drop down click on ""Courses""

    # THEN: The course stats page is loaded


@test_case('')
@tutor
def test_update_salesforce(tutor_base_url, selenium, admin):
    """Test admin to update salesforce."""
    # GIVEN: logged in as admin

    # WHEN: Go to Tutor admin console
    # AND: Click on ""Salesforce"" in the navbar
    # AND: In the dropdown click on ""Actions""
    # AND: Click on ""Update Salesforce""

    # THEN: Salesforce is updated.


@test_case('')
@tutor
def test_add_notification(tutor_base_url, selenium, admin):
    """Test admin to add notification."""
    # GIVEN: logged in as admin

    # WHEN: Go to Tutor admin console
    # AND: Click on ""System Settings"" in the navbar
    # AND: In the drop down click on ""Notifications""
    # AND: Choose either ""General Notifications"" or ""Instructor Notifications"" and fill out the necessary fields
    # AND: Click ""Add""

    # THEN: A new notification is created.


@test_case('')
@tutor
def test_delete_notification(tutor_base_url, selenium, admin):
    """Test admin to delete notification."""
    # GIVEN: logged in as admin

    # WHEN: Go to Tutor admin console
    # AND: Click on ""System Settings"" in the navbar
    # AND: In the drop down click on ""Notifications""
    # AND: Click ""Remove"" next to a current notification

    # THEN: The notification is removed from the notification list.


@test_case('')
@tutor
def test_delete_targeted_contract(tutor_base_url, selenium, admin):
    """Test admin to delete targeted contract."""
    # GIVEN: logged in as admin

    # WHEN: Go to Tutor admin console
    # AND: Click on ""Legal"" in the navbar
    # AND: In the drop down click on ""Targeted Contract""
    # AND: Click on ""delete"".

