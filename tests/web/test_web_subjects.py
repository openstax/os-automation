
@test_case('')
@web
def test_get_book_links(web_base_url, selenium):
    """Tests ability to view get book links."""
    
    # GIVEN: On the OpenStax homepage

    # WHEN: Select a subject 

    # AND: Select a textbook

    # THEN: Table of contents, view online download pdf present

    # AND: Download for kindle, Order a print copy, Bookshare, Download for iBooks can be present


@test_case('')
@web
def test_textbook_table_of_contents(web_base_url, selenium):
    """Tests ability to view textbook table of contents."""
    
    # GIVEN: On the OpenStax homepage

    # WHEN: Go to Subjects - Science

    # AND: Select Biology

    # AND: Click "Table of contents"

    # THEN: The entire list of table of contents of the textbook should be visible


@test_case('')
@web
def test_view_textbook_online(web_base_url, selenium):
    """Tests ability to view textbook online."""
    
    # GIVEN: On the OpenStax homepage

    # WHEN: Go to Subjects - Science

    # AND: Select Biology

    # AND: Click "view online"

    # THEN: A new tab is opened, displaying the content of the textbook, in the original page, a donation banner is shown


@test_case('')
@web
def test_textbook_pdf_download(web_base_url, selenium):
    """Tests ability to download math pdf."""
    
    # GIVEN: On the OpenStax homepage

    # WHEN: Go to Subjects - Science

    # AND: Select Biology

    # AND: Click "Download as pdf"

    # THEN: A pdf version of the textbook is downloaded


@test_case('')
@web
def test_order_print(web_base_url, selenium):
    """Tests ability to order print copy."""
    
    # GIVEN: On the OpenStax homepage

    # WHEN: Go to Subjects - Science

    # AND: Select Biology

    # AND: Click "order a print copy"

    # THEN: A small window pops up. Clicking "order on amazon" takes user to the amazon page


@test_case('')
@web
def test_kindle_download(web_base_url, selenium):
    """Tests ability to download kindle version."""
    
    # GIVEN: On the OpenStax homepage

    # WHEN: Go to Subjects - Science

    # AND: Select Biology

    # AND: Click "Download for Kindle"

    # THEN: User is taken to amazon kindle book purchase page


@test_case('')
@web
def test_bookshare_download(web_base_url, selenium):
    """Tests ability to download bookshare version."""
    
    # GIVEN: On the OpenStax homepage

    # WHEN: Go to Subjects - Science

    # AND: Select Biology

    # AND: Click "BookShare"

    # THEN: User is taken to bookshare purchase page


@test_case('')
@web
def test_ibook_download(web_base_url, selenium):
    """Tests ability to download iBook version."""
    
    # GIVEN: On the OpenStax homepage

    # WHEN: Go to Subjects - Science

    # AND: Select Biology

    # AND: Click "Download for iBooks"

    # THEN: User is taken to itunes book purchase page"


@test_case('')
@web
def test_textbook_summary_visible(web_base_url, selenium):
    """Tests visibility of textbook summary."""
    
    # GIVEN: On the OpenStax homepage

    # WHEN: go to a random subject

    # AND: Click on a textbook

    # THEN: Summary of the textbook is visible


@test_case('')
@web
def test_textbook_author_visible(web_base_url, selenium):
    """Tests visibility of textbook author."""
    
    # GIVEN: On the OpenStax homepage

    # WHEN: go to a random subject

    # AND: Click on a textbook

    # THEN: Author of the textbook is visible


@test_case('')
@web
def test_textbook_errata_visible(web_base_url, selenium):
    """Tests visibility of errata list."""
    
    # GIVEN: On the OpenStax homepage

    # WHEN: go to a random subject

    # AND: Click on a textbook

    # AND: Click "Errata List"

    # THEN: An Errata List is visible


@test_case('')
@web
def test_textbook_isbn_visible(web_base_url, selenium):
    """Tests visibility of isbn."""
    
    # GIVEN: On the OpenStax homepage

    # WHEN: go to a random subject

    # AND: Click on a textbook
    
    # THEN: ISBN of the textbook is visible


@test_case('')
@web
def test_textbook_license_visible(web_base_url, selenium):
    """Tests visibility of license."""
    
    # GIVEN: On the OpenStax homepage

    # WHEN: go to a random subject

    # AND: Click on a textbook
    
    # THEN: License of the textbook is visible 


@test_case('')
@web
def test_textbook_signup(web_base_url, selenium):
    """Tests textbook signup to learn more button."""
    
    # GIVEN: On the OpenStax homepage

    # WHEN: go to a random subject

    # AND: Click on a textbook
    
    # AND: Click "Sign up to learn more"

    # AND: Fill out the personal information

    # THEN: User is taken to a "Thank user" page


@test_case('')
@web
def test_instructor_resources(web_base_url, selenium):
    """Tests ability to download instructor resources."""
    
    # GIVEN: On the OpenStax homepage

    # WHEN: go to a random subject

    # AND: Click on a textbook

    # AND: Click "instructor resources"

    # AND: Click on a instructor resource visible and try to download it

    # THEN: User is able to download resources marked with green download sign

    # AND: User is unable to download resources marked with ""lock"" sign 

    # AND: User is prompt to log in if trying to download resources marked with ""lock"" sign


@test_case('')
@web
def test_student_resources(web_base_url, selenium):
    """Tests ability to download student resources."""
    
    # GIVEN: On the OpenStax homepage

    # WHEN: go to a random subject

    # AND: Click on a textbook

    # AND: Click student resources

    # AND: Select a visible resource and try to download it

    # THEN: User is able to download resources marked with green download sign

    # AND: User is unable to download resources marked with ""lock"" sign 

    # AND: User is prompt to log in if trying to download resources marked with ""lock"" sign