"""OpenStax Tutor Payments fixtures."""

import pytest

__all__ = ['payments_base_url']
SPLIT = 'payments'


@pytest.fixture(scope='session')
def payments_base_url(request):
    """Return a base URL for OpenStax Tutor Payments."""
    config = request.config
    base_url = (config.getoption('payments_base_url') or
                config.getini('payments_base_url'))
    instance = (config.getoption('instance') or
                config.getini('instance')).lower()
    if instance and base_url:
        segments = base_url.split(SPLIT)
        return '{0}{3}-{2}{1}'.format(*segments, instance, SPLIT)
    if base_url is not None:
        return base_url