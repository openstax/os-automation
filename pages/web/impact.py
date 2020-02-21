"""The Our Impact webpage."""

from pypom import Region
from selenium.webdriver.common.by import By

from pages.web.base import WebBase
from utils.utilities import Utility, go_to_
from utils.web import Web


class Section(Region):
    """A basic section of the Our Impact page."""

    _heading_locator = (By.CSS_SELECTOR, 'h1 , h2')
    _description_locator = (By.CSS_SELECTOR, 'h2 ~ div')

    @property
    def heading(self):
        """Return the section heading."""
        return self.find_element(*self._heading_locator).text

    @property
    def description(self):
        """Return the section description or sub-heading text."""
        return self.find_element(*self._description_locator).text


class OurImpact(WebBase):
    """The Our Impact page."""

    URL_TEMPLATE = '/impact'

    _section_locator = (By.CSS_SELECTOR, 'section')
    _backgrounds_locator = (By.CSS_SELECTOR, '#banner , #map')
    _images_locator = (By.CSS_SELECTOR, 'img')

    @property
    def loaded(self):
        """Return True when the background image and partner images load."""
        return (len(self.sections) == 12 and
                Utility.load_background_images(
                    driver=self.driver, locator=self._backgrounds_locator) and
                Utility.is_image_visible(
                    driver=self.driver, locator=self._images_locator))

    def is_displayed(self):
        """Return True if the heading statement is displayed."""
        return self.banner.heading

    @property
    def sections(self):
        """Return the section roots."""
        return self.find_elements(*self._section_locator)

    @property
    def banner(self):
        """Access the banner section."""
        return self.Banner(self, self.sections[Web.BANNER])

    @property
    def revolution(self):
        """Access the revolution section."""
        return self.Revolution(self, self.sections[Web.REVOLUTION])

    @property
    def founding(self):
        """Access the founding section."""
        return self.Founding(self, self.sections[Web.FOUNDING])

    @property
    def reach(self):
        """Access the reach section."""
        return self.Reach(self, self.sections[Web.REACH])

    @property
    def testimonials(self):
        """Access the testimonials section."""
        return self.Testimonials(self, self.sections[Web.TESTIMONIALS])

    @property
    def sustainability(self):
        """Access the sustainability section."""
        return self.Sustainability(self, self.sections[Web.SUSTAINABILITY])

    @property
    def disruption(self):
        """Access the disruption section."""
        return self.Disruption(self, self.sections[Web.DISRUPTION])

    @property
    def looking_ahead(self):
        """Access the looking ahead section."""
        return self.Ahead(self, self.sections[Web.LOOKING_AHEAD])

    @property
    def map(self):
        """Access the map section."""
        return self.Map(self, self.sections[Web.MAP])

    @property
    def tutor(self):
        """Access the Tutor Beta section."""
        return self.Tutor(self, self.sections[Web.OS_TUTOR])

    @property
    def partners(self):
        """Access the philanthropic section."""
        return self.Partners(self, self.sections[Web.PHILANTHROPIC_PARTNERS])

    @property
    def give(self):
        """Access the donation section."""
        return self.Give(self, self.sections[Web.DONATION])

    class Banner(Section):
        """The introductory section."""

        _description_locator = (By.CSS_SELECTOR, '[data-html=description] p')
        _give_locator = (By.CSS_SELECTOR, '[href$=give]')

        def give_today(self):
            """Click the 'Give today!' button."""
            button = self.find_element(*self._give_locator)
            Utility.click_option(self.driver, element=button)
            from pages.web.donation import Give
            return go_to_(Give(self.driver, self.page.base_url))

    class Revolution(Section):
        """On OpenStax direction and effect on education."""

        _letter_locator = (By.CSS_SELECTOR, '.text-block > p')
        _signature_locator = (By.CSS_SELECTOR, '.signature-image')
        _role_locator = (By.CSS_SELECTOR, '[data-html=signatureText] p')
        _picture_locator = (By.CSS_SELECTOR, 'img.hide-on-mobile')

        @property
        def description(self):
            """Return the body of the letter."""
            return self.letter

        @property
        def letter(self):
            """Return the body of the letter."""
            return ('\n'.join(
                paragraph.text
                for paragraph in self.find_elements(*self._letter_locator)))

        @property
        def signature(self):
            """Return the signature image."""
            return self.find_element(*self._signature_locator)

        @property
        def role(self):
            """Return the advisor's name and/or their role with OpenStax."""
            return ('\n'.join(
                line.text
                for line in self.find_elements(*self._role_locator)))

        @property
        def picture(self):
            """Return the advisor's portrait."""
            return self.find_element(*self._picture_locator)

    class Founding(Section):
        """The vision for OpenStax according to the founder."""

        _picture_locator = (By.CSS_SELECTOR, 'img')
        _name_locator = (By.CSS_SELECTOR, '.caption b')
        _role_locator = (By.CSS_SELECTOR, '.hide-on-mobile p:last-child')

        @property
        def picture(self):
            """Return the founder's portrait."""
            return self.find_element(*self._picture_locator)

        @property
        def name(self):
            """Return the founder's name."""
            line = self.find_element(*self._name_locator).text
            if line.endswith(','):
                return line[:-1]
            return line

        @property
        def role(self):
            """Return the founder's role."""
            return self.find_element(*self._role_locator).text

    class Reach(Section):
        """The reach of OpenStax materials."""

        _box_locator = (By.CSS_SELECTOR, '.fact-boxes .card')

        @property
        def boxes(self):
            """Access the stats boxes."""
            return [self.Box(self, root)
                    for root in self.find_elements(*self._box_locator)]

        @property
        def stats(self):
            """Return the group of stats."""
            return [box.stat for box in self.boxes]

        class Box(Region):
            """An information box."""

            _number_locator = (By.CSS_SELECTOR, '.card-header')
            _order_locator = (By.CSS_SELECTOR, '.smaller')
            _category_locator = (By.CSS_SELECTOR, 'div.card-header ~ div')

            @property
            def stat(self):
                """Return the combined stat line."""
                number = self.find_element(*self._number_locator).text,
                order = self.find_element(*self._order_locator).text,
                description = self.find_element(*self._category_locator).text
                return '{number}{order} {description}'.format(
                    number=number, order=order, description=description)

    class Testimonials(Section):
        """User testimonials."""

        _box_locator = (By.CSS_SELECTOR, '.testimonial-boxes')

        @property
        def testimonial(self):
            """Access the quote boxes."""
            return [self.Box(self, root)
                    for root in self.find_elements(*self._box_locator)]

        class Box(Region):
            """A quote box."""

            _picture_locator = (By.CSS_SELECTOR, 'img')
            _quote_locator = (By.CSS_SELECTOR, '.text-block > div')
            _link_locator = (By.CSS_SELECTOR, '.text-block > a')

            @property
            def picture(self):
                """Return the user's picture."""
                return self.find_element(*self._picture_locator)

            @property
            def quote(self):
                """Return the user's quote."""
                return self.find_element(*self._quote_locator).text

            def read_more(self):
                """Click on the 'Read more' link to view the blog entry."""
                link = self.find_element(*self._link_locator)
                Utility.click_option(self.driver, element=link)
                from pages.web.blog import Article
                return go_to_(Article(self.driver, self.page.page.base_url))

    class Sustainability(Section):
        """The sustainability of OpenStax ecosystems section."""

        _partner_locator = (By.CSS_SELECTOR, 'img')

        @property
        def partners(self):
            """Return a dictionary of partner names to logos."""
            return {company.get_attribute('alt'): company
                    for company in self.find_elements(*self._partner_locator)}

    class Disruption(Section):
        """The disruption in the book marketplace."""

        _cost_graph_locator = (By.CSS_SELECTOR, 'img')

        @property
        def cost_graph(self):
            """Return the cost graph image."""
            return self.find_element(*self._cost_graph_locator)

    class Ahead(Section):
        """Upcoming content from OpenStax."""

        _business_locator = (By.CSS_SELECTOR, '[href$=business]')
        _image_locator = (By.CSS_SELECTOR, 'img')

        def view_business_textbooks(self):
            """Click on the 'business textbooks' link to view the subject."""
            link = self.find_element(*self._business_locator)
            Utility.click_option(self.driver, element=link)
            from pages.web.subject import Subjects
            return go_to_(Subjects(self.driver, self.page.base_url))

        @property
        def image(self):
            """Return the future subjects image."""
            return self.find_element(*self._image_locator)

    class Map(Section):
        """Textbook usage in the world."""

        _demo_map_locator = (By.CSS_SELECTOR, 'img')
        _adoptions_locator = (By.CSS_SELECTOR, 'a')

        @property
        def demo_map(self):
            """Return the demo map image."""
            return self.find_element(*self._demo_map_locator)

        def view_adoptions(self):
            """Click on adoptions link."""
            link = self.find_element(*self._adoptions_locator)
            Utility.click_option(self.driver, element=link)
            from pages.web.adopters import Adopters
            return go_to_(Adopters(self.driver, self.page.base_url))

    class Tutor(Section):
        """About OpenStax Tutor Beta."""

        _demo_image_locator = (By.CSS_SELECTOR, '.right-image')
        _learn_more_locator = (By.CSS_SELECTOR, 'a')
        _bottom_image_locator = (By.CSS_SELECTOR, '.bottom-image')

        @property
        def demo_tutor(self):
            """Return the student Tutor demo image."""
            return self.find_element(*self._demo_image_locator)

        def learn_more_about_openstax_tutor_beta(self):
            """Click on the 'Learn more...' link."""
            link = self.find_element(*self._learn_more_locator)
            Utility.click_option(self.driver, element=link)
            from pages.web.tutor import TutorMarketing
            return go_to_(TutorMarketing(self.driver, self.page.base_url))

    class Partners(Section):
        """Philanthropic partners."""

        _advisor_locator = (By.CSS_SELECTOR, '.text-overlapping-photo')

        @property
        def advisors(self):
            """Access the OpenStax advisor blocks."""
            return [self.Advisor(self, advisor)
                    for advisor in self.find_elements(*self._advisor_locator)]

        class Advisor(Region):
            """An OpenStax advisor."""

            _picture_locator = (By.CSS_SELECTOR, 'img')
            _name_locator = (By.CSS_SELECTOR, '.name')
            _role_locator = (By.CSS_SELECTOR, '.title')
            _quote_locator = (By.CSS_SELECTOR,
                              '.big-orange-quote > div:not(.attribution)')

            @property
            def picture(self):
                """Return the advisor's headshot."""
                return self.find_element(*self._picture_locator)

            @property
            def name(self):
                """Return the advisor's name."""
                return self.find_element(*self._name_locator).text

            @property
            def role(self):
                """Return the advisor's role and position."""
                return self.find_element(*self._role_locator).text

            @property
            def quote(self):
                """Return the advisor's quote."""
                return self.find_element(*self._quote_locator).text

    class Give(Section):
        """Donate to OpenStax."""

        _give_locator = (By.CSS_SELECTOR, '[href$=give]')

        def give_today(self):
            """Click on the 'Give today!' button."""
            button = self.find_element(*self._give_locator)
            Utility.click_option(self.driver, element=button)
            from pages.web.donation import Give
            return go_to_(Give(self.driver, self.page.base_url))
