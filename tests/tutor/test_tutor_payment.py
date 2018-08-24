"""Test case for tutor page student payment interaction."""

from tests.markers import nondestructive, skip_test, test_case, tutor


@test_case('')
@skip_test(reason='Script not written')
@nondestructive
@tutor
def test_tutor_payment_page(tutor_base_url, selenium, student):
    """Test the tutor payment page."""
    # GIVEN: Tutor page logged in as a student

    # WHEN: The user clicks on the "Manage payments" menu item

    # THEN: The Payment Management page loads


@test_case('')
@skip_test(reason='Script not written')
@nondestructive
@tutor
def test_tutor_invoice_page(tutor_base_url, selenium, student):
    """Test the tutor invoice page."""
    # GIVEN: Tutor page logged in as a student

    # WHEN: The user clicks on "Manage payments" menu item

    # AND: The user clicks "Invoice" of any one of the transactions

    # THEN: A page of the detailed invoice loads


@test_case('')
@skip_test(reason='Script not written')
@tutor
def test_payment_option(tutor_base_url, selenium, student):
    """Test the tutor payment option section."""
    # GIVEN: Logged into Tutor as a student

    # WHEN: The user goes to student enrollment url for a paid course

    # AND: The user agrees to Tutor Terms of Use and Privacy Policy

    # AND: From "Pay now or pay later" screen, the user click "Buy access now"

    # THEN: Payment screen -- with options for Free Trial and to Buy Access to
    # course now is loaded


@test_case('')
@skip_test(reason='Script not written')
@tutor
def test_course_payment(tutor_base_url, selenium, student):
    """Test the process of making payment for a course."""
    # GIVEN: Logged into Tutor as a student

    # WHEN: The user goes to the url of a paid course

    # AND: The user sign Terms and Privacy policy

    # AND: Fill out information and click on "Buy access now"

    # THEN: Student gets confirmation that payment was accepted successfully,
    # and there should be an option to "Access User's Course"


@test_case('')
@skip_test(reason='Script not written')
@tutor
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
@skip_test(reason='Script not written')
@tutor
def test_unfilled_purchase(tutor_base_url, selenium, student):
    """Test the tutor assignment review."""
    # GIVEN: Logged into Tutor as a student

    # AND: Being at the payment page

    # WHEN: The user clicks purchase directly

    # THEN: Multiple warning shows up


@test_case('')
@skip_test(reason='Script not written')
@tutor
def test_not_payed_course_skip_payment(tutor_base_url, selenium, student):
    """Test that course not payed skips the payment section."""
    # GIVEN:  Logged into tutor as a student

    # WHEN: The user goes throught the enrollment process

    # AND: Put student id

    # THEN: Student account page is loaded


@test_case('')
@skip_test(reason='Script not written')
@tutor
def test_buy_free_trial(tutor_base_url, selenium, student):
    """Test buying a course from free trial."""
    # GIVEN: Logged into Tutor as a student

    # AND: Enrolled in a class with 14 days trial mode

    # WHEN: The user clicks "Pay Now"

    # AND: Complete the payment

    # THEN: Free trial tag no longer there
