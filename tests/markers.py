"""Pytest markers for OpenStax test cases."""

import pytest
from pytest_testrail.plugin import pytestrail

accounts = pytest.mark.accounts
biglearn = pytest.mark.biglearn
exercises = pytest.mark.exercises
payments = pytest.mark.payments
support = pytest.mark.support
tutor = pytest.mark.tutor
web = pytest.mark.web

expected_failure = pytest.mark.xfail
nondestructive = pytest.mark.nondestructive
parameters = pytest.mark.parametrize
skip_if_headless = pytest.mark.skip_if_headless
skip_test = pytest.mark.skip
smoke_test = pytest.mark.smoke_test
social = pytest.mark.social
test_case = pytestrail.case
