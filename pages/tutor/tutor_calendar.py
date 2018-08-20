"""The main calendar page for both student and teacher."""

from pypom import Region

from pages.tutor.base import TutorBase


class TutorCalendar(TutorBase):
    """Tutor course page."""

    @property
    def calendar(self):
        """Access the instructor calendar."""
        return self.TeacherCalendar(self.driver)

    @property
    def nav(self):
        """Return the nav region."""
        from regions.tutor.nav import TutorNav
        return TutorNav(self)

    class TeacherCalendar(Region):
        """Tutor calendar page object."""

        pass
