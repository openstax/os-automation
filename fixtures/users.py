"""Test user accounts for testing."""

import pytest

__all__ = ['student', 'teacher', 'admin', 'content',
           'salesforce', 'facebook', 'google', 'gmail']


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
def google(request):
    """Set the Facebook user information."""
    return _data_return(request, 'google')


@pytest.fixture(scope='module')
def gmail(request):
    """Set the Facebook user information."""
    return _data_return(request, 'gmail')


def _data_return(request, target):
    """Retrieve user account information from the environment file."""
    config = request.config
    user = (config.getoption(target) or config.getini(target))
    return (user[0], user[1])
