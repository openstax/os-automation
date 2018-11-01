"""OpenStax Web globals."""

import re

from utils.utilities import Utility


class Web(object):
    """Website shared variables."""

    # Sizing
    PHONE = 601
    TABLET = 961

    # RegEx matchers
    FILENAME_MATCHER = re.compile(r'url\([\w\-\:\/\.]*\)\;')

    # Web banner carousel options
    FREE_BOOKS_NO_CATCH = 0
    EDUCATION_OVER_PROFIT = 1
    ACADEMIC_FREEDOM = 2
    _29_BOOKS = 3

    # Quotes
    SUBSCRIBE = 0
    BOOK_QUALITY_RIGGS = 1
    BOOKSTORE_SUPPLIERS = 2

    # Home page boxes
    BOOKS = 0
    TECH = 1
    OUR_IMPACT = 0
    OPENSTAX_PARTNERS = 1

    # Book page tabs
    BOOK_DETAILS = 0
    INSTRUCTOR_RESOURCES = 1
    PARTNER_RESOURCES = 2
    STUDENT_RESOURCES = 3

    # Book page order modals
    INDIVIDUAL = 0
    BOOKSTORES = 1

    # Matching strings
    ABOUT = 'about'
    BOOKSTORE = 'bookstore-suppliers'
    GIVE = 'give'
    IMPACT = 'impact'
    NEWSLETTER = 'www2.openstax.org'
    NO_FILTER = 'View All'
    PARTNERS = 'partners'
    RESEARCH = 'research'
    SUBJECTS = 'subjects'
    TECHNOLOGY = 'technology'
    TUTOR = 'openstax-tutor'

    # Menus
    VIEW_ALL = 'All'
    VIEW_MATH = 'Math'
    VIEW_SCIENCE = 'Science'
    VIEW_SOCIAL_SCIENCES = 'Social Sciences'
    VIEW_HUMANITIES = 'Humanities'
    VIEW_BUSINESS = 'Business'
    VIEW_AP = 'AP®'
    VIEW_TECHNOLOGY = 'Technology Options'
    VIEW_TUTOR = 'About OpenStax Tutor'
    VIEW_PARTNERS = 'OpenStax Partners'
    VIEW_ABOUT_US = 'About Us'
    VIEW_TEAM = 'Team'
    VIEW_RESEARCH = 'Research'

    # User types
    STUDENT = 'Student'
    INSTRUCTOR = 'Faculty'
    ADMINISTRATOR = 'Administrator'
    LIBRARIAN = 'Librarian'
    DESIGNER = 'Instructional Designer'
    HOMESCHOOL = 'Home School Teacher'
    ADJUNCT = 'Adjunct Faculty'
    OTHER = 'Other'

    USERS = [
        STUDENT,
        INSTRUCTOR,
        ADMINISTRATOR,
        LIBRARIAN,
        DESIGNER,
        HOMESCHOOL,
        ADJUNCT,
        OTHER
    ]

    # Adoption or interest status
    ADOPTED = 'Confirmed Adoption Won'
    RECOMMENDED = 'Confirmed Will Recommend'

    USING_STATUS = [
        ADOPTED,
        RECOMMENDED
    ]

    STUDENT_MIN = 1
    STUDENT_MAX = 999

    # Expected lists
    ACCESSIBILITY = [
        'Accessibility',
        'Web Accessibility',
        'Our progress',
        'Feedback',
        'Interactive Simulations',
        'User-Contributed Content'
    ]
    URL_APPENDS = [
        'math',
        'science',
        'social-sciences',
        'humanities',
        'business',
        'ap'
    ]
    FILTERS = [
        VIEW_MATH,
        VIEW_SCIENCE,
        VIEW_SOCIAL_SCIENCES,
        VIEW_HUMANITIES,
        VIEW_BUSINESS,
        VIEW_AP
    ]
    MENU_SUBJECTS = [
        VIEW_ALL,
        *FILTERS
    ]
    MENU_TECHNOLOGY = [
        VIEW_TECHNOLOGY,
        VIEW_TUTOR,
        VIEW_PARTNERS
    ]
    MENU_WHAT_WE_DO = [
        VIEW_ABOUT_US,
        VIEW_TEAM,
        VIEW_RESEARCH
    ]


