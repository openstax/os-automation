"""Salesforce model stub."""

from pages.salesforce.home import Salesforce
from tests.markers import nondestructive, support, test_case


@test_case('C195134')
@nondestructive
@support
def test_at_salesforce(selenium):
    """Return True if at the OpenStax Salesforce help webpage."""
    page = Salesforce(selenium).open()
    assert(page.at_salesforce), 'Not at the Salesforce help page'
