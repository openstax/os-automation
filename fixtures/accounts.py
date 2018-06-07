"""OpenStax Accounts fixtures."""

import pytest

__all__ = ['accounts_base_url']
SPLIT = 'accounts'


@pytest.fixture(scope='session')
def accounts_base_url(request):
    """Return a base URL for OpenStax Accounts."""
    config = request.config
    base_url = (config.getoption('accounts_base_url') or
                config.getini('accounts_base_url'))
    instance = (config.getoption('instance') or
                config.getini('instance'))
    if instance and base_url:
        segments = base_url.split(SPLIT)
        return '{0}{3}-{2}{1}'.format(*segments, instance, SPLIT)
    if base_url is not None:
        return base_url
