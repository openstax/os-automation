"""Rice model stub."""

from pages.rice.home import Rice
from tests.markers import nondestructive, support, test_case


@test_case('C195133')
@nondestructive
@support
def test_at_rice(selenium):
    """Return True if at Rice's webpage."""
    page = Rice(selenium).open()
    assert(page.at_rice), 'Not at the Rice University homepage'
