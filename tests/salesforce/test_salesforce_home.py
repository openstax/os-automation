"""Salesforce model stub."""
import pytest
from pytest_testrail.plugin import testrail

from pages.salesforce.home import Salesforce


@testrail('C195134')
@pytest.mark.nondestructive
def test_at_rice(base_url, selenium):
    """Return True if at the OpenStax Salesforce help webpage."""
    page = Salesforce(selenium, base_url).open()
    assert(page.at_salesforce), 'Not at the Salesforce help page'
