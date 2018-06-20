"""Test the Tutor teacher performance forecast functions."""

from tests.markers import expected_failure, nondestructive, test_case, tutor


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_view_period_performance_forecast(tutor_base_url, selenium, teacher):
    """View performance forecast page."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: Click on "Performance Forecast" in the user menu
    # AND: Click on the desired period

    # THEN: The period Performance Forecast is presented to the user


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_performance_forecast_info_icon(tutor_base_url, selenium, teacher):
    """View info icon in performance forecast page."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: Click on "Performance Forecast" in the user menu
    # AND: Hover the cursor over the info icon

    # THEN: Info icon shows an explanation of the data


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_view_the_performance_color_key(tutor_base_url, selenium, teacher):
    """View performance color key in performance forecast page."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: Click on "Performance Forecast" in the user menu

    # THEN: The performance color key is presented to the user


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_period_tabs_are_shown(tutor_base_url, selenium, teacher):
    """Check period tabs in performance forecast page."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course
    # AND: Has more than one period

    # WHEN: Click on "Performance Forecast" in the user menu

    # THEN: The period tabs are shown to the user


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_period_with_zero_answers(tutor_base_url, selenium, teacher):
    """Check that a period with no answers doesn't show section breakdowns."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course
    # AND: Has a period that hasn't answered assignments

    # WHEN: Click on "Performance Forecast" in the user menu
    # AND: Click on the period with zero answers

    # THEN: The user should see no section breakdowns and the message:
    # "There have been no questions worked for this period."


@expected_failure
@nondestructive
@test_case('')
@tutor
def test_perforemance_forecast_weaker_areas(tutor_base_url, selenium, teacher):
    """Check weaker areas show up to four problematic sections."""
    # GIVEN: Logged into Tutor as a teacher
    # AND: Has an existing course

    # WHEN: Click on "Performance Forecast" in the user menu
    # AND: Click on the desired period

    # THEN: Weaker Areas show up to four problematic sections
