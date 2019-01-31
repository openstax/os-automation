"""OpenStax Web fixtures."""

import pytest

__all__ = ['web_base_url']
SPLIT = 'openstax'


@pytest.fixture(scope='session')
def web_base_url(request):
    """Return a base URL for OpenStax Web."""
    config = request.config
    base_url = (config.getoption('web_base_url') or
                config.getini('web_base_url'))
    instance = (config.getoption('instance') or
                config.getini('instance')).lower()
    if instance and base_url:
        segments = base_url.split(SPLIT)
        insert = ('' if instance.startswith('prod') else
                  'cms-{instance}.'.format(instance=instance))
        return '{0}{3}{2}{1}'.format(*segments, SPLIT, insert)
    if base_url is not None:
        return base_url
