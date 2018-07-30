"""All tests for openstax payment site."""

from pages.payments.login import PaymentsLogin
from pages.tutor.home import TutorHome
from pages.tutor.student_enrolling import StudentEnroll
from pages.accounts.profile import Profile
from tests.markers import expected_failure, nondestructive, payments, test_case


@nondestructive
@payments
@test_case('C208906')
def test_os_log_in(payments_base_url, driver, admin):
    """Test logging in with os accounts."""
    # GIVEN:
    # WHEN: Go to OpenStax payments admin page
    page = PaymentsLogin(driver, payments_base_url).open()
    assert(not page.logged_in), 'Unexpected active user session.'
    # AND: Log in as an admin in OpenStax accounts
    page = page.login_with_osa(*admin)
    # THEN: User should be able to log in and be taken to payment's home page
    assert page.logged_in, 'Failed to log in.'


@nondestructive
@payments
@test_case('C208907')
def test_log_out_from_nav_bar(payments_base_url, driver, admin):
    """Test logging out from navbar."""
    # GIVEN: User is logged in as admin
    page = PaymentsLogin(driver, payments_base_url).open()
    page = page.login_with_osa(*admin)
    # WHEN: Click 'log out' at nav bar
    page.nav.log_out()
    # THEN: User should be able to log out
    assert(not page.logged_in), 'Failed to log out'


@nondestructive
@payments
@test_case('C208908')
def test_click_logo(payments_base_url, driver, admin):
    """Test clicking logo to go back to home page."""
    # GIVEN: User is logged in as admin
    page = PaymentsLogin(driver, payments_base_url).open()
    page = page.login_with_osa(*admin)
    # AND: User is at a page other then the home
    page.go_to_orders()
    # WHEN: Click the logo at top left
    page.nav.click_logo()
    # THEN: User should be taken to the home page
    assert 'order' not in driver.current_url, 'Failed to land on order page.'


@nondestructive
@payments
@test_case('C208909')
def test_go_to_email_logs(payments_base_url, driver, admin):
    """Test email logs page."""
    # GIVEN: User is logged in as admin
    page = PaymentsLogin(driver, payments_base_url).open()
    page = page.login_with_osa(*admin)
    # WHEN: Click 'email logs' on the page
    page = page.go_to_email_logs()
    # THEN: User should be taken to the email logs page
    assert 'emaillog' in driver.current_url, 'Failed to land email log page.'
    # AND: User should be able to see a list of emails with correct properties
    elist = page.email_list
    assert elist
    assert (
            elist.lastest_item.get_email_type and
            elist.lastest_item.get_email_address and
            elist.lastest_item.get_email_time and
            elist.lastest_item.get_email_status
    ), 'Email fields missing.'


@nondestructive
@payments
@test_case('C208910')
def test_go_to_orders(payments_base_url, driver, admin):
    """Test orders page."""
    # GIVEN: User is logged in as admin
    page = PaymentsLogin(driver, payments_base_url).open()
    page = page.login_with_osa(*admin)
    # WHEN: Click 'orders' on the page
    page = page.go_to_orders()
    # THEN: User should be taken to the orders page
    assert 'order' in driver.current_url
    # AND: User should be able to see a list of orders with correct properties
    olist = page.orders_list
    assert olist
    assert (
        olist.lastest_item.get_order_time and
        olist.lastest_item.get_order_identifier and
        olist.lastest_item.get_order_product and
        olist.lastest_item.get_order_uuid
    ), 'Order fields missing.'


@nondestructive
@payments
@test_case('C210266')
def test_go_into_order_detail(payments_base_url, driver, admin):
    """Test order's detail page."""
    # GIVEN: User is logged in as admin
    page = PaymentsLogin(driver, payments_base_url).open()
    page = page.login_with_osa(*admin)
    # AND: Is at the orders page
    page = page.go_to_orders()
    # WHEN: User click on an order item
    page.orders_list.lastest_item.click_item()
    # THEN: User should be taken to the order's detail page for that order
    assert 'change' in driver.current_url


@expected_failure
@nondestructive
@payments
@test_case('C208911')
def test_email_log_for_student_payments(payments_base_url, tutor_base_url,
                                        accounts_base_url, driver, admin,
                                        student, teacher, address, city, visa,
                                        zipcode, exp_date, cvv, billing):
    """Test the new email log for student payments."""
    # GIVEN: A new student's payment have just being made
    page = TutorHome(driver, tutor_base_url).open().log_in(*teacher)
    page = page.nav.go_to_create_course().create_new_course()
    course_url = page.nav.go_to_course_settings().get_access_url()
    page = Profile(driver, accounts_base_url).open().log_out()
    emails = page.log_in(*student).emails
    page = StudentEnroll(driver, course_url).open().logged_in_enroll_pay_now()
    page.payment_proceed(address, city, zip, visa, exp_date, cvv, billing)

    # WHEN: Go to payments and sign up as an admin
    page = PaymentsLogin(driver, payments_base_url).open()
    page = page.login_with_osa(*admin)

    # AND: Go to the email logs page
    page = page.go_to_email_logs()

    # THEN: The new payment should show up in email logs page
    elist = page.email_list
    email = elist.lastest_item.get_email_address
    assert email in emails


@expected_failure
@nondestructive
@payments
@test_case('C208912')
def test_order_item_for_student_payments(payments_base_url, tutor_base_url,
                                         accounts_base_url, driver, admin,
                                         student, teacher, address, city, visa,
                                         zipcode, exp_date, cvv, billing):
    """Test the new order item for student payments."""
    # GIVEN: A new student's payment have just being made
    page = TutorHome(driver, tutor_base_url).open().log_in(*teacher)
    page = page.nav.go_to_create_course().create_new_course()
    course_url = page.nav.go_to_course_settings().get_access_url()
    page = Profile(driver, accounts_base_url).open().log_out()
    page.log_in(*student)
    page = StudentEnroll(driver, course_url).open().logged_in_enroll_pay_now()
    page.payment_proceed(address, city, zip, visa, exp_date, cvv, billing)

    # WHEN: Go to payments and sign up as an admin
    page = PaymentsLogin(driver, payments_base_url).open()
    page = page.login_with_osa(*admin)
    # AND: Go to the orders page
    page = page.go_to_orders().orders_list.lastest_item.click_item()
    # THEN: The new payment should show up as success
    transaction = page.transactions_list.lastest_item.get_status
    assert transaction


@expected_failure
@nondestructive
@payments
@test_case('C208913')
def test_order_item_for_student_refund(payments_base_url, driver, admin):
    """Docstring."""
    # GIVEN: A student has just submitted a refund request for a course

    # WHEN: Go to payments and sign up as an admin
    # AND: Go to the orders page

    # THEN: The new refund should show up
    pass
