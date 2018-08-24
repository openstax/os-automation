"""All tests for openstax payment site."""

from pages.payments.login import PaymentsLogin
from pages.tutor.home import TutorHome
from pages.tutor.student_enrolling import StudentEnroll
from tests.markers import expected_failure, nondestructive, payments, test_case


@test_case('C208906')
@nondestructive
@payments
def test_log_into_payments_with_admin_account(payments_base_url,
                                              selenium, admin):
    """Test logging in with a Payments admin account."""
    # GIVEN: the Payments login screen is loaded
    page = PaymentsLogin(selenium, payments_base_url).open()

    # WHEN: the user logs in as an admin using OpenStax Accounts
    page = page.login_with_osa(*admin)

    # THEN: the user is logged in
    # AND: the Payment's home page is displayed
    assert(page.logged_in), 'Failed to log in.'
    assert(page.nav.is_displayed), 'Nav not loaded'


@test_case('C208907')
@expected_failure
@nondestructive
@payments
def test_log_out_from_nav_bar(payments_base_url, selenium, admin):
    """Test logging out from the navbar control."""
    # GIVEN: a user logged into Payments as admin
    page = PaymentsLogin(selenium, payments_base_url).open()
    page = page.login_with_osa(*admin)

    # WHEN: they click 'log out' on the navigation bar
    page.nav.log_out()

    # THEN: the user is logged out
    assert(not page.logged_in), 'Failed to log out'


@test_case('C208908')
@expected_failure
@nondestructive
@payments
def test_click_logo(payments_base_url, selenium, admin):
    """Clicking the logo to go back to the home page."""
    # GIVEN: a user logged in as a Payments admin
    # AND: they are viewing the orders page
    page = PaymentsLogin(selenium, payments_base_url).open()
    page = page.login_with_osa(*admin)
    page.go_to_orders()

    # WHEN: they click the logo at top left
    page.nav.click_logo()

    # THEN: the home page is loaded
    assert ('order' not in selenium.current_url), \
        'Failed to land on order page.'


@test_case('C208909')
@expected_failure
@nondestructive
@payments
def test_go_to_email_logs(payments_base_url, selenium, admin):
    """Go to the email logs."""
    # GIVEN: an admin logged into Payments
    page = PaymentsLogin(selenium, payments_base_url).open()
    page = page.login_with_osa(*admin)

    # WHEN: they click the 'email logs' link on the home page
    page = page.go_to_email_logs()

    # THEN: the email log list is displayed
    assert('emaillog' in selenium.current_url), \
        'Failed to land email log page.'
    elist = page.email_list
    assert(elist)
    assert(elist.newest_order.get_email_type and
           elist.newest_order.get_email_address and
           elist.newest_order.get_email_time and
           elist.newest_order.get_email_status), \
        'Email fields missing.'


@test_case('C208910')
@expected_failure
@nondestructive
@payments
def test_go_to_orders(payments_base_url, selenium, admin):
    """Go to the orders page."""
    # GIVEN: an admin logged into Payments
    page = PaymentsLogin(selenium, payments_base_url).open()
    page = page.login_with_osa(*admin)

    # WHEN: the click the 'orders' link on the home page
    page = page.go_to_orders()

    # THEN: the orders page is displayed
    # AND: orders are presented
    # AND: have the correct properties
    assert('order' in selenium.current_url), 'Not viewing orders'
    olist = page.orders_list
    assert(olist)
    assert(olist.newest_order.get_order_time and
           olist.newest_order.get_order_identifier and
           olist.newest_order.get_order_product and
           olist.newest_order.get_order_uuid), \
        'Order fields missing.'


@test_case('C210266')
@expected_failure
@nondestructive
@payments
def test_view_the_details_for_an_order(payments_base_url, selenium, admin):
    """View an order's detail page."""
    # GIVEN: an admin logged into Payments
    # AND: viewing the orders page
    page = PaymentsLogin(selenium, payments_base_url).open()
    page = page.login_with_osa(*admin)
    page = page.go_to_orders()

    # WHEN: the user clicks on a the latest order item
    page.orders_list.newest_order.click_item()

    # THEN: the order's detail page is displayed
    assert('change' in selenium.current_url), 'Not at an order detail page'


