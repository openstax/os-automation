"""OpenStax Exercises fixtures."""

import pytest

__all__ = ['exercises_base_url']
SPLIT = 'exercises'


@pytest.fixture(scope='session')
def exercises_base_url(request):
    """Return a base URL for OpenStax Exercises."""
    config = request.config
    base_url = (config.getoption('exercises_base_url') or
                config.getini('exercises_base_url'))
    instance = (config.getoption('instance') or
                config.getini('instance')).lower()
    if instance == 'unique':
        return base_url
    if instance and base_url:
        segments = base_url.split(SPLIT)
        insert = ('' if instance.startswith('prod') else f'-{instance}')
        return '{0}{2}{3}{1}'.format(*segments, SPLIT, insert)
    if base_url is not None:
        return base_url
