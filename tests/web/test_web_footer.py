"""Tests for the OpenStax footer."""

from tests.markers import expected_failure, nondestructive, test_case, web


@test_case('')
@expected_failure
@nondestructive
@web
def test_opensource_link(web_base_url, selenium):
    """Tests the opensource link."""
    # GIVEN: On the OpenStax homepage

    # WHEN: Go to bottom of the page and click
    # on Open Source in the footer with dark background

    # THEN: Open Source page is loaded


@test_case('')
@expected_failure
@nondestructive
@web
def test_presskit_link(web_base_url, selenium):
    """Tests the presskit link."""
    # GIVEN: On the OpenStax homepage

    # WHEN: Go to bottom of the page and click
    # on press kit in the footer with dark background

    # THEN: Press kit page is loaded


@test_case('')
@expected_failure
@nondestructive
@web
def test_newsletter_link(web_base_url, selenium):
    """Tests the newsletter link."""
    # GIVEN: On the OpenStax homepage

    # WHEN: Go to bottom of the page and click
    # on newsletter in the footer with dark background

    # THEN: Newsletter page is loaded


@test_case('')
@expected_failure
@nondestructive
@web
def test_contact_link(web_base_url, selenium):
    """Tests the contact link."""
    # GIVEN: On the OpenStax homepage

    # WHEN: Go to bottom of the page and click
    # on contact in the footer with dark background

    # THEN: Contact page is loaded


@test_case('')
@expected_failure
@nondestructive
@web
def test_facebook_link(web_base_url, selenium):
    """Tests the facebook link."""
    # GIVEN: On the OpenStax homepage

    # WHEN: Go to bottom of the page and click
    # on facebook in the footer with dark background

    # THEN: facebook page is loaded


@test_case('')
@expected_failure
@nondestructive
@web
def test_linkedin_link(web_base_url, selenium):
    """Tests the linkedin link."""
    # GIVEN: On the OpenStax homepage

    # WHEN: Go to bottom of the page and click
    # on linkedin in the footer with dark background

    # THEN: linkedin page is loaded


@test_case('')
@expected_failure
@nondestructive
@web
def test_twitter_link(web_base_url, selenium):
    """Tests the twitter link."""
    # GIVEN: On the OpenStax homepage

    # WHEN: Go to bottom of the page and click
    # on twitter in the footer with dark background

    # THEN: twitter page is loaded