class TechProviders():
    """Adoption and interest technology providers."""

    AMBASSADOR = 'Ambassador'
    BARNES_AND_NOBLE = 'Barnes & Noble Education'
    BLENDING_EDUCATION = 'Blending Education'
    BLUPOINT = 'BluPoint'
    CARNEGIE = 'Carnegie Learning'
    CAROLINA_LEARNING = 'Carolina Distance Learning'
    CHEGG = 'Chegg'
    CHEGG_STUDY = 'Chegg Study'
    CHEGG_TUTORS = 'Chegg Tutors'
    CHEM101 = 'Chem101'
    CLASSAVO = 'Classavo'
    COGBOOKS = 'CogBooks'
    CONNECT = 'Connect For Education'
    COPIA = 'Copia'
    EMATH = 'eMath'
    EXPERT_TA = 'Expert TA'
    EXPERT_TA_ASSESS = 'Expert TA Assess'
    EXPERT_TA_STUDY = 'Expert TA Study'
    GRAPHLOCK = 'GraphLock'
    JUNCTION = 'Junction'
    KNEWTON = 'Knewton'
    LRNR = 'Lrnr'
    MCGRAW_HILL = 'McGraw-Hill Education'
    MEMORY_SCIENCE = 'Memory Science'
    ODIGIA = 'Odigia'
    TUTOR = 'OpenStax Tutor Beta'
    PANOPEN = 'panOpen'
    PERLEGO = 'Perlego'
    PERUSALL = 'Perusall'
    REALIZEIT = 'Realizeit'
    RICE_ONLINE = 'Rice Online Learning'
    SAPLING = 'Sapling Learning'
    SIMBIO = 'SimBio'
    TOP_HAT = 'Top Hat'
    VISIBLE_BODY = 'Visible Body'
    WEBASSIGN = 'WebAssign'
    WILEY = 'Wiley'
    XYZ = 'XYZ Homework'
    ZYBOOKS = 'zyBooks'
    OTHER = 'Other (specify below)'

    tech_list = [
        AMBASSADOR, BARNES_AND_NOBLE, BLENDING_EDUCATION, BLUPOINT,
        CARNEGIE, CAROLINA_LEARNING, CHEGG, CHEGG_STUDY, CHEGG_TUTORS,
        CHEM101, CLASSAVO, COGBOOKS, CONNECT, COPIA, EMATH, EXPERT_TA,
        EXPERT_TA_ASSESS, EXPERT_TA_STUDY, GRAPHLOCK, JUNCTION, KNEWTON,
        LRNR, MCGRAW_HILL, MEMORY_SCIENCE, ODIGIA, TUTOR, PANOPEN, PERLEGO,
        PERUSALL, REALIZEIT, RICE_ONLINE, SAPLING, SIMBIO, TOP_HAT,
        VISIBLE_BODY, WEBASSIGN, WILEY, XYZ, ZYBOOKS, OTHER
    ]

    @classmethod
    def get_tech(self, number=1):
        """Return a subset of the tech list for the forms."""
        return Utility.random_set(self.tech_list, number)


