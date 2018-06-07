"""OpenStax Tutor fixtures."""

import pytest

__all__ = ['tutor_base_url']
SPLIT = 'tutor'


@pytest.fixture(scope='session')
def tutor_base_url(request):
    """Return a base URL for OpenStax Tutor."""
    config = request.config
    base_url = (config.getoption('tutor_base_url') or
                config.getini('tutor_base_url'))
    instance = (config.getoption('instance') or
                config.getini('instance')).lower()
    if instance and base_url:
        segments = base_url.split(SPLIT)
        return '{0}{3}-{2}{1}'.format(*segments, instance, SPLIT)
    if base_url is not None:
        return base_url
