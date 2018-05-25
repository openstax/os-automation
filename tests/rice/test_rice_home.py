"""Rice model stub."""
import pytest
from pytest_testrail.plugin import pytestrail

from pages.rice.home import Rice


@pytestrail.case('C195133')
@pytest.mark.nondestructive
def test_at_rice(base_url, selenium):
    """Return True if at Rice's webpage."""
    page = Rice(selenium, base_url).open()
    assert(page.at_rice), 'Not at the Rice University homepage'
