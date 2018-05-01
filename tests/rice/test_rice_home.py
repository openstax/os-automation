"""Rice model stub."""
import pytest

from pages.rice.home import Rice


@pytest.mark.nondestructive
def test_at_rice(base_url, selenium):
    """Return True if at Rice's webpage."""
    page = Rice(selenium, base_url).open()
    assert(page.at_rice), 'Not at the Rice University homepage'
