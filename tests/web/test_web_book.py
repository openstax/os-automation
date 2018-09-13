"""Test the books webpage."""

from tests.markers import nondestructive, skip_test, test_case, web


@test_case('C210348')
@skip_test(reason='Script not written')
@nondestructive
@web
def test_the_book_title_is_displayed(web_base_url, selenium):
    """A book title is shown when a book details page is loaded."""


@test_case('C210349')
@skip_test(reason='Script not written')
@nondestructive
@web
def test_a_book_has_details_and_may_have_resources(web_base_url, selenium):
    """Books have a book details tab and may have user-specific resources."""


@test_case('C210350')
@skip_test(reason='Script not written')
@nondestructive
@web
def test_the_table_of_contents_is_available(web_base_url, selenium):
    """Books have a table of contents."""


@test_case('C210351')
@skip_test(reason='Script not written')
@nondestructive
@web
def test_the_webview_book_is_available(web_base_url, selenium):
    """The online version of a book is available."""


@test_case('C210352')
@skip_test(reason='Script not written')
@nondestructive
@web
def test_able_to_download_the_book_pdf(web_base_url, selenium):
    """The PDF version of a book is available for download."""


@test_case('C210353')
@skip_test(reason='Script not written')
@nondestructive
@web
def test_links_are_available_for_purchasing_print_copies(
        web_base_url, selenium):
    """Users are directed to resellers when they need a print copy."""


@test_case('C210354')
@skip_test(reason='Script not written')
@nondestructive
@web
def test_links_are_available_for_purchasing_print_copies_on_a_mobile_device(
        web_base_url, selenium):
    """Mobile users are directed to resellers when they need a print copy."""


@test_case('C210355')
@skip_test(reason='Script not written')
@nondestructive
@web
def test_a_bookshare_copy_of_a_book_may_be_available(web_base_url, selenium):
    """Users are directed to Bookshare."""


@test_case('C210356')
@skip_test(reason='Script not written')
@nondestructive
@web
def test_an_ibook_version_may_be_available_on_itunes(web_base_url, selenium):
    """Users are directed to iTunes for iBooks."""


@test_case('C210357')
@skip_test(reason='Script not written')
@nondestructive
@web
def test_a_kindle_version_may_be_available_on_amazon(web_base_url, selenium):
    """Users are directed to Amazon for Kindle e-books."""


@test_case('C210358')
@skip_test(reason='Script not written')
@nondestructive
@web
def test_interested_parties_are_directed_to_the_interest_form(
        web_base_url, selenium):
    """Users interested in a subject are directed to the interest form."""


@test_case('C210359')
@skip_test(reason='Script not written')
@nondestructive
@web
def test_people_currently_using_a_book_are_directed_to_the_adoption_form(
        web_base_url, selenium):
    """Current book adopters are directed to the adoption form."""


@test_case('C210360')
@skip_test(reason='Script not written')
@nondestructive
@web
def test_a_book_contains_a_summary_authors_publish_date_isbn_and_license(
        web_base_url, selenium):
    """A book detail lists a summary, authors, date, ISBN, and license."""


@test_case('C210361')
@skip_test(reason='Script not written')
@nondestructive
@web
def test_a_current_book_edition_has_an_errata_section(web_base_url, selenium):
    """Current book editions have an open errata log."""


@test_case('C210362')
@skip_test(reason='Script not written')
@nondestructive
@web
def test_an_old_book_edition_does_not_have_an_errata_section(
        web_base_url, selenium):
    """Previous book editions do not have an open errata log."""


@test_case('C210363')
@skip_test(reason='Script not written')
@nondestructive
@web
def test_users_may_view_current_errata_for_a_book(web_base_url, selenium):
    """All users may view the errata log for a subject."""


@test_case('C210364')
@skip_test(reason='Script not written')
@nondestructive
@web
def test_logged_in_users_may_access_the_errata_form(web_base_url, selenium):
    """Logged in users may access the errata submission form."""


@test_case('C210365')
@skip_test(reason='Script not written')
@nondestructive
@web
def test_users_must_log_in_to_access_the_errata_form(web_base_url, selenium):
    """Users must log in to access the errata submission form."""


@test_case('C210366')
@skip_test(reason='Script not written')
@nondestructive
@web
def test_mobile_users_must_log_in_to_access_the_errata_submission_form(
        web_base_url, selenium):
    """Mobile users must log in to access the errata submission form."""


@test_case('C210367')
@skip_test(reason='Script not written')
@nondestructive
@web
def test_users_must_sign_up_to_access_locked_instructor_content(
        web_base_url, selenium):
    """Users are directed to Accounts sign up to access locked content."""


@test_case('C210368')
@skip_test(reason='Script not written')
@nondestructive
@web
def test_pending_accounts_see_access_pending_for_locked_resources(
        web_base_url, selenium):
    """Accounts pending verification see Access pending for locked content."""


@test_case('C210369')
@skip_test(reason='Script not written')
@nondestructive
@web
def test_locked_resources_are_accessible_after_a_teacher_logs_in(
        web_base_url, selenium):
    """Locked resources are available after a verified instructor logs in."""


@test_case('C210370')
@skip_test(reason='Script not written')
@nondestructive
@web
def test_resources_have_a_title_description_and_access_type(
        web_base_url, selenium):
    """Resource have a title, a description, and an access type."""


@test_case('C210371')
@skip_test(reason='Script not written')
@nondestructive
@web
def test_unverified_users_are_sent_to_faculty_verification_for_resource_locks(
        web_base_url, selenium):
    """Unverified, logged in users are sent to verification."""


@test_case('C210372')
@skip_test(reason='No locked student content')
@nondestructive
@web
def test_users_are_sent_to_sign_up_for_locked_student_content(
        web_base_url, selenium):
    """Users are directed to sign up to access locked student content."""


@test_case('C210373')
@skip_test(reason='Script not written')
@nondestructive
@web
def test_users_may_view_the_webinar_schedule(web_base_url, selenium):
    """Users may view the current webinar schedule."""


@test_case('C210374')
@skip_test(reason='Script not written')
@nondestructive
@web
def test_book_allies_have_a_name_description_and_link(web_base_url, selenium):
    """OpenStax Allies show the company information and site link."""


@test_case('C210375')
@skip_test(reason='Script not written')
@nondestructive
@web
def test_available_student_resources_have_a_download_link(
        web_base_url, selenium):
    """Student resources have a download link."""