class Library():
    """OpenStax book library."""

    # Business
    ETHICS = 'Business Ethics'
    BUSINESS = 'Introduction to Business'

    # Humanities
    US_HISTORY = 'U.S. History'

    # Math
    ALGEBRA_TRIG = 'Algebra and Trigonometry'
    CALCULUS_1 = 'Calculus Volume 1'
    CALCULUS_2 = 'Calculus Volume 2'
    CALCULUS_3 = 'Calculus Volume 3'
    ALGEBRA = 'College Algebra'
    ELEM_ALGEBRA = 'Elementary Algebra'
    INTER_ALGEBRA = 'Intermediate Algebra'
    BUSINESS_STATS = 'Introductory Business Statistics'
    INTRO_STATS = 'Introductory Statistics'
    PREALGEBRA = 'Prealgebra'
    PRECALCULUS = 'Precalculus'

    # Science
    ANATOMY_PHYS = 'Anatomy and Physiology'
    ASTRONOMY = 'Astronomy'
    BIOLOGY = 'Biology'
    BIOLOGY_2E = 'Biology 2e'
    AP_BIO = 'Biology for AP® Courses'
    CHEMISTRY = 'Chemistry'
    CHEM_ATOMS = 'Chemistry: Atoms First'
    PHYSICS = 'College Physics'
    AP_PHYS = 'The AP Physics Collection'
    BIO_CONCEPTS = 'Concepts of Biology'
    FIZYKA_1 = 'Fizyka dla szkół wyższych. Tom 1'
    FIZYKA_2 = 'Fizyka dla szkół wyższych. Tom 2'
    FIZYKA_3 = 'Fizyka dla szkół wyższych. Tom 3'
    MICROBIOLOGY = 'Microbiology'
    U_PHYS_1 = 'University Physics Volume 1'
    U_PHYS_2 = 'University Physics Volume 2'
    U_PHYS_3 = 'University Physics Volume 3'

    # Social Sciences
    GOVERNMENT = 'American Government'
    SOCIOLOGY = 'Introduction to Sociology 2e'
    PRINCIPLES_ECON = 'Principles of Economics 2e'
    PRINCIPLES_MACRO = 'Principles of Macroeconomics 2e'
    AP_MACRO = 'Principles of Macroeconomics for AP® Courses 2e'
    PRINCIPLES_MICRO = 'Principles of Microeconomics 2e'
    AP_MICRO = 'Principles of Microeconomics for AP® Courses 2e'
    PSYCHOLOGY = 'Psychology'

    # Fields and limiters
    ADOPTION = 'interest'
    ALL_BOOKS = 'all'
    BOOKSHARE = 'bookshare'
    CATEGORY = 'subject'
    CURRENT = 'current'
    DETAILS = 'details'
    ENGLISH = 'English'
    INTEREST = ADOPTION
    IS_AP = 'is_ap?'
    ITUNES = 'itunes'
    KINDLE = 'kindle'
    LANGUAGE = 'language'
    OPENSTAX = 'openstax'
    POLISH = 'Polish'
    SHORT_NAME = 'short_name'
    SUPERSEDED = 'not_current'

    # Subjects
    ALL = 'View All'
    AP = 'AP®'
    BUSINESS = 'Business'
    HUMANITIES = 'Humanities'
    MATH = 'Math'
    SCIENCE = 'Science'
    SOCIAL = 'Social Sciences'

    OLD_EDITIONS = [
        BIOLOGY
    ]

    def __init__(self):
        """Initialize the library."""
        self._books = {

            # Business
            self.ETHICS: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.BUSINESS],
                self.DETAILS: 'business-ethics',
                self.INTEREST: 'Business%20Ethics',
                self.IS_AP: False,
                self.ITUNES: False,
                self.KINDLE: False,
                self.LANGUAGE: self.ENGLISH,
                self.SHORT_NAME: 'Business Ethics', },
            self.BUSINESS: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.BUSINESS],
                self.DETAILS: 'introduction-business',
                self.INTEREST: 'Intro%20to%20Business',
                self.IS_AP: False,
                self.ITUNES: False,
                self.KINDLE: False,
                self.LANGUAGE: self.ENGLISH,
                self.SHORT_NAME: 'Introduction to Business', },

            # Humanities
            self.US_HISTORY: {
                self.BOOKSHARE: True,
                self.CATEGORY: [self.ALL, self.HUMANITIES],
                self.DETAILS: 'us-history',
                self.INTEREST: 'US%20History',
                self.IS_AP: False,
                self.ITUNES: True,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.SHORT_NAME: 'U.S. History', },

            # Math
            self.ALGEBRA_TRIG: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.MATH],
                self.DETAILS: 'algebra-and-trigonometry',
                self.INTEREST: 'Algebra%20and%20Trigonometry',
                self.IS_AP: False,
                self.ITUNES: False,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.SHORT_NAME: 'Algebra and Trigonometry', },
            self.CALCULUS_1: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.MATH],
                self.DETAILS: 'calculus-volume-1',
                self.INTEREST: 'Calculus',
                self.IS_AP: False,
                self.ITUNES: False,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.SHORT_NAME: 'Calculus', },
            self.CALCULUS_2: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.MATH],
                self.DETAILS: 'calculus-volume-2',
                self.INTEREST: 'Calculus',
                self.IS_AP: False,
                self.ITUNES: False,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.SHORT_NAME: 'Calculus', },
            self.CALCULUS_3: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.MATH],
                self.DETAILS: 'calculus-volume-3',
                self.INTEREST: 'Calculus',
                self.IS_AP: False,
                self.ITUNES: False,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.SHORT_NAME: 'Calculus', },
            self.ALGEBRA: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.MATH],
                self.DETAILS: 'college-algebra',
                self.INTEREST: 'College%20Algebra',
                self.IS_AP: False,
                self.ITUNES: False,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.SHORT_NAME: 'College Algebra', },
            self.ELEM_ALGEBRA: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.MATH],
                self.DETAILS: 'elementary-algebra',
                self.INTEREST: 'Elementary%20Algebra',
                self.IS_AP: False,
                self.ITUNES: False,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.SHORT_NAME: 'Elementary Algebra', },
            self.INTER_ALGEBRA: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.MATH],
                self.DETAILS: 'intermediate-algebra',
                self.INTEREST: 'Intermediate%20Algebra',
                self.IS_AP: False,
                self.ITUNES: False,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.SHORT_NAME: 'Intermediate Algebra', },
            self.BUSINESS_STATS: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.MATH],
                self.DETAILS: 'introductory-business-statistics',
                self.INTEREST: 'Business%20Statistics',
                self.IS_AP: False,
                self.ITUNES: False,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.SHORT_NAME: 'Introductory Business Statistics', },
            self.INTRO_STATS: {
                self.BOOKSHARE: True,
                self.CATEGORY: [self.ALL, self.MATH],
                self.DETAILS: 'introductory-statistics',
                self.INTEREST: 'Introductory%20Statistics',
                self.IS_AP: False,
                self.ITUNES: True,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.SHORT_NAME: 'Introductory Statistics', },
            self.PREALGEBRA: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.MATH],
                self.DETAILS: 'prealgebra',
                self.INTEREST: 'Prealgebra',
                self.IS_AP: False,
                self.ITUNES: False,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.SHORT_NAME: 'Prealgebra', },
            self.PRECALCULUS: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.MATH],
                self.DETAILS: 'precalculus',
                self.INTEREST: 'Precalc',
                self.IS_AP: False,
                self.ITUNES: True,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.SHORT_NAME: 'Precalculus', },

            # Science
            self.ANATOMY_PHYS: {
                self.BOOKSHARE: True,
                self.CATEGORY: [self.ALL, self.SCIENCE],
                self.DETAILS: 'anatomy-and-physiology',
                self.INTEREST: 'Anatomy%20%26%20Physiology',
                self.IS_AP: False,
                self.ITUNES: True,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.SHORT_NAME: 'Anatomy & Physiology', },
            self.ASTRONOMY: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.SCIENCE],
                self.DETAILS: 'astronomy',
                self.INTEREST: 'Astronomy',
                self.IS_AP: False,
                self.ITUNES: True,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.SHORT_NAME: 'Astronomy', },
            self.BIOLOGY: {
                self.BOOKSHARE: True,
                self.CATEGORY: [self.ALL, self.SCIENCE],
                self.DETAILS: 'biology',
                self.INTEREST: 'Biology',
                self.IS_AP: False,
                self.ITUNES: True,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.SHORT_NAME: 'Biology', },
            self.BIOLOGY_2E: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.SCIENCE],
                self.DETAILS: 'biology-2e',
                self.INTEREST: 'Biology',
                self.IS_AP: False,
                self.ITUNES: True,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.SHORT_NAME: 'Biology', },
            self.AP_BIO: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.AP, self.SCIENCE],
                self.DETAILS: 'biology-ap-courses',
                self.INTEREST: 'AP%20Bio',
                self.IS_AP: True,
                self.ITUNES: False,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.SHORT_NAME: 'AP Biology', },
            self.CHEMISTRY: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.SCIENCE],
                self.DETAILS: 'chemistry',
                self.INTEREST: 'Chemistry',
                self.IS_AP: False,
                self.ITUNES: False,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.SHORT_NAME: 'Chemistry', },
            self.CHEM_ATOMS: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.SCIENCE],
                self.DETAILS: 'chemistry-atoms-first',
                self.INTEREST: 'Chem%3A%20Atoms%20First',
                self.IS_AP: False,
                self.ITUNES: True,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.SHORT_NAME: 'Chemistry: Atoms First', },
            self.PHYSICS: {
                self.BOOKSHARE: True,
                self.CATEGORY: [self.ALL, self.SCIENCE],
                self.DETAILS: 'college-physics',
                self.INTEREST: 'College%20Physics%20(Algebra)',
                self.IS_AP: False,
                self.ITUNES: True,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.SHORT_NAME: 'College Physics', },
            self.AP_PHYS: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.AP, self.SCIENCE],
                self.DETAILS: 'college-physics-ap-courses',
                self.INTEREST: 'AP%20Physics',
                self.IS_AP: True,
                self.ITUNES: True,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.SHORT_NAME: 'AP Physics', },
            self.BIO_CONCEPTS: {
                self.BOOKSHARE: True,
                self.CATEGORY: [self.ALL, self.SCIENCE],
                self.DETAILS: 'concepts-biology',
                self.INTEREST: 'Concepts%20of%20Bio%20(non-majors)',
                self.IS_AP: False,
                self.ITUNES: True,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.SHORT_NAME: 'Concepts of Biology', },
            self.FIZYKA_1: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.SCIENCE],
                self.DETAILS: ('fizyka-dla-szk%C3%B3%C5%82-wy%C5%BCszych'
                               '-tom-1'),
                self.INTEREST: None,
                self.IS_AP: False,
                self.ITUNES: False,
                self.KINDLE: False,
                self.LANGUAGE: self.POLISH,
                self.SHORT_NAME: None, },
            self.FIZYKA_2: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.SCIENCE],
                self.DETAILS: ('fizyka-dla-szk%C3%B3%C5%82-wy%C5%BCszych'
                               '-tom-2'),
                self.INTEREST: None,
                self.IS_AP: False,
                self.ITUNES: False,
                self.KINDLE: False,
                self.LANGUAGE: self.POLISH,
                self.SHORT_NAME: None, },
            self.FIZYKA_3: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.SCIENCE],
                self.DETAILS: ('fizyka-dla-szk%C3%B3%C5%82-wy%C5%BCszych'
                               '-tom-3'),
                self.INTEREST: None,
                self.IS_AP: False,
                self.ITUNES: False,
                self.KINDLE: False,
                self.LANGUAGE: self.POLISH,
                self.SHORT_NAME: None, },
            self.MICROBIOLOGY: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.SCIENCE],
                self.DETAILS: 'microbiology',
                self.INTEREST: 'Microbiology',
                self.IS_AP: False,
                self.ITUNES: True,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.SHORT_NAME: 'Microbiology', },
            self.U_PHYS_1: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.SCIENCE],
                self.DETAILS: 'university-physics-volume-1',
                self.INTEREST: 'University%20Physics%20(Calc)',
                self.IS_AP: False,
                self.ITUNES: True,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.SHORT_NAME: 'University Physics', },
            self.U_PHYS_2: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.SCIENCE],
                self.DETAILS: 'university-physics-volume-2',
                self.INTEREST: 'University%20Physics%20(Calc)',
                self.IS_AP: False,
                self.ITUNES: True,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.SHORT_NAME: 'University Physics', },
            self.U_PHYS_3: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.SCIENCE],
                self.DETAILS: 'university-physics-volume-3',
                self.INTEREST: 'University%20Physics%20(Calc)',
                self.IS_AP: False,
                self.ITUNES: True,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.SHORT_NAME: 'University Physics', },

            # Social Sciences
            self.GOVERNMENT: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.SOCIAL],
                self.DETAILS: 'american-government',
                self.INTEREST: 'American%20Government',
                self.IS_AP: False,
                self.ITUNES: True,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.SHORT_NAME: 'American Government', },
            self.SOCIOLOGY: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.SOCIAL],
                self.DETAILS: 'introduction-sociology-2e',
                self.INTEREST: 'Introduction%20to%20Sociology',
                self.IS_AP: False,
                self.ITUNES: True,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.SHORT_NAME: 'Introduction to Sociology 2e', },
            self.PRINCIPLES_ECON: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.SOCIAL],
                self.DETAILS: 'principles-economics-2e',
                self.INTEREST: 'Economics',
                self.IS_AP: False,
                self.ITUNES: True,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.SHORT_NAME: 'Principles of Economics', },
            self.PRINCIPLES_MACRO: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.SOCIAL],
                self.DETAILS: 'principles-macroeconomics-2e',
                self.INTEREST: 'Macro%20Econ',
                self.IS_AP: False,
                self.ITUNES: True,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.SHORT_NAME: 'Principles of Macroeconomics', },
            self.AP_MACRO: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.AP, self.SOCIAL],
                self.DETAILS: 'principles-macroeconomics-ap-courses-2e',
                self.INTEREST: 'AP%20Macro%20Econ',
                self.IS_AP: True,
                self.ITUNES: False,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.SHORT_NAME: 'AP Macro Econ', },
            self.PRINCIPLES_MICRO: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.SOCIAL],
                self.DETAILS: 'principles-microeconomics-2e',
                self.INTEREST: 'Micro%20Econ',
                self.IS_AP: False,
                self.ITUNES: True,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.SHORT_NAME: 'Principles of Microeconomics', },
            self.AP_MICRO: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.AP, self.SOCIAL],
                self.DETAILS: 'principles-microeconomics-ap-courses-2e',
                self.INTEREST: 'AP%20Micro%20Econ',
                self.IS_AP: True,
                self.ITUNES: False,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.SHORT_NAME: 'AP Micro Econ', },
            self.PSYCHOLOGY: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.SOCIAL],
                self.DETAILS: 'psychology',
                self.INTEREST: 'Psychology',
                self.IS_AP: False,
                self.ITUNES: True,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.SHORT_NAME: 'Psychology', },
        }

    @property
    def books(self):
        """Return the books library."""
        return self._books

    @property
    def ap(self):
        """Return the AP books."""
        return [(book, self.get(book)) for book in self.books
                if self.get(book, self.IS_AP)]

    @property
    def bookshare(self):
        """Return the books available through Bookshare."""
        return [(book, self.get(book)) for book in self.books
                if self.get(book, self.BOOKSHARE)]

    @property
    def business(self):
        """Return the business books."""
        return self.get_by_category(self.BUSINESS)

    @property
    def current(self):
        """Return the current edition of each book."""
        return [(book, self.get(book)) for book in self.books
                if book not in self.OLD_EDITIONS]

    @property
    def humanities(self):
        """Return the humanities books."""
        return self.get_by_category(self.HUMANITIES)

    @property
    def itunes(self):
        """Return the books available through iTunes."""
        return [(book, self.get(book)) for book in self.books
                if self.get(book, self.ITUNES)]

    @property
    def katalyst(self):
        """Return the Katalyst-modified books."""
        return [(book, self.get(book)) for book in self.books
                if self.get(book, self.LANGUAGE) == self.POLISH]

    @property
    def kindle(self):
        """Return the books available through Amazon ebooks."""
        return [(book, self.get(book)) for book in self.books
                if self.get(book, self.KINDLE)]

    @property
    def math(self):
        """Return the math books."""
        return self.get_by_category(self.MATH)

    @property
    def openstax(self):
        """Return the OpenStax books."""
        return [(book, self.get(book)) for book in self.books
                if self.get(book, self.LANGUAGE) == self.ENGLISH]

    @property
    def science(self):
        """Return the science books."""
        return self.get_by_category(self.SCIENCE)

    @property
    def short_names(self):
        """Return a unique list of short names in use."""
        return list(set([self.get(book, self.SHORT_NAME) for book in self.books
                        if self.get(book, self.SHORT_NAME)]))

    @property
    def social_sciences(self):
        """Return the social science books."""
        return self.get_by_category(self.SOCIAL)

    @property
    def superseded(self):
        """Return older books with a newer version available."""
        return [(book, self.get(book)) for book in self.books
                if book in self.OLD_EDITIONS]

    def get_titles(self, group=None):
        """Return a list of book titles."""
        collection = group if group else self.books
        return [book[0] for book in collection]

    def book_passthrough(self, using):
        """Return the Subjects book name and form append for a book set."""
        return [(book, self.get(book, self.INTEREST)) for book in using]

    def get(self, book, field=None):
        """Return the field or fields for a specific book."""
        if field:
            return self.books.get(book).get(field)
        return self.books.get(book)

    def get_by_category(self, category):
        """Return the books within a specific category."""
        return [(book, self.get(book)) for book in self.books
                if category in self.get(book, self.CATEGORY)]

    def get_name_set(self, book=None):
        """Return the name set for a book.

        Return:
            (book record, book short name, book full name, book details append)
        """
        using = (self.get(book) if book else
                 self.random_book(short_name=False))
        return (using[0],
                using[0][1].get(self.SHORT_NAME),
                [key for key in using[0]][0],
                using[0][1].get(self.DETAILS))

    def random_book(self, number=1, short_name=True):
        """Return a list of random book short names."""
        if short_name:
            return Utility.random_set(self.short_names, number)
        return Utility.random_set(self.openstax, number)
