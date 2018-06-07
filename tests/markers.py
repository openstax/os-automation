"""Pytest markers for OpenStax test cases."""

import pytest
from pytest_testrail.plugin import pytestrail

nondestructive = pytest.mark.nondestructive
accounts = pytest.mark.accounts
exercises = pytest.mark.exercises
payments = pytest.mark.payments
tutor = pytest.mark.tutor
web = pytest.mark.web

test_case = pytestrail.case

expected_failure = pytest.mark.xfail
social = pytest.mark.social
