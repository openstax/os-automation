"""Test user accounts for testing."""

import pytest

__all__ = ['student', 'teacher', 'admin', 'content',
           'salesforce',
           'facebook', 'facebook_signup',
           'google', 'google_signup']


@pytest.fixture(scope='module')
def student(request):
    """Set the student user information."""
    return _data_return(request, 'student')


@pytest.fixture(scope='module')
def teacher(request):
    """Set the instructor user information."""
    return _data_return(request, 'teacher')


@pytest.fixture(scope='module')
def admin(request):
    """Set the administrative user information."""
    return _data_return(request, 'admin')


@pytest.fixture(scope='module')
def content(request):
    """Set the content user information."""
    return _data_return(request, 'content')


@pytest.fixture(scope='module')
def salesforce(request):
    """Set the Salesforce user information."""
    return _data_return(request, 'salesforce')


@pytest.fixture(scope='module')
def facebook(request):
    """Set the Facebook user information."""
    return _data_return(request, 'facebook')


@pytest.fixture(scope='module')
def facebook_signup(request):
    """Set the Facebook user email information."""
    return _data_return(request, 'facebook_signup')


@pytest.fixture(scope='module')
def google(request):
    """Set the Google user information."""
    return _data_return(request, 'google')


@pytest.fixture(scope='module')
def google_signup(request):
    """Set the Google Gmail user information."""
    return _data_return(request, 'google_signup')


def _data_return(request, target):
    """Retrieve user account information from the environment file."""
    config = request.config
    user = (config.getoption(target) or config.getini(target))
    return (user[0], user[1])
