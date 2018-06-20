"""Tests for the OpenStax blog webpage."""

from tests.markers import expected_failure, test_case, web


@test_case()
@web
@expected_failure
def test_top_article(web_base_url, selenium):
    """Test if the top article link functions properly."""
    # GIVEN: On the OpenStax homepage
    # WHEN: From the top nav bar find Blog button and click it
    # AND: On the region below header, click the title of the article
    # THEN: Full blog article page is loaded.


@test_case()
@web
@expected_failure
def test_top_article_read_more(web_base_url, selenium):
    """Test if the read more link functions properly."""
    # GIVEN: On the OpenStax homepage
    # WHEN: From the top nav bar find Blog button and click it
    # AND: On the region below header, click Read More
    # THEN: Full blog article page is loaded.


@test_case()
@web
@expected_failure
def test_sign_up_from_blog(web_base_url, selenium):
    """Test if user could use the sign up button from blog."""
    # GIVEN: On the OpenStax homepage
    # WHEN: From the top nav bar find Blog button and click it
    # AND: Find the Sign Up button on the page and click it
    # THEN: A new tap of sign up page is loaded
