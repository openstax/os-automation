
@test_case('')
@web
def test_edit_higher_ed_page(web_base_url, seleniumm, admin):
    """Tests ability to edit higher education page."""

    # GIVEN: Logged into the website content management system as a admin

    # WHEN: Click on the explorer tab

    # AND: Click on Openstax Homepage

    # AND: Click on Higher Education to edit

    # THEN: The content input on the cms will show up on the higher ed page


@test_case('')
@web
def test_edit_partner_page(web_base_url, seleniumm, admin):
    """Tests ability to edit partner page."""

    # GIVEN: Logged into the website content management system as a admin

    # WHEN: Go to Openstax homepage/admin

    # AND: Click Explorer

    # AND: Click OpenStax Homepage

    # AND: Click on OpenStax Partners

    # AND: Fill in required fields and click publish

    # THEN: Admin has the page show up with the content inputed from the CMS


@test_case('')
@web
def test_edit_support_page(web_base_url, seleniumm, admin):
    """Tests ability to edit support page."""

    # GIVEN: Logged into the website content management system as a admin

    # WHEN: Go to Openstax homepage/admin

    # AND: Click Explorer

    # AND: Click OpenStax Homepage

    # AND: Click on OpenStax Support

    # AND: Fill in required fields and click publish

    # THEN: Support page is updated with CMS content


@test_case('')
@web
def test_edit_add_books(web_base_url, seleniumm, admin):
    """Tests ability to edit or add books."""

    # GIVEN: Logged into the website content management system as a admin

    # WHEN: Go to Openstax homepage/admin

    # AND: Click the log in button

    # AND:Click Explorer

    # AND: Click arrow next to OpenStax Homepage

    # AND: Click on Subjects

    # AND: Click on the book user want updated

    # AND: Enter SalesForce Name and SalesForce Abbreviation

    # Click publish

    # THEN: Book titles show up properly in the drop down of forms