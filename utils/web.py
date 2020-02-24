"""OpenStax Web globals."""

import re

from selenium.common.exceptions import WebDriverException

from utils.utilities import Utility


class Web(object):
    """Website shared variables."""

    # Supplemental base URLs
    NEWSLETTER_SIGNUP = "http://www2.openstax.org/l/218812/2016-10-04/lvk"
    SALESFORCE_SUPPORT = "https://openstax.secure.force.com/help"

    # Sizing
    PHONE = 600
    SMALL_TABLET = 760
    TABLET = 960
    FULL = 1024

    # RegEx matchers
    FILENAME_MATCHER = re.compile(r'url\([\w\-\:\/\.]*\)\;')

    # *** HOME PAGE, NAV BARS, and FOOTER ***

    # Web banner carousel options
    INTERACTIVE_MAP = 0
    NEW_APP = 1
    FREE_BOOKS_NO_CATCH = 2

    # Quotes
    SUBSCRIBE = 0
    BOOK_QUALITY_RIGGS = 1
    BOOKSTORE_SUPPLIERS = 2

    # Home page boxes
    BOOKS = 0
    TECH = 1
    OUR_IMPACT = 0
    REPORT = 0
    OPENSTAX_PARTNERS = 1

    # *** BOOK DETAILS ***

    # Book page tabs
    BOOK_DETAILS = 0
    INSTRUCTOR_RESOURCES = 1
    PARTNER_RESOURCES = 3
    STUDENT_RESOURCES = 2

    # Book page order modals
    INDIVIDUAL = 0
    BOOKSTORES = 1

    # *** BOOKSTORE SUPPLIERS ***

    # Bookstore supplier cards
    MBS_TEXTBOOK = 0
    TRILITERAL = 1
    VRETTA = 2

    XANEDU = 0
    LAD_CUSTOM = 1
    MONTEZUMA = 2

    # *** CONTACT US ***

    ABOUT_GENERAL = 'General'
    ABOUT_ADOPTION = 'Adopting OpenStax Textbooks'
    ABOUT_TUTOR = 'OpenStax Tutor Support'
    ABOUT_CNX = 'OpenStax CNX'
    ABOUT_DONATIONS = 'Donations'
    ABOUT_PARTNERSHIP = 'College/University Partnerships'
    ABOUT_MEDIA = 'Media Inquiries'
    ABOUT_FOUNDATION = 'Foundational Support'

    TOPICS = [
        ABOUT_GENERAL, ABOUT_ADOPTION, ABOUT_TUTOR, ABOUT_CNX,
        ABOUT_DONATIONS, ABOUT_PARTNERSHIP, ABOUT_MEDIA, ABOUT_FOUNDATION
    ]

    # *** DONATIONS ***

    # Donation page values
    MIN_DONATION = 5
    DOLLAR_OPTIONS = [
        10, 25, 50, 100, 500, 1000, 'Other'
    ]

    # *** OUR IMPACT ***

    # Sections
    BANNER = 0
    REVOLUTION = 1
    FOUNDING = 2
    REACH = 3
    TESTIMONIALS = 4
    SUSTAINABILITY = 5
    DISRUPTION = 6
    LOOKING_AHEAD = 7
    MAP = 8
    OS_TUTOR = 9
    PHILANTHROPIC_PARTNERS = 10
    DONATION = 11

    # *** PRESS ***

    # Press mobile section options
    PRESS_RELEASES = 'Press releases'
    NEWS_MENTIONS = 'News mentions'
    PRESS_INQUIRIES = 'Press inquiries'
    BOOKING = 'Booking'

    PRESS_OPTIONS = [
        PRESS_RELEASES,
        NEWS_MENTIONS,
        PRESS_INQUIRIES,
        BOOKING
    ]

    # Press social media accounts
    FACEBOOK = 'facebook'
    INSTAGRAM = 'instagram'
    LINKEDIN = 'linkedin'
    TWITTER = 'twitter'
    MEDIA = {
        FACEBOOK: 'Facebook',
        INSTAGRAM: 'Instagram',
        LINKEDIN: 'LinkedIn',
        TWITTER: 'Twitter',
    }

    # *** PRIVACY POLICY ***

    # Privacy policy section headings
    PRIVACY = [
        'About this Privacy Policy',
        'Definitions',
        'Modifications',
        'Information We Collect',
        'How We Use Your Information',
        'Sharing Your Information',
        'Accuracy of Data, Storage',
        'Links to Other Websites',
        ('Security and Liability for Theft and/or Disclosure'
         ' of Login Credentials')
    ]

    # *** OPENSTAX RESEARCH ***

    # Research page tabs
    ALUMNI = 0
    CURRENT_MEMBERS = 1
    EXTERNAL_COLLABORATORS = 2

    AUTHOR = 0
    TITLE = 2
    YEAR = 1

    # *** OPENSTAX TEAM ***

    # Team page tabs
    OPENSTAX_TEAM = 0
    STRATEGIC_ADVISORS = 1
    ADVISORY_BOARD = 2

    TEAM_GROUPS = [
        'OpenStax Team',
        'Strategic Advisors'
    ]

    # *** TUTOR MARKETING ***

    # Tutor Marketing sections
    NEW_FRONTIER = 0
    HOW_IT_WORKS = 1
    WHAT_STUDENTS_GET = 2
    FEATURE_MATRIX = 3
    WHERE_MONEY_GOES = 4
    THE_SCIENCE = 5
    TUTOR_FAQ = 6
    LEARN_MORE = 7

    GET_STARTED = 0
    JOIN_A_WEBINAR = 1

    # Book page resource status options
    ACCESS = "Access on OpenStax's YouTube Channel"
    CODE = 'Request your comp code'
    COMING_SOON = 'Coming soon!'
    DOWNLOAD = 'Download'
    EXTERNAL = 'Go'
    LOCKED = 'Click here to unlock'
    PENDING = 'Access pending'
    REQUEST = 'Request your copy'
    TRANSITION = 'Transition Guide'

    ACCESS_OK = [
        ACCESS, CODE, DOWNLOAD, EXTERNAL, PENDING,
        REQUEST, TRANSITION
    ]

    # Matching strings
    ABOUT = 'about'
    ANNUAL_REPORT = 'annual-report'
    BOOKSTORE = 'bookstore-suppliers'
    GIVE = 'give'
    IMPACT = 'impact'
    INSTITUTION = 'institutional-partnership'
    NEWSLETTER = 'www2.openstax.org'
    NO_FILTER = 'View All'
    PARTNERS = 'partners'
    GLOBAL_REACH = 'global-reach'
    RESEARCH = 'research'
    ROVER = 'rover-by-openstax'
    SE_APP = 'download-openstax-se-app'
    SUBJECTS = 'subjects'
    TECHNOLOGY = 'technology'
    TUTOR = 'openstax-tutor'

    # Menus
    VIEW_ALL = 'All'
    VIEW_AP = 'AP®'
    VIEW_BUSINESS = 'Business'
    VIEW_ESSENTIALS = 'Essentials'
    VIEW_HUMANITIES = 'Humanities'
    VIEW_MATH = 'Math'
    VIEW_SCIENCE = 'Science'
    VIEW_SOCIAL_SCIENCES = 'Social Sciences'

    VIEW_PARTNERS = 'OpenStax Tech Scout'
    VIEW_ROVER = 'Rover by OpenStax'
    VIEW_TUTOR = 'OpenStax Tutor'

    VIEW_ABOUT_US = 'About Us'
    VIEW_CREATOR_FEST = 'Creator Fest'
    VIEW_PARTNERSHIPS = 'Institutional Partnerships'
    VIEW_RESEARCH = 'Research'
    VIEW_TEAM = 'Team'

    # User types
    ADJUNCT = 'Adjunct Faculty'
    ADMINISTRATOR = 'Administrator'
    DESIGNER = 'Instructional Designer'
    HOMESCHOOL = 'Home School Teacher'
    INSTRUCTOR = 'Faculty'
    LIBRARIAN = 'Librarian'
    NO_USER_TYPE = 'Please select one'
    OTHER = 'Other'
    STUDENT = 'Student'

    USERS = [
        STUDENT,
        'Instructor',
        'Homeschool Instructor',
        ADMINISTRATOR,
        LIBRARIAN,
        DESIGNER,
        ADJUNCT,
        OTHER
    ]

    USER_CONVERSION = {
        ADJUNCT: ADJUNCT,
        ADMINISTRATOR: ADMINISTRATOR,
        DESIGNER: DESIGNER,
        USERS[2]: HOMESCHOOL,
        USERS[1]: INSTRUCTOR,
        INSTRUCTOR: USERS[1],
        LIBRARIAN: LIBRARIAN,
        OTHER: OTHER,
        STUDENT: STUDENT, }

    # Adoption or interest status
    ADOPTED = 'Confirmed Adoption Won'
    RECOMMENDED = 'Confirmed Will Recommend'

    USING_STATUS = [
        ADOPTED,
        RECOMMENDED
    ]

    STUDENT_MIN = 1
    STUDENT_MAX = 999

    BY_COLLEAGUE = 'Colleague'
    BY_CONFERENCE = 'Conference'
    BY_EMAIL = 'Email'
    BY_FACEBOOK = 'Facebook'
    BY_PARTNER = 'Partner organization'
    BY_TWITTER = 'Twitter'
    BY_WEBINAR = 'Webinar'
    BY_WEB_SEARCH = 'Web search'
    COURSEWARE = 'Adaptive courseware partners'
    HOMEWORK = 'Online homework partners'
    TOOLS = 'Customization tool partners'

    ADDITIONAL = [
        HOMEWORK,
        COURSEWARE,
        TOOLS
    ]
    HEARD_BY = [
        BY_WEB_SEARCH,
        BY_COLLEAGUE,
        BY_CONFERENCE,
        BY_EMAIL,
        BY_FACEBOOK,
        BY_TWITTER,
        BY_WEBINAR,
        BY_PARTNER
    ]

    @classmethod
    def resources(cls, options=1, randomize=True, get_partner_resources=True):
        """Return a list of additional resource options."""
        option_list = (Web.ADDITIONAL if get_partner_resources
                       else Web.HEARD_BY)
        if options >= len(option_list):
            return option_list
        if randomize:
            options = Utility.random(options, len(option_list))
        from random import sample
        random_options = sample(option_list, len(option_list))
        while len(random_options) > options:
            random_options.pop()
        return random_options

    @classmethod
    def heard_by(cls, options=1, randomize=True):
        """Return a list of heard by options."""
        return Web.resources(
            options, randomize=randomize, get_partner_resources=False)

    # Expected lists
    ACCESSIBILITY = [
        'Accessibility',
        'Web Accessibility',
        'Our progress',
        'Feedback',
        'Interactive Simulations',
        'User-Contributed Content',
        'Voluntary Product Accessibility Template (VPAT)'
    ]
    URL_APPENDS = [
        'math',
        'science',
        'social-sciences',
        'humanities',
        'business',
        'essentials',
        'ap'
    ]
    FILTERS = [
        VIEW_MATH,
        VIEW_SCIENCE,
        VIEW_SOCIAL_SCIENCES,
        VIEW_HUMANITIES,
        VIEW_BUSINESS,
        VIEW_ESSENTIALS,
        VIEW_AP
    ]
    MENU_SUBJECTS = [
        VIEW_ALL,
        *FILTERS
    ]
    PARTNER_FILTERS = {
        VIEW_ALL: 0,
        VIEW_MATH: 1,
        VIEW_SCIENCE: 2,
        VIEW_SOCIAL_SCIENCES: 3,
        VIEW_HUMANITIES: 4,
        VIEW_BUSINESS: 5,
        VIEW_ESSENTIALS: 6,
        VIEW_AP: 7,
    }
    MENU_TECHNOLOGY = [
        VIEW_TUTOR,
        VIEW_ROVER,
        VIEW_PARTNERS
    ]
    MENU_WHAT_WE_DO = [
        VIEW_ABOUT_US,
        VIEW_TEAM,
        VIEW_RESEARCH,
        VIEW_PARTNERSHIPS,
        VIEW_CREATOR_FEST
    ]


class TechProviders():
    """Adoption and interest technology providers."""

    AMBASSADOR = 'Ambassador'
    BARNES_AND_NOBLE = 'Barnes & Noble Education'
    BLENDING_EDUCATION = 'Blending Education'
    BLUPOINT = 'BluPoint'
    CARNEGIE = 'Carnegie Learning'
    CAROLINA_LEARNING = 'Carolina Distance Learning'
    CATALYST = 'Catalyst Education'
    CENGAGE = 'Cengage'
    CHEGG = 'Chegg'
    CHEGG_STUDY = 'Chegg Study'
    CHEGG_TUTORS = 'Chegg Tutors'
    CHEM101 = 'Chem101'
    CLASSAVO = 'Classavo'
    COGBOOKS = 'CogBooks'
    COGNELLA = 'Cognella'
    CONNECT = 'Connect For Education'
    COPIA = 'Copia'
    CRITICAL_CHEM = 'Critical Chemistry'
    EDFINITY = 'Edfinity'
    EMATH = 'eMath'
    EXPERT_TA = 'Expert TA'
    EXPERT_TA_ASSESS = 'Expert TA Assess'
    EXPERT_TA_STUDY = 'Expert TA Study'
    GRAPHLOCK = 'GraphLock'
    HAWKES = 'Hawkes Learning'
    INTELLUS = 'Intellus Learning'
    JUNCTION = 'Junction'
    KNEWTON = 'Knewton'
    LABARCHIVES = 'LabArchives'
    LRNR = 'Lrnr'
    LUMEN = 'Lumen'
    LYRYX = 'Lyryx Learning'
    MCGRAW_HILL = 'McGraw-Hill Education'
    MINDEDGE = 'MindEdge Learning'
    ODIGIA = 'Odigia'
    OPEN_TEXTBOOK_NETWORK = 'Open Textbook Network'
    TUTOR = 'OpenStax Tutor Beta'
    PANOPEN = 'panOpen'
    PERLEGO = 'Perlego'
    PERUSALL = 'Perusall'
    REALIZEIT = 'Realizeit'
    RICE_ONLINE = 'Rice Online Learning'
    SAPLING = 'Sapling Learning'
    SIMBIO = 'SimBio'
    SQUARECAP = 'Squarecap'
    STUDY_EDGE = 'Study Edge'
    TOP_HAT = 'Top Hat'
    VANGRINER = 'Van-Griner Learning'
    VARAFY = 'Varafy'
    VISIBLE_BODY = 'Visible Body'
    VRETTA = 'Vretta'
    WEBASSIGN = 'WebAssign'
    WILEY = 'Wiley'
    XYZ = 'XYZ Homework'
    ZYBOOKS = 'zyBooks'
    OTHER = 'Other (specify below)'

    tech_list = [
        AMBASSADOR, BARNES_AND_NOBLE, BLENDING_EDUCATION, BLUPOINT,
        CARNEGIE, CAROLINA_LEARNING, CATALYST, CENGAGE, CHEGG, CHEGG_STUDY,
        CHEGG_TUTORS, CHEM101, CLASSAVO, COGBOOKS, COGNELLA, CONNECT, COPIA,
        CRITICAL_CHEM, EDFINITY, EMATH, EXPERT_TA, EXPERT_TA_ASSESS,
        EXPERT_TA_STUDY, GRAPHLOCK, HAWKES, INTELLUS, JUNCTION, KNEWTON,
        LABARCHIVES, LRNR, LUMEN, LYRYX, MCGRAW_HILL, MINDEDGE, ODIGIA,
        OPEN_TEXTBOOK_NETWORK, TUTOR, PANOPEN, PERLEGO, PERUSALL, REALIZEIT,
        RICE_ONLINE, SAPLING, SIMBIO, SQUARECAP, STUDY_EDGE, TOP_HAT,
        VANGRINER, VARAFY, VISIBLE_BODY, VRETTA, WEBASSIGN, WILEY, XYZ,
        ZYBOOKS, OTHER
    ]

    full_catalog = [
        AMBASSADOR,
        BLENDING_EDUCATION,
        BLUPOINT,
        COGNELLA,
        COPIA,
        ODIGIA,
        PERUSALL,
        REALIZEIT,
        SQUARECAP,
        VANGRINER
    ]

    math_titles = [
        GRAPHLOCK
    ]

    no_titles = [
        CHEGG_STUDY,
        CHEGG_TUTORS,
        OPEN_TEXTBOOK_NETWORK
    ]

    @classmethod
    def book_selection(cls):
        """Return a list of providers offering services for specific books."""
        return [provider for provider in cls.tech_list
                if (provider not in cls.full_catalog and
                    provider not in cls.math_titles and
                    provider not in cls.no_titles)]

    @classmethod
    def get_tech(cls, number=1):
        """Return a subset of the tech list for the forms."""
        return Utility.random_set(cls.tech_list, number)


class Library():
    """OpenStax book library."""

    # Business
    ACCOUNTING_1 = 'Principles of Accounting, Volume 1: Financial Accounting'
    ACCOUNTING_1_ALT = 'Financial Accounting'
    ACCOUNTING_2 = 'Principles of Accounting, Volume 2: Managerial Accounting'
    ACCOUNTING_2_ALT = 'Managerial Accounting'
    BUSINESS_STATS = 'Introductory Business Statistics'
    BUS_LAW_1 = 'Business Law I Essentials'
    ENTREPRENEUR = 'Entrepreneurship'
    ETHICS = 'Business Ethics'
    INTRO_BUSINESS = 'Introduction to Business'
    MANAGEMENT = 'Principles of Management'
    MANAGEMENT_ALT = 'Management'
    ORG_BEHAVIOR = 'Organizational Behavior'

    # Humanities
    US_HISTORY = 'U.S. History'

    # Math
    ALGEBRA = 'College Algebra'
    ALGEBRA_TRIG = 'Algebra and Trigonometry'
    CALCULUS_1 = 'Calculus Volume 1'
    CALCULUS_2 = 'Calculus Volume 2'
    CALCULUS_3 = 'Calculus Volume 3'
    ELEM_ALGEBRA = 'Elementary Algebra'
    INTER_ALGEBRA = 'Intermediate Algebra'
    INTRO_STATS = 'Introductory Statistics'
    PREALGEBRA = 'Prealgebra'
    PRECALCULUS = 'Precalculus'

    # Science
    ANATOMY_PHYS = 'Anatomy and Physiology'
    ANATOMY_PHYS_ALT = 'Anatomy & Physiology'
    AP_BIO = 'Biology for AP® Courses'  # book title
    AP_BIO_ALT = 'AP Biology'  # shortened list title
    AP_PHYS = 'College Physics for AP® Courses'  # book title
    AP_PHYS_ALT = 'The AP Physics Collection'  # alternate title
    AP_PHYS_ALT_2 = 'AP Physics'  # shortened list title
    ASTRONOMY = 'Astronomy'
    BIOLOGY_2E = 'Biology 2e'
    BIO_CONCEPTS = 'Concepts of Biology'
    CHEMISTRY_2E = 'Chemistry 2e'
    CHEM_ATOMS_2E = 'Chemistry: Atoms First 2e'
    FIZYKA_1 = 'Fizyka dla szkół wyższych. Tom 1'
    FIZYKA_2 = 'Fizyka dla szkół wyższych. Tom 2'
    FIZYKA_3 = 'Fizyka dla szkół wyższych. Tom 3'
    MICROBIOLOGY = 'Microbiology'
    PHYSICS = 'College Physics'
    U_PHYS_1 = 'University Physics Volume 1'
    U_PHYS_2 = 'University Physics Volume 2'
    U_PHYS_3 = 'University Physics Volume 3'
    U_PHYS_ALT = 'University Physics'

    # Social Sciences
    AP_MACRO = 'Principles of Macroeconomics for AP® Courses 2e'
    AP_MICRO = 'Principles of Microeconomics for AP® Courses 2e'
    GOVERNMENT_2E = 'American Government 2e'
    PRINCIPLES_ECON = 'Principles of Economics 2e'
    PRINCIPLES_MACRO = 'Principles of Macroeconomics 2e'
    PRINCIPLES_MICRO = 'Principles of Microeconomics 2e'
    PSYCHOLOGY = 'Psychology'
    SOCIOLOGY = 'Introduction to Sociology 2e'

    # Fields and limiters
    ADOPTION = 'interest'
    ALL_BOOKS = 'all'
    AVAILABLE = 'available'
    BOOKSHARE = 'bookshare'
    CATEGORY = 'subject'
    CHEGG = 'chegg'
    COMP_COPY = 'comp_copy'
    CURRENT = 'current'
    DETAILS = 'details'
    ENGLISH = 'English'
    HAS_I_LOCK = 'instructor_locked'
    HAS_I_UNLOCK = 'instructor_unlocked'
    HAS_S_LOCK = 'student_locked'
    HAS_S_UNLOCK = 'student_unlocked'
    INTEREST = ADOPTION
    IS_AP = 'is_ap?'
    ITUNES = 'itunes'
    KINDLE = 'kindle'
    LANGUAGE = 'language'
    OPENSTAX = 'openstax'
    POLISH = 'Polish'
    PRE_RELEASE = 'Coming Soon'
    PRINT_COPY = 'print'
    SHORT_NAME = 'short_name'
    SUPERSEDED = 'not_current'

    # Subjects
    ALL = 'View All'
    AP = 'AP®'
    BUSINESS = 'Business'
    ESSENTIALS = 'Essentials'
    HUMANITIES = 'Humanities'
    MATH = 'Math'
    SCIENCE = 'Science'
    SOCIAL = 'Social Sciences'

    OLD_EDITIONS = []

    def __init__(self):
        """Initialize the library."""
        self._books = {

            # Business
            self.ACCOUNTING_1: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.BUSINESS],
                self.CHEGG: False,
                self.COMP_COPY: False,
                self.DETAILS: 'principles-financial-accounting',
                self.HAS_I_LOCK: True,
                self.HAS_I_UNLOCK: True,
                self.HAS_S_LOCK: False,
                self.HAS_S_UNLOCK: True,
                self.INTEREST: 'Financial%20Accounting',
                self.IS_AP: False,
                self.ITUNES: False,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.PRE_RELEASE: False,
                self.PRINT_COPY: True,
                self.SHORT_NAME: 'Financial Accounting', },
            self.ACCOUNTING_2: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.BUSINESS],
                self.CHEGG: False,
                self.COMP_COPY: False,
                self.DETAILS: 'principles-managerial-accounting',
                self.HAS_I_LOCK: True,
                self.HAS_I_UNLOCK: True,
                self.HAS_S_LOCK: False,
                self.HAS_S_UNLOCK: True,
                self.INTEREST: 'Managerial%20Accounting',
                self.IS_AP: False,
                self.ITUNES: False,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.PRE_RELEASE: False,
                self.PRINT_COPY: True,
                self.SHORT_NAME: 'Managerial Accounting', },
            self.BUSINESS_STATS: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.BUSINESS, self.MATH],
                self.CHEGG: True,
                self.COMP_COPY: False,
                self.DETAILS: 'introductory-business-statistics',
                self.HAS_I_LOCK: True,
                self.HAS_I_UNLOCK: True,
                self.HAS_S_LOCK: False,
                self.HAS_S_UNLOCK: True,
                self.INTEREST: 'Business%20Statistics',
                self.IS_AP: False,
                self.ITUNES: False,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.PRE_RELEASE: False,
                self.PRINT_COPY: True,
                self.SHORT_NAME: 'Introductory Business Statistics', },
            self.BUS_LAW_1: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.BUSINESS, self.ESSENTIALS],
                self.CHEGG: False,
                self.COMP_COPY: False,
                self.DETAILS: 'business-law-i-essentials',
                self.HAS_I_LOCK: False,
                self.HAS_I_UNLOCK: True,
                self.HAS_S_LOCK: False,
                self.HAS_S_UNLOCK: True,
                self.INTEREST: r'Business%20Law%20I%20Essentials',
                self.IS_AP: False,
                self.ITUNES: False,
                self.KINDLE: False,
                self.LANGUAGE: self.ENGLISH,
                self.PRE_RELEASE: False,
                self.PRINT_COPY: False,
                self.SHORT_NAME: 'Business Law I Essentials', },
            self.ENTREPRENEUR: {  # Pre-release
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.BUSINESS, self.ESSENTIALS],
                self.CHEGG: False,
                self.COMP_COPY: False,
                self.DETAILS: 'entrepreneurship',
                self.HAS_I_LOCK: False,
                self.HAS_I_UNLOCK: True,
                self.HAS_S_LOCK: False,
                self.HAS_S_UNLOCK: True,
                self.INTEREST: None,
                self.IS_AP: False,
                self.ITUNES: False,
                self.KINDLE: False,
                self.LANGUAGE: self.ENGLISH,
                self.PRE_RELEASE: True,
                self.PRINT_COPY: False,
                self.SHORT_NAME: None, },
            self.ETHICS: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.BUSINESS],
                self.CHEGG: True,
                self.COMP_COPY: False,
                self.DETAILS: 'business-ethics',
                self.HAS_I_LOCK: True,
                self.HAS_I_UNLOCK: True,
                self.HAS_S_LOCK: False,
                self.HAS_S_UNLOCK: True,
                self.INTEREST: r'Business%20Ethics',
                self.IS_AP: False,
                self.ITUNES: False,
                self.KINDLE: False,
                self.LANGUAGE: self.ENGLISH,
                self.PRE_RELEASE: False,
                self.PRINT_COPY: True,
                self.SHORT_NAME: 'Business Ethics', },
            self.INTRO_BUSINESS: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.BUSINESS],
                self.CHEGG: False,
                self.COMP_COPY: False,
                self.DETAILS: 'introduction-business',
                self.HAS_I_LOCK: True,
                self.HAS_I_UNLOCK: True,
                self.HAS_S_LOCK: False,
                self.HAS_S_UNLOCK: True,
                self.INTEREST: r'Introduction%20to%20Business',
                self.IS_AP: False,
                self.ITUNES: False,
                self.KINDLE: False,
                self.LANGUAGE: self.ENGLISH,
                self.PRE_RELEASE: False,
                self.PRINT_COPY: True,
                self.SHORT_NAME: 'Introduction to Business', },
            self.MANAGEMENT: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.BUSINESS],
                self.CHEGG: False,
                self.COMP_COPY: False,
                self.DETAILS: 'principles-management',
                self.HAS_I_LOCK: True,
                self.HAS_I_UNLOCK: True,
                self.HAS_S_LOCK: False,
                self.HAS_S_UNLOCK: True,
                self.INTEREST: 'Management',
                self.IS_AP: False,
                self.ITUNES: False,
                self.KINDLE: False,
                self.LANGUAGE: self.ENGLISH,
                self.PRE_RELEASE: False,
                self.PRINT_COPY: True,
                self.SHORT_NAME: 'Management', },
            self.ORG_BEHAVIOR: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.BUSINESS],
                self.CHEGG: False,
                self.COMP_COPY: False,
                self.DETAILS: 'organizational-behavior',
                self.HAS_I_LOCK: True,
                self.HAS_I_UNLOCK: True,
                self.HAS_S_LOCK: False,
                self.HAS_S_UNLOCK: True,
                self.INTEREST: 'Behavior',
                self.IS_AP: False,
                self.ITUNES: False,
                self.KINDLE: False,
                self.LANGUAGE: self.ENGLISH,
                self.PRE_RELEASE: False,
                self.PRINT_COPY: False,
                self.SHORT_NAME: 'Behavior', },

            # Essentials
            #     currently, only Entrepreneurship and Busness Law I are in
            #     Essentials

            # Humanities
            self.US_HISTORY: {
                self.BOOKSHARE: True,
                self.CATEGORY: [self.ALL, self.HUMANITIES],
                self.CHEGG: True,
                self.COMP_COPY: True,
                self.DETAILS: 'us-history',
                self.HAS_I_LOCK: True,
                self.HAS_I_UNLOCK: True,
                self.HAS_S_LOCK: False,
                self.HAS_S_UNLOCK: True,
                self.INTEREST: 'US%20History',
                self.IS_AP: False,
                self.ITUNES: True,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.PRE_RELEASE: False,
                self.PRINT_COPY: True,
                self.SHORT_NAME: 'U.S. History', },

            # Math
            self.ALGEBRA_TRIG: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.MATH],
                self.CHEGG: False,
                self.COMP_COPY: False,
                self.DETAILS: 'algebra-and-trigonometry',
                self.HAS_I_LOCK: True,
                self.HAS_I_UNLOCK: True,
                self.HAS_S_LOCK: False,
                self.HAS_S_UNLOCK: True,
                self.INTEREST: r'Algebra%20and%20Trigonometry',
                self.IS_AP: False,
                self.ITUNES: False,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.PRE_RELEASE: False,
                self.PRINT_COPY: True,
                self.SHORT_NAME: 'Algebra and Trigonometry', },
            self.CALCULUS_1: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.MATH],
                self.CHEGG: False,
                self.COMP_COPY: False,
                self.DETAILS: 'calculus-volume-1',
                self.HAS_I_LOCK: True,
                self.HAS_I_UNLOCK: True,
                self.HAS_S_LOCK: True,
                self.HAS_S_UNLOCK: True,
                self.INTEREST: 'Calculus',
                self.IS_AP: False,
                self.ITUNES: False,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.PRE_RELEASE: False,
                self.PRINT_COPY: True,
                self.SHORT_NAME: 'Calculus', },
            self.CALCULUS_2: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.MATH],
                self.CHEGG: False,
                self.COMP_COPY: False,
                self.DETAILS: 'calculus-volume-2',
                self.HAS_I_LOCK: True,
                self.HAS_I_UNLOCK: True,
                self.HAS_S_LOCK: True,
                self.HAS_S_UNLOCK: True,
                self.INTEREST: 'Calculus',
                self.IS_AP: False,
                self.ITUNES: False,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.PRE_RELEASE: False,
                self.PRINT_COPY: True,
                self.SHORT_NAME: 'Calculus', },
            self.CALCULUS_3: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.MATH],
                self.CHEGG: False,
                self.COMP_COPY: False,
                self.DETAILS: 'calculus-volume-3',
                self.HAS_I_LOCK: True,
                self.HAS_I_UNLOCK: True,
                self.HAS_S_LOCK: True,
                self.HAS_S_UNLOCK: True,
                self.INTEREST: 'Calculus',
                self.IS_AP: False,
                self.ITUNES: False,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.PRE_RELEASE: False,
                self.PRINT_COPY: True,
                self.SHORT_NAME: 'Calculus', },
            self.ALGEBRA: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.MATH],
                self.CHEGG: False,
                self.COMP_COPY: False,
                self.DETAILS: 'college-algebra',
                self.HAS_I_LOCK: True,
                self.HAS_I_UNLOCK: True,
                self.HAS_S_LOCK: False,
                self.HAS_S_UNLOCK: True,
                self.INTEREST: 'College%20Algebra',
                self.IS_AP: False,
                self.ITUNES: False,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.PRE_RELEASE: False,
                self.PRINT_COPY: True,
                self.SHORT_NAME: 'College Algebra', },
            self.ELEM_ALGEBRA: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.MATH],
                self.CHEGG: True,
                self.COMP_COPY: False,
                self.DETAILS: 'elementary-algebra',
                self.HAS_I_LOCK: True,
                self.HAS_I_UNLOCK: True,
                self.HAS_S_LOCK: False,
                self.HAS_S_UNLOCK: True,
                self.INTEREST: 'Elementary%20Algebra',
                self.IS_AP: False,
                self.ITUNES: False,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.PRE_RELEASE: False,
                self.PRINT_COPY: True,
                self.SHORT_NAME: 'Elementary Algebra', },
            self.INTER_ALGEBRA: {
                self.BOOKSHARE: True,
                self.CATEGORY: [self.ALL, self.MATH],
                self.CHEGG: False,
                self.COMP_COPY: False,
                self.DETAILS: 'intermediate-algebra',
                self.HAS_I_LOCK: True,
                self.HAS_I_UNLOCK: True,
                self.HAS_S_LOCK: False,
                self.HAS_S_UNLOCK: True,
                self.INTEREST: 'Intermediate%20Algebra',
                self.IS_AP: False,
                self.ITUNES: False,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.PRE_RELEASE: False,
                self.PRINT_COPY: True,
                self.SHORT_NAME: 'Intermediate Algebra', },
            self.INTRO_STATS: {
                self.BOOKSHARE: True,
                self.CATEGORY: [self.ALL, self.MATH],
                self.CHEGG: False,
                self.COMP_COPY: True,
                self.DETAILS: 'introductory-statistics',
                self.HAS_I_LOCK: True,
                self.HAS_I_UNLOCK: True,
                self.HAS_S_LOCK: False,
                self.HAS_S_UNLOCK: True,
                self.INTEREST: 'Introductory%20Statistics',
                self.IS_AP: False,
                self.ITUNES: True,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.PRE_RELEASE: False,
                self.PRINT_COPY: True,
                self.SHORT_NAME: 'Introductory Statistics', },
            self.PREALGEBRA: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.MATH],
                self.CHEGG: False,
                self.COMP_COPY: False,
                self.DETAILS: 'prealgebra',
                self.HAS_I_LOCK: True,
                self.HAS_I_UNLOCK: True,
                self.HAS_S_LOCK: False,
                self.HAS_S_UNLOCK: True,
                self.INTEREST: 'Prealgebra',
                self.IS_AP: False,
                self.ITUNES: False,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.PRE_RELEASE: False,
                self.PRINT_COPY: True,
                self.SHORT_NAME: 'Prealgebra', },
            self.PRECALCULUS: {
                self.BOOKSHARE: True,
                self.CATEGORY: [self.ALL, self.MATH],
                self.CHEGG: False,
                self.COMP_COPY: True,
                self.DETAILS: 'precalculus',
                self.HAS_I_LOCK: True,
                self.HAS_I_UNLOCK: True,
                self.HAS_S_LOCK: False,
                self.HAS_S_UNLOCK: True,
                self.INTEREST: 'Precalc',
                self.IS_AP: False,
                self.ITUNES: True,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.PRE_RELEASE: False,
                self.PRINT_COPY: True,
                self.SHORT_NAME: 'Precalculus', },

            # Science
            self.ANATOMY_PHYS: {
                self.BOOKSHARE: True,
                self.CATEGORY: [self.ALL, self.SCIENCE],
                self.CHEGG: True,
                self.COMP_COPY: False,
                self.DETAILS: 'anatomy-and-physiology',
                self.HAS_I_LOCK: True,
                self.HAS_I_UNLOCK: True,
                self.HAS_S_LOCK: True,
                self.HAS_S_UNLOCK: True,
                self.INTEREST: r'Anatomy%20%26%20Physiology',
                self.IS_AP: False,
                self.ITUNES: True,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.PRE_RELEASE: False,
                self.PRINT_COPY: True,
                self.SHORT_NAME: 'Anatomy & Physiology', },
            self.ASTRONOMY: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.SCIENCE],
                self.CHEGG: True,
                self.COMP_COPY: True,
                self.DETAILS: 'astronomy',
                self.HAS_I_LOCK: True,
                self.HAS_I_UNLOCK: True,
                self.HAS_S_LOCK: False,
                self.HAS_S_UNLOCK: True,
                self.INTEREST: 'Astronomy',
                self.IS_AP: False,
                self.ITUNES: True,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.PRE_RELEASE: False,
                self.PRINT_COPY: True,
                self.SHORT_NAME: 'Astronomy', },
            self.BIOLOGY_2E: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.SCIENCE],
                self.CHEGG: True,
                self.COMP_COPY: True,
                self.DETAILS: 'biology-2e',
                self.HAS_I_LOCK: True,
                self.HAS_I_UNLOCK: True,
                self.HAS_S_LOCK: True,
                self.HAS_S_UNLOCK: True,
                self.INTEREST: 'Biology',
                self.IS_AP: False,
                self.ITUNES: True,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.PRE_RELEASE: False,
                self.PRINT_COPY: True,
                self.SHORT_NAME: 'Biology', },
            self.AP_BIO: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.AP, self.SCIENCE],
                self.CHEGG: True,
                self.COMP_COPY: False,
                self.DETAILS: 'biology-ap-courses',
                self.HAS_I_LOCK: True,
                self.HAS_I_UNLOCK: True,
                self.HAS_S_LOCK: True,
                self.HAS_S_UNLOCK: True,
                self.INTEREST: 'AP%20Bio',
                self.IS_AP: True,
                self.ITUNES: False,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.PRE_RELEASE: False,
                self.PRINT_COPY: True,
                self.SHORT_NAME: 'AP Biology', },
            self.CHEMISTRY_2E: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.SCIENCE],
                self.CHEGG: False,
                self.COMP_COPY: False,
                self.DETAILS: 'chemistry-2e',
                self.HAS_I_LOCK: True,
                self.HAS_I_UNLOCK: True,
                self.HAS_S_LOCK: True,
                self.HAS_S_UNLOCK: True,
                self.INTEREST: 'Chemistry',
                self.IS_AP: False,
                self.ITUNES: False,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.PRE_RELEASE: False,
                self.PRINT_COPY: True,
                self.SHORT_NAME: 'Chemistry', },
            self.CHEM_ATOMS_2E: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.SCIENCE],
                self.CHEGG: False,
                self.COMP_COPY: False,
                self.DETAILS: 'chemistry-atoms-first-2e',
                self.HAS_I_LOCK: True,
                self.HAS_I_UNLOCK: True,
                self.HAS_S_LOCK: True,
                self.HAS_S_UNLOCK: True,
                self.INTEREST: r'Chem%3A%20Atoms%20First',
                self.IS_AP: False,
                self.ITUNES: False,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.PRE_RELEASE: False,
                self.PRINT_COPY: True,
                self.SHORT_NAME: 'Chemistry: Atoms First', },
            self.PHYSICS: {
                self.BOOKSHARE: True,
                self.CATEGORY: [self.ALL, self.SCIENCE],
                self.CHEGG: False,
                self.COMP_COPY: False,
                self.DETAILS: 'college-physics',
                self.HAS_I_LOCK: True,
                self.HAS_I_UNLOCK: True,
                self.HAS_S_LOCK: True,
                self.HAS_S_UNLOCK: True,
                self.INTEREST: 'College%20Physics%20(Algebra)',
                self.IS_AP: False,
                self.ITUNES: True,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.PRE_RELEASE: False,
                self.PRINT_COPY: True,
                self.SHORT_NAME: 'College Physics', },
            self.AP_PHYS: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.AP, self.SCIENCE],
                self.CHEGG: False,
                self.COMP_COPY: True,
                self.DETAILS: 'college-physics-ap-courses',
                self.HAS_I_LOCK: True,
                self.HAS_I_UNLOCK: True,
                self.HAS_S_LOCK: True,
                self.HAS_S_UNLOCK: True,
                self.INTEREST: 'AP%20Physics',
                self.IS_AP: True,
                self.ITUNES: True,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.PRE_RELEASE: False,
                self.PRINT_COPY: True,
                self.SHORT_NAME: 'AP Physics', },
            self.BIO_CONCEPTS: {
                self.BOOKSHARE: True,
                self.CATEGORY: [self.ALL, self.SCIENCE],
                self.CHEGG: True,
                self.COMP_COPY: False,
                self.DETAILS: 'concepts-biology',
                self.HAS_I_LOCK: True,
                self.HAS_I_UNLOCK: True,
                self.HAS_S_LOCK: True,
                self.HAS_S_UNLOCK: True,
                self.INTEREST: r'Concepts%20of%20Bio%20(non-majors)',
                self.IS_AP: False,
                self.ITUNES: True,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.PRE_RELEASE: False,
                self.PRINT_COPY: True,
                self.SHORT_NAME: 'Concepts of Biology', },
            self.FIZYKA_1: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.SCIENCE],
                self.CHEGG: False,
                self.COMP_COPY: False,
                self.DETAILS: r'fizyka-dla-szkół-wyższych-tom-1',
                self.HAS_I_LOCK: False,
                self.HAS_I_UNLOCK: False,
                self.HAS_S_LOCK: False,
                self.HAS_S_UNLOCK: False,
                self.INTEREST: None,
                self.IS_AP: False,
                self.ITUNES: False,
                self.KINDLE: False,
                self.LANGUAGE: self.POLISH,
                self.PRE_RELEASE: False,
                self.PRINT_COPY: False,
                self.SHORT_NAME: None, },
            self.FIZYKA_2: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.SCIENCE],
                self.CHEGG: False,
                self.COMP_COPY: False,
                self.DETAILS: r'fizyka-dla-szkół-wyższych-tom-2',
                self.HAS_I_LOCK: False,
                self.HAS_I_UNLOCK: False,
                self.HAS_S_LOCK: False,
                self.HAS_S_UNLOCK: False,
                self.INTEREST: None,
                self.IS_AP: False,
                self.ITUNES: False,
                self.KINDLE: False,
                self.LANGUAGE: self.POLISH,
                self.PRE_RELEASE: False,
                self.PRINT_COPY: False,
                self.SHORT_NAME: None, },
            self.FIZYKA_3: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.SCIENCE],
                self.CHEGG: False,
                self.COMP_COPY: False,
                self.DETAILS: r'fizyka-dla-szkół-wyższych-tom-3',
                self.HAS_I_LOCK: False,
                self.HAS_I_UNLOCK: False,
                self.HAS_S_LOCK: False,
                self.HAS_S_UNLOCK: False,
                self.INTEREST: None,
                self.IS_AP: False,
                self.ITUNES: False,
                self.KINDLE: False,
                self.LANGUAGE: self.POLISH,
                self.PRE_RELEASE: False,
                self.PRINT_COPY: False,
                self.SHORT_NAME: None, },
            self.MICROBIOLOGY: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.SCIENCE],
                self.CHEGG: True,
                self.COMP_COPY: True,
                self.DETAILS: 'microbiology',
                self.HAS_I_LOCK: True,
                self.HAS_I_UNLOCK: True,
                self.HAS_S_LOCK: False,
                self.HAS_S_UNLOCK: True,
                self.INTEREST: 'Microbiology',
                self.IS_AP: False,
                self.ITUNES: True,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.PRE_RELEASE: False,
                self.PRINT_COPY: True,
                self.SHORT_NAME: 'Microbiology', },
            self.U_PHYS_1: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.SCIENCE],
                self.CHEGG: False,
                self.COMP_COPY: True,
                self.DETAILS: 'university-physics-volume-1',
                self.HAS_I_LOCK: True,
                self.HAS_I_UNLOCK: True,
                self.HAS_S_LOCK: True,
                self.HAS_S_UNLOCK: True,
                self.INTEREST: 'University%20Physics%20(Calc)',
                self.IS_AP: False,
                self.ITUNES: True,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.PRE_RELEASE: False,
                self.PRINT_COPY: True,
                self.SHORT_NAME: 'University Physics', },
            self.U_PHYS_2: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.SCIENCE],
                self.CHEGG: False,
                self.COMP_COPY: True,
                self.DETAILS: 'university-physics-volume-2',
                self.HAS_I_LOCK: True,
                self.HAS_I_UNLOCK: True,
                self.HAS_S_LOCK: True,
                self.HAS_S_UNLOCK: True,
                self.INTEREST: 'University%20Physics%20(Calc)',
                self.IS_AP: False,
                self.ITUNES: True,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.PRE_RELEASE: False,
                self.PRINT_COPY: True,
                self.SHORT_NAME: 'University Physics', },
            self.U_PHYS_3: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.SCIENCE],
                self.CHEGG: False,
                self.COMP_COPY: True,
                self.DETAILS: 'university-physics-volume-3',
                self.HAS_I_LOCK: True,
                self.HAS_I_UNLOCK: True,
                self.HAS_S_LOCK: True,
                self.HAS_S_UNLOCK: True,
                self.INTEREST: 'University%20Physics%20(Calc)',
                self.IS_AP: False,
                self.ITUNES: True,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.PRE_RELEASE: False,
                self.PRINT_COPY: True,
                self.SHORT_NAME: 'University Physics', },

            # Social Sciences
            self.AP_MACRO: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.AP, self.SOCIAL],
                self.CHEGG: False,
                self.COMP_COPY: False,
                self.DETAILS: 'principles-macroeconomics-ap-courses-2e',
                self.HAS_I_LOCK: True,
                self.HAS_I_UNLOCK: True,
                self.HAS_S_LOCK: False,
                self.HAS_S_UNLOCK: True,
                self.INTEREST: r'AP%20Macro%20Econ',
                self.IS_AP: True,
                self.ITUNES: False,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.PRE_RELEASE: False,
                self.PRINT_COPY: False,
                self.SHORT_NAME: 'AP Macro Econ', },
            self.AP_MICRO: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.AP, self.SOCIAL],
                self.CHEGG: False,
                self.COMP_COPY: False,
                self.DETAILS: 'principles-microeconomics-ap-courses-2e',
                self.HAS_I_LOCK: True,
                self.HAS_I_UNLOCK: True,
                self.HAS_S_LOCK: False,
                self.HAS_S_UNLOCK: True,
                self.INTEREST: r'AP%20Micro%20Econ',
                self.IS_AP: True,
                self.ITUNES: False,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.PRE_RELEASE: False,
                self.PRINT_COPY: False,
                self.SHORT_NAME: 'AP Micro Econ', },
            self.GOVERNMENT_2E: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.SOCIAL],
                self.CHEGG: False,
                self.COMP_COPY: False,
                self.DETAILS: 'american-government-2e',
                self.HAS_I_LOCK: True,
                self.HAS_I_UNLOCK: True,
                self.HAS_S_LOCK: False,
                self.HAS_S_UNLOCK: True,
                self.INTEREST: r'American%20Government',
                self.IS_AP: False,
                self.ITUNES: False,
                self.KINDLE: False,
                self.LANGUAGE: self.ENGLISH,
                self.PRE_RELEASE: False,
                self.PRINT_COPY: True,
                self.SHORT_NAME: 'American Government', },
            self.PRINCIPLES_ECON: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.SOCIAL],
                self.CHEGG: False,
                self.COMP_COPY: True,
                self.DETAILS: 'principles-economics-2e',
                self.HAS_I_LOCK: True,
                self.HAS_I_UNLOCK: True,
                self.HAS_S_LOCK: False,
                self.HAS_S_UNLOCK: True,
                self.INTEREST: 'Economics',
                self.IS_AP: False,
                self.ITUNES: True,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.PRE_RELEASE: False,
                self.PRINT_COPY: True,
                self.SHORT_NAME: 'Principles of Economics', },
            self.PRINCIPLES_MACRO: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.SOCIAL],
                self.CHEGG: False,
                self.COMP_COPY: True,
                self.DETAILS: 'principles-macroeconomics-2e',
                self.HAS_I_LOCK: True,
                self.HAS_I_UNLOCK: True,
                self.HAS_S_LOCK: False,
                self.HAS_S_UNLOCK: True,
                self.INTEREST: r'Principles%20of%20Macroeconomics',
                self.IS_AP: False,
                self.ITUNES: True,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.PRE_RELEASE: False,
                self.PRINT_COPY: True,
                self.SHORT_NAME: 'Principles of Macroeconomics', },
            self.PRINCIPLES_MICRO: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.SOCIAL],
                self.CHEGG: False,
                self.COMP_COPY: True,
                self.DETAILS: 'principles-microeconomics-2e',
                self.HAS_I_LOCK: True,
                self.HAS_I_UNLOCK: True,
                self.HAS_S_LOCK: False,
                self.HAS_S_UNLOCK: True,
                self.INTEREST: r'Micro%20Econ',
                self.IS_AP: False,
                self.ITUNES: True,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.PRE_RELEASE: False,
                self.PRINT_COPY: True,
                self.SHORT_NAME: 'Principles of Microeconomics', },
            self.PSYCHOLOGY: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.SOCIAL],
                self.CHEGG: True,
                self.COMP_COPY: False,
                self.DETAILS: 'psychology',
                self.HAS_I_LOCK: True,
                self.HAS_I_UNLOCK: True,
                self.HAS_S_LOCK: True,
                self.HAS_S_UNLOCK: True,
                self.INTEREST: 'Psychology',
                self.IS_AP: False,
                self.ITUNES: True,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.PRE_RELEASE: False,
                self.PRINT_COPY: True,
                self.SHORT_NAME: 'Psychology', },
            self.SOCIOLOGY: {
                self.BOOKSHARE: False,
                self.CATEGORY: [self.ALL, self.SOCIAL],
                self.CHEGG: True,
                self.COMP_COPY: False,
                self.DETAILS: 'introduction-sociology-2e',
                self.HAS_I_LOCK: True,
                self.HAS_I_UNLOCK: True,
                self.HAS_S_LOCK: True,
                self.HAS_S_UNLOCK: True,
                self.INTEREST: 'Introduction%20to%20Sociology',
                self.IS_AP: False,
                self.ITUNES: True,
                self.KINDLE: True,
                self.LANGUAGE: self.ENGLISH,
                self.PRE_RELEASE: False,
                self.PRINT_COPY: True,
                self.SHORT_NAME: 'Introduction to Sociology 2e', },
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
    def available(self):
        """Return the available book.

        Not pre-release

        """
        return [(book, self.get(book))
                for book
                in self.books
                if (not self.get(book, self.PRE_RELEASE) and
                    self.get(book, self.LANGUAGE) == self.ENGLISH)]

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
    def chegg(self):
        """Return the books available through Chegg."""
        return [(book, self.get(book)) for book in self.books
                if self.get(book, self.CHEGG)]

    @property
    def coming_soon(self):
        """Return the pre-release books."""
        return [(book, self.get(book)) for book in self.books
                if self.get(book, self.PRE_RELEASE)]

    @property
    def comp_copy(self):
        """Return books with available complimentary copies."""
        return [(book, self.get(book)) for book in self.books
                if self.get(book, self.COMP_COPY)]

    @property
    def current(self):
        """Return the current edition of each book."""
        return [(book, self.get(book)) for book in self.books
                if book not in self.OLD_EDITIONS]

    @property
    def essentials(self):
        """Return the essentials books."""
        return self.get_by_category(self.ESSENTIALS)

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
    def locked_instructor(self):
        """Return the books with locked instructor resources."""
        return [(book, self.get(book)) for book in self.books
                if self.get(book, self.HAS_I_LOCK)]

    @property
    def locked_student(self):
        """Return the books with locked student resources."""
        return [(book, self.get(book)) for book in self.books
                if self.get(book, self.HAS_S_LOCK)]

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
    def print(self):
        """Return the books offering a print edition."""
        return [(book, self.get(book)) for book in self.books
                if self.get(book, self.PRINT_COPY)]

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

    @property
    def unlocked_instructor(self):
        """Return the books with unlocked instructor resources."""
        return [(book, self.get(book)) for book in self.books
                if self.get(book, self.HAS_I_UNLOCK)]

    @property
    def unlocked_student(self):
        """Return the books with unlocked student resources."""
        return [(book, self.get(book)) for book in self.books
                if self.get(book, self.HAS_S_UNLOCK)]

    def book_passthrough(self, using):
        """Return the Subjects book name and form append for a book set."""
        return [(book, self.get(book, self.INTEREST)) for book in using]

    def get(self, book, field=None):
        """Return the field or fields for a specific book."""
        alts = {self.ANATOMY_PHYS_ALT: self.ANATOMY_PHYS,
                self.AP_PHYS_ALT: self.AP_PHYS,
                self.AP_PHYS_ALT_2: self.AP_PHYS,
                self.AP_BIO_ALT: self.AP_BIO,
                self.ACCOUNTING_1_ALT: self.ACCOUNTING_1,
                self.ACCOUNTING_2_ALT: self.ACCOUNTING_2,
                self.MANAGEMENT_ALT: self.MANAGEMENT,
                self.U_PHYS_ALT: self.U_PHYS_1, }

        if book in alts:  # Is the book using an altered title?
            return_book = self.books.get(alts[book])
        else:  # Try to get the book information
            return_book = self.books.get(book)
        if return_book is None:  # Retrieval failed; is it a second edition?
            return_book = self.books.get(book + ' 2e')
        if return_book is None:  # Retrieval failed; not a second edition...
            raise WebException(f'{book} not found in the library')

        # Book found...
        if field:  # return the requested field value.
            return return_book.get(field)
        return return_book  # return all of the book's field values.

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
        if isinstance(using, list):
            using = using[0][1]
        return (using,
                using.get(self.SHORT_NAME),
                book,
                using.get(self.DETAILS))

    def get_titles(self, group=None):
        """Return a list of book titles."""
        collection = group if group else self.books
        return [book[0] for book in collection]

    def random_book(self, number=1, short_name=True, full_name=False):
        """Return a list of random book short names."""
        if short_name and not full_name:
            return Utility.random_set(self.short_names, number)
        if full_name:
            group = Utility.random_set(self.openstax, number)
            names = []
            for book in group:
                names.append(book[0])
            return names[0] if len(names) == 1 else names
        return Utility.random_set(self.available, number)


class WebException(WebDriverException):
    """A generic exception for the OpenStax website."""

    pass
