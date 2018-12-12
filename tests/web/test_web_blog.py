"""Test the website blog app."""

from pages.web.blog import Blog
from tests.markers import nondestructive, smoke_test, test_case, web
from utils.utilities import Utility


@test_case('C210401')
@nondestructive
@web
def test_one_blog_entry_is_pinned(web_base_url, selenium):
    """Test one blog entry is pinned to the top of the blog page."""
    # GIVEN: a user viewing the blog page
    blog = Blog(selenium, web_base_url).open()

    # WHEN:

    # THEN: one article pinned to the top
    assert(blog.pinned.is_displayed()), \
        'The pinned blog entry is not displayed'


@test_case('C210402')
@nondestructive
@web
def test_able_to_view_the_newsletter_sign_up_form(web_base_url, selenium):
    """Test the newsletter sign up form is available."""
    # GIVEN: a user viewing the blog page
    blog = Blog(selenium, web_base_url).open()

    # WHEN: they click on the "Sign Up" button
    sign_up = blog.get_newsletter()

    # THEN: the newsletter sign up form is displayed in the new tab
    assert(sign_up.is_displayed())
    assert('www2' in sign_up.location)


@test_case('C210403')
@nondestructive
@web
def test_able_to_retrieve_the_rss_feed(web_base_url, selenium):
    """Test the ability to download the raw OpenStax RSS feed."""
    # GIVEN: a user viewing the blog page
    blog = Blog(selenium, web_base_url).open()

    # WHEN: they click on the RSS icon
    rss = blog.test_rss_feed()

    # THEN: the XML feed is downloaded
    if not rss.ok:
        Utility.test_url_and_warn(code=rss.status_code,
                                  message='RSS feed')


@test_case('C210404')
@smoke_test
@nondestructive
@web
def test_each_blog_entry_has_an_image_title_excerpt_author_and_date(
        web_base_url, selenium):
    """Test for the attributes of each blog entry tile."""
    # GIVEN: a user viewing the blog page
    blog = Blog(selenium, web_base_url).open()

    # WHEN:

    # THEN: each tile has an image, a title, a text
    #       excerpt, one or more authors, and a date when
    #       the post was published
    for entry in blog.articles:
        assert(entry.image.is_displayed())
        assert(entry.title)
        assert(entry.excerpt)
        assert(entry.authors)
        assert(entry.date)


@test_case('C210405')
@nondestructive
@web
def test_load_a_blog_entry(web_base_url, selenium):
    """Test select a random blog entry to view the full article."""
    # GIVEN: a user viewing the blog page
    blog = Blog(selenium, web_base_url).open()

    # WHEN: they click on a linked resource
    article = blog.view_post()

    # THEN: the full article is displayed
    assert(article.is_displayed())
    assert(not article.location.endswith('/blog')), \
        'Still viewing the blog page ({url})'.format(url=article.location)


@test_case('C210406')
@nondestructive
@web
def test_disqus_loads_below_the_full_article(web_base_url, selenium):
    """Test Disqus's comment section loads below a full blog article."""
    # GIVEN: a user viewing a blog post
    blog = Blog(selenium, web_base_url).open()
    article = blog.view_post()

    # WHEN: they scroll below the body text
    article.view_comments()

    # THEN: the Disqus iframe is displayed
    assert(article.disqus.is_displayed())


@test_case('C210407')
@nondestructive
@web
def test_other_blog_entry_tiles_are_below_a_full_article(
        web_base_url, selenium):
    """Test for the presence of other blog tiles below a full article."""
    # GIVEN: a user viewing a blog post
    blog = Blog(selenium, web_base_url).open()
    article = blog.view_post()

    # WHEN: they scroll below the Disqus frame
    article.view_other_posts()

    # THEN: the other blog post tiles are displayed
    # AND:  the current blog post's tile is not displayed
    current_title = article.title
    for entry in article.other_posts:
        Utility.scroll_to(selenium, element=entry.root, shift=-80)
        assert(entry.is_displayed())
        assert(entry.title != current_title)
