
@test_case('')
@web
def test_view_home(web_base_url, selenium):
    """Tests ability view homepage from other pages."""
    
    # GIVEN: On the OpenStax homepage

    # WHEN: Click "About Us"

    # AND: Click the OpenStax logo on the upper left corner

    # THEN: On homepage