"""Tests for the OpenStax blog webpage."""

from tests.markers import skip_test, test_case, web


@test_case('')
@skip_test(reason='Script not written')
@web
def test_top_article(web_base_url, selenium):
    """Test if the top article link functions properly."""
    # GIVEN: On the blog page

    # WHEN: On the region below header, click the title of the article

    # THEN: Full blog article page is loaded


@test_case('')
@skip_test(reason='Script not written')
@web
def test_top_article_read_more(web_base_url, selenium):
    """Test if the read more link functions properly."""
    # GIVEN: On the blog page

    # WHEN: On the region below header, click Read More

    # THEN: Full blog article page is loaded


@test_case('')
@skip_test(reason='Script not written')
@web
def test_sign_up_from_blog(web_base_url, selenium):
    """Test if user could use the sign up button from blog."""
    # GIVEN: On the blog page

    # WHEN: Click the sign up button

    # THEN: A new type of sign up page is loaded
