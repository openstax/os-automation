"""Test the website press page."""

from pages.web.home import WebHome
from tests.markers import nondestructive, test_case, web
from utils.utilities import Utility
from utils.web import Web


@test_case('C210470')
@nondestructive
@web
def test_the_two_most_recent_press_releases_are_shown(web_base_url, selenium):
    """The two most recent press releases are displayed."""
    # GIVEN: a user viewing the press page
    home = WebHome(selenium, web_base_url).open()
    press = home.footer.directory.press()

    # WHEN:

    # THEN: two press releases are displayed
    # AND:  they have an author, date, title, blurb, and
    #       a "Continue reading" link
    assert(len(press.releases) == 2)
    for release in press.releases:
        assert(release.author)
        assert(release.date)
        assert(release.headline)
        assert(release.excerpt)
        assert(release.continue_reading)

    # WHEN: they click on the "See more press releases"
    #       toggle
    press.see_more_releases()

    # THEN: ten press releases are displayed
    # AND:  the blurb and "Continue reading" link are
    #       not visible
    assert(len(press.releases) == 10)
    for release in press.releases:
        assert(release.author)
        assert(release.date)
        assert(release.headline)
        assert(not release.excerpt)
        assert(not release.continue_reading)

    # WHEN: they click on the "Older" link
    new_date = press.releases[-1].date
    press.view_older_releases()

    # THEN: older press releases are displayed
    for release in press.releases:
        assert(release.date < new_date)

    # WHEN: they click on the "See fewer press releases"
    press.see_fewer_releases()

    # THEN: the two most recent press releases are displayed
    assert(len(press.releases) == 2)

    # WHEN: they click on the release title
    article = press.releases[0].select()

    # THEN: the full article is displayed
    # AND:  other press releases are linked at the bottom of
    #       the full article page
    assert(article.is_displayed())
    assert(article.is_an_article)
    assert(article.other_releases), 'No other releases found'


@test_case('C210471')
@nondestructive
@web
def test_the_ten_most_recent_new_mentions_are_shown(web_base_url, selenium):
    """The ten most recent press mentions are displayed."""
    # GIVEN: a user viewing the press page
    home = WebHome(selenium, web_base_url).open()
    press = home.footer.directory.press()

    # WHEN:

    # THEN: ten news mentions are displayed
    # AND:  the mentions have a host icon, host, date, and
    #       title
    assert(len(press.mentions) == 10)

    # WHEN: they click on the "Older" link
    newest_article_headline = press.mentions[0].headline
    new_mention_date = press.mentions[-1].date
    press.view_older_mentions()

    # THEN: older news mentions are displayed
    assert(press.mentions)
    assert(press.mentions[0].date <= new_mention_date)

    # WHEN: they click on the "Newer" link
    press.view_newer_mentions()

    # THEN: the original news mentions are displayed
    assert(press.mentions[0].headline == newest_article_headline)

    # WHEN: they click on a news article title
    article = press.mentions[Utility.random(end=len(press.mentions) - 1)]
    url = article.url
    headline = article.headline

    # THEN: the full article exists
    Utility.test_url_and_warn(
        url=url, message='"{0}"'.format(headline), driver=selenium)


@test_case('C210472')
@nondestructive
@web
def test_the_openstax_mission_statement_is_outlined(web_base_url, selenium):
    """The OpenStax mission is outlined."""
    # GIVEN: a user viewing the press page
    home = WebHome(selenium, web_base_url).open()
    press = home.footer.directory.press()

    # WHEN:

    # THEN: the mission goal is presented
    assert('To improve educational access and learning for everyone' in
           press.mission_statement)


@test_case('C210473')
@nondestructive
@web
def test_press_inquiry_options(web_base_url, selenium):
    """Press inquiries are directed to MarComm, social accounts, or the kit."""
    # GIVEN: a user viewing the press page
    home = WebHome(selenium, web_base_url).open()
    press = home.footer.directory.press()

    # WHEN:

    # THEN: contact information is displayed
    # AND:  the OpenStax social accounts are linked
    assert(press.contact)
    assert(len(press.social) == 4)

    for social in press.social:
        # WHEN: they click on the social service icon
        social_page = social.check_media_link()

        # THEN: the OpenStax social page is displayed in a
        #       new tab (skip if a 429 from Instagram or
        #       400 from Twitter due to rate limiting)
        if (not social_page.ok
                and social_page.status_code != 429
                and social_page.status_code != 400):
            Utility.test_url_and_warn(code=social_page.status_code,
                                      url=social.url,
                                      message=social.name,
                                      driver=selenium)

    # WHEN: they close the new tab
    # AND:  switch to the original tab
    # AND:  query the "Download press kit" button
    press_kit = press.check_press_kit()

    # THEN: the press kit is available
    if not press_kit.ok:
        Utility.test_url_and_warn(code=press_kit.status_code,
                                  message='Press kit download',
                                  driver=selenium)


@test_case('C210474')
@nondestructive
@web
def test_expert_speaker_availability(web_base_url, selenium):
    """Expert speakers are listed."""
    # GIVEN: a user viewing the press page
    home = WebHome(selenium, web_base_url).open()
    press = home.footer.directory.press()

    # WHEN:

    # THEN: three speakers are shown with a portrait, name,
    #       title, and bio
    assert(len(press.experts) == 2)
    for expert in press.experts:
        assert(expert.has_portrait)
        assert(expert.name)
        assert(expert.role)
        assert(expert.bio)


@test_case('C210475')
@nondestructive
@web
def test_mobile_users_are_presented_a_drop_down_menu(web_base_url, selenium):
    """A section drop down menu covers the page sections for phone viewers."""
    # GIVEN: a user viewing the press page
    # AND:  the screen is 600 pixels wide
    home = WebHome(selenium, web_base_url)
    home.resize_window(width=600)
    home.open()
    press = home.footer.directory.press()

    # WHEN:

    # THEN: ten press releases are displayed
    # AND:  the press release blurbs are not displayed
    assert(len(press.releases) == 10)
    for release in press.releases:
        assert(not release.excerpt)

    # WHEN: they click on the "In the news" pull down menu
    # AND:  select the "News mentions" option
    press.select(Web.NEWS_MENTIONS)

    # THEN: ten news mentions are displayed
    assert(len(press.mentions) == 10)

    # WHEN: they click on the "In the news" pull down menu
    # AND:  select the "Press inquiries" option
    press.select(Web.PRESS_INQUIRIES)

    # THEN: contact information, social media accounts, and
    #       the press kit download are displayed
    assert(press.contact.name)
    assert(press.contact.phone)
    assert(press.contact.email)
    assert(len(press.social) == 4)
    assert(press.press_kit.is_displayed())

    # WHEN: they click on the "In the news" pull down menu
    # AND:  select the "Booking" option
    press.select(Web.BOOKING)

    # THEN: expert speakers are displayed
    assert(len(press.experts) == 2)
    assert(press.experts[0].is_displayed())


@test_case('C210476')
@nondestructive
@web
def test_mobile_users_do_not_see_the_mission_statement(web_base_url, selenium):
    """The mission statement is hidden for mobile users."""
    # GIVEN: a user viewing the press page
    # AND:  the screen is 600 pixels wide
    home = WebHome(selenium, web_base_url)
    home.resize_window(width=600)
    home.open()
    press = home.footer.directory.press()

    # WHEN:

    # THEN: the mission statement section is not displayed
    assert(not press.mission_displayed)
