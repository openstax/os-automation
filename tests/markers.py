"""Pytest markers for OpenStax test cases."""

import pytest
from pytest_testrail.plugin import pytestrail

nondestructive = pytest.mark.nondestructive
parameters = pytest.mark.parametrize

accounts = pytest.mark.accounts
biglearn = pytest.mark.biglearn
exercises = pytest.mark.exercises
hypothesis = pytest.mark.hypothesis
payments = pytest.mark.payments
tutor = pytest.mark.tutor
web = pytest.mark.web

smoke_test = pytest.mark.smoke_test
test_case = pytestrail.case

expected_failure = pytest.mark.xfail
skip_test = pytest.mark.skip
social = pytest.mark.social