@test_case('C208911')
@expected_failure
@payments
def test_email_log_for_student_payments(payments_base_url, tutor_base_url,
                                        selenium, admin, student, teacher,
                                        address, city, visa, zipcode,
                                        exp_date, cvv, billing_zip):
    """Test the new email log for student payments."""
    # GIVEN: A new student's payment have just being made
    page = TutorHome(selenium, tutor_base_url).open().log_in(*teacher)
    page = page.nav.go_to_create_course().create_new_course()
    course_url = page.nav.go_to_course_settings().get_access_url()
    page.nav.log_out().log_in(*student)
    emails = page.nav.go_to_my_account().emails.email_texts
    page = StudentEnroll(selenium, course_url, timeout=60) \
        .open().logged_in_enroll_pay_now()
    page, number = page.make_purchase(address, city, zipcode,
                                      visa, exp_date, cvv, billing_zip)
    page.nav.log_out()

    # WHEN: Go to payments and sign up as an admin
    # AND: Go to the email logs page
    page = PaymentsLogin(selenium, payments_base_url).open()
    page = page.login_with_osa(*admin)

    page = page.go_to_email_logs()

    # THEN: The new payment should show up in email logs page
    elist = page.email_list
    email = elist.newest_order.get_email_address
    assert(email in emails)


@test_case('C208912')
@expected_failure
@payments
def test_order_item_for_student_payments(payments_base_url, tutor_base_url,
                                         selenium, admin, student, teacher,
                                         address, city, visa, zipcode,
                                         exp_date, cvv, billing_zip):
    """Test the new order item for student payments."""
    # GIVEN: A new student's payment have just being made
    page = TutorHome(selenium, tutor_base_url).open().log_in(*teacher)
    page = page.nav.go_to_create_course().create_new_course()
    course_url = page.nav.go_to_course_settings().get_access_url()
    page.nav.log_out().log_in(*student)
    page = StudentEnroll(selenium, course_url, timeout=60) \
        .open().logged_in_enroll_pay_now()
    page, number = page.make_purchase(address, city, zipcode,
                                      visa, exp_date, cvv, billing_zip)
    page.nav.log_out()

    # WHEN: Go to payments and sign up as an admin
    page = PaymentsLogin(selenium, payments_base_url).open()
    page = page.login_with_osa(*admin)

    # AND: Go to the orders page
    page = page.go_to_orders().orders_list.newest_order.click_item()

    # THEN: The new payment should show up as success
    transaction = page.transactions_list.newest_order.get_status
    assert number == page.get_identifier
    assert transaction.get_type == 'Payment'
    assert transaction == 'Success'


@test_case('C208913')
@expected_failure
@payments
def test_order_item_for_student_refund(payments_base_url, tutor_base_url,
                                       selenium, admin, student, teacher,
                                       address, city, visa, zipcode,
                                       exp_date, cvv, billing_zip):
    """Refund a student."""
    # GIVEN: A student has just submitted a refund request for a course
    page = TutorHome(selenium, tutor_base_url).open().log_in(*teacher)
    page = page.nav.go_to_create_course().create_new_course()
    course_url = page.nav.go_to_course_settings().get_access_url()
    page.nav.log_out().log_in(*student)
    page = StudentEnroll(selenium, course_url, timeout=60) \
        .open().logged_in_enroll_pay_now()
    page, number = page.make_purchase(address, city, zipcode,
                                      visa, exp_date, cvv, billing_zip)
    page = page.nav.go_to_manage_payments()
    page.get_latest_order.request_refund()
    page.nav.log_out()

    # WHEN: Go to payments and sign up as an admin
    page = PaymentsLogin(selenium, payments_base_url).open()
    page = page.login_with_osa(*admin)

    # AND: Go to the orders page
    page = page.go_to_orders().orders_list.newest_order.click_item()

    # THEN: The new refund should show up
    transaction = page.transactions_list.items[1]
    assert number == page.get_identifier
    assert transaction.get_type == 'Refund'
    assert transaction.get_status == 'Success'
