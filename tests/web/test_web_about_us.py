
@test_case('')
@web
def test_view_about_us(web_base_url, selenium):
    """Tests ability go to about us page."""
    
    # GIVEN: On the OpenStax homepage

    # WHEN: Click "About Us"

    # THEN: User is on the about us page


@test_case('')
@web
def test_view_about_us_hyperlinks(web_base_url, selenium):
    """Tests hyperlinks are present in about us page."""
    
    # GIVEN: On the OpenStax homepage

    # WHEN: Click "About Us"

    # THEN: Hyperlinks in about us are present


@test_case('')
@web
def test_view_team_members(web_base_url, selenium):
    """Tests ability to view team members."""
    
    # GIVEN: On the OpenStax homepage

    # WHEN: Click "About Us"

    # THEN: Click a team member photo, a window will appear on top with the introduction

    # AND: Click the x and the window introduction will close