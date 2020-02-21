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
    if instance == 'unique':
        return base_url
    if instance and base_url:
        segments = base_url.split(SPLIT)
        insert = '' if instance.startswith('prod') else f'-{instance}.'
        return '{0}{2}{3}{1}'.format(*segments, SPLIT, insert)
    if base_url is not None:
        return base_url
