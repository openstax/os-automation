"""Test user accounts for testing."""

import pytest

__all__ = ['student', 'teacher', 'admin', 'content',
           'salesforce', 'facebook', 'google', 'gmail']


@pytest.fixture(scope='module')
def student(request):
    """Setup the student user information."""
    return _data_return(request, 'student')


@pytest.fixture(scope='module')
def teacher(request):
    """Setup the instructor user information."""
    return _data_return(request, 'teacher')


@pytest.fixture(scope='module')
def admin(request):
    """Setup the administrative user information."""
    return _data_return(request, 'admin')


@pytest.fixture(scope='module')
def content(request):
    """Setup the content user information."""
    return _data_return(request, 'content')


@pytest.fixture(scope='module')
def salesforce(request):
    """Setup the Salesforce user information."""
    return _data_return(request, 'salesforce')


@pytest.fixture(scope='module')
def facebook(request):
    """Setup the Facebook user information."""
    return _data_return(request, 'facebook')


@pytest.fixture(scope='module')
def google(request):
    """Setup the Facebook user information."""
    return _data_return(request, 'google')


@pytest.fixture(scope='module')
def gmail(request):
    """Setup the Facebook user information."""
    return _data_return(request, 'gmail')


def _data_return(request, target):
    """Data retrival helper for user account information."""
    config = request.config
    user = (config.getoption(target) or config.getini(target))
    return (user[0], user[1])
