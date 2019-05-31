"""A term and definition selector for OpenStax Tutor Beta books."""

from __future__ import annotations

from random import randint
from typing import Tuple

Term = Tuple[str, str]


class BookIndexError(IndexError):
    """A error for when a book section index is not found."""

    pass


class OpenStaxBook(object):
    """An index of book terms for use in free response questions."""

    @property
    def book_title(self) -> str:
        """Return the book title."""
        return self._book_title

    def get_term(self, section: str) -> Term:
        """Return a random term and definition from a specific section.

        :param str section: the book section to pull a term from
        :return: a book term and definition
        :rtype: tuple(str, str)

        :raises :py:class:`~utils.bookterm.BookIndexError`: if the section
            number does not exist within the book or the requested section does
            not contain any defined terms

        """
        terms = self._terms.get(section)
        if not terms:
            raise BookIndexError('No terms found in section {0} of {1}'
                                 .format(section, self.book_title))
        keys = self._terms.get(section).keys()
        term = keys[randint(0, len(keys) - 1)]
        return (term, terms.get(term))

    def get_random_term(self) -> Term:
        """Return a random term and definition from the book.

        :return: a book term and definition
        :rtype: tuple(str, str)

        """
        sections = self._terms.keys()
        section = sections[randint(0, len(sections) - 1)]
        return self.get_term(section)


class Biology2e(OpenStaxBook):
    """Biology 2e."""

    def __init__(self) -> None:
        """Initialize the term group."""
        self._book_title = "Biology 2e"
        self._terms = {
            # TODO - add the biology book terms
        }


class CollegePhysics(OpenStaxBook):
    """College Physics."""

    def __init__(self) -> None:
        """Initialize the term group."""
        self._book_title = "College Physics"
        self._terms = {
            "1.1": {
                "classical physics":
                    "physics that was developed from the Renaissance to the "
                    "end of the 19th century",
                "law":
                    "a description, using concise language or a mathematical "
                    "formula, a generalized pattern in nature that is "
                    "supported by scientific evidence and repeated "
                    "experiments",
                "model":
                    "representation of something that is often too difficult "
                    "(or impossible) to display directly",
                "modern physics":
                    "the study of relativity, quantum mechanics, or both",
                "physics":
                    "the science concerned with describing the interactions "
                    "of energy, matter, space, and time; it is especially "
                    "interested in what fundamental mechanisms underlie every "
                    "phenomenon",
                "quantum mechanics":
                    "the study of objects smaller than can be seen with a "
                    "microscope",
                "relativity":
                    "the study of objects moving at speeds greater than about "
                    r"1% of the speed of light, or of objects being affected "
                    "by a strong gravitational field",
                "scientific method":
                    "a method that typically begins with an observation and "
                    "question that the scientist will research; next, the "
                    "scientist typically performs some research about the "
                    "topic and then devises a hypothesis; then, the scientist "
                    "will test the hypothesis by performing an experiment; "
                    "finally, the scientist analyzes the results of the "
                    "experiment and draws a conclusion",
                "theory":
                    "an explanation for patterns in nature that is supported "
                    "by scientific evidence and verified multiple times by "
                    "various groups of researchers", },
            "1.2": {
                "conversion factor":
                    "a ratio expressing how many of one unit are equal to "
                    "another unit",
                "derived units":
                    "units that can be calculated using algebraic "
                    "combinations of the fundamental units",
                "English units":
                    "system of measurement used in the United States; "
                    "includes units of measurement such as feet, gallons, and "
                    "pounds",
                "fundamental units":
                    "units that can only be expressed relative to the "
                    "procedure used to measure them",
                "kilogram":
                    "the SI unit for mass, abbreviated (kg)",
                "meter":
                    "the SI unit for length, abbreviated (m)",
                "metric system":
                    "a system in which values can be calculated in factors of "
                    "10",
                "order of magnitude":
                    "refers to the size of a quantity as it relates to a "
                    "power of 10",
                "physical quantity":
                    "a characteristic or property of an object that can be "
                    "measured or calculated from other measurements",
                "second":
                    "the SI unit for time, abbreviated (s)",
                "SI units":
                    "the international system of units that scientists in "
                    "most countries have agreed to use; includes units such "
                    "as meters, liters, and grams",
                "units":
                    "a standard used for expressing and comparing "
                    "measurements", },
            "1.3": {
                "accuracy":
                    "the degree to which a measured value agrees with correct "
                    "value for that measurement",
                "method of adding percents":
                    "the percent uncertainty in a quantity calculated by "
                    "multiplication or division is the sum of the percent "
                    "uncertainties in the items used to make the calculation",
                "percent uncertainty":
                    "the ratio of the uncertainty of a measurement to the "
                    "measured value, expressed as a percentage",
                "precision":
                    "the degree to which repeated measurements agree with "
                    "each other",
                "significant figures":
                    "express the precision of a measuring tool used to "
                    "measure a value",
                "uncertainty":
                    "a quantitative measure of how much your measured values "
                    "deviate from a standard or expected value", },
            "1.4": {
                "approximation":
                    "an estimated value based on prior experience and "
                    "reasoning", },
            "2": {
                "kinematics":
                    "the study of motion without considering its causes", },
            "2.1": {
                "displacement":
                    "the change in position of an object",
                "distance":
                    "the magnitude of displacement between two positions",
                "distance traveled":
                    "the total length of the path traveled between two "
                    "positions",
                "position":
                    "the location of an object at a particular time", },
            "2.2": {
                "scalar":
                    "a quantity that is described by magnitude, but not "
                    "direction",
                "vector":
                    "a quantity that is described by both magnitude and "
                    "direction", },
            "2.3": {
                "average speed":
                    "distance traveled divided by time during which motion "
                    "occurs",
                "average velocity":
                    "displacement divided by time over which displacement "
                    "occurs",
                "elapsed time":
                    "the difference between the ending time and beginning "
                    "time",
                "instantaneous speed":
                    "magnitude of the instantaneous velocity",
                "instantaneous velocity":
                    "velocity at a specific instant, or the average velocity "
                    "over an infinitesimal time interval",
                "model":
                    "simplified description that contains only those elements "
                    "necessary to describe the physics of a physical "
                    "situation",
                "time":
                    "change, or the interval over which change occurs", },
            "2.4": {
                "acceleration":
                    "the rate of change in velocity; the change in velocity "
                    "over time",
                "average acceleration":
                    "the change in velocity divided by the time over which it "
                    "changes",
                "deceleration":
                    "acceleration in the direction opposite to velocity; "
                    "acceleration that results in a decrease in velocity",
                "instantaneous acceleration":
                    "acceleration at a specific point in time", },
            "2.7": {
                "acceleration due to gravity":
                    "acceleration of an object as a result of gravity",
                "free-fall":
                    "the state of movement that results from gravitational "
                    "force only", },
            "2.8": {
                "dependent variable":
                    "the variable that is being measured; usually plotted "
                    "along the y-axis",
                "independent variable":
                    "the variable that the dependent variable is measured "
                    "with respect to; usually plotted along the x-axis",
                "slope":
                    "the difference in y-value (the rise) divided by the "
                    "difference in x-value (the run) of two points on a "
                    "straight line",
                "y-intercept":
                    "the y-value when x=0, or when the graph crosses the "
                    "y-axis", },
            "3.2": {
                "commutative":
                    "refers to the interchangeability of order in a function; "
                    "vector addition is commutative because the order in "
                    "which vectors are added together does not affect the "
                    "final sum",
                "component (of a 2-d vector)":
                    "a piece of a vector that points in either the vertical "
                    "or the horizontal direction; every 2-d vector can be "
                    "expressed as a sum of two vertical and horizontal vector "
                    "components",
                "direction (of a vector)":
                    "the orientation of a vector in space",
                "head (of a vector)":
                    "the end point of a vector; the location of the tip of "
                    "the vector’s arrowhead; also referred to as the “tip”",
                "head-to-tail method":
                    "a method of adding vectors in which the tail of each "
                    "vector is placed at the head of the previous vector",
                "magnitude (of a vector)":
                    "the length or size of a vector; magnitude is a scalar "
                    "quantity",
                "resultant":
                    "the sum of two or more vectors",
                "resultant vector":
                    "the vector sum of two or more vectors",
                "scalar":
                    "a quantity with magnitude but no direction",
                "tail":
                    "the start point of a vector; opposite to the head or tip "
                    "of the arrow",
                "vector":
                    "a quantity that has both magnitude and direction; an "
                    "arrow used to represent quantities with both magnitude "
                    "and direction", },
            "3.3": {
                "analytical methods":
                    "the method of determining the magnitude and direction "
                    "of a resultant vector using the Pythagorean theorem and "
                    "trigonometric identities", },
            "3.4": {
                "air resistance":
                    "a frictional force that slows the motion of objects as "
                    "they travel through the air; when solving basic physics "
                    "problems, air resistance is assumed to be zero",
                "kinematics":
                    "the study of motion without regard to mass or force",
                "motion":
                    "displacement of an object as a function of time",
                "projectile":
                    "an object that travels through the air and experiences "
                    "only acceleration due to gravity",
                "projectile motion":
                    "the motion of an object that is subject only to the "
                    "acceleration of gravity",
                "range":
                    "the maximum horizontal distance that a projectile "
                    "travels",
                "trajectory":
                    "the path of a projectile through the air", },
            "3.5": {
                "classical relativity":
                    "the study of relative velocities in situations where "
                    r"speeds are less than about 1% of the speed of light—"
                    "that is, less than 3000 km/s",
                "relative velocities":
                    "the velocity of an object as observed from a particular "
                    "reference frame",
                "relativity":
                    "the study of how different observers moving relative to "
                    "each other measure the same phenomenon",
                "vector addition":
                    "the rules that apply to adding vectors together",
                "velocity":
                    "speed in a given direction", },
            "4.1": {
                "dynamics":
                    "the study of how forces affect the motion of objects and "
                    "systems",
                "force":
                    "a push or pull on an object with a specific magnitude "
                    "and direction; can be represented by vectors; can be "
                    "expressed as a multiple of a standard force",
                "free-body diagram":
                    "a sketch showing all of the external forces acting on an "
                    "object or system; the system is represented by a dot, "
                    "and the forces are represented by vectors extending "
                    "outward from the dot", },
            "4.2": {
                "inertia":
                    "the tendency of an object to remain at rest or remain in "
                    "motion",
                "law of inertia":
                    "see Newton’s first law of motion",
                "mass":
                    "the quantity of matter in a substance; measured in "
                    "kilograms",
                "Newton’s first law of motion":
                    "a body at rest remains at rest, or, if in motion, "
                    "remains in motion at a constant velocity unless acted on "
                    "by a net external force; also known as the law of "
                    "inertia", },
            "4.3": {
                "acceleration":
                    "the rate at which an object’s velocity changes over a "
                    "period of time",
                "external force":
                    "a force acting on an object or system that originates "
                    "outside of the object or system",
                "free-fall":
                    "a situation in which the only force acting on an object "
                    "is the force due to gravity",
                "friction":
                    "a force past each other of objects that are touching; "
                    "examples include rough surfaces and air resistance",
                "net external force":
                    "the vector sum of all external forces acting on an "
                    "object or system; causes a mass to accelerate",
                "newton":
                    "the SI unit of force (abbreviated N); the force needed "
                    "to accelerate a 1-kg system at the rate of  1 m/s²",
                "Newton’s second law of motion":
                    "the net external force F_net on an object with mass m is "
                    "proportional to and in the same direction as the "
                    "acceleration of the object, a, and inversely "
                    "proportional to the mass; defined mathematically as "
                    "a=F_net/m",
                "system":
                    "defined by the boundaries of an object or collection of "
                    "objects being observed; all forces originating from "
                    "outside of the system are considered external forces",
                "weight":
                    "the force w due to gravity acting on an object of mass "
                    "m; defined mathematically as: w=mg, where g is the "
                    "magnitude and direction of the acceleration due to "
                    "gravity", },
            "4.4": {
                "Newton’s third law of motion":
                    "whenever one body exerts a force on a second body, the "
                    "first body experiences a force that is equal in "
                    "magnitude and opposite in direction to the force that "
                    "the first body exerts",
                "thrust":
                    "a reaction force that pushes a body forward in response "
                    "to a backward force; rockets, airplanes, and cars are "
                    "pushed forward by a thrust reaction force", },
            "4.5": {
                "inertial frame of reference":
                    "a coordinate system that is not accelerating; all forces "
                    "acting in an inertial frame of reference are real "
                    "forces, as opposed to fictitious forces that are "
                    "observed due to an accelerating frame of reference",
                "normal force":
                    "the force that a surface applies to an object to support "
                    "the weight of the object; acts perpendicular to the "
                    "surface on which the object rests",
                "tension":
                    "the pulling force that acts along a medium, especially a "
                    "stretched flexible connector, such as a rope or cable; "
                    "when a rope supports the weight of an object, the force "
                    "on the object due to the rope is called a tension "
                    "force", },
            "4.8": {
                "carrier particles":
                    "a fundamental particle of nature that is surrounded by a "
                    "characteristic force field; photons are carrier "
                    "particles of the electromagnetic force",
                "force field":
                    "a region in which a test particle will experience a "
                    "force", },
            "5.1": {
                "friction":
                    "a force that opposes relative motion or attempts at "
                    "motion between systems in contact",
                "kinetic friction":
                    "a force that opposes the motion of two systems that are "
                    "in contact and moving relative to one another",
                "magnitude of kinetic friction":
                    "f_k=μ_k N , where μ_k is the coefficient of kinetic "
                    "friction",
                "magnitude of static friction":
                    "f_s≤μ_s N, where μ_s is the coefficient of static "
                    "friction and N is the magnitude of the normal force",
                "static friction":
                    "a force that opposes the motion of two systems that are "
                    "in contact and are not moving relative to one another", },
            "5.2": {
                "drag force":
                    "F_D, found to be proportional to the square of the speed "
                    "of the object; mathematically F_D ∝ v²; F_D=½ C_ρ A v², "
                    "where C is the drag coefficient, A is the area of the "
                    "object facing the fluid, and ρ is the density of the "
                    "fluid",
                "Stokes’ law":
                    "Fs=6πrηv, where r is the radius of the object, η is the "
                    "viscosity of the fluid, and v is the object’s "
                    "velocity", },
            "5.3": {
                "deformation":
                    "change in shape due to the application of force",
                "Hooke’s law":
                    "proportional relationship between the force F on a "
                    "material and the deformation ΔL it causes, F=kΔL",
                "shear deformation":
                    "deformation perpendicular to the original length of an "
                    "object",
                "strain":
                    "ratio of change in length to original length",
                "stress":
                    "ratio of force to area",
                "Tensile strength":
                    "the breaking stress that will cause permanent "
                    "deformation or fraction of a material", },
            "6": {
                "uniform circular motion":
                    "the motion of an object in a circular path at constant "
                    "speed", },
            "6.1": {
                "angular velocity":
                    "ω, the rate of change of the angle with which an object "
                    "moves on a circular path",
                "arc length":
                    "Δs, the distance traveled by an object along a circular "
                    "path",
                "pit":
                    "a tiny indentation on the spiral track moulded into the "
                    "top of the polycarbonate layer of CD",
                "radians":
                    "a unit of angle measurement",
                "radius of curvature":
                    "radius of a circular path",
                "rotation angle":
                    "the ratio of the arc length to the radius of curvature "
                    "on a circular path: Δθ=Δs/r", },
            "6.2": {
                "centrifuge":
                    "a machine with a rapidly rotating container that applies "
                    "centrifugal force to its contents, typically to separate "
                    "fluids of different densities or liquids from solids",
                "centripetal acceleration":
                    "the acceleration of an object moving in a circle, "
                    "directed toward the center",
                "ultracentrifuge":
                    "a centrifuge optimized for spinning a rotor at very high "
                    "speeds", },
            "6.3": {
                "banked curves":
                    "the curve in a road that is sloping in a manner that "
                    "helps a vehicle negotiate the curve",
                "centripetal force":
                    "any net force causing uniform circular motion",
                "ideal angle":
                    "the angle at which a car can turn safely on a steep "
                    "curve, which is in proportion to the ideal speed",
                "ideal banking":
                    "the sloping of a curve in a road, where the angle of the "
                    "slope allows the vehicle to negotiate the curve at a "
                    "certain speed without the aid of friction between the "
                    "tires and the road; the net external force on the "
                    "vehicle equals the horizontal centripetal force in the "
                    "absence of friction",
                "ideal speed":
                    "the maximum safe speed at which a vehicle can turn on a "
                    "curve without the aid of friction between the tire and "
                    "the road", },
            "6.4": {
                "centrifugal force":
                    "a fictitious force that tends to throw an object off "
                    "when the object is rotating in a non-inertial frame of "
                    "reference",
                "Coriolis force":
                    "the fictitious force causing the apparent deflection of "
                    "moving objects when viewed in a rotating frame of "
                    "reference",
                "fictitious force":
                    "a force having no physical origin",
                "non-inertial frame of reference":
                    "an accelerated frame of reference", },
            "6.5": {
                "center of mass":
                    "the point where the entire mass of an object can be "
                    "thought to be concentrated",
                "gravitational constant":
                    "a proportionality factor used in the equation for "
                    "Newton’s universal law of gravitation; it is a universal "
                    "constant—that is, it is thought to be the same "
                    "everywhere in the universe",
                "microgravity":
                    "an environment in which the apparent net acceleration of "
                    "a body is small compared with that produced by Earth at "
                    "its surface",
                "Newton’s universal law of gravitation":
                    "every particle in the universe attracts every other "
                    "particle with a force along a line joining them; the "
                    "force is directly proportional to the product of their "
                    "masses and inversely proportional to the square of the "
                    "distance between them", },
            "7": {
                "conservation of energy":
                    "energy can neither be created nor destroyed",
                "energy":
                    "the ability to do work", },
            "7.1": {
                "joule":
                    "SI unit of work and energy, equal to one newton-meter",
                "newton-meters":
                    "a unit of torque in the SI system; one newton metre is "
                    "equal to the torque resulting from a force of one newton "
                    "applied perpendicularly to the end of a moment arm that "
                    "is one metre long",
                "work":
                    "the transfer of energy by a force that causes an object "
                    "to be displaced; the product of the component of the "
                    "force in the direction of the displacement and the "
                    "magnitude of the displacement", },
            "7.2": {
                "kinetic energy":
                    "the energy an object has by reason of its motion, equal "
                    "to ½mv² for the translational (i.e., non-rotational) "
                    "motion of an object of mass m moving at speed v",
                "net work":
                    "work done by the net force, or vector sum of all the "
                    "forces, acting on an object",
                "work-energy theorem":
                    "the result, based on Newton’s laws, that the net work "
                    "done on an object is equal to its change in kinetic "
                    "energy", },
            "7.3": {
                "gravitational potential energy":
                    "the energy an object has due to its position in a "
                    "gravitational field", },
            "7.4": {
                "conservation of mechanical energy":
                    "the rule that the sum of the kinetic energies and "
                    "potential energies remains constant if only conservative "
                    "forces act on and within a system",
                "conservative force":
                    "a force that does the same work for any given initial "
                    "and final configuration, regardless of the path followed",
                "mechanical energy":
                    "the sum of kinetic energy and potential energy",
                "potential energy":
                    "energy due to position, shape, or configuration",
                "potential energy of a spring":
                    "the stored energy of a spring as a function of its "
                    "displacement; when Hooke’s law applies, it is given by "
                    "the expression ½kx² where x is the distance the spring "
                    "is compressed or extended and k is the spring "
                    "constant", },
            "7.5": {
                "friction":
                    "the force between surfaces that opposes one sliding on "
                    "the other; friction changes mechanical energy into "
                    "thermal energy",
                "nonconservative force":
                    "a force whose work depends on the path followed between "
                    "the given initial and final configurations",
                "thermal energy":
                    "the energy within an object due to the random motion of "
                    "its atoms and molecules that accounts for the object's "
                    "temperature", },
            "7.6": {
                "chemical energy":
                    "the energy in a substance stored in the bonds between "
                    "atoms and molecules that can be released in a chemical "
                    "reaction",
                "efficiency":
                    "a measure of the effectiveness of the input of energy to "
                    "do work; useful energy or work divided by the total "
                    "input of energy",
                "electrical energy":
                    "the energy carried by a flow of charge",
                "law of conservation of energy":
                    "the general law that total energy is constant in any "
                    "process; energy may change in form or be transferred "
                    "from one system to another, but the total remains the "
                    "same",
                "nuclear energy":
                    "energy released by changes within atomic nuclei, such as "
                    "the fusion of two light nuclei or the fission of a heavy "
                    "nucleus",
                "radiant energy":
                    "the energy carried by electromagnetic waves", },
            "7.7": {
                "horsepower":
                    "an older non-SI unit of power, with 1 hp=746 W",
                "kilowatt-hours":
                    "(kW⋅h) unit used primarily for electrical energy "
                    "provided by electric utility companies",
                "power":
                    "the rate at which work is done",
                "watt":
                    "(W) SI unit of power, with 1 W=1 J/s", },
            "7.8": {
                "basal metabolic rate":
                    "the total energy conversion rate of a person at rest",
                "metabolic rate":
                    "the rate at which the body uses food energy to sustain "
                    "life and to do different activities",
                "useful work":
                    "work done on an external system", },
            "7.9": {
                "fossil fuels":
                    "oil, natural gas, and coal",
                "renewable forms of energy":
                    "those sources that cannot be used up, such as water, "
                    "wind, solar, and biomass", },
            "8.1": {
                "linear momentum":
                    "the product of mass and velocity",
                "second law of motion":
                    "physical law that states that the net external force "
                    "equals the change in momentum of a system divided by the "
                    "time over which it changes", },
            "8.2": {
                "change in momentum":
                    "the difference between the final and initial momentum; "
                    "the mass times the change in velocity",
                "impulse":
                    "the average net external force times the time it acts; "
                    "equal to the change in momentum", },
            "8.3": {
                "conservation of momentum principle":
                    "when the net external force is zero, the total momentum "
                    "of the system is conserved or constant",
                "isolated system":
                    "a system in which the net external force is zero",
                "quarks":
                    "fundamental constituent of matter and an elementary "
                    "particle", },
            "8.4": {
                "elastic collision":
                    "a collision that also conserves internal kinetic energy",
                "Internal kinetic energy":
                    "the sum of the kinetic energies of the objects in a "
                    "system", },
            "8.5": {
                "inelastic collision":
                    "a collision in which internal kinetic energy is not "
                    "conserved",
                "perfectly inelastic collision":
                    "a collision in which the colliding objects stick "
                    "together", },
            "8.6": {
                "point masses":
                    "structureless particles with no rotation or spin", },
            "9.1": {
                "dynamic equilibrium":
                    "a state of equilibrium in which the net external force "
                    "and torque on a system moving with constant velocity "
                    "are zero",
                "static equilibrium":
                    "a state of equilibrium in which the net external force "
                    "and torque acting on a system is zero", },
            "9.2": {
                "center of gravity":
                    "the point where the total weight of the body is assumed "
                    "to be concentrated",
                "perpendicular lever arm":
                    "the shortest distance from the pivot point to the line "
                    "along which F lies",
                "SI unit of torque":
                    "newton times meters, usually written as N·m",
                "torque":
                    "turning or twisting effectiveness of a force", },
            "9.3": {
                "neutral equilibrium":
                    "a state of equilibrium that is independent of a system’s "
                    "displacements from its original position",
                "stable equilibrium":
                    "a system, when displaced, experiences a net force or "
                    "torque in a direction opposite to the direction of the "
                    "displacement",
                "unstable equilibrium":
                    "a system, when displaced, experiences a net force or "
                    "torque in the same direction as the displacement from "
                    "equilibrium", },
            "9.4": {
                "static equilibrium":
                    "equilibrium in which the acceleration of the system is "
                    "zero and accelerated rotation does not occur", },
            "9.5": {
                "mechanical advantage":
                    "the ratio of output to input forces for any simple "
                    "machine", },
            "10.1": {
                "angular acceleration":
                    "the rate of change of angular velocity with time",
                "change in angular velocity":
                    "the difference between final and initial values of "
                    "angular velocity",
                "tangential acceleration":
                    "the acceleration in a direction tangent to the circle at "
                    "the point of interest in circular motion", },
            "10.2": {
                "kinematics of rotational motion":
                    "describes the relationships among rotation angle, "
                    "angular velocity, angular acceleration, and time", },
            "10.3": {
                "moment of inertia":
                    "mass times the square of perpendicular distance from the "
                    "rotation axis; for a point mass, it is I=mr² and, "
                    "because any object can be built up from a collection of "
                    "point masses, this relationship is the basis for all "
                    "other moments of inertia",
                "rotational inertia":
                    "resistance to change of rotation. The more rotational "
                    "inertia an object has, the harder it is to rotate",
                "torque":
                    "the turning effectiveness of a force", },
            "10.4": {
                "rotational kinetic energy":
                    "the kinetic energy due to the rotation of an object. "
                    "This is part of its total kinetic energy",
                "work-energy theorem":
                    "if one or more external forces act upon a rigid object, "
                    "causing its kinetic energy to change from KE_1 to KE_2, "
                    "then the work W done by the net force is equal to the "
                    "change in kinetic energy", },
            "10.5": {
                "angular momentum":
                    "the product of moment of inertia and angular velocity",
                "law of conservation of angular momentum":
                    "angular momentum is conserved, i.e., the initial angular "
                    "momentum is equal to the final angular momentum when no "
                    "external torque is applied to the system", },
            "10.7": {
                "right-hand rule":
                    "direction of angular velocity ω and angular momentum L "
                    "in which the thumb of your right hand points when you "
                    "curl your fingers in the direction of the disk’s "
                    "rotation", },
            "11.1": {
                "fluids":
                    "liquids and gases; a fluid is a state of matter that "
                    "yields to shearing forces", },
            "11.2": {
                "density":
                    "the mass per unit volume of a substance or object", },
            "11.3": {
                "pressure":
                    "the force per unit area perpendicular to the force, over "
                    "which the force acts", },
            "11.4": {
                "pressure":
                    "the weight of the fluid divided by the area supporting "
                    "it", },
            "11.5": {
                "Pascal’s Principle":
                    "a change in pressure applied to an enclosed fluid is "
                    "transmitted undiminished to all portions of the fluid "
                    "and to the walls of its container", },
            "11.6": {
                "absolute pressure":
                    "the sum of gauge pressure and atmospheric pressure",
                "diastolic pressure":
                    "the minimum blood pressure in the artery",
                "gauge pressure":
                    "the pressure relative to atmospheric pressure",
                "systolic pressure":
                    "the maximum blood pressure in the artery", },
            "11.7": {
                "Archimedes’ principle":
                    "the buoyant force on an object equals the weight of the "
                    "fluid it displaces",
                "buoyant force":
                    "the net upward force on any object in any fluid",
                "specific gravity":
                    "the ratio of the density of an object to a fluid "
                    "(usually water)", },
            "11.8": {
                "adhesive forces":
                    "the attractive forces between molecules of different "
                    "types",
                "capillary action":
                    "the tendency of a fluid to be raised or lowered in a "
                    "narrow tube",
                "cohesive forces":
                    "the attractive forces between molecules of the same type",
                "contact angle":
                    "the angle θ between the tangent to the liquid surface "
                    "and the surface",
                "surface tension":
                    "the cohesive forces between molecules which cause the "
                    "surface of a liquid to contract to the smallest possible "
                    "surface area", },
            "11.9": {
                "diastolic pressure":
                    "minimum arterial blood pressure; indicator for the fluid "
                    "balance",
                "glaucoma":
                    "condition caused by the buildup of fluid pressure in the "
                    "eye",
                "intraocular pressure":
                    "fluid pressure in the eye",
                "micturition reflex":
                    "stimulates the feeling of needing to urinate, triggered "
                    "by bladder pressure",
                "systolic pressure":
                    "maximum arterial blood pressure; indicator for the blood "
                    "flow", },
            "12": {
                "fluid dynamics":
                    "the physics of fluids in motion", },
            "12.1": {
                "flow rate":
                    "abbreviated Q, it is the volume V that flows past a "
                    "particular point during a time t, or Q = V/t",
                "liter":
                    "a unit of volume, equal to 0.001 m³", },
            "12.2": {
                "Bernoulli’s equation":
                    "the equation resulting from applying conservation of "
                    "energy to an incompressible frictionless fluid: "
                    "P + ½pv² + pgh = constant , through the fluid",
                "Bernoulli’s principle":
                    "Bernoulli’s equation applied at constant depth: "
                    "P_1 + ½pv_1² = P_2 + ½pv_2²", },
            "12.4": {
                "laminar":
                    "a type of fluid flow in which layers do not mix",
                "Poiseuille’s law":
                    "the rate of laminar flow of an incompressible fluid in a "
                    "tube: Q = (P_2 − P_1)πr⁴/8ηl",
                "Poiseuille’s law for resistance":
                    "the resistance to laminar flow of an incompressible "
                    "fluid in a tube: R = 8ηl/πr⁴",
                "turbulence":
                    "fluid flow in which layers mix together via eddies and "
                    "swirls",
                "viscosity":
                    "the friction in a fluid, defined in terms of the "
                    "friction between layers", },
            "12.5": {
                "Reynolds number":
                    "a dimensionless parameter that can reveal whether a "
                    "particular flow is laminar or turbulent", },
            "12.6": {
                "terminal speed":
                    "the speed at which the viscous drag of an object falling "
                    "in a viscous fluid is equal to the other forces acting "
                    "on the object (such as gravity), so that the "
                    "acceleration of the object is zero",
                "viscous drag":
                    "a resistance force exerted on a moving object, with a "
                    "nontrivial dependence on velocity", },
            "12.7": {
                "active transport":
                    "the process in which a living membrane expends energy to "
                    "move substances across",
                "dialysis":
                    "the transport of any molecule other than water through a "
                    "semipermeable membrane from a region of high "
                    "concentration to one of low concentration",
                "diffusion":
                    "the movement of substances due to random thermal "
                    "molecular motion",
                "osmosis":
                    "the transport of water through a semipermeable membrane "
                    "from a region of high concentration to one of low "
                    "concentration",
                "osmotic pressure":
                    "the back pressure which stops the osmotic process if one "
                    "solution is pure water",
                "relative osmotic pressure":
                    "the back pressure which stops the osmotic process if "
                    "neither solution is pure water",
                "reverse dialysis":
                    "the process that occurs when back pressure is sufficient "
                    "to reverse the normal direction of dialysis through "
                    "membranes",
                "reverse osmosis":
                    "the process that occurs when back pressure is sufficient "
                    "to reverse the normal direction of osmosis through "
                    "membranes",
                "semipermeable":
                    "a type of membrane that allows only certain small "
                    "molecules to pass through", },
            "13": {
                "heat transfer":
                    "the movement of heat energy from one place or material "
                    "to another", },
            "13.1": {
                "absolute zero":
                    "the lowest possible temperature; the temperature at "
                    "which all molecular motion ceases",
                "Celsius scale":
                    "temperature scale in which the freezing point of water "
                    "is 0ºC and the boiling point of water is 100ºC",
                "degree Celsius":
                    "unit on the Celsius temperature scale",
                "degree Fahrenheit":
                    "unit on the Fahrenheit temperature scale",
                "Fahrenheit scale":
                    "temperature scale in which the freezing point of water "
                    "is 32ºF and the boiling point of water is 212ºF",
                "Kelvin scale":
                    "temperature scale in which 0 K is the lowest possible "
                    "temperature, representing absolute zero",
                "temperature":
                    "the quantity measured by a thermometer",
                "thermal equilibrium":
                    "the condition in which heat no longer flows between two "
                    "objects that are in contact; the two objects have the "
                    "same temperature",
                "zeroth law of thermodynamics":
                    "law that states that if two objects are in thermal "
                    "equilibrium, and a third object is in thermal "
                    "equilibrium with one of those objects, it is also in "
                    "thermal equilibrium with the other object", },
            "13.2": {
                "coefficient of linear expansion":
                    "α , the change in length, per unit length, per 1ºC "
                    "change in temperature; a constant used in the "
                    "calculation of linear expansion; the coefficient of "
                    "linear expansion depends on the material and to some "
                    "degree on the temperature of the material",
                "coefficient of volume expansion":
                    "β , the change in volume, per unit volume, per 1ºC "
                    "change in temperature",
                "thermal expansion":
                    "the change in size or volume of an object with change in "
                    "temperature",
                "thermal stress":
                    "stress caused by thermal expansion or contraction", },
            "13.3": {
                "Avogadro’s number":
                    "N_A, the number of molecules or atoms in one mole of a "
                    "substance; N_A=6.02×10²³ particles/mole",
                "Boltzmann constant":
                    "k, a physical constant that relates energy to "
                    "temperature; k=1.38×10^(–23) J/K",
                "ideal gas law":
                    "the physical law that relates the pressure and volume of "
                    "a gas to the number of gas molecules or number of moles "
                    "of gas and the temperature of the gas",
                "mole":
                    "the quantity of a substance whose mass (in grams) is "
                    "equal to its molecular mass", },
            "13.4": {
                "thermal energy":
                    "avg(KE), the average translational kinetic energy of a "
                    "molecule", },
            "13.5": {
                "critical point":
                    "the temperature above which a liquid cannot exist",
                "critical pressure":
                    "the minimum pressure needed for a liquid to exist at the "
                    "critical temperature",
                "critical temperature":
                    "the temperature above which a liquid cannot exist",
                "Dalton’s law of partial pressures":
                    "the physical law that states that the total pressure of "
                    "a gas is the sum of partial pressures of the component "
                    "gases",
                "partial pressure":
                    "the pressure a gas would create if it occupied the total "
                    "volume of space available",
                "phase diagrams":
                    "a graph of pressure vs. temperature of a particular "
                    "substance, showing at which pressures and temperatures "
                    "the three phases of the substance occur",
                "PV diagram":
                    "a graph of pressure vs. volume",
                "sublimation":
                    "the phase change from solid to gas",
                "triple point":
                    "the pressure and temperature at which a substance exists "
                    "in equilibrium as a solid, liquid, and gas",
                "vapor":
                    "a gas at a temperature below the boiling temperature",
                "vapor pressure":
                    "the pressure at which a gas coexists with its solid or "
                    "liquid phase", },
            "13.6": {
                "dew point":
                    "the temperature at which relative humidity is 100%; the "
                    "temperature at which water starts to condense out of the "
                    "air",
                "percent relative humidity":
                    "the ratio of vapor density to saturation vapor density",
                "relative humidity":
                    "the amount of water in the air relative to the maximum "
                    "amount the air can hold",
                "saturation":
                    r"the condition of 100% relative humidity", },
            "14.1": {
                "heat":
                    "the spontaneous transfer of energy due to a temperature "
                    "difference",
                "kilocalorie":
                    "1 kilocalorie = 1000 calories",
                "mechanical equivalent of heat":
                    "the work needed to produce the same effects as heat "
                    "transfer", },
            "14.2": {
                "specific heat":
                    "the amount of heat necessary to change the temperature "
                    "of 1.00 kg of a substance by 1.00 ºC", },
            "14.3": {
                "heat of sublimation":
                    "the energy required to change a substance from the solid "
                    "phase to the vapor phase",
                "latent heat coefficients":
                    "a physical constant equal to the amount of heat "
                    "transferred for every 1 kg of a substance during the "
                    "change in phase of the substance",
                "sublimation":
                    "the transition from the solid phase to the vapor "
                    "phase", },
            "14.4": {
                "conduction":
                    "heat transfer through stationary matter by physical "
                    "contact",
                "convection":
                    "heat transfer by the macroscopic movement of fluid",
                "radiation":
                    "heat transfer which occurs when microwaves, infrared "
                    "radiation, visible light, or other electromagnetic "
                    "radiation is emitted or absorbed", },
            "14.5": {
                "R factor":
                    "the ratio of thickness to the conductivity of a material",
                "rate of conductive heat transfer":
                    "rate of heat transfer from one material to another",
                "thermal conductivity":
                    "the property of a material’s ability to conduct heat", },
            "14.7": {
                "emissivity":
                    "measure of how well an object radiates",
                "greenhouse effect":
                    "warming of the Earth that is due to gases such as carbon "
                    "dioxide and methane that absorb infrared radiation from "
                    "the Earth’s surface and reradiate it in all directions, "
                    "thus sending a fraction of it back toward the surface of "
                    "the Earth",
                "net rate of heat transfer by radiation":
                    "is Q_net/t=σeA(T_2^4−T_1^4)",
                "radiation":
                    "energy transferred by electromagnetic waves directly as "
                    "a result of a temperature difference",
                "Stefan-Boltzmann law of radiation":
                    "Q/t=σeAT^4,  where σ is the Stefan-Boltzmann constant, "
                    "A is the surface area of the object, T is the absolute "
                    "temperature, and e is the emissivity", },
            "15.1": {
                "first law of thermodynamics":
                    "states that the change in internal energy of a system "
                    "equals the net heat transfer into the system minus the "
                    "net work done by the system",
                "human metabolism":
                    "conversion of food into heat transfer, work, and stored "
                    "fat",
                "internal energy":
                    "the sum of the kinetic and potential energies of a "
                    "system’s atoms and molecules", },
            "15.2": {
                "adiabatic process":
                    "a process in which no heat transfer takes place",
                "heat engine":
                    "a machine that uses heat transfer to do work",
                "isobaric process":
                    "constant-pressure process in which a gas does work",
                "isochoric process":
                    "a constant-volume process",
                "isothermal process":
                    "a constant-temperature process",
                "reversible process":
                    "a process in which both the heat engine system and the "
                    "external environment theoretically can be returned to "
                    "their original states", },
            "15.3": {
                "cyclical process":
                    "a process in which the path returns to its original "
                    "state at the end of every cycle",
                "irreversible process":
                    "any process that depends on path direction",
                "Otto cycle":
                    "a thermodynamic cycle, consisting of a pair of adiabatic "
                    "processes and a pair of isochoric processes, that "
                    "converts heat into work, e.g., the four-stroke engine "
                    "cycle of intake, compression, ignition, and exhaust",
                "second law of thermodynamics":
                    "heat transfer flows from a hotter to a cooler object, "
                    "never the reverse, and some heat energy in any process "
                    "is lost to available work in a cyclical process", },
            "15.4": {
                "Carnot cycle":
                    "a cyclical process that uses only reversible processes, "
                    "the adiabatic and isothermal processes",
                "Carnot efficiency":
                    "the maximum theoretical efficiency for a heat engine",
                "Carnot engine":
                    "a heat engine that uses a Carnot cycle", },
            "15.5": {
                "coefficient of performance":
                    "for a heat pump, it is the ratio of heat transfer at "
                    "the output (the hot reservoir) to the work supplied; for "
                    "a refrigerator or air conditioner, it is the ratio of "
                    "heat transfer from the cold reservoir to the work "
                    "supplied",
                "heat pump":
                    "a machine that generates heat transfer from cold to "
                    "hot", },
            "15.6": {
                "change in entropy":
                    "the ratio of heat transfer to temperature Q/T",
                "entropy":
                    "a measurement of a system's disorder and its inability "
                    "to do work in a system",
                "second law of thermodynamics stated in terms of entropy":
                    "the total entropy of a system either increases or "
                    "remains constant; it never decreases", },
            "15.7": {
                "macrostate":
                    "an overall property of a system",
                "microstate":
                    "each sequence within a larger macrostate",
                "statistical analysis":
                    "using statistics to examine data, such as counting "
                    "microstates and macrostates", },
            "16": {
                "oscillate":
                    "moving back and forth regularly between two points", },
            "16.1": {
                "beat frequency":
                    "the frequency of the amplitude fluctuations of a wave",
                "deformation":
                    "displacement from equilibrium",
                "elastic potential energy":
                    "potential energy stored as a result of deformation of an "
                    "elastic object, such as the stretching of a spring",
                "force constant":
                    "a constant related to the rigidity of a system: the "
                    "larger the force constant, the more rigid the system; "
                    "the force constant is represented by k",
                "restoring force":
                    "force acting in opposition to the force caused by a "
                    "deformation", },
            "16.2": {
                "frequency":
                    "number of events per unit of time",
                "period":
                    "time it takes to complete one oscillation",
                "periodic motion":
                    "motion that repeats itself at regular time intervals", },
            "16.3": {
                "amplitude":
                    "the maximum displacement from the equilibrium position "
                    "of an object oscillating around the equilibrium position",
                "simple harmonic motion":
                    "the oscillatory motion in a system where the net force "
                    "can be described by Hooke’s law",
                "simple harmonic oscillator":
                    "a device that implements Hooke’s law, such as a mass "
                    "that is attached to a spring, with the other end of the "
                    "spring being connected to a rigid support such as a "
                    "wall", },
            "16.4": {
                "simple pendulum":
                    "an object with a small mass suspended from a light wire "
                    "or string", },
            "16.7": {
                "critical damping":
                    "the condition in which the damping of an oscillator "
                    "causes it to return as quickly as possible to its "
                    "equilibrium position without oscillating back and forth "
                    "about this position",
                "over damping":
                    "the condition in which damping of an oscillator causes "
                    "it to return to equilibrium without oscillating; "
                    "oscillator moves more slowly toward equilibrium than in "
                    "the critically damped system",
                "under damping":
                    "the condition in which damping of an oscillator causes "
                    "it to return to equilibrium with the amplitude gradually "
                    "decreasing to zero; system returns to equilibrium faster "
                    "but overshoots and crosses the equilibrium position one "
                    "or more times", },
            "16.8": {
                "natural frequency":
                    "the frequency at which a system would oscillate if there "
                    "were no driving and no damping forces",
                "resonance":
                    "the phenomenon of driving a system with a frequency "
                    "equal to the system's natural frequency",
                "resonate":
                    "a system being driven at its natural frequency", },
            "16.9": {
                "longitudinal wave":
                    "a wave in which the disturbance is parallel to the "
                    "direction of propagation",
                "transverse wave":
                    "a wave in which the disturbance is perpendicular to the "
                    "direction of propagation",
                "wave":
                    "a disturbance that moves from its source and carries "
                    "energy",
                "wave velocity":
                    "the speed at which the disturbance moves. Also called "
                    "the propagation velocity or propagation speed",
                "wavelength":
                    "the distance between adjacent identical parts of a "
                    "wave", },
            "16.10": {
                "antinode":
                    "the location of maximum amplitude in standing waves",
                "beat frequency":
                    "the number of beats per second, equal to the difference "
                    "in the frequencies of two interacting tones or "
                    "oscillations",
                "constructive interference":
                    "when two waves arrive at the same point exactly in "
                    "phase; that is, the crests of the two waves are "
                    "precisely aligned, as are the troughs",
                "destructive interference":
                    "when two identical waves arrive at the same point "
                    "exactly out of phase; that is, precisely aligned crest "
                    "to trough",
                "fundamental frequency":
                    "the lowest frequency of a periodic waveform",
                "nodes":
                    "the points where the string does not move; more "
                    "generally, nodes are where the wave disturbance is zero "
                    "in a standing wave",
                "overtones":
                    "multiples of the fundamental frequency of a sound",
                "standing wave":
                    "a wave which oscillates in time but whose peak amplitude "
                    "profile does not move in space; the peak amplitude of "
                    "the wave oscillations at any point in space is constant "
                    "with time, and the oscillations at different points "
                    "throughout the wave are in phase",
                "superposition":
                    "the phenomenon that occurs when two or more waves arrive "
                    "at the same point", },
            "16.11": {
                "intensity":
                    "power per unit area", },
            "17.1": {
                "hearing":
                    "the perception of sound",
                "sound":
                    "a disturbance of matter that is transmitted from its "
                    "source outward", },
            "17.2": {
                "pitch":
                    "the perception of the frequency of a sound", },
            "17.3": {
                "intensity":
                    "the power per unit area carried by a wave",
                "sound intensity level":
                    "a unitless quantity telling you the level of the sound "
                    "relative to a fixed standard",
                "sound pressure level":
                    "the ratio of the pressure amplitude to a reference "
                    "pressure", },
            "17.4": {
                "bow wake":
                    "V-shaped disturbance created when the wave source moves "
                    "faster than the wave propagation speed",
                "Doppler effect":
                    "an alteration in the observed frequency of a sound due "
                    "to motion of either the source or the observer",
                "Doppler shift":
                    "the actual change in frequency due to relative motion of "
                    "source and observer",
                "sonic boom":
                    "a constructive interference of sound created by an "
                    "object moving faster than sound", },
            "17.5": {
                "antinode":
                    "point of maximum displacement",
                "fundamental":
                    "the lowest-frequency resonance",
                "harmonics":
                    "the term used to refer collectively to the fundamental "
                    "and its overtones",
                "node":
                    "point of zero displacement",
                "overtones":
                    "all resonant frequencies higher than the fundamental", },
            "17.6": {
                "infrasound":
                    "sounds below 20 Hz",
                "loudness":
                    "the perception of sound intensity",
                "note":
                    "basic unit of music with specific names, combined to "
                    "generate tunes",
                "phon":
                    "the numerical unit of loudness",
                "timbre":
                    "number and relative intensity of multiple sound "
                    "frequencies",
                "tone":
                    "number and relative intensity of multiple sound "
                    "frequencies",
                "ultrasound":
                    "sounds above 20,000 Hz", },
            "17.7": {
                "acoustic impedance":
                    "property of medium that makes the propagation of sound "
                    "waves more difficult",
                "Doppler-shifted ultrasound":
                    "a medical technique to detect motion and determine "
                    "velocity through the Doppler shift of an echo",
                "intensity reflection coefficient":
                    "a measure of the ratio of the intensity of the wave "
                    "reflected off a boundary between two media relative to "
                    "the intensity of the incident wave", },
            "18": {
                "electromagnetic force":
                    "one of the four fundamental forces of nature; the "
                    "electromagnetic force consists of static electricity, "
                    "moving electricity and magnetism",
                "static electricity":
                    "a buildup of electric charge on the surface of an "
                    "object", },
            "18.1": {
                "electric charge":
                    "a physical property of an object that causes it to be "
                    "attracted toward or repelled from another charged "
                    "object; each charged object generates and is influenced "
                    "by a force called an electromagnetic force",
                "electron":
                    "a particle orbiting the nucleus of an atom and carrying "
                    "the smallest unit of negative charge",
                "law of conservation of charge":
                    "states that whenever a charge is created, an equal "
                    "amount of charge with the opposite sign is created "
                    "simultaneously",
                "protons":
                    "a particle in the nucleus of an atom and carrying a "
                    "positive charge equal in magnitude and opposite in sign "
                    "to the amount of negative charge carried by an "
                    "electron", },
            "18.2": {
                "conductor":
                    "a material that allows electrons to move separately from "
                    "their atomic orbits",
                "electrostatic repulsion":
                    "the phenomenon of two objects with like charges "
                    "repelling each other",
                "free electron":
                    "an electron that is free to move away from its atomic "
                    "orbit",
                "induction":
                    "the process by which an electrically charged object "
                    "brought near a neutral object creates a charge in that "
                    "object",
                "insulators":
                    "a material that holds electrons securely within their "
                    "atomic orbits",
                "polarization":
                    "slight shifting of positive and negative charges to "
                    "opposite sides of an atom or molecule", },
            "18.3": {
                "Coulomb’s law":
                    "the mathematical equation calculating the electrostatic "
                    "force vector between two charged particles",
                "electrostatic force":
                    "the amount and direction of attraction or repulsion "
                    "between two charged bodies", },
            "18.4": {
                "Coulomb force":
                    "another term for the electrostatic force",
                "electric field strength":
                    "the electric field created by a point charge by using "
                    "the equation E=kQ/r²",
                "field":
                    "a map of the amount and direction of a force acting on "
                    "other objects, extending out into space",
                "point charge":
                    "A charged particle, designated Q, generating an electric "
                    "field",
                "test charge ":
                    "A particle (designated q) with either a positive or "
                    "negative charge set down within an electric field "
                    "generated by a point charge", },
            "18.5": {
                "electric field lines":
                    "a series of lines drawn from a point charge representing "
                    "the magnitude and direction of force exerted by that "
                    "charge",
                "vector":
                    "a quantity with both magnitude and direction",
                "vector addition":
                    "mathematical combination of two or more vectors, "
                    "including their magnitudes, directions, and positions", },
            "18.6": {
                "Coulomb interaction":
                    "the interaction between two charged particles generated "
                    "by the Coulomb forces they exert on one another",
                "dipole":
                    "a molecule’s lack of symmetrical charge distribution, "
                    "causing one side to be more positive and another to be "
                    "more negative",
                "polar molecule":
                    "a molecule with an asymmetrical distribution of positive "
                    "and negative charge",
                "screening":
                    "the dilution or blocking of an electrostatic force on a "
                    "charged object by the presence of other charges "
                    "nearby", },
            "18.7": {
                "conductor":
                    "an object with properties that allow charges to move "
                    "about freely within it",
                "electric field":
                    "a three-dimensional map of the electric force extended "
                    "out into space from a point charge",
                "electrostatic equilibrium":
                    "an electrostatically balanced state in which all free "
                    "electrical charges have stopped moving about",
                "Faraday cage":
                    "a metal shield which prevents electric charge from "
                    "penetrating its surface",
                "free charge":
                    "an electrical charge (either positive or negative) which "
                    "can move about separately from its base molecule",
                "ionosphere":
                    "a layer of charged particles located around 100 km above "
                    "the surface of Earth, which is responsible for a range "
                    "of phenomena including the electric field surrounding "
                    "Earth",
                "polarized":
                    "a state in which the positive and negative charges "
                    "within an object have collected in separate locations", },
            "18.8": {
                "electrostatic precipitators":
                    "filters that apply charges to particles in the air, then "
                    "attract those charges to a filter, removing them from "
                    "the airstream",
                "electrostatics":
                    "the study of electric forces that are static or slow-"
                    "moving",
                "grounded":
                    "when a conductor is connected to the Earth, allowing "
                    "charge to freely flow to and from Earth’s unlimited "
                    "reservoir",
                "ink jet printer":
                    "small ink droplets sprayed with an electric charge are "
                    "controlled by electrostatic plates to create images on "
                    "paper",
                "laser printers":
                    "uses a laser to create a photoconductive image on a "
                    "drum, which attracts dry ink particles that are then "
                    "rolled onto a sheet of paper to print a high-quality "
                    "copy of the image",
                "photoconductor":
                    "a substance that is an insulator until it is exposed to "
                    "light, when it becomes a conductor",
                "Van de Graaff generators":
                    "a machine that produces a large amount of excess charge, "
                    "used for experiments with high voltage",
                "xerography":
                    "a dry copying process based on electrostatics", },
            "19.1": {
                "electric potential":
                    "potential energy per unit charge",
                "electron volt":
                    "the energy given to a fundamental charge accelerated "
                    "through a potential difference of one volt",
                "mechanical energy":
                    "sum of the kinetic energy and potential energy of a "
                    "system; this sum is a constant",
                "potential difference (voltage)":
                    "change in potential energy of a charge moved from one "
                    "point to another, divided by the charge; units of "
                    "potential difference are joules per coulomb, known as "
                    "volt",
                "voltage":
                    "potential difference between two points", },
            "19.2": {
                "scalar":
                    "physical quantity with magnitude but no direction",
                "vector":
                    "physical quantity with both magnitude and direction", },
            "19.4": {
                "equipotential line":
                    "a line along which the electric potential is constant",
                "grounding":
                    "fixing a conductor at zero volts by connecting it to the "
                    "earth or ground", },
            "19.5": {
                "capacitance":
                    "amount of charge stored per unit volt",
                "capacitor":
                    "a device that stores electric charge",
                "dielectric":
                    "an insulating material",
                "dielectric strength":
                    "the maximum electric field above which an insulating "
                    "material begins to break down and conduct",
                "parallel plate capacitor":
                    "two identical conducting plates separated by a distance",
                "polar molecule":
                    "a molecule with inherent separation of charge", },
            "19.7": {
                "defibrillator":
                    "a machine used to provide an electrical shock to a heart "
                    "attack victim's heart in order to restore the heart's "
                    "normal rhythmic pattern", },
            "20.1": {
                "ampere":
                    "(amp) the SI unit for current; 1 A = 1 C/s",
                "drift velocity":
                    "the average velocity at which free charges flow in "
                    "response to an electric field",
                "electric current":
                    "the rate at which charge flows, I = ΔQ/Δt", },
            "20.2": {
                "ohm":
                    "the unit of resistance, given by 1Ω = 1 V/A",
                "Ohm’s law":
                    "an empirical relation stating that the current I is "
                    "proportional to the potential difference V, ∝ V; it is "
                    "often written as I = V/R, where R is the resistance",
                "ohmic":
                    "a type of a material for which Ohm's law is valid",
                "resistance":
                    "the electric property that impedes current; for ohmic "
                    "materials, it is the ratio of voltage to current, "
                    "R = V/I",
                "simple circuit":
                    "a circuit with a single voltage source and a single "
                    "resistor", },
            "20.3": {
                "resistivity":
                    "an intrinsic property of a material, independent of its "
                    "shape or size, directly proportional to the resistance, "
                    "denoted by ρ",
                "temperature coefficient of resistivity":
                    "an empirical quantity, denoted by α, which describes the "
                    "change in resistance or resistivity of a material with "
                    "temperature", },
            "20.4": {
                "electric power":
                    "the rate at which electrical energy is supplied by a "
                    "source or dissipated by a device; it is the product of "
                    "current times voltage", },
            "20.5": {
                "AC current":
                    "current that fluctuates sinusoidally with time, "
                    "expressed as I = I₀ sin 2πft, where I is the current at "
                    "time t, I₀ is the peak current, and f is the frequency "
                    "in hertz",
                "AC voltage":
                    "voltage that fluctuates sinusoidally with time, "
                    "expressed as V = V₀ sin 2πft, where V is the voltage at "
                    "time t, V₀ is the peak voltage, and f is the frequency "
                    "in hertz",
                "alternating current":
                    "(AC) the flow of electric charge that periodically "
                    "reverses direction",
                "direct current":
                    "(DC) the flow of electric charge in only one direction",
                "rms current":
                    "the root mean square of the current, I_rms=I₀/√2 , where "
                    "I₀ is the peak current, in an AC system",
                "rms voltage":
                    "the root mean square of the voltage, V_rms=V₀/√2 , where "
                    "V₀ is the peak voltage, in an AC system", },
            "20.6": {
                "microshock sensitive":
                    "a condition in which a person’s skin resistance is "
                    "bypassed, possibly by a medical procedure, rendering the "
                    "person vulnerable to electrical shock at currents about "
                    "1/1000 the normally required level",
                "shock hazard":
                    "when electric current passes through a person",
                "short circuit":
                    "also known as a “short,” a low-resistance path between "
                    "terminals of a voltage source",
                "thermal hazard":
                    "a hazard in which electric current causes undesired "
                    "thermal effects", },
            "20.7": {
                "bioelectricity":
                    "electrical effects in and created by biological systems",
                "electrocardiogram (ECG)":
                    "usually abbreviated ECG, a record of voltages created by "
                    "depolarization and repolarization, especially in the "
                    "heart",
                "nerve conduction":
                    "the transport of electrical signals by nerve cells",
                "semipermeable":
                    "property of a membrane that allows only certain types of "
                    "ions to cross it", },
            "21.1": {
                "current":
                    "the flow of charge through an electric circuit past a "
                    "given point of measurement",
                "Joule’s law":
                    "the relationship between potential electrical power, "
                    "voltage, and resistance in an electrical circuit, given "
                    "by: P_e=IV",
                "Ohm’s law":
                    "the relationship between current, voltage, and "
                    "resistance within an electrical circuit: V=IR",
                "parallel":
                    "the wiring of resistors or other components in an "
                    "electrical circuit such that each component receives an "
                    "equal voltage from the power source; often pictured in a "
                    "ladder-shaped diagram, with each component on a rung of "
                    "the ladder",
                "resistance":
                    "causing a loss of electrical power in a circuit",
                "resistor":
                    "a component that provides resistance to the current "
                    "flowing through an electrical circuit",
                "series":
                    "a sequence of resistors or other components wired into a "
                    "circuit one after the other",
                "voltage":
                    "the electrical potential energy per unit charge; "
                    "electric pressure created by a power source, such as a "
                    "battery",
                "voltage drop":
                    "the loss of electrical power as a current travels "
                    "through a resistor, wire or other component", },
            "21.2": {
                "electromotive force":
                    "the potential difference of a source of electricity when "
                    "no current is flowing; measured in volts",
                "internal resistance":
                    "the amount of resistance within the voltage source",
                "potential difference":
                    "the difference in electric potential between two points "
                    "in an electric circuit, measured in volts",
                "terminal voltage":
                    "the voltage measured across the terminals of a source of "
                    "potential difference", },
            "21.3": {
                "conservation laws":
                    "require that energy and charge be conserved in a system",
                "junction rule":
                    "Kirchhoff’s first rule, which applies the conservation "
                    "of charge to a junction; current is the flow of charge; "
                    "thus, whatever charge flows into the junction must flow "
                    "out; the rule can be stated I₁=I₂+I₃",
                "Kirchhoff’s rules":
                    "a set of two rules, based on conservation of charge and "
                    "energy, governing current and changes in potential in an "
                    "electric circuit",
                "loop rule":
                    "Kirchhoff’s second rule, which states that in a closed "
                    "loop, whatever energy is supplied by emf must be "
                    "transferred into other forms by devices in the loop, "
                    "since there are no other ways in which energy can be "
                    "transferred into or out of the circuit. Thus, the emf "
                    "equals the sum of the IR (voltage) drops in the loop and "
                    "can be stated: emf=Ir+IR₁+IR₂", },
            "21.4": {
                "ammeter":
                    "an instrument that measures current",
                "analog meter":
                    "a measuring instrument that gives a readout in the form "
                    "of a needle movement over a marked gauge",
                "current sensitivity":
                    "the maximum current that a galvanometer can read",
                "digital meter":
                    "a measuring instrument that gives a readout in a digital "
                    "form",
                "full-scale deflection":
                    "the maximum deflection of a galvanometer needle, also "
                    "known as current sensitivity; a galvanometer with a full-"
                    "scale deflection of 50 μA has a maximum deflection of "
                    "its needle when 50 μA flows through it",
                "galvanometer":
                    "an analog measuring device, denoted by G, that measures "
                    "current flow using a needle deflection caused by a "
                    "magnetic field force acting upon a current-carrying wire",
                "shunt resistance":
                    "a small resistance R placed in parallel with a "
                    "galvanometer G to produce an ammeter; the larger the "
                    "current to be measured, the smaller R must be; most of "
                    "the current flowing through the meter is shunted through "
                    "R to protect the galvanometer",
                "voltmeter":
                    "an instrument that measures voltage", },
            "21.5": {
                "bridge device":
                    "a device that forms a bridge between two branches of a "
                    "circuit; some bridge devices are used to make null "
                    "measurements in circuits",
                "null measurements":
                    "methods of measuring current and voltage more accurately "
                    "by balancing the circuit so that no current flows "
                    "through the measurement device",
                "ohmmeter":
                    "an instrument that applies a voltage to a resistance, "
                    "measures the current, calculates the resistance using "
                    "Ohm’s law, and provides a readout of this calculated "
                    "resistance",
                "potentiometer":
                    "a null measurement device for measuring potentials "
                    "(voltages)",
                "Wheatstone bridge":
                    "a null measurement device for calculating resistance by "
                    "balancing potential drops in a circuit", },
            "21.6": {
                "capacitance":
                    "the maximum amount of electric potential energy that can "
                    "be stored (or separated) for a given electric potential",
                "capacitor":
                    "an electrical component used to store energy by "
                    "separating electric charge on two opposing plates",
                "RC circuit":
                    "a circuit that contains both a resistor and a "
                    "capacitor", },
            "22.1": {
                "north magnetic pole":
                    "the end or the side of a magnet that is attracted toward "
                    "Earth’s geographic north pole",
                "south magnetic pole":
                    "the end or the side of a magnet that is attracted toward "
                    "Earth’s geographic south pole", },
            "22.2": {
                "Curie temperature":
                    "the temperature above which a ferromagnetic material "
                    "cannot be magnetized",
                "domains":
                    "regions within a material that behave like small bar "
                    "magnets",
                "electromagnet":
                    "an object that is temporarily magnetic when an "
                    "electrical current is passed through it",
                "electromagnetism":
                    "the use of electrical currents to induce magnetism",
                "ferromagnetic":
                    "materials, such as iron, cobalt, nickel, and gadolinium, "
                    "that exhibit strong magnetic effects",
                "magnetic monopoles":
                    "an isolated magnetic pole; a south pole without a north "
                    "pole, or vice versa (no magnetic monopole has ever been "
                    "observed)",
                "magnetized":
                    "to be turned into a magnet; to be induced to be "
                    "magnetic", },
            "22.3": {
                "B-field":
                    "another term for magnetic field",
                "direction of magnetic field lines":
                    "the direction that the north end of a compass needle "
                    "points",
                "magnetic field":
                    "the representation of magnetic forces",
                "magnetic field lines":
                    "the pictorial representation of the strength and the "
                    "direction of a magnetic field", },
            "22.4": {
                "gauss":
                    "G, the unit of the magnetic field strength; 1 G=10⁻⁴ T",
                "Lorentz force":
                    "the force on a charge moving in a magnetic field",
                "magnetic force":
                    "the force on a charge produced by its motion through a "
                    "magnetic field; the Lorentz force",
                "right hand rule (RHR-1)":
                    "the rule to determine the direction of the magnetic "
                    "force on a positive moving charge: when the thumb of the "
                    "right hand points in the direction of the charge’s "
                    "velocity v and the fingers point in the direction of the "
                    "magnetic field B, then the force on the charge is "
                    "perpendicular and away from the palm; the force on a "
                    "negative charge is perpendicular and into the palm",
                "tesla":
                    "T, the SI unit of the magnetic field strength; 1 T = "
                    "1 N/A⋅m", },
            "22.6": {
                "Hall effect":
                    "the creation of voltage across a current-carrying "
                    "conductor by a magnetic field",
                "Hall emf":
                    "the electromotive force created by a current-carrying "
                    "conductor by a magnetic field, ε=Blv", },
            "22.8": {
                "meter":
                    "common application of magnetic torque on a current-"
                    "carrying loop that is very similar in construction to a "
                    "motor; by design, the torque is proportional to I and "
                    "not θ, so the needle deflection is proportional to the "
                    "current",
                "motor":
                    "loop of wire in a magnetic field; when current is passed "
                    "through the loops, the magnetic field exerts torque on "
                    "the loops, which rotates a shaft; electrical energy is "
                    "converted to mechanical work in the process", },
            "22.9": {
                "Ampere’s law":
                    "the physical law that states that the magnetic field "
                    "around an electric current is proportional to the "
                    "current; each segment of current produces a magnetic "
                    "field like that of a long straight wire, and the total "
                    "field of any shape current is the vector sum of the "
                    "fields due to each segment",
                "Biot-Savart law":
                    "a physical law that describes the magnetic field "
                    "generated by an electric current in terms of a specific "
                    "equation",
                "magnetic field strength (magnitude) produced by a long "
                    "straight current-carrying wire":
                    "defined as B=μ₀I/2πr, where I is the current, r is the "
                    "shortest distance to the wire, and μ₀ is the "
                    "permeability of free space",
                "magnetic field strength at the center of a circular loop":
                    "defined as B=μ₀I/2R where R is the radius of the loop",
                "magnetic field strength inside a solenoid":
                    "defined as B=μ₀nI where n is the number of loops per "
                    "unit length of the solenoid (n=N/l, with N being the "
                    "number of loops and l the length)",
                "Maxwell’s equations":
                    "a set of four equations that describe electromagnetic "
                    "phenomena",
                "permeability of free space":
                    "the measure of the ability of a material, in this case "
                    "free space, to support a magnetic field; the constant "
                    "μ₀=4π × 10⁻⁷ T⋅m/A",
                "right hand rule (RHR-2)":
                    "a rule to determine the direction of the magnetic field "
                    "induced by a current-carrying wire: Point the thumb of "
                    "the right hand in the direction of current, and the "
                    "fingers curl in the direction of the magnetic field "
                    "loops",
                "solenoid":
                    "a thin wire wound into a coil that produces a magnetic "
                    "field when an electric current is passed through it", },
            "22.10": {
                "ampere":
                    "one ampere of current through each of two parallel "
                    "conductors of infinite length, separated by one meter in "
                    "empty space free of other magnetic fields, causes a "
                    "force of exactly 2 × 10⁻⁷ N/m on each conductor", },
            "22.11": {
                "magnetic resonance imaging (MRI)":
                    "a medical imaging technique that uses magnetic fields "
                    "create detailed images of internal tissues and organs",
                "magnetocardiogram (MCG)":
                    "a recording of the heart’s magnetic field as it beats",
                "magnetoencephalogram (MEG)":
                    "a measurement of the brain’s magnetic field",
                "nuclear magnetic resonance (NMR)":
                    "a phenomenon in which an externally applied magnetic "
                    "field interacts with the nuclei of certain atoms", },
            "23.1": {
                "induction":
                    "(magnetic induction) the creation of emfs and hence "
                    "currents by magnetic fields", },
            "23.2": {
                "Faraday’s law of induction":
                    "the means of calculating the emf in a coil due to "
                    "changing magnetic flux, given by emf = −N ΔΦ/Δt",
                "Lenz’s law":
                    "the minus sign in Faraday’s law, signifying that the emf "
                    "induced in a coil opposes the change in magnetic flux", },
            "23.4": {
                "eddy current":
                    "a current loop in a conductor caused by motional emf",
                "magnetic damping":
                    "the drag produced by eddy currents", },
            "23.5": {
                "electric generators":
                    "a device for converting mechanical work into electric "
                    "energy; it induces an emf by rotating a coil in a "
                    "magnetic field",
                "emf induced in a generator coil":
                    "emf=NABωsinωt , where A is the area of an N-turn coil "
                    "rotated at a constant angular velocity ω in a uniform "
                    "magnetic field B, over a period of time t",
                "peak emf":
                    "emf₀=NABω", },
            "23.6": {
                "back emf":
                    "the emf generated by a running motor, because it "
                    "consists of a coil turning in a magnetic field; it "
                    "opposes the voltage powering the motor", },
            "23.7": {
                "step-down transformer":
                    "a transformer that decreases voltage",
                "step-up transformer":
                    "a transformer that increases voltage",
                "transformer":
                    "a device that transforms voltages from one value to "
                    "another using induction",
                "transformer equation":
                    "the equation showing that the ratio of the secondary to "
                    "primary voltages in a transformer equals the ratio of "
                    "the number of loops in their coils; V_s/V_p=N_s/N_p", },
            "23.8": {
                "shock hazard":
                    "the term for electrical hazards due to current passing "
                    "through a human",
                "thermal hazard":
                    "the term for electrical hazards due to overheating",
                "three-wire system":
                    "the wiring system used at present for safety reasons, "
                    "with live, neutral, and ground wires", },
            "23.9": {
                "energy stored in an inductor ":
                    "calculated by E_(ind) = ½LI²",
                "henry":
                    "the unit of inductance; 1H=1Ω⋅s",
                "inductance":
                    "a property of a device describing how efficient it is at "
                    "inducing emf in another device",
                "inductor":
                    "a device that exhibits significant self-inductance",
                "mutual inductance":
                    "how effective a pair of devices are at inducing emfs in "
                    "each other",
                "self-inductance":
                    "how effective a device is at inducing emf in itself", },
            "23.10": {
                "characteristic time constant":
                    "denoted by τ, of a particular series RL circuit is "
                    "calculated by τ=L/R, where L is the inductance and R is "
                    "the resistance",
                "electromagnetic induction":
                    "the process of inducing an emf (voltage) with a change "
                    "in magnetic flux",
                "magnetic flux":
                    "the amount of magnetic field going through a particular "
                    "area, calculated with Φ=BAcosθ where B is the magnetic "
                    "field strength over an area A at an angle θ with the "
                    "perpendicular to the area", },
            "23.11": {
                "capacitive reactance":
                    "the opposition of a capacitor to a change in current; "
                    "calculated by X_C = 1 / 2πfC",
                "inductive reactance":
                    "the opposition of an inductor to a change in current; "
                    "calculated by X_L=2πfL", },
            "23.12": {
                "impedance":
                    "the AC analogue to resistance in a DC circuit; it is the "
                    "combined effect of resistance, inductive reactance, and "
                    "capacitive reactance in the form Z = √(R² + (X_L−X_C)²)",
                "phase angle":
                    "denoted by ϕ, the amount by which the voltage and "
                    "current are out of phase with each other in a circuit",
                "power factor":
                    "the amount by which the power delivered in the circuit "
                    "is less than the theoretical maximum of the circuit due "
                    "to voltage and current being out of phase; calculated by "
                    "cosϕ",
                "resonant frequency":
                    "the frequency at which the impedance in a circuit is at "
                    "a minimum, and also the frequency at which the circuit "
                    "would oscillate if not driven by a voltage source; "
                    "calculated by f₀=1 / (2π√(LC))", },
            "24.1": {
                "electric field lines":
                    "a pattern of imaginary lines that extend between an "
                    "electric source and charged objects in the surrounding "
                    "area, with arrows pointed away from positively charged "
                    "objects and toward negatively charged objects. The more "
                    "lines in the pattern, the stronger the electric field in "
                    "that region",
                "electric field strength":
                    "the magnitude of the electric field, denoted E-field",
                "electromotive force":
                    "energy produced per unit charge, drawn from a source "
                    "that produces an electrical current",
                "hertz":
                    "an SI unit denoting the frequency of an electromagnetic "
                    "wave, in cycles per second",
                "magnetic field lines":
                    "a pattern of continuous, imaginary lines that emerge "
                    "from and enter into opposite magnetic poles. The density "
                    "of the lines indicates the magnitude of the magnetic "
                    "field",
                "magnetic field strength":
                    "the magnitude of the magnetic field, denoted B-field",
                "Maxwell’s equations":
                    "a set of four equations that comprise a complete, "
                    "overarching theory of electromagnetism",
                "RLC circuit":
                    "an electric circuit that includes a resistor, capacitor "
                    "and inductor",
                "speed of light":
                    "in a vacuum, such as space, the speed of light is a "
                    "constant 3 x 10⁸ m/s", },
            "24.2": {
                "amplitude":
                    "the height, or magnitude, of an electromagnetic wave",
                "electric field":
                    "a vector quantity (E); the lines of electric force per "
                    "unit charge, moving radially outward from a positive "
                    "charge and in toward a negative charge",
                "electromagnetic waves":
                    "radiation in the form of waves of electric and magnetic "
                    "energy",
                "frequency":
                    "the number of complete wave cycles (up-down-up) passing "
                    "a given point within one second (cycles/second)",
                "magnetic field":
                    "a vector quantity (B); can be used to determine the "
                    "magnetic force on a moving charged particle",
                "oscillate":
                    "to fluctuate back and forth in a steady beat",
                "resonant":
                    "a system that displays enhanced oscillation when "
                    "subjected to a periodic disturbance of the same "
                    "frequency as its natural frequency",
                "standing wave":
                    "a wave that oscillates in place, with nodes where no "
                    "motion happens",
                "transverse wave":
                    "a wave, such as an electromagnetic wave, which "
                    "oscillates perpendicular to the axis along the line of "
                    "travel",
                "wavelength":
                    "the distance from one peak to the next in a wave", },
            "24.3": {
                "amplitude modulation":
                    "a method for placing information on electromagnetic "
                    "waves by modulating the amplitude of a carrier wave with "
                    "an audio signal, resulting in a wave with constant "
                    "frequency but varying amplitude",
                "carrier wave":
                    "an electromagnetic wave that carries a signal by "
                    "modulation of its amplitude or frequency",
                "electromagnetic spectrum":
                    "the full range of wavelengths or frequencies of "
                    "electromagnetic radiation",
                "extremely low frequency (ELF)":
                    "electromagnetic radiation with wavelengths usually in "
                    "the range of 0 to 300 Hz, but also about 1kHz",
                "frequency modulation":
                    "a method of placing information on electromagnetic waves "
                    "by modulating the frequency of a carrier wave with an "
                    "audio signal, producing a wave of constant amplitude but "
                    "varying frequency",
                "gamma ray":
                    "(γ ray); extremely high frequency electromagnetic "
                    "radiation emitted by the nucleus of an atom, either from "
                    "natural nuclear decay or induced nuclear processes in "
                    "nuclear reactors and weapons. The lower end of the γ-ray "
                    "frequency range overlaps the upper end of the X-ray "
                    "range, but γ rays can have the highest frequency of any "
                    "electromagnetic radiation",
                "Infrared radiation":
                    "a region of the electromagnetic spectrum with a "
                    "frequency range that extends from just below the red "
                    "region of the visible light spectrum up to the microwave "
                    "region, or from 0.74μm to 300μm",
                "microwaves":
                    "electromagnetic waves with wavelengths in the range from "
                    "1 mm to 1 m; they can be produced by currents in "
                    "macroscopic circuits and devices",
                "radar":
                    "a common application of microwaves. Radar can determine "
                    "the distance to objects as diverse as clouds and "
                    "aircraft, as well as determine the speed of a car or the "
                    "intensity of a rainstorm",
                "radio waves":
                    "electromagnetic waves with wavelengths in the range "
                    "from 1 mm to 100 km; they are produced by currents in "
                    "wires and circuits and by astronomical phenomena",
                "television":
                    "video and audio signals broadcast on electromagnetic "
                    "waves",
                "thermal agitation":
                    "the thermal motion of atoms and molecules in any object "
                    "at a temperature above absolute zero, which causes them "
                    "to emit and absorb radiation",
                "ultra high frequency":
                    "TV channels in an even higher frequency range than VHF, "
                    "of 470 to 1000 MHz",
                "ultraviolet radiation (UV)":
                    "electromagnetic radiation in the range extending upward "
                    "in frequency from violet light and overlapping with the "
                    "lowest X-ray frequencies, with wavelengths from 400 nm "
                    "down to about 10 nm",
                "very high frequency":
                    "TV channels utilizing frequencies in the two ranges of "
                    "54 to 88 MHz and 174 to 222 MHz",
                "visible light":
                    "the narrow segment of the electromagnetic spectrum to "
                    "which the normal human eye responds",
                "X-ray":
                    "invisible, penetrating form of very high frequency "
                    "electromagnetic radiation, overlapping both the "
                    "ultraviolet range and the γ-ray range", },
            "24.4": {
                "intensity":
                    "the power of an electric or magnetic field per unit "
                    "area, for example, Watts per square meter",
                "maximum field strength":
                    "the maximum amplitude an electromagnetic wave can reach, "
                    "representing the maximum amount of electric force and/or "
                    "magnetic flux that the wave can exert", },
            "25.1": {
                "geometric optics":
                    "part of optics dealing with the ray aspect of light",
                "ray":
                    "straight line that originates at some point", },
            "25.2": {
                "law of reflection":
                    "angle of reflection equals the angle of incidence", },
            "25.3": {
                "index of refraction":
                    "for a material, the ratio of the speed of light in "
                    "vacuum to that in the material",
                "law of refraction":
                    "for a ray at a given incident angle, a large change in "
                    "speed causes a large change in direction, and thus a "
                    "large change in angle",
                "refraction":
                    "changing of a light ray’s direction when it passes "
                    "through variations in matter", },
            "25.4": {
                "corner reflector":
                    "an object consisting of two mutually perpendicular "
                    "reflecting surfaces, so that the light that enters is "
                    "reflected back exactly parallel to the direction from "
                    "which it came",
                "critical angle":
                    "incident angle that produces an angle of refraction of "
                    "90º",
                "endoscope":
                    "light is transmitted down one fiber bundle to illuminate "
                    "internal parts, and the reflected light is transmitted "
                    "back out through another to be observed",
                "fiber optics":
                    "transmission of light down fibers of plastic or glass, "
                    "applying the principle of total internal reflection",
                "total internal reflection":
                    "all of the light is reflected back",
                "zircon":
                    "natural gemstone with a large index of refraction", },
            "25.5": {
                "dispersion":
                    "spreading of white light into its full spectrum of "
                    "wavelengths",
                "rainbow":
                    "dispersion of sunlight into a continuous distribution of "
                    "colors according to wavelength, produced by the "
                    "refraction and reflection of sunlight by water droplets "
                    "in the sky", },
            "25.6": {
                "converging lens":
                    "a convex lens in which light rays that enter it parallel "
                    "to its axis converge at a single point on the opposite "
                    "side",
                "diverging lens":
                    "a concave lens in which light rays that enter it "
                    "parallel to its axis bend away (diverge) from its axis",
                "focal length":
                    "distance from the center of a lens or curved mirror to "
                    "its focal point",
                "focal point":
                    "for a converging lens or mirror, the point at which "
                    "converging light rays cross; for a diverging lens or "
                    "mirror, the point from which diverging light rays appear "
                    "to originate",
                "Image distance ":
                    "the distance of the image from the center of a lens",
                "magnification":
                    "ratio of image height to object height",
                "power":
                    "inverse of focal length",
                "ray tracing":
                    "the technique of determining or following (tracing) the "
                    "paths that light rays take",
                "real image":
                    "image that can be projected",
                "thin lens":
                    "one whose thickness allows rays to refract but does not "
                    "allow properties such as dispersion and aberrations",
                "thin lens equations":
                    "1/d_o +1/d_i = 1/f and h_i/h_o = −d_i/d_o = m",
                "virtual image":
                    "image that cannot be projected", },
            "25.7": {
                "converging mirror":
                    "a concave mirror in which light rays that strike it "
                    "parallel to its axis converge at one or more points "
                    "along the axis",
                "diverging mirror":
                    "a convex mirror in which light rays that strike it "
                    "parallel to its axis bend away (diverge) from its axis",
                "mirror":
                    "smooth surface that reflects light at specific angles, "
                    "forming an image of the person or object in front of "
                    "it", },
            "26.1": {
                "accommodation":
                    "the ability of the eye to adjust its focal length is "
                    "known as accommodation",
                "presbyopia":
                    "a condition in which the lens of the eye becomes "
                    "progressively unable to focus on objects close to the "
                    "viewer", },
            "26.2": {
                "astigmatism":
                    "the result of an inability of the cornea to properly "
                    "focus an image onto the retina",
                "far point":
                    "the object point imaged by the eye onto the retina in an "
                    "unaccommodated eye",
                "farsightedness":
                    "another term for hyperopia, the condition of an eye "
                    "where incoming rays of light reach the retina before "
                    "they converge into a focused image",
                "hyperopia":
                    "the condition of an eye where incoming rays of light "
                    "reach the retina before they converge into a focused "
                    "image",
                "laser vision correction":
                    "a medical procedure used to correct astigmatism and "
                    "eyesight deficiencies such as myopia and hyperopia",
                "myopia":
                    "a visual defect in which distant objects appear blurred "
                    "because their images are focused in front of the retina "
                    "rather than being focused on the retina",
                "near point":
                    "the point nearest the eye at which an object is "
                    "accurately focused on the retina at full accommodation",
                "nearsightedness":
                    "another term for myopia, a visual defect in which "
                    "distant objects appear blurred because their images are "
                    "focused in front of the retina rather than being focused "
                    "on the retina", },
            "26.3": {
                "color constancy":
                    "a part of the visual perception system that allows "
                    "people to perceive color in a variety of conditions and "
                    "to see some consistency in the color",
                "hues":
                    "identity of a color as it relates specifically to the "
                    "spectrum",
                "retinex":
                    "a theory proposed to explain color and brightness "
                    "perception and constancies; is a combination of the "
                    "words retina and cortex, which are the two areas "
                    "responsible for the processing of visual information",
                "retinex theory of color vision":
                    "the ability to perceive color in an ambient-colored "
                    "environment",
                "rods and cones":
                    "two types of photoreceptors in the human retina; rods "
                    "are responsible for vision at low light levels, while "
                    "cones are active at higher light levels",
                "simplified theory of color vision":
                    "a theory that states that there are three primary "
                    "colors, which correspond to the three types of cones", },
            "26.4": {
                "compound microscope":
                    "a microscope constructed from two convex lenses, the "
                    "first serving as the ocular lens(close to the eye) and "
                    "the second serving as the objective lens",
                "eyepiece":
                    "the lens or combination of lenses in an optical "
                    "instrument nearest to the eye of the observer",
                "numerical aperture (NA)":
                    "a number or measure that expresses the ability of a lens "
                    "to resolve fine detail in an object being observed. "
                    "Derived by mathematical formula NA=n sin α, where n is "
                    "the refractive index of the medium between the lens and "
                    "the specimen and α=θ/2",
                "objective lens":
                    "the lens nearest to the object being examined", },
            "26.5": {
                "adaptive optics":
                    "optical technology in which computers adjust the lenses "
                    "and mirrors in a device to correct for image distortions",
                "angular magnification":
                    "a ratio related to the focal lengths of the objective "
                    "and eyepiece and given as M=−f_o/f_e", },
            "26.6": {
                "aberrations":
                    "failure of rays to converge at one focus because of "
                    "limitations or defects in a lens or mirror", },
            "27.1": {
                "wavelength in a medium":
                    "λ_n = λ/n , where λ is the wavelength in vacuum, and n "
                    "is the index of refraction of the medium", },
            "27.2": {
                "diffraction":
                    "the bending of a wave around the edges of an opening or "
                    "an obstacle",
                "Huygens’s principle":
                    "every point on a wavefront is a source of wavelets that "
                    "spread out in the forward direction at the same speed as "
                    "the wave itself. The new wavefront is a line tangent to "
                    "all of the wavelets", },
            "27.3": {
                "coherent":
                    "waves are in phase or have a definite phase relationship",
                "constructive interference for a double slit":
                    "the path length difference must be an integral multiple "
                    "of the wavelength",
                "destructive interference for a double slit":
                    "the path length difference must be a half-integral "
                    "multiple of the wavelength",
                "incoherent":
                    "waves have random phase relationships",
                "order":
                    "the integer m used in the equations for constructive and "
                    "destructive interference for a double slit", },
            "27.4": {
                "constructive interference for a diffraction grating":
                    "occurs when the condition dsinθ=mλ (for m=0, 1, –1, 2, "
                    "–2, …) is satisfied, where d is the distance between "
                    "slits in the grating, λ is the wavelength of light, and "
                    "m is the order of the maximum",
                "diffraction grating":
                    "a large number of evenly spaced parallel slits", },
            "27.5": {
                "destructive interference for a single slit":
                    "occurs when D sin θ = mλ, (for m=1, –1, 2, –2, 3, …), "
                    "where D is the slit width, λ is the light’s wavelength, "
                    "θ is the angle relative to the original direction of the "
                    "light, and m is the order of the minimum", },
            "27.6": {
                "Rayleigh criterion":
                    "two images are just resolvable when the center of the "
                    "diffraction pattern of one is directly over the first "
                    "minimum of the diffraction pattern of the other", },
            "27.7": {
                "thin film interference":
                    "interference between light reflected from different "
                    "surfaces of a thin film", },
            "27.8": {
                "axis of a polarizing filter":
                    "the direction along which the filter passes the electric "
                    "field of an EM wave",
                "birefringent":
                    "crystals that split an unpolarized beam of light into "
                    "two beams",
                "Brewster’s angle":
                    "θ_b = tan⁻ⁱ (n₂/n₁),  where n₂ is the index of "
                    "refraction of the medium from which the light is "
                    "reflected and n₁ is the index of refraction of the "
                    "medium in which the reflected light travels",
                "Brewster’s law":
                    "tan θ_b = n₂/n₁, where n₁ is the medium in which the "
                    "incident and reflected light travel and n₂ is the index "
                    "of refraction of the medium that forms the interface "
                    "that reflects the light",
                "direction of polarization":
                    "the direction parallel to the electric field for EM "
                    "waves",
                "horizontally polarized":
                    "the oscillations are in a horizontal plane",
                "optically active":
                    "substances that rotate the plane of polarization of "
                    "light passing through them",
                "polarization":
                    "the attribute that wave oscillations have a definite "
                    "direction relative to the direction of propagation of "
                    "the wave",
                "polarized":
                    "waves having the electric and magnetic field "
                    "oscillations in a definite direction",
                "reflected light is completely polarized":
                    "light reflected at the angle of reflection θ_b, known as "
                    "Brewster’s angle",
                "unpolarized":
                    "waves that are randomly polarized",
                "vertically polarized":
                    "the oscillations are in a vertical plane", },
            "27.9": {
                "confocal microscopes":
                    "microscopes that use the extended focal region to obtain "
                    "three-dimensional images rather than two-dimensional "
                    "images",
                "contrast":
                    "the difference in intensity between objects and the "
                    "background on which they are observed",
                "Interference microscopes":
                    "microscopes that enhance contrast between objects and "
                    "background by superimposing a reference beam of light "
                    "upon the light emerging from the sample",
                "phase-contrast microscope":
                    "microscope utilizing wave interference and differences "
                    "in phases to enhance contrast",
                "polarization microscope":
                    "microscope that enhances contrast by utilizing a wave "
                    "characteristic of light, useful for objects that are "
                    "optically active",
                "ultraviolet (UV) microscopes":
                    "microscopes constructed with special lenses that "
                    "transmit UV rays and utilize photographic or electronic "
                    "techniques to record images", },
            "28.1": {
                "first postulate of special relativity":
                    "the idea that the laws of physics are the same and can "
                    "be stated in their simplest form in all inertial frames "
                    "of reference",
                "inertial frame of reference":
                    "a reference frame in which a body at rest remains at "
                    "rest and a body in motion moves at a constant speed in a "
                    "straight line unless acted on by an outside force",
                "Michelson-Morley experiment":
                    "an investigation performed in 1887 that proved that the "
                    "speed of light in a vacuum is the same in all frames of "
                    "reference from which it is viewed",
                "relativity":
                    "the study of how different observers measure the same "
                    "event",
                "second postulate of special relativity":
                    "the idea that the speed of light c is a constant, "
                    "independent of the source",
                "special relativity":
                    "the theory that, in an inertial frame of reference, the "
                    "motion of an object is relative to the frame from which "
                    "it is viewed or measured", },
            "28.2": {
                "proper time ":
                    "Δt₀ - the time measured by an observer at rest relative "
                    "to the event being observed: Δt = Δt₀ / √(1 − (v²/c²)) = "
                    "γ Δt₀, where γ = 1 / √(1 − (v²/c²))",
                "time dilation":
                    "the phenomenon of time passing slower to an observer who "
                    "is moving relative to another observer",
                "twin paradox":
                    "this asks why a twin traveling at a relativistic speed "
                    "away and then back towards the Earth ages less than the "
                    "Earth-bound twin. The premise to the paradox is faulty "
                    "because the traveling twin is accelerating, and special "
                    "relativity does not apply to accelerating frames of "
                    "reference", },
            "28.3": {
                "length contraction ":
                    "L , the shortening of the measured length of an object "
                    "moving relative to the observer’s frame: L = L₀ "
                    "√(1−(v²/c²)) = L₀/γ",
                "proper length ":
                    "L₀; the distance between two points measured by an "
                    "observer who is at rest relative to both of the points; "
                    "Earth-bound observers measure proper length when "
                    "measuring the distance between two points that are "
                    "stationary relative to the Earth", },
            "28.4": {
                "relativistic velocity addition":
                    "the method of adding velocities of an object moving at a "
                    "relativistic speed: u = (v + u′) / (1 + (vu′)/c²), where "
                    "v is the relative velocity between two observers, u is "
                    "the velocity of an object relative to one observer, and "
                    "u′ is the velocity relative to the other observer", },
            "28.5": {
                "relativistic momentum":
                    "p, the momentum of an object moving at relativistic "
                    "velocity; p = γ m u, where m is the rest mass of the "
                    "object, u is its velocity relative to an observer, and "
                    "the relativistic factor γ = 1 / √(1 − (v²/c²))",
                "rest mass":
                    "the mass of an object as measured by a person at rest "
                    "relative to the object", },
            "28.6": {
                "relativistic Doppler effects":
                    "a change in wavelength of radiation that is moving "
                    "relative to the observer; the wavelength of the "
                    "radiation is longer (called a red shift) than that "
                    "emitted by the source when the source moves away from "
                    "the observer and shorter (called a blue shift) when the "
                    "source moves toward the observer; the shifted wavelength "
                    "is described by the equation λ_(obs) = λ_s √((1 + u/c) / "
                    "(1 − u/c)) where λ_(obs) is the observed wavelength, λ_s "
                    "is the source wavelength, and u is the velocity of the "
                    "source to the observer",
                "relativistic kinetic energy":
                    "the kinetic energy of an object moving at relativistic "
                    "speeds: K E_(rel) = (γ − 1) m c², where γ = 1 / √(1 − "
                    "(v²/c²))",
                "rest energy":
                    "the energy stored in an object at rest: E₀ = mc²",
                "total energy ":
                    "defined as E = γ mc², where γ = 1 / √(1 − (v²/c²))", },
            "29": {
                "correspondence principle":
                    "in the classical limit (large, slow-moving objects), "
                    "quantum mechanics becomes the same as classical physics",
                "quantized":
                    "the fact that certain physical entities exist only with "
                    "particular discrete values and not every conceivable "
                    "value",
                "quantum mechanics":
                    "the branch of physics that deals with small objects and "
                    "with the quantization of various entities, especially "
                    "energy", },
            "29.1": {
                "atomic spectra":
                    "the electromagnetic emission from atoms and molecules",
                "blackbody":
                    "an ideal radiator, which can radiate equally well at all "
                    "wavelengths",
                "blackbody radiation":
                    "the electromagnetic radiation from a blackbody",
                "Planck’s constant":
                    "h = 6.626 × 10⁻³⁴J⋅s", },
            "29.2": {
                "binding energy":
                    "also called the work function; the amount of energy "
                    "necessary to eject an electron from a material",
                "photoelectric effect":
                    "the phenomenon whereby some materials eject electrons "
                    "when light is shined on them",
                "photon":
                    "a quantum, or particle, of electromagnetic radiation",
                "photon energy":
                    "the amount of energy a photon has; E=hf", },
            "29.3": {
                "bremsstrahlung":
                    "German for braking radiation; produced when electrons "
                    "are decelerated",
                "characteristic x rays":
                    "x rays whose energy depends on the material they were "
                    "produced in",
                "gamma rays":
                    "also γ-ray; highest-energy photon in the EM spectrum",
                "infrared radiation (IR)":
                    "photons with energies slightly less than red light",
                "ionizing radiation":
                    "radiation that ionizes materials that absorb it",
                "microwaves":
                    "photons with wavelengths on the order of a micron (μm)",
                "ultraviolet radiation":
                    "UV; ionizing photons slightly more energetic than violet "
                    "light",
                "visible light":
                    "the range of photon energies the human eye can detect",
                "x-rays":
                    "EM photon between γ-ray and UV in energy", },
            "29.4": {
                "Compton effect":
                    "the phenomenon whereby x rays scattered from materials "
                    "have decreased energy",
                "photon momentum":
                    "the amount of momentum a photon has, calculated by p = "
                    "h/λ = E/c", },
            "29.5": {
                "particle-wave duality":
                    "the property of behaving like either a particle or a "
                    "wave; the term for the phenomenon that all particles "
                    "have wave characteristics", },
            "29.6": {
                "de Broglie wavelength":
                    "the wavelength possessed by a particle of matter, "
                    "calculated by λ=h/p", },
            "29.7": {
                "Heisenberg’s uncertainty principle ":
                    "a fundamental limit to the precision with which pairs of "
                    "quantities (momentum and position, and energy and time) "
                    "can be measured",
                "probability distribution":
                    "the overall spatial distribution of probabilities to "
                    "find a particle at a given location",
                "uncertainty in energy":
                    "lack of precision or lack of knowledge of precise "
                    "results in measurements of energy",
                "uncertainty in momentum":
                    "lack of precision or lack of knowledge of precise "
                    "results in measurements of momentum",
                "uncertainty in position":
                    "lack of precision or lack of knowledge of precise "
                    "results in measurements of position",
                "uncertainty in time":
                    "lack of precision or lack of knowledge of precise "
                    "results in measurements of time", },
            "30.1": {
                "atom":
                    "basic unit of matter, which consists of a central, "
                    "positively charged nucleus surrounded by negatively "
                    "charged electrons",
                "Brownian motion":
                    "the continuous random movement of particles of matter "
                    "suspended in a liquid or gas", },
            "30.2": {
                "cathode-ray tube":
                    "a vacuum tube containing a source of electrons and a "
                    "screen to view images",
                "planetary model of the atom":
                    "the most familiar model or illustration of the structure "
                    "of the atom", },
            "30.3": {
                "Bohr radius":
                    "the mean radius of the orbit of an electron around the "
                    "nucleus of a hydrogen atom in its ground state",
                "double-slit interference":
                    "an experiment in which waves or particles from a single "
                    "source impinge upon two slits so that the resulting "
                    "interference pattern may be observed",
                "energies of hydrogen-like atoms":
                    "Bohr formula for energies of electron states in hydrogen-"
                    "like atoms: E_n = − Z²/n² E₀(n = 1, 2, 3, …)",
                "energy-level diagram":
                    "a diagram used to analyze the energy level of electrons "
                    "in the orbits of an atom",
                "hydrogen spectrum wavelength":
                    "the wavelengths of visible light from hydrogen; can be "
                    "calculated by 1/λ = R(1/(n_f)² − 1/(n_i²))",
                "hydrogen-like atom":
                    "any atom with only a single electron",
                "Rydberg constant":
                    "a physical constant related to the atomic spectra with "
                    "an established value of 1.097 × 10⁷m⁻ⁱ", },
            "30.4": {
                "x-ray diffraction":
                    "a technique that provides the detailed information about "
                    "crystallographic structure of natural and manufactured "
                    "materials",
                "x-rays":
                    "a form of electromagnetic radiation", },
            "30.5": {
                "atomic de-excitation":
                    "process by which an atom transfers from an excited "
                    "electronic state back to the ground state electronic "
                    "configuration; often occurs by emission of a photon",
                "atomic excitation":
                    "a state in which an atom or ion acquires the necessary "
                    "energy to promote one or more of its electrons to "
                    "electronic states higher in energy than their ground "
                    "state",
                "fluorescence":
                    "any process in which an atom or molecule, excited by a "
                    "photon of a given energy, de-excites by emission of a "
                    "lower-energy photon",
                "hologram":
                    "means entire picture (from the Greek word holo, as in "
                    "holistic), because the image produced is three "
                    "dimensional",
                "holography":
                    "the process of producing holograms",
                "laser":
                    "acronym for light amplification by stimulated emission "
                    "of radiation",
                "metastable":
                    "a state whose lifetime is an order of magnitude longer "
                    "than the most short-lived states",
                "phosphorescence":
                    "the de-excitation of a metastable state",
                "population inversion":
                    "the condition in which the majority of atoms in a sample "
                    "are in a metastable state",
                "Stimulated emission":
                    "emission by atom or molecule in which an excited state "
                    "is stimulated to decay, most readily caused by a photon "
                    "of the same energy that is necessary to excite the "
                    "state", },
            "30.7": {
                "fine structure":
                    "the splitting of spectral lines of the hydrogen spectrum "
                    "when the spectral lines are examined at very high "
                    "resolution",
                "intrinsic magnetic field ":
                    "the magnetic field generated due to the intrinsic spin "
                    "of electrons",
                "intrinsic spin":
                    "the internal or intrinsic angular momentum of electrons",
                "orbital angular momentum":
                    "an angular momentum that corresponds to the quantum "
                    "analog of classical angular momentum",
                "orbital magnetic field":
                    "the magnetic field generated due to the orbital motion "
                    "of electrons",
                "space quantization":
                    "the fact that the orbital angular momentum can have only "
                    "certain directions",
                "Zeeman effect":
                    "the effect of external magnetic fields on spectral "
                    "lines", },
            "30.8": {
                "angular momentum quantum number":
                    "a quantum number associated with the angular momentum of "
                    "electrons",
                "magnitude of the intrinsic (internal) spin angular momentum":
                    "given by S = √(s (s + 1) (h/(2π)))",
                "quantum numbers":
                    "the values of quantized entities, such as energy and "
                    "angular momentum",
                "spin projection quantum number":
                    "quantum number that can be used to calculate the "
                    "intrinsic electron angular momentum along the z-axis",
                "spin quantum number":
                    "the quantum number that parameterizes the intrinsic "
                    "angular momentum (or spin angular momentum, or simply "
                    "spin) of a given particle",
                "z-component of spin angular momentum":
                    "component of intrinsic electron spin along the z-axis",
                "z-component of the angular momentum":
                    "component of orbital angular momentum of electron along "
                    "the z-axis", },
            "30.9": {
                "atomic number":
                    "the number of protons in the nucleus of an atom",
                "Pauli exclusion principle":
                    "a principle that states that no two electrons can have "
                    "the same set of quantum numbers; that is, no two "
                    "electrons can be in the same state",
                "shell":
                    "a probability cloud for electrons that has a single "
                    "principal quantum number",
                "subshell":
                    "the probability cloud for electrons that has a single "
                    "angular momentum quantum number l", },
            "31.1": {
                "alpha rays":
                    "one of the types of rays emitted from the nucleus of an "
                    "atom",
                "beta rays":
                    "one of the types of rays emitted from the nucleus of an "
                    "atom",
                "decay":
                    "the process by which an atomic nucleus of an unstable "
                    "atom loses mass and energy by emitting ionizing "
                    "particles",
                "gamma rays":
                    "one of the types of rays emitted from the nucleus of an "
                    "atom",
                "ionizing radiation":
                    "radiation (whether nuclear in origin or not) that "
                    "produces ionization whether nuclear in origin or not",
                "nuclear radiation":
                    "rays that originate in the nuclei of atoms, the first "
                    "examples of which were discovered by Becquerel",
                "nucleus":
                    "a region consisting of protons and neutrons at the "
                    "center of an atom",
                "radioactive":
                    "a substance or object that emits nuclear radiation",
                "radioactivity":
                    "the emission of rays from the nuclei of atoms",
                "range of radiation":
                    "the distance that the radiation can travel through a "
                    "material", },
            "31.2": {
                "Geiger tube":
                    "a very common radiation detector that usually gives an "
                    "audio output",
                "photomultiplier":
                    "a device that converts light into electrical signals",
                "radiation detector":
                    "a device that is used to detect and track the radiation "
                    "from a radioactive reaction",
                "scintillators":
                    "a radiation detection method that records light produced "
                    "when radiation interacts with materials",
                "solid-state radiation detectors":
                    "semiconductors fabricated to directly convert incident "
                    "radiation into electrical current", },
            "31.3": {
                "atomic mass":
                    "the total mass of the protons, neutrons, and electrons "
                    "in a single atom",
                "atomic number":
                    "number of protons in a nucleus",
                "chart of the nuclides":
                    "a table comprising stable and unstable nuclei",
                "isotopes":
                    "nuclei having the same Z and different Ns",
                "magic numbers":
                    "a number that indicates a shell structure for the "
                    "nucleus in which closed shells are more stable",
                "mass number":
                    "number of nucleons in a nucleus",
                "neutron":
                    "a neutral particle that is found in a nucleus",
                "nucleons":
                    "the particles found inside nuclei",
                "nuclide":
                    "a type of atom whose nucleus has specific numbers of "
                    "protons and neutrons",
                "protons":
                    "the positively charged nucleons found in a nucleus",
                "radius of a nucleus":
                    "the radius of a nucleus is r = r₀A^(1/3)", },
            "31.4": {
                "alpha decay":
                    "type of radioactive decay in which an atomic nucleus "
                    "emits an alpha particle",
                "antielectron":
                    "another term for positron",
                "antimatter":
                    "composed of antiparticles",
                "beta decay":
                    "type of radioactive decay in which an atomic nucleus "
                    "emits a beta particle",
                "daughter":
                    "the nucleus obtained when parent nucleus decays and "
                    "produces another nucleus following the rules and the "
                    "conservation laws",
                "decay equation":
                    "the equation to find out how much of a radioactive "
                    "material is left after a given period of time",
                "decay series":
                    "process whereby subsequent nuclides decay until a stable "
                    "nuclide is produced",
                "electron capture":
                    "the process in which a proton-rich nuclide absorbs an "
                    "inner atomic electron and simultaneously emits a "
                    "neutrino",
                "electron capture equation":
                    "equation representing the electron capture",
                "electron’s antineutrino":
                    "antiparticle of electron’s neutrino",
                "electron’s neutrino":
                    "a subatomic elementary particle which has no net "
                    "electric charge",
                "gamma decay":
                    "type of radioactive decay in which an atomic nucleus "
                    "emits a gamma particle",
                "neutrino":
                    "an electrically neutral, weakly interacting elementary "
                    "subatomic particle",
                "nuclear reaction energy":
                    "the energy created in a nuclear reaction",
                "parent":
                    "the original state of nucleus before decay",
                "positron":
                    "the particle that results from positive beta decay; also "
                    "known as an antielectron",
                "positron decay":
                    "type of beta decay in which a proton is converted to a "
                    "neutron, releasing a positron and a neutrino", },
            "31.5": {
                "activity":
                    "the rate of decay for radioactive nuclides",
                "becquerel":
                    "SI unit for rate of decay of a radioactive material",
                "carbon-14 dating":
                    "a radioactive dating technique based on the "
                    "radioactivity of carbon-14",
                "curie":
                    "the activity of 1 g of ²²⁶Ra, equal to 3.70 × 10ⁱ⁰ Bq",
                "decay constant":
                    "quantity that is inversely proportional to the half-life "
                    "and that is used in equation for number of nuclei as a "
                    "function of time",
                "half-life":
                    "the time in which there is a 50% chance that a nucleus "
                    "will decay",
                "radioactive dating":
                    "an application of radioactive decay in which the age of "
                    "a material is determined by the amount of radioactivity "
                    "of a particular type that occurs",
                "rate of decay":
                    "the number of radioactive events per unit time", },
            "31.6": {
                "binding energy":
                    "the energy needed to separate nucleus into individual "
                    "protons and neutrons",
                "binding energy per nucleon":
                    "the binding energy calculated per nucleon; it reveals "
                    "the details of the nuclear force—larger the BE/A, the "
                    "more stable the nucleus", },
            "31.7": {
                "barrier penetration":
                    "quantum mechanical effect whereby a particle has a "
                    "nonzero probability to cross through a potential energy "
                    "barrier despite not having sufficient energy to pass "
                    "over the barrier; also called quantum mechanical "
                    "tunneling",
                "quantum mechanical tunneling":
                    "quantum mechanical effect whereby a particle has a "
                    "nonzero probability to cross through a potential energy "
                    "barrier despite not having sufficient energy to pass "
                    "over the barrier; also called barrier penetration",
                "tunneling":
                    "a quantum mechanical process of potential energy barrier "
                    "penetration", },
            "32.1": {
                "Anger camera":
                    "a common medical imaging device that uses a scintillator "
                    "connected to a series of photomultipliers",
                "gamma camera":
                    "another name for an Anger camera",
                "positron emission tomography (PET)":
                    "tomography technique that uses β⁺ emitters and detects "
                    "the two annihilation γ rays, aiding in source "
                    "localization",
                "radiopharmaceutical":
                    "compound used for medical imaging",
                "single-photon-emission computed tomography (SPECT)":
                    "tomography performed with γ-emitting "
                    "radiopharmaceuticals",
                "tagged":
                    "process of attaching a radioactive substance to a "
                    "chemical compound", },
            "32.2": {
                "gray (Gy)":
                    "the SI unit for radiation dose which is defined to be 1 "
                    "Gy=1 J/kg=100 rad",
                "high dose":
                    "a dose greater than 1 Sv (100 rem)",
                "hormesis":
                    "a term used to describe generally favorable biological "
                    "responses to low exposures of toxins or radiation",
                "linear hypothesis":
                    "assumption that risk is directly proportional to risk "
                    "from high doses",
                "low dose":
                    "a dose less than 100 mSv (10 rem)",
                "moderate dose":
                    "a dose from 0.1 Sv to 1 Sv (10 to 100 rem)",
                "quality factor":
                    "same as relative biological effectiveness",
                "rad":
                    "the ionizing energy deposited per kilogram of tissue",
                "relative biological effectiveness":
                    "a number that expresses the relative amount of damage "
                    "that a fixed amount of ionizing radiation of a given "
                    "type can inflict on biological tissues",
                "roentgen equivalent man":
                    "a dose unit more closely related to effects in "
                    "biological tissue",
                "shielding":
                    "a technique to limit radiation exposure",
                "sievert":
                    "the SI equivalent of the rem", },
            "32.3": {
                "radiotherapy":
                    "the use of ionizing radiation to treat ailments",
                "therapeutic ratio":
                    "the ratio of abnormal cells killed to normal cells "
                    "killed", },
            "32.4": {
                "food irradiation":
                    "treatment of food with ionizing radiation",
                "free radicals":
                    "ions with unstable oxygen- or hydrogen-containing "
                    "molecules",
                "radiolytic products":
                    "compounds produced due to chemical reactions of free "
                    "radicals", },
            "32.5": {
                "break-even":
                    "when fusion power produced equals the heating power "
                    "input",
                "Ignition":
                    "when a fusion reaction produces enough energy to be self-"
                    "sustaining after external energy input is cut off",
                "inertial confinement":
                    "a technique that aims multiple lasers at tiny fuel "
                    "pellets evaporating and crushing them to high density",
                "magnetic confinement":
                    "a technique in which charged particles are trapped in a "
                    "small region because of difficulty in crossing magnetic "
                    "field lines",
                "nuclear fusion":
                    "a reaction in which two nuclei are combined, or fused, "
                    "to form a larger nucleus",
                "proton-proton cycle":
                    "the combined reactions ¹H+¹H → ²H+e⁺+vₑ, ¹H+²H → ³He+γ, "
                    "and ³He+³He → ⁴He+¹H+¹H", },
            "32.6": {
                "breeder reactors":
                    "reactors that are designed specifically to make "
                    "plutonium",
                "breeding":
                    "reaction process that produces ²³⁹Pu",
                "critical mass":
                    "minimum amount necessary for self-sustained fission of a "
                    "given nuclide",
                "criticality":
                    "condition in which a chain reaction easily becomes "
                    "self-sustaining",
                "fission fragments":
                    "a daughter nuclei",
                "liquid drop model":
                    "a model of nucleus (only to understand some of its "
                    "features) in which nucleons in a nucleus act like atoms "
                    "in a drop",
                "neutron-induced fission":
                    "fission that is initiated after the absorption of "
                    "neutron",
                "nuclear fission":
                    "reaction in which a nucleus splits",
                "supercriticality":
                    "an exponential increase in fissions", },
            "33": {
                "particle physics":
                    "the study of and the quest for those truly fundamental "
                    "particles having no substructure", },
            "33.1": {
                "meson":
                    "particle whose mass is intermediate between the electron "
                    "and nucleon masses",
                "pion":
                    "particle exchanged between nucleons, transmitting the "
                    "force between them",
                "virtual particles":
                    "particles which cannot be directly observed but their "
                    "effects can be directly observed", },
            "33.2": {
                "Feynman diagram":
                    "a graph of time versus position that describes the "
                    "exchange of virtual particles between subatomic "
                    "particles",
                "gluons":
                    "exchange particles, analogous to the exchange of photons "
                    "that gives rise to the electromagnetic force between two "
                    "charged particles",
                "quantum electrodynamics":
                    "the theory of electromagnetism on the particle scale", },
            "33.3": {
                "colliding beams":
                    "head-on collisions between particles moving in opposite "
                    "directions",
                "cyclotron":
                    "accelerator that uses fixed-frequency alternating "
                    "electric fields and fixed magnets to accelerate "
                    "particles in a circular spiral path",
                "linear accelerator":
                    "accelerator that accelerates particles in a straight "
                    "line",
                "synchrotron":
                    "a version of a cyclotron in which the frequency of the "
                    "alternating voltage and the magnetic field strength are "
                    "increased as the beam particles are accelerated",
                "synchrotron radiation":
                    "radiation caused by a magnetic field accelerating a "
                    "charged particle perpendicular to its velocity",
                "Van de Graaff":
                    "early accelerator: simple, large-scale version of the "
                    "electron gun", },
            "33.4": {
                "baryon number":
                    "a conserved physical quantity that is zero for mesons "
                    "and leptons and ±1 for baryons and antibaryons, "
                    "respectively",
                "baryons":
                    "hadrons that always decay to another baryon",
                "boson":
                    "particle with zero or an integer value of intrinsic spin",
                "conservation of total ":
                    "a general rule stating the family number stays the same "
                    "through an interaction",
                "conservation of total baryon number":
                    "a general rule based on the observation that the total "
                    "number of nucleons was always conserved in nuclear "
                    "reactions and decays",
                "conservation of total electron family number":
                    "a general rule stating that the total electron family "
                    "number stays the same through an interaction",
                "conservation of total muon family number":
                    "a general rule stating that the total muon family number "
                    "stays the same through an interaction",
                "electron family number ":
                    "the number ±1 that is assigned to all members of the "
                    "electron family, or the number 0 that is assigned to all "
                    "particles not in the electron family",
                "fermion":
                    "particle with a half-integer value of intrinsic spin",
                "gauge bosons":
                    "particle that carries one of the four forces",
                "hadrons":
                    "particles that feel the strong nuclear force",
                "leptons":
                    "particles that do not feel the strong nuclear force",
                "mesons":
                    "hadrons that can decay to leptons and leave no hadrons",
                "muon family number":
                    "the number ±1 that is assigned to all members of the "
                    "muon family, or the number 0 that is assigned to all "
                    "particles not in the muon family",
                "strangeness":
                    "a physical quantity assigned to various particles based "
                    "on decay systematics", },
            "33.5": {
                "bottom":
                    "a quark flavor",
                "charm":
                    "a quark flavor, which is the counterpart of the strange "
                    "quark",
                "color":
                    "a quark flavor",
                "down":
                    "the second-lightest of all quarks",
                "flavors":
                    "quark type",
                "fundamental particle":
                    "particle with no substructure",
                "quantum chromodynamics":
                    "quark theory including color",
                "quark":
                    "an elementary particle and a fundamental constituent of "
                    "matter",
                "strange":
                    "the third lightest of all quarks",
                "theory of quark confinement":
                    "explains how quarks can exist and yet never be isolated "
                    "or directly observed",
                "top":
                    "a quark flavor",
                "up":
                    "the lightest of all quarks", },
            "33.6": {
                "electroweak theory":
                    "theory showing connections between EM and weak forces",
                "frand unified theory (GUT)":
                    "theory that shows unification of the strong and "
                    "electroweak forces",
                "gluons":
                    "eight proposed particles which carry the strong force",
                "Higgs boson":
                    "a massive particle that, if observed, would give "
                    "validity to the theory that carrier particles are "
                    "identical under certain circumstances",
                "quantum chromodynamics":
                    "the governing theory of connecting quantum number color "
                    "to gluons",
                "standard model":
                    "combination of quantum chromodynamics and electroweak "
                    "theory",
                "superstring theory":
                    "a theory of everything based on vibrating strings some "
                    "10⁻³⁵m in length", },
            "34.1": {
                "Big Bang":
                    "a gigantic explosion that threw out matter a few billion "
                    "years ago",
                "cosmic microwave background":
                    "the spectrum of microwave radiation of cosmic origin",
                "cosmological red shift":
                    "the photon wavelength is stretched in transit from the "
                    "source to the observer because of the expansion of space "
                    "itself",
                "cosmology":
                    "the study of the character and evolution of the universe",
                "electroweak epoch":
                    "the stage before 10⁻ⁱⁱ back to 10⁻³⁴ after the Big Bang",
                "GUT epoch":
                    "the time period from 10⁻⁴³ to 10⁻³⁴ after the Big Bang, "
                    "when Grand Unification Theory, in which all forces "
                    "except gravity are identical, governed the universe",
                "Hubble constant":
                    "a central concept in cosmology whose value is determined "
                    "by taking the slope of a graph of velocity versus "
                    "distance, obtained from red shift measurements",
                "inflationary scenario":
                    "the rapid expansion of the universe by an incredible "
                    "factor of 10⁻⁵⁰ for the brief time from 10⁻³⁵ to about "
                    "10⁻³²s",
                "spontaneous symmetry breaking":
                    "the transition from GUT to electroweak where the forces "
                    "were no longer unified",
                "superforce":
                    "hypothetical unified force in TOE epoch",
                "TOE epoch":
                    "before 10⁻⁴³ after the Big Bang", },
            "34.2": {
                "black holes":
                    "objects having such large gravitational fields that "
                    "things can fall in, but nothing, not even light, can "
                    "escape",
                "escape velocity":
                    "takeoff velocity when kinetic energy just cancels "
                    "gravitational potential energy",
                "event horizon":
                    "the distance from the object at which the escape "
                    "velocity is exactly the speed of light",
                "general relativity":
                    "Einstein’s theory that describes all types of relative "
                    "motion including accelerated motion and the effects of "
                    "gravity",
                "gravitational waves":
                    "mass-created distortions in space that propagate at the "
                    "speed of light and that are predicted by general "
                    "relativity",
                "neutron stars":
                    "literally a star composed of neutrons",
                "quantum gravity":
                    "the theory that deals with particle exchange of "
                    "gravitons as the mechanism for the force",
                "quasars":
                    "the moderately distant galaxies that emit as much or "
                    "more energy than a normal galaxy",
                "Schwarzschild radius":
                    "the radius of the event horizon",
                "thought experiment":
                    "mental analysis of certain carefully and clearly defined "
                    "situations to develop an idea", },
            "34.3": {
                "superstring theory":
                    "a theory to unify gravity with the other three forces in "
                    "which the fundamental particles are considered to act "
                    "like one-dimensional vibrating strings", },
            "34.4": {
                "axions":
                    "a type of WIMPs having masses about 10⁻ⁱ⁰ of an electron "
                    "mass",
                "cosmological constant":
                    "a theoretical construct intimately related to the "
                    "expansion and closure of the universe",
                "critical density":
                    "the density of matter needed to just halt universal "
                    "expansion",
                "dark matter":
                    "indirectly observed non-luminous matter",
                "flat (zero curvature) universe":
                    "a universe that is infinite but not curved",
                "MACHOs":
                    "massive compact halo objects; microlensing objects of "
                    "huge mass",
                "massive compact halo objects":
                    "massive compact halo objects; microlensing objects of "
                    "huge mass",
                "microlensing":
                    "a process in which light from a distant star is focused "
                    "and the star appears to brighten in a characteristic "
                    "manner, when a small body (smaller than about 1/1000 the "
                    "mass of the Sun) passes between us and the star",
                "negatively curved":
                    "an open universe that expands forever",
                "neutralinos":
                    "a type of WIMPs having masses several orders of "
                    "magnitude greater than nucleon masses",
                "neutrino oscillations":
                    "a process in which any type of neutrino could change "
                    "spontaneously into any other",
                "positively curved":
                    "a universe that is closed and eventually contracts",
                "weakly interacting massive particles":
                    "weakly interacting massive particles; chargeless leptons "
                    "(non-baryonic matter) interacting negligibly with normal "
                    "matter",
                "WIMPs":
                    "weakly interacting massive particles; chargeless leptons "
                    "(non-baryonic matter) interacting negligibly with normal "
                    "matter", },
            "34.5": {
                "chaos":
                    "word used to describe systems the outcomes of which are "
                    "extremely sensitive to initial conditions",
                "complexity":
                    "an emerging field devoted to the study of complex "
                    "systems", },
            "34.6": {
                "critical temperature":
                    "the temperature at which and below which a material "
                    "becomes a superconductor",
                "superconductors":
                    "materials with resistivity of zero", },
        }


class IntroductionToSociology2e(OpenStaxBook):
    """Introduction to Sociology 2e."""

    def __init__(self) -> None:
        """Initialize the term group."""
        self._book_title = "Introduction To Sociology 2e"
        self._terms = {
            "1.1": {
                "culture":
                    "a group's shared practices, values, and beliefs",
                "figuration":
                    "the process of simultaneously analyzing the behavior of "
                    "an individual and the society that shapes that behavior",
                "macro-level":
                    "a wide-scale view of the role of social structures "
                    "within a society",
                "micro-level theories":
                    "the study of specific relationships between individuals "
                    "or small groups",
                "reification":
                    "an error of treating an abstract concept as though it "
                    "has a real, material existence",
                "social facts":
                    "the laws, morals, values, religious beliefs, customs, "
                    "fashions, rituals, and all of the cultural rules that "
                    "govern social life",
                "society":
                    "a group of people who live in a defined geographical "
                    "area who interact with one another and who share a "
                    "common culture",
                "sociological imagination":
                    "the ability to understand how your own past relates to "
                    "that of other people, as well as to history in general "
                    "and societal structures in particular",
                "sociology":
                    "the systematic study of society and social interaction",
                    },
            "1.2": {
                "antipositivism":
                    "the view that social researchers should strive for "
                    "subjectivity as they worked to represent social "
                    "processes, cultural norms, and societal values",
                "generalized others":
                    "the organized and generalized attitude of a social group",
                "positivism":
                    "the scientific study of social patterns",
                "qualitative sociology":
                    "in-depth interviews, focus groups, and/or analysis of "
                    "content sources as the source of its data",
                "quantitative sociology":
                    "statistical methods such as surveys with large numbers "
                    "of participants",
                "significant others":
                    "specific individuals that impact a person's life",
                "verstehen":
                    "a German word that means to understand in a deep way", },
            "1.3": {
                "conflict theory":
                    "a theory that looks at society as a competition for "
                    "limited resources",
                "constructivism":
                    "an extension of symbolic interaction theory which "
                    "proposes that reality is what humans cognitively "
                    "construct it to be",
                "dramaturgical analysis":
                    "a technique sociologists use in which they view society "
                    "through the metaphor of theatrical performance",
                "dynamic equilibrium":
                    "a stable state in which all parts of a healthy society "
                    "work together properly",
                "dysfunctions":
                    "social patterns that have undesirable consequences for "
                    "the operation of society",
                "function":
                    "the part a recurrent activity plays in the social life "
                    "as a whole and the contribution it makes to structural "
                    "continuity",
                "functionalism":
                    "a theoretical approach that sees society as a structure "
                    "with interrelated parts designed to meet the biological "
                    "and social needs of individuals that make up that "
                    "society",
                "grand theories":
                    "an attempt to explain large-scale relationships and "
                    "answer fundamental questions such as why societies form "
                    "and why they change",
                "hypothesis":
                    "a testable proposition",
                "latent functions":
                    "the unrecognized or unintended consequences of a social "
                    "process",
                "manifest functions":
                    "sought consequences of a social process",
                "paradigms":
                    "philosophical and theoretical frameworks used within a "
                    "discipline to formulate theories, generalizations, and "
                    "the experiments performed in support of them",
                "social institutions":
                    "patterns of beliefs and behaviors focused on meeting "
                    "social needs",
                "social solidarity":
                    "the social ties that bind a group of people together "
                    "such as kinship, shared location, and religion",
                "symbolic interactionism":
                    "a theoretical perspective through which scholars examine "
                    "the relationship of individuals within their society by "
                    "studying their communication (language and symbols)",
                "theory":
                    "a proposed explanation about social interactions or "
                    "society", },
            "2": {
                "empirical evidence":
                    "evidence that comes from direct experience, "
                    "scientifically gathered data, or experimentation",
                "meta-analysis":
                    "a technique in which the results of virtually all "
                    "previous studies on a specific subject are evaluated "
                    "together",
                "scientific method":
                    "an established scholarly research method that involves "
                    "asking a question, researching existing sources, forming "
                    "a hypothesis, designing and conducting a study, and "
                    "drawing conclusions", },
            "2.1": {
                "dependent variable":
                    "a variable changed by other variables",
                "hypothesis":
                    "a testable educated guess about predicted outcomes "
                    "between two or more variables",
                "independent variables":
                    "variables that cause changes in dependent variables",
                "interpretive framework":
                    "a sociological research approach that seeks in-depth "
                    "understanding of a topic or subject through observation "
                    "or interaction; this approach is not based on hypothesis "
                    "testing",
                "literature review":
                    "a scholarly research step that entails identifying and "
                    "studying all existing studies on a topic to create a "
                    "basis for new research",
                "operational definition":
                    "specific explanations of abstract concepts that a "
                    "researcher plans to study",
                "reliability":
                    "a measure of a study’s consistency that considers how "
                    "likely results are to be replicated if a study is "
                    "reproduced",
                "validity":
                    "the degree to which a sociological measure accurately "
                    "reflects the topic of study", },
            "2.2": {
                "case study":
                    "in-depth analysis of a single event, situation, or "
                    "individual",
                "content analysis":
                    "applying a systematic approach to record and value "
                    "information gleaned from secondary data as it relates to "
                    "the study at hand",
                "correlation":
                    "when a change in one variable coincides with a change in "
                    "another variable, but does not necessarily indicate "
                    "causation",
                "ethnography":
                    "observing a complete social setting and all that it "
                    "entails",
                "experiment":
                    "the testing of a hypothesis under controlled conditions",
                "field research":
                    "gathering data from a natural environment without doing "
                    "a lab experiment or a survey",
                "Hawthorne effect":
                    "when study subjects behave in a certain manner due to "
                    "their awareness of being observed by a researcher",
                "interview":
                    "a one-on-one conversation between the researcher and the "
                    "subject",
                "nonreactive research":
                    "using secondary data, does not include direct contact "
                    "with subjects and will not alter or influence people’s "
                    "behaviors",
                "participant observation":
                    "when a researcher immerses herself in a group or social "
                    "setting in order to make observations from an “insider” "
                    "perspective",
                "population":
                    "a defined group serving as the subject of a study",
                "primary data":
                    "data that are collected directly from firsthand "
                    "experience",
                "qualitative data":
                    "comprise information that is subjective and often based "
                    "on what is seen in a natural setting",
                "quantitative data":
                    "represent research collected in numerical form that can "
                    "be counted",
                "random sample":
                    "a study’s participants being randomly selected to serve "
                    "as a representation of a larger population",
                "sample":
                    "small, manageable number of subjects that represent the "
                    "population",
                "secondary data analysis":
                    "using data collected by others but applying new "
                    "interpretations",
                "survey":
                    "collect data from subjects who respond to a series of "
                    "questions about behaviors and opinions, often in the "
                    "form of a questionnaire", },
            "2.3": {
                "code of ethics":
                    "a set of guidelines that the American Sociological "
                    "Association has established to foster ethical research "
                    "and professionally responsible scholarship in sociology",
                "value neutrality":
                    "a practice of remaining impartial, without bias or "
                    "judgment during the course of a study and in publishing "
                    "results", },
            "3": {
                "culture":
                    "shared beliefs, values, and practices",
                "society":
                    "people who live in a definable community and who share a "
                    "culture", },
            "3.1": {
                "cultural imperialism":
                    "the deliberate imposition of one’s own cultural values "
                    "on another culture",
                "cultural relativism":
                    "the practice of assessing a culture by its own "
                    "standards, and not in comparison to another culture",
                "cultural universals":
                    "patterns or traits that are globally common to all "
                    "societies",
                "culture shock":
                    "an experience of personal disorientation when confronted "
                    "with an unfamiliar way of life",
                "ethnocentrism":
                    "the practice of evaluating another culture according to "
                    "the standards of one’s own culture",
                "material culture":
                    "the objects or belongings of a group of people",
                "nonmaterial culture":
                    "the ideas, attitudes, and beliefs of a society",
                "xenocentrism":
                    "a belief that another culture is superior to one’s own",
                    },
            "3.2": {
                "beliefs":
                    "tenets or convictions that people hold to be true",
                "folkways":
                    "direct, appropriate behavior in the day-to-day practices "
                    "and expressions of a culture",
                "formal norms":
                    "established, written rules",
                "ideal culture":
                    "the standards a society would like to embrace and live "
                    "up to",
                "informal norms":
                    "casual behaviors that are generally and widely conformed "
                    "to",
                "language":
                    "a symbolic system of communication",
                "mores":
                    "the moral views and principles of a group",
                "norms":
                    "the visible and invisible rules of conduct through which "
                    "societies are structured",
                "real culture":
                    "the way society really is based on what actually occurs "
                    "and exists",
                "sanction":
                    "a way to authorize or formally disapprove of certain "
                    "behaviors",
                "Sapir-Whorf hypothesis":
                    "the way that people understand the world based on their "
                    "form of language",
                "social control":
                    "a way to encourage conformity to cultural norms",
                "symbols":
                    "gestures or objects that have meanings associated with "
                    "them that are recognized by people who share a culture",
                "values":
                    "a culture’s standard for discerning what is good and "
                    "just in society", },
            "3.3": {
                "countercultures":
                    "groups that reject and oppose society’s widely accepted "
                    "cultural patterns",
                "culture lag":
                    "the gap of time between the introduction of material "
                    "culture and nonmaterial culture’s acceptance of it",
                "diffusion":
                    "the spread of material and nonmaterial culture from one "
                    "culture to another",
                "discoveries":
                    "things and ideas found from what already exists",
                "globalization":
                    "the integration of international trade and finance "
                    "markets",
                "high culture":
                    "the cultural patterns of a society’s elite",
                "innovation":
                    "new objects or ideas introduced to culture for the first "
                    "time",
                "inventions":
                    "a combination of pieces of existing reality into new "
                    "forms",
                "popular culture":
                    "mainstream, widespread patterns among a society’s "
                    "population",
                "subculture":
                    "groups that share a specific identification, apart from "
                    "a society’s majority, even as the members exist within a "
                    "larger society", },
            "4.1": {
                "agricultural societies":
                    "societies that rely on farming as a way of life",
                "feudal societies":
                    "societies that operate on a strict hierarchical system "
                    "of power based around land ownership and protection",
                "horticultural societies":
                    "societies based around the cultivation of plants",
                "hunter-gatherer societies":
                    "societies that depend on hunting wild animals and "
                    "gathering uncultivated plants for survival",
                "industrial societies":
                    "societies characterized by a reliance on mechanized "
                    "labor to create material goods",
                "information societies":
                    "societies based on the production of nonmaterial goods "
                    "and services",
                "pastoral societies":
                    "societies based around the domestication of animals",
                "society":
                    "a group of people who live in a definable community and "
                    "share the same culture", },
            "4.2": {
                "alienation":
                    "an individual’s isolation from his society, his work, "
                    "and his sense of self",
                "anomie":
                    "a situation in which society no longer has the support "
                    "of a firm collective consciousness",
                "bourgeoisie":
                    "the owners of the means of production in a society",
                "capitalism":
                    "a way of organizing an economy so that the things that "
                    "are used to make and transport products (such as land, "
                    "oil, factories, ships, etc.) are owned by individual "
                    "people and companies rather than by the government",
                "class consciousness":
                    "the awareness of one’s rank in society",
                "collective conscience":
                    "the communal beliefs, morals, and attitudes of a society",
                "false consciousness":
                    "a person’s beliefs and ideology that are in conflict "
                    "with her best interests",
                "iron cage":
                    "a situation in which an individual is trapped by social "
                    "institutions",
                "mechanical solidarity":
                    "a type of social order maintained by the collective "
                    "consciousness of a culture",
                "organic solidarity":
                    "a type of social order based around an acceptance of "
                    "economic and social differences",
                "proletariat":
                    "the laborers in a society",
                "rationalization":
                    "a belief that modern society should be built around "
                    "logic and efficiency rather than morality or tradition",
                "social integration":
                    "how strongly a person is connected to his or her social "
                    "group", },
            "4.3": {
                "achieved statuses":
                    "the status a person chooses, such as a level of "
                    "education or income",
                "ascribed":
                    "the status outside of an individual’s control, such as "
                    "sex or race",
                "habitualization":
                    "the idea that society is constructed by us and those "
                    "before us, and it is followed like a habit",
                "institutionalization":
                    "the act of implanting a convention or norm into society",
                "looking-glass self":
                    "our reflection of how we think we appear to others",
                "role conflict":
                    "a situation when one or more of an individual’s roles "
                    "clash",
                "role performance":
                    "the expression of a role",
                "role strain":
                    "stress that occurs when too much is required of a single "
                    "role",
                "role-set":
                    "an array of roles attached to a particular status",
                "roles":
                    "patterns of behavior that are representative of a "
                    "person’s social status",
                "self-fulfilling prophecy":
                    "an idea that becomes true when acted upon",
                "status":
                    "the responsibilities and benefits that a person "
                    "experiences according to his or her rank and role in "
                    "society",
                "Thomas theorem":
                    "how a subjective reality can drive events to develop in "
                    "accordance with that reality, despite being originally "
                    "unsupported by objective reality", },
            "5": {
                "socialization":
                    "the process wherein people come to understand societal "
                    "norms and expectations, to accept society’s beliefs, and "
                    "to be aware of societal values", },
            "5.1": {
                "generalized other":
                    "the common behavioral expectations of general society",
                "moral development":
                    "the way people learn what is “good” and “bad” in society",
                "self":
                    "a person’s distinct sense of identity as developed "
                    "through social interaction", },
            "5.2": {
                "nature":
                    "the influence of our genetic makeup on self-development",
                "nurture":
                    "the role that our social environment plays in self-"
                    "development", },
            "5.3": {
                "hidden curriculum":
                    "the informal teaching done in schools that socializes "
                    "children to societal norms",
                "mass media":
                    "distributes impersonal information to a wide audience, "
                    "via television, newspapers, radio, and the Internet",
                "peer group":
                    "a group made up of people who are similar in age and "
                    "social status and who share interests", },
            "5.4": {
                "anticipatory socialization":
                    "the way we prepare for future life roles",
                "degradation ceremony":
                    "the process by which new members of a total institution "
                    "lose aspects of their old identities and are given new "
                    "ones",
                "resocialization":
                    "the process by which old behaviors are removed and new "
                    "behaviors are learned in their place", },
            "6.1": {
                "aggregate":
                    "a collection of people who exist in the same place at "
                    "the same time, but who don’t interact or share a sense "
                    "of identity",
                "category":
                    "people who share similar characteristics but who are not "
                    "connected in any way",
                "expressive functions":
                    "a group function that serves an emotional need",
                "group":
                    "any collection of at least two people who interact with "
                    "some frequency and who share some sense of aligned "
                    "identity",
                "in-group":
                    "a group a person belongs to and feels is an integral "
                    "part of his identity",
                "instrumental function":
                    "being oriented toward a task or goal",
                "out-group":
                    "a group that an individual is not a member of, and may "
                    "even compete with",
                "primary groups":
                    "small, informal groups of people who are closest to us",
                "reference group":
                    "groups to which an individual compares herself",
                "secondary groups":
                    "larger and more impersonal groups that are task-focused "
                    "and time limited", },
            "6.2": {
                "authoritarian leaders":
                    "a leader who issues orders and assigns tasks",
                "conformity":
                    "the extent to which an individual complies with group or "
                    "societal norms",
                "democratic leaders":
                    "a leader who encourages group participation and "
                    "consensus-building before moving into action",
                "dyad":
                    "a two-member group",
                "expressive leaders":
                    "a leader who is concerned with process and with ensuring "
                    "everyone’s emotional wellbeing",
                "instrumental leader":
                    "a leader who is goal oriented with a primary focus on "
                    "accomplishing tasks",
                "laissez-faire leader":
                    "a hands-off leader who allows members of the group to "
                    "make their own decisions",
                "leadership function":
                    "the main focus or goal of a leader",
                "leadership styles":
                    "the style a leader uses to achieve goals or elicit "
                    "action from group members",
                "triad":
                    "a three-member group", },
            "6.3": {
                "bureaucracies":
                    "formal organizations characterized by a hierarchy of "
                    "authority, a clear division of labor, explicit rules, "
                    "and impersonality.",
                "clear division of labor":
                    "the fact that each individual in a bureaucracy has a "
                    "specialized task to perform",
                "coercive organizations":
                    "organizations that people do not voluntarily join, such "
                    "as prison or a mental hospital",
                "explicit rules":
                    "the types of rules in a bureaucracy; rules that are "
                    "outlined, recorded, and standardized",
                "formal organizations":
                    "large, impersonal organizations",
                "hierarchy of authority":
                    "a clear chain of command found in a bureaucracy",
                "impersonality":
                    "the removal of personal feelings from a professional "
                    "situation",
                "Iron Rule of Oligarchy":
                    "the theory that an organization is ruled by a few elites "
                    "rather than through collaboration",
                "McDonaldization of Society":
                    "the increasing presence of the fast food business model "
                    "in common social institutions",
                "meritocracies":
                    "a bureaucracy where membership and advancement is based "
                    "on merit—proven and documented skills",
                "normative organizations":
                    "organizations that people join to pursue shared "
                    "interests or because they provide some intangible "
                    "rewards",
                "total institutions":
                    "an organization in which participants live a controlled "
                    "lifestyle and in which total resocialization occurs",
                "utilitarian organizations":
                    "organizations that are joined to fill a specific "
                    "material need",
                "voluntary organizations":
                    "normative organizations; based on shared interests", },
            "7.1": {
                "deviance":
                    "a violation of contextual, cultural, or social norms",
                "formal sanctions":
                    "sanctions that are officially recognized and enforced",
                "informal sanctions":
                    "sanctions that occur in face-to-face interactions",
                "negative sanctions":
                    "punishments for violating norms",
                "positive sanctions":
                    "rewards given for conforming to norms",
                "sanctions":
                    "the means of enforcing rules",
                "social control":
                    "the regulation and enforcement of norms",
                "social order":
                    "an arrangement of practices and behaviors on which "
                    "society’s members base their daily lives", },
            "7.2": {
                "conflict theory":
                    "a theory that examines social and economic factors as "
                    "the causes of criminal deviance",
                "control theory":
                    "a theory that states social control is directly affected "
                    "by the strength of social bonds and that deviance "
                    "results from a feeling of disconnection from society",
                "cultural deviance theory":
                    "a theory that suggests conformity to the prevailing "
                    "cultural norms of lower-class society causes crime",
                "differential association theory":
                    "a theory that states individuals learn deviant behavior "
                    "from those close to them who provide models of and "
                    "opportunities for deviance",
                "labeling theory":
                    "the ascribing of a deviant behavior to another person by "
                    "members of society",
                "master status":
                    "a label that describes the chief characteristic of an "
                    "individual",
                "power elite":
                    "a small group of wealthy and influential people at the "
                    "top of society who hold the power and resources",
                "primary deviance":
                    "a violation of norms that does not result in any long-"
                    "term effects on the individual’s self-image or "
                    "interactions with others",
                "secondary deviance":
                    "deviance that occurs when a person’s self-concept and "
                    "behavior begin to change after his or her actions are "
                    "labeled as deviant by members of society",
                "social disorganization theory":
                    "a theory that asserts crime occurs in communities with "
                    "weak social ties and the absence of social control",
                "strain theory":
                    "a theory that addresses the relationship between having "
                    "socially acceptable goals and having socially acceptable "
                    "means to reach those goals", },
            "7.3": {
                "corporate crime":
                    "crime committed by white-collar workers in a business "
                    "environment",
                "corrections system":
                    "the system tasked with supervising individuals who have "
                    "been arrested for, convicted of, or sentenced for "
                    "criminal offenses",
                "court":
                    "a system that has the authority to make decisions based "
                    "on law",
                "crime":
                    "a behavior that violates official law and is punishable "
                    "through formal sanctions",
                "criminal justice system":
                    "an organization that exists to enforce a legal code",
                "hate crimes":
                    "attacks based on a person’s race, religion, or other "
                    "characteristics",
                "legal codes":
                    "codes that maintain formal social control through laws",
                "nonviolent crimes":
                    "crimes that involve the destruction or theft of "
                    "property, but do not use force or the threat of force",
                "police":
                    "a civil force in charge of regulating laws and public "
                    "order at a federal, state, or community level",
                "self-report study":
                    "a collection of data acquired using voluntary response "
                    "methods, such as questionnaires or telephone interviews",
                "street crime":
                    "crime committed by average people against other people "
                    "or organizations, usually in public spaces",
                "victimless crime":
                    "activities against the law, but that do not result in "
                    "injury to any individual other than the person who "
                    "engages in them",
                "violent crimes":
                    "crimes based on the use of force or the threat of force",
                    },
            "8.1": {
                "digital divide":
                    "the uneven access to technology around race, class, and "
                    "geographic lines",
                "e-readiness":
                    "the ability to sort through, interpret, and process "
                    "digital knowledge",
                "knowledge gap":
                    "the gap in information that builds as groups grow up "
                    "without access to technology",
                "net neutrality":
                    "the principle that all Internet data should be treated "
                    "equally by internet service providers",
                "technology":
                    "the application of science to solve problems in daily "
                    "life", },
            "8.2": {
                "design patent":
                    "patents that are granted when someone has invented a new "
                    "and original design for a manufactured product",
                "evolutionary model of technological change":
                    "a breakthrough in one form of technology that leads to a "
                    "number of variations, from which a prototype emerges, "
                    "followed by a period of slight adjustments to the "
                    "technology, interrupted by a breakthrough",
                "media":
                    "all print, digital, and electronic means of "
                    "communication",
                "new media":
                    "all interactive forms of information exchange",
                "planned obsolescence":
                    "the act of a technology company planning for a product "
                    "to be obsolete or unable from the time it’s created",
                "plant patents":
                    "patents that recognize the discovery of new plant types "
                    "that can be asexually reproduced",
                "utility patents":
                    "patents that are granted for the invention or discovery "
                    "of any new and useful process, product, or machine", },
            "8.3": {
                "media consolidation":
                    "a process by which fewer and fewer owners control the "
                    "majority of media outlets",
                "media globalization":
                    "the worldwide integration of media through the cross-"
                    "cultural exchange of ideas",
                "oligopoly":
                    "a situation in which a few firms dominate a marketplace",
                "technological diffusion":
                    "the spread of technology across borders",
                "technological globalization":
                    "the cross-cultural development and exchange of "
                    "technology", },
            "8.4": {
                "cyberfeminism":
                    "the application to and promotion of feminism online",
                "gatekeeping":
                    "the sorting process by which thousands of possible "
                    "messages are shaped into a mass media-appropriate form "
                    "and reduced to a manageable amount",
                "narcotizing dysfunction":
                    "a result in which people are too overwhelmed with media "
                    "input to really care about the issue, so their "
                    "involvement becomes defined by awareness instead of by "
                    "action",
                "neo-Luddites":
                    "those who see technology as a symbol of the coldness of "
                    "modern life",
                "panoptic surveillance":
                    "a form of constant monitoring in which the observation "
                    "posts are decentralized and the observed is never "
                    "communicated with directly",
                "technophiles":
                    "those who see technology as symbolizing the potential "
                    "for a brighter future", },
            "9.1": {
                "caste system":
                    "a system in which people are born into a social standing "
                    "that they will retain their entire lives",
                "class":
                    "a group who shares a common social status based on "
                    "factors like wealth, income, education, and occupation",
                "class system":
                    "social standing based on social factors and individual "
                    "accomplishments",
                "endogamous union":
                    "unions of people within the same social category",
                "exogamous marriages":
                    "unions of spouses from different social categories",
                "income":
                    "the money a person earns from work or investments",
                "meritocracy":
                    "an ideal system in which personal effort—or merit—"
                    "determines social standing",
                "primogeniture":
                    "a law stating that all property passes to the firstborn "
                    "son",
                "social stratification":
                    "a socioeconomic system that divides society’s members "
                    "into categories ranking from high to low, based on "
                    "things like wealth, power, and prestige",
                "status consistency":
                    "the consistency, or lack thereof, of an individual’s "
                    "rank across social categories like income, education, "
                    "and occupation",
                "wealth":
                    "the value of money and assets a person has from, for "
                    "example, inheritance", },
            "9.2": {
                "class traits":
                    "the typical behaviors, customs, and norms that define "
                    "each class (also called class markers)",
                "downward mobility":
                    "a lowering of one’s social class",
                "intergenerational mobility":
                    "a difference in social class between different "
                    "generations of a family",
                "intragenerational mobility":
                    "a difference in social class between different members "
                    "of the same generation",
                "social mobility":
                    "the ability to change positions within a social "
                    "stratification system",
                "standard of living":
                    "the level of wealth available to acquire material goods "
                    "and comforts to maintain a particular socioeconomic "
                    "lifestyle",
                "structural mobility":
                    "a societal change that enables a whole group of people "
                    "to move up or down the class ladder",
                "upward mobility":
                    "an increase—or upward shift—in social class", },
            "9.3": {
                "global stratification":
                    "a comparison of the wealth, economic stability, status, "
                    "and power of countries as a whole", },
            "9.4": {
                "conspicuous consumption":
                    "the act of buying and using products to make a statement "
                    "about social standing",
                "Davis-Moore thesis":
                    "a thesis that argues some social stratification is a "
                    "social necessity", },
            "10.1": {
                "capital flight":
                    "the movement (flight) of capital from one nation to "
                    "another, via jobs and resources",
                "core nations":
                    "dominant capitalist countries",
                "debt accumulation":
                    "the buildup of external debt, wherein countries borrow "
                    "money from other nations to fund their expansion or "
                    "growth goals",
                "deindustrialization":
                    "the loss of industrial production, usually to peripheral "
                    "and semi-peripheral nations where the costs are lower",
                "first world":
                    "a term from the Cold War era that is used to describe "
                    "industrialized capitalist democracies",
                "fourth world":
                    "a term that describes stigmatized minority groups who "
                    "have no voice or representation on the world stage",
                "GINI coefficient":
                    "a measure of income inequality between countries using a "
                    "100-point scale, in which 1 represents complete equality "
                    "and 100 represents the highest possible inequality",
                "global inequality":
                    "the concentration of resources in core nations and in "
                    "the hands of a wealthy minority",
                "global stratification":
                    "the unequal distribution of resources between countries",
                "gross national income (GNI) per capita":
                    "the income of a nation calculated based on goods and "
                    "services produced, plus income earned by citizens and "
                    "corporations headquartered in that country",
                "peripheral nations":
                    "nations on the fringes of the global economy, dominated "
                    "by core nations, with very little industrialization",
                "second world":
                    "a term from the Cold War era that describes nations with "
                    "moderate economies and standards of living",
                "semi-peripheral nations":
                    "in-between nations, not powerful enough to dictate "
                    "policy but acting as a major source of raw materials and "
                    "an expanding middle class marketplace",
                "third world":
                    "a term from the Cold War era that refers to poor, "
                    "unindustrialized countries", },
            "10.2": {
                "absolute poverty":
                    "the state where one is barely able, or unable, to afford "
                    "basic necessities",
                "chattel slavery":
                    "a form of slavery in which one person owns another",
                "debt bondage":
                    "the act of people pledging themselves as servants in "
                    "exchange for money for passage, and are subsequently "
                    "paid too little to regain their freedom",
                "global feminization of poverty":
                    "a pattern that occurs when women bear a disproportionate "
                    "percentage of the burden of poverty",
                "relative poverty":
                    "the state of poverty where one is unable to live the "
                    "lifestyle of the average person in the country",
                "subjective poverty":
                    "a state of poverty composed of many dimensions, "
                    "subjectively present when one’s actual income does not "
                    "meet one’s expectations",
                "underground economy":
                    "an unregulated economy of labor and goods that operates "
                    "outside of governance, regulatory systems, or human "
                    "protections", },
            "10.3": {
                "dependency theory":
                    "a theory which states that global inequity is due to the "
                    "exploitation of peripheral and semi-peripheral nations "
                    "by core nations",
                "modernization theory":
                    "a theory that low-income countries can improve their "
                    "global economic standing by industrialization of "
                    "infrastructure and a shift in cultural attitudes towards "
                    "work", },
            "11": {
                "racial profiling":
                    "the use by law enforcement of race alone to determine "
                    "whether to stop and detain someone", },
            "11.1": {
                "dominant group":
                    "a group of people who have more power in a society than "
                    "any of the subordinate groups",
                "ethnicity":
                    "shared culture, which may include heritage, language, "
                    "religion, and more",
                "minority group":
                    "any group of people who are singled out from the others "
                    "for differential and unequal treatment",
                "scapegoat theory":
                    "a theory that suggests that the dominant group will "
                    "displace its unfocused aggression onto a subordinate "
                    "group",
                "social construction of race":
                    "the school of thought that race is not biologically "
                    "identifiable",
                "subordinate group":
                    "a group of people who have less power than the dominant "
                    "group", },
            "11.2": {
                "colorism":
                    "the belief that one type of skin tone is superior or "
                    "inferior to another within a racial group",
                "de facto segregation":
                    "a situation in which legislation did not overtly "
                    "segregate people by race, but nevertheless segregation "
                    "continued",
                "discrimination":
                    "prejudiced action against a group of people",
                "institutional racism":
                    "racism embedded in social institutions",
                "prejudice":
                    "biased thought based on flawed assumptions about a group "
                    "of people",
                "racial steering":
                    "the act of real estate agents directing prospective "
                    "homeowners toward or away from certain neighborhoods "
                    "based on their race",
                "racism":
                    "a set of attitudes, beliefs, and practices that are used "
                    "to justify the belief that one racial category is "
                    "somehow superior or inferior to others",
                "redlining":
                    "the practice of routinely refusing mortgages for "
                    "households and business located in predominately "
                    "minority communities",
                "sedimentation of racial inequality":
                    "the intergenerational impact of de facto and de jure "
                    "racism that limits the abilities of black people to "
                    "accumulate wealth",
                "stereotypes":
                    "oversimplified ideas about groups of people",
                "white privilege":
                    "the benefits people receive simply by being part of the "
                    "dominant group", },
            "11.3": {
                "culture of prejudice":
                    "the theory that prejudice is embedded in our culture",
                "intersection theory":
                    "theory that suggests we cannot separate the effects of "
                    "race, class, gender, sexual orientation, and other "
                    "attributes", },
            "11.4": {
                "amalgamation":
                    "the process by which a minority group and a majority "
                    "group combine to form a new group",
                "assimilation":
                    "the process by which a minority individual or group "
                    "takes on the characteristics of the dominant culture",
                "expulsion":
                    "the act of a dominant group forcing a subordinate group "
                    "to leave a certain area or even the country",
                "genocide":
                    "the deliberate annihilation of a targeted (usually "
                    "subordinate) group",
                "pluralism":
                    "the ideal of the United States as a “salad bowl:” a "
                    "mixture of different cultures where each culture retains "
                    "its own identity and yet adds to the “flavor” of the "
                    "whole",
                "segregation":
                    "the physical separation of two groups, particularly in "
                    "residence, but also in workplace and social functions", },
            "11.5": {
                "model minority":
                    "the stereotype applied to a minority group that is seen "
                    "as reaching higher educational, professional, and "
                    "socioeconomic levels without protest against the "
                    "majority establishment", },
            "12.1": {
                "DOMA":
                    "Defense of Marriage Act, a 1996 U.S. law explicitly "
                    "limiting the definition of “marriage” to a union between "
                    "one man and one woman and allowing each individual state "
                    "to recognize or deny same-sex marriages performed in "
                    "other states",
                "gender":
                    "a term that refers to social or cultural distinctions of "
                    "behaviors that are considered male or female",
                "Gender Dysphoria":
                    "a condition listed in the DSM-5 in which people whose "
                    "gender at birth is contrary to the one they identify "
                    "with. This condition replaces \"gender identity "
                    "disorder\"",
                "gender identity":
                    "a person’s deeply held internal perception of his or her "
                    "gender",
                "gender role":
                    "society’s concept of how men and women should behave",
                "heterosexism":
                    "an ideology and a set of institutional practices that "
                    "privilege heterosexuals and heterosexuality over other "
                    "sexual orientations",
                "heterosexual":
                    "an extreme or irrational aversion to homosexuals",
                "sex":
                    "a term that denotes the presence of physical or "
                    "physiological differences between males and females",
                "sexual orientation":
                    "a person’s physical, mental, emotional, and sexual "
                    "attraction to a particular sex (male or female)",
                "transgender":
                    "an adjective that describes individuals who identify "
                    "with the behaviors and characteristics that are other "
                    "than their biological sex",
                "transsexuals":
                    "transgender individuals who attempt to alter their "
                    "bodies through medical interventions such as surgery and "
                    "hormonal therapy", },
            "12.2": {
                "biological determinism":
                    "the belief that men and women behave differently due to "
                    "inherent sex differences related to their biology",
                "doing gender":
                    "the performance of tasks based upon the gender assigned "
                    "to us by society and, in turn, ourselves",
                "sexism":
                    "the prejudiced belief that one sex should be valued over "
                    "another",
                "social construction of sexuality":
                    "socially created definitions about the cultural "
                    "appropriateness of sex-linked behavior which shape how "
                    "people see and experience sexuality", },
            "12.3": {
                "queer theory":
                    "an interdisciplinary approach to sexuality studies that "
                    "identifies Western society’s rigid splitting of gender "
                    "into male and female roles and questions its "
                    "appropriateness",
                "sexuality":
                    "a person’s capacity for sexual feelings",
                "double standard":
                    "the concept that prohibits premarital sexual intercourse "
                    "for women but allows it for men", },
            "13": {
                "centenarians":
                    "people 100 years old or older",
                "supercentenarians":
                    "people 110 of age or older", },
            "13.1": {
                "baby boomers":
                    "people in the United States born between approximately "
                    "1946 and 1964",
                "cohort":
                    "a group of people who share a statistical or demographic "
                    "trait",
                "dependency ratio":
                    "the number of nonproductive citizens (young, disabled, "
                    "elderly) to productive working citizens",
                "filial piety":
                    "deference and respect to one’s parents and ancestors in "
                    "all things",
                "gerontology":
                    "a field of science that seeks to understand the process "
                    "of aging and the challenges encountered as seniors grow "
                    "older",
                "life expectancy":
                    "the number of years a newborn is expected to live",
                "social gerontology":
                    "a specialized field of gerontology that examines the "
                    "social (and sociological) aspects of aging", },
            "13.2": {
                "geriatrics":
                    "a medical specialty focusing on the elderly",
                "grief":
                    "a psychological, emotional, and social response to the "
                    "feelings of loss that accompanies death or a similar "
                    "event",
                "hospice":
                    "healthcare that treats terminally ill people by "
                    "providing comfort during the dying process",
                "life course":
                    "the period from birth to death, including a sequence of "
                    "predictable life events",
                "physician-assisted suicide":
                    "the voluntary use of lethal medication provided by a "
                    "medical doctor to end one’s life",
                "primary aging":
                    "biological factors such as molecular and cellular "
                    "changes",
                "secondary aging":
                    "aging that occurs due to controllable factors like "
                    "exercise and diet",
                "thanatology":
                    "the systematic study of death and dying", },
            "13.3": {
                "ageism":
                    "discrimination based on age",
                "elder abuse":
                    "the act of a caretaker intentionally depriving an older "
                    "person of care or harming the person in their charge",
                "gerontocracy":
                    "a type of social structure wherein the power is held by "
                    "a society’s oldest members",
                "senescence":
                    "the aging process, including biological, intellectual, "
                    "emotional, social, and spiritual changes", },
            "13.4": {
                "activity theory":
                    "a theory which suggests that for individuals to enjoy "
                    "old age and feel satisfied, they must maintain "
                    "activities and find a replacement for the statuses and "
                    "associated roles they have left behind as they aged",
                "age stratification theory":
                    "a theory which states that members of society are "
                    "stratified by age, just as they are stratified by race, "
                    "class, and gender",
                "continuity theory":
                    "a theory which states that the elderly make specific "
                    "choices to maintain consistency in internal (personality "
                    "structure, beliefs) and external structures "
                    "(relationships), remaining active and involved "
                    "throughout their elder years",
                "disengagement theory":
                    "a theory which suggests that withdrawing from society "
                    "and social relationships is a natural part of growing "
                    "old",
                "exchange theory":
                    "a theory which suggests that we experience an increased "
                    "dependence as we age and must increasingly submit to the "
                    "will of others, because we have fewer ways of compelling "
                    "others to submit to us",
                "gerotranscendence":
                    "the idea that as people age, they transcend limited "
                    "views of life they held in earlier times",
                "modernization theory":
                    "a theory which suggests that the primary cause of the "
                    "elderly losing power and influence in society are the "
                    "parallel forces of industrialization and modernization",
                "selective optimization with compensation theory":
                    "a theory based on the idea that successful personal "
                    "development throughout the life course and subsequent "
                    "mastery of the challenges associated with everyday life "
                    "are based on the components of selection, optimization, "
                    "and compensation",
                "subculture of aging theory":
                    "a theory that focuses on the shared community created by "
                    "the elderly when they are excluded (due to age), "
                    "voluntarily or involuntarily, from participating in "
                    "other groups", },
            "14.1": {
                "ambilineal":
                    "a type of unilateral descent that follows either the "
                    "father’s or the mother’s side exclusively",
                "bigamy":
                    "the act of entering into marriage while still married to "
                    "another person",
                "bilateral descent":
                    "the tracing of kinship through both parents’ ancestral "
                    "lines",
                "cohabitation":
                    "the act of a couple sharing a residence while they are "
                    "not married",
                "family":
                    "socially recognized groups of individuals who may be "
                    "joined by blood, marriage, or adoption and who form an "
                    "emotional connection and an economic unit of society",
                "family life course":
                    "a sociological model of family that sees the progression "
                    "of events as fluid rather than as occurring in strict "
                    "stages",
                "family life cycle":
                    "a set of predictable steps and patterns families "
                    "experience over time",
                "family of orientation":
                    "the family into which one is born",
                "family of procreation":
                    "a family that is formed through marriage",
                "kinship":
                    "a person’s traceable ancestry (by blood, marriage, "
                    "and/or adoption)",
                "marriage":
                    "a legally recognized contract between two or more people "
                    "in a sexual relationship who have an expectation of "
                    "permanence about their relationship",
                "matrilineal":
                    "a type of unilateral descent that follows the mother’s "
                    "side only",
                "matrilocal residence":
                    "a system in which it is customary for a husband to live "
                    "with the his wife’s family",
                "monogamy":
                    "the act of being married to only one person at a time",
                "patrilineal":
                    "a type of unilateral descent that follows the father’s "
                    "line only",
                "patrilocal residence":
                    "a system in which it is customary for the a wife to live "
                    "with (or near) the her husband’s family",
                "polyandry":
                    "a form of marriage in which one woman is married to more "
                    "than one man at one time",
                "polygamy":
                    "the state of being committed or married to more than one "
                    "person at a time",
                "polygyny":
                    "a form of marriage in which one man is married to more "
                    "than one woman at one time",
                "unilateral descent":
                    "the tracing of kinship through one parent only", },
            "14.2": {
                "extended family":
                    "a household that includes at least one parent and child "
                    "as well as other relatives like grandparents, aunts, "
                    "uncles, and cousins",
                "nuclear family":
                    "two parents (traditionally a married husband and wife) "
                    "and children living in the same household", },
            "14.3": {
                "intimate partner violence":
                    "violence that occurs between individuals who maintain a "
                    "romantic or sexual relationship",
                "shaken-baby syndrome":
                    "a group of medical symptoms such as brain swelling and "
                    "retinal hemorrhage resulting from forcefully shaking or "
                    "impacting an infant’s head", },
            "15": {
                "religion":
                    "a system of beliefs, values, and practices concerning "
                    "what a person holds to be sacred or spiritually "
                    "significant", },
            "15.1": {
                "religious beliefs":
                    "specific ideas that members of a particular faith hold "
                    "to be true",
                "religious experience":
                    "the conviction or sensation that one is connected to "
                    "“the divine”",
                "religious rituals":
                    "behaviors or practices that are either required for or "
                    "expected of the members of a particular group", },
            "15.2": {
                "animism":
                    "the religion that believes in the divinity of nonhuman "
                    "beings, like animals, plants, and objects of the natural "
                    "world",
                "atheism":
                    "the belief in no deities",
                "atheists":
                    "those who do not believe in a divine being or entity",
                "cults":
                    "religious groups that are small, secretive, and highly "
                    "controlling of members and have a charismatic leader",
                "denomination":
                    "a large, mainstream religion that is not sponsored by "
                    "the state",
                "ecclesia":
                    "a religion that is considered the state religion",
                "established sects":
                    "sects that last but do not become denominations",
                "monotheism":
                    "a religion based on belief in a single deity",
                "polytheism":
                    "a religion based on belief in multiple deities",
                "polytheistic":
                    "relating to or characterized by belief in or worship of "
                    "more than one god",
                "sect":
                    "a small, new offshoot of a denomination",
                "totemism":
                    "the belief in a divine connection between humans and "
                    "other natural beings", },
            "15.3": {
                "liberation theology":
                    "the use of a church to promote social change via the "
                    "political arena",
                "megachurch":
                    "a Christian church that has a very large congregation "
                    "averaging more than 2,000 people who attend regular "
                    "weekly services", },
            "16.1": {
                "cultural transmission":
                    "the way people come to learn the values, beliefs, and "
                    "social norms of their culture",
                "education":
                    "a social institution through which a society’s children "
                    "are taught basic academic knowledge, learning skills, "
                    "and cultural norms",
                "formal education":
                    "the learning of academic facts and concepts",
                "informal education":
                    "education that involves learning about cultural values, "
                    "norms, and expected behaviors through participation in a "
                    "society",
                "universal access":
                    "the equal ability of all people to participate in an "
                    "education system", },
            "16.2": {
                "credentialism":
                    "the emphasis on certificates or degrees to show that a "
                    "person has a certain skill, has attained a certain level "
                    "of education, or has met certain job qualifications",
                "cultural capital":
                    "cultural knowledge that serves (metaphorically) as "
                    "currency to help one navigate a culture",
                "grade inflation":
                    "the idea that the achievement level associated with an A "
                    "today is notably lower than the achievement level "
                    "associated with A-level work a few decades ago",
                "hidden curriculum":
                    "the type of nonacademic knowledge that people learn "
                    "through informal learning and cultural transmission",
                "social placement":
                    "the use of education to improve one’s social standing",
                "sorting":
                    "classifying students based on academic merit or "
                    "potential",
                "tracking":
                    "a formalized sorting system that places students on "
                    "“tracks” (advanced, low achievers) that perpetuate "
                    "inequalities", },
            "16.3": {
                "Head Start program":
                    "a federal program that provides academically focused "
                    "preschool to students of low socioeconomic status",
                "No Child Left Behind Act":
                    "an act that requires states to test students in "
                    "prescribed grades, with the results of those tests "
                    "determining eligibility to receive federal funding", },
            "17.1": {
                "authority":
                    "power that people accept because it comes from a source "
                    "that is perceived as legitimate",
                "charismatic authority":
                    "power legitimized on the basis of a leader’s exceptional "
                    "personal qualities",
                "patrimonialism":
                    "a type of authority wherein military and administrative "
                    "factions enforce the power of the master",
                "power":
                    "the ability to exercise one’s will over others",
                "rational-legal authority":
                    "power that is legitimized by rules, regulations, and "
                    "laws",
                "traditional authority":
                    "power legitimized on the basis of long-standing "
                    "customs", },
            "17.2": {
                "absolute monarchies":
                    "governments wherein a monarch has absolute or "
                    "unmitigated power",
                "anarchy":
                    "the absence of any organized government",
                "constitutional monarchies":
                    "national governments that recognize monarchs but require "
                    "these figures to abide by the laws of a greater "
                    "constitution",
                "democracy":
                    "a form of government that provides all citizens with an "
                    "equal voice or vote in determining state policy",
                "dictatorship":
                    "a form of government in which a single person (or a "
                    "very small group) wields complete and absolute authority "
                    "over a government or populace after the dictator rises "
                    "to power, usually through economic or military might",
                "monarchy":
                    "a form of government in which a single person (a "
                    "monarch) rules until that individual dies or abdicates "
                    "the throne",
                "oligarchy":
                    "a form of government in which power is held by a small, "
                    "elite group",
                "representative democracy":
                    "a government wherein citizens elect officials to "
                    "represent their interests",
                "totalitarian dictatorship":
                    "an extremely oppressive form of dictatorship in which "
                    "most aspects of citizens’ lives are controlled by the "
                    "leader", },
            "17.3": {
                "one person, one vote":
                    "a concept holding that each person’s vote should be "
                    "counted equally",
                "politics":
                    "a means of studying a nation’s or group’s underlying "
                    "social norms as values as evidenced through its "
                    "political structure and practices", },
            "17.4": {
                "power elite":
                    "a small group of powerful people who control much of a "
                    "society", },
            "18": {
                "economy":
                    "the social institution through which a society’s "
                    "resources (goods and services) are managed",
                "mechanical solidarity":
                    "a form of social cohesion that comes from sharing "
                    "similar work, education, and religion, as might be found "
                    "in simpler societies",
                "organic solidarity":
                    "a form of social cohesion that arises out of the mutual "
                    "interdependence created by the specialization of work", },
            "18.1": {
                "bartering":
                    "a process where people exchange one form of goods or "
                    "services for another",
                "capitalism":
                    "an economic system in which there is private ownership "
                    "(as opposed to state ownership) and where there is an "
                    "impetus to produce profit, and thereby wealth",
                "career inheritance":
                    "a practice where children tend to enter the same or "
                    "similar occupation as their parents",
                "convergence theory":
                    "a sociological theory to explain how and why societies "
                    "move toward similarity over time as their economies "
                    "develop",
                "depression":
                    "a sustained recession across several economic sectors",
                "market socialism":
                    "a subtype of socialism that adopts certain traits of "
                    "capitalism, like allowing limited private ownership or "
                    "consulting market demand",
                "mercantilism":
                    "an economic policy based on national policies of "
                    "accumulating silver and gold by controlling markets with "
                    "colonies and other countries through taxes and customs "
                    "charges",
                "money":
                    "an object that a society agrees to assign a value to so "
                    "it can be exchanged as payment",
                "mutualism":
                    "a form of socialism under which individuals and "
                    "cooperative groups exchange products with one another on "
                    "the basis of mutually satisfactory contracts",
                "recession":
                    "two or more consecutive quarters of economic decline",
                "socialism":
                    "an economic system in which there is government "
                    "ownership (often referred to as “state run”) of goods "
                    "and their production, with an impetus to share work and "
                    "wealth equally among the members of a society",
                "subsistence farming":
                    "farming where farmers grow only enough to feed "
                    "themselves and their families", },
            "18.2": {
                "global assembly lines":
                    "a practice where products are assembled over the course "
                    "of several international transactions",
                "global commodity chains":
                    "internationally integrated economic links that connect "
                    "workers and corporations for the purpose of manufacture "
                    "and marketing",
                "globalization":
                    "the process of integrating governments, cultures, and "
                    "financial markets through international trade into a "
                    "single world market",
                "xenophobia":
                    "an illogical fear and even hatred of foreigners and "
                    "foreign goods", },
            "18.3": {
                "automation":
                    "workers being replaced by technology",
                "outsourcing":
                    "a practice where jobs are contracted to an outside "
                    "source, often in another country",
                "polarization":
                    "a practice where the differences between low-end and "
                    "high-end jobs become greater and the number of people in "
                    "the middle levels decreases",
                "structural unemployment":
                    "a societal level of disjuncture between people seeking "
                    "jobs and the jobs that are available",
                "underemployment":
                    "a state in which a person accepts a lower paying, lower "
                    "status job than his or her education and experience "
                    "qualifies him or her to perform", },
            "19.1": {
                "contested illnesses":
                    "illnesses that are questioned or considered questionable "
                    "by some medical professionals",
                "medical sociology":
                    "the systematic study of how humans manage issues of "
                    "health and illness, disease and disorders, and "
                    "healthcare for both the sick and the healthy",
                "stigmatization of illness":
                    "illnesses that are discriminated against and whose "
                    "sufferers are looked down upon or even shunned by "
                    "society", },
            "19.2": {
                "social epidemiology":
                    "the study of the causes and distribution of diseases", },
            "19.3": {
                "anxiety disorders":
                    "feelings of worry and fearfulness that last for months "
                    "at a time",
                "disability":
                    "a reduction in one’s ability to perform everyday tasks; "
                    "the World Health Organization notes that this is a "
                    "social limitation",
                "impairment":
                    "the physical limitations a less-able person faces",
                "medicalization":
                    "the process by which aspects of life that were "
                    "considered bad or deviant are redefined as sickness and "
                    "needing medical attention to remedy",
                "mood disorders":
                    "long-term, debilitating illnesses like depression and "
                    "bipolar disorder",
                "morbidity":
                    "the incidence of disease",
                "mortality":
                    "the number of deaths in a given time or place",
                "personality disorders":
                    "disorders that cause people to behave in ways that are "
                    "seen as abnormal to society but seem normal to them",
                "stereotype interchangeability":
                    "stereotypes that don’t change and that get recycled for "
                    "application to a new subordinate group",
                "stigmatization":
                    "the act of spoiling someone's identity; they are labeled "
                    "as different, discriminated against, and sometimes even "
                    "shunned due to an illness or disability", },
            "19.4": {
                "epidemiology":
                    "the study of the incidence, distribution, and possible "
                    "control of diseases",
                "individual mandate":
                    "a government rule that requires everyone to have "
                    "insurance coverage or they will have to pay a penalty",
                "private healthcare":
                    "health insurance that a person buys from a private "
                    "company; private healthcare can either be employer-"
                    "sponsored or direct-purchase",
                "public healthcare":
                    "health insurance that is funded or provided by the "
                    "government",
                "socialized medicine":
                    "when the government owns and runs the entire healthcare "
                    "system",
                "underinsured":
                    "people who spend at least 10 percent of their income on "
                    "healthcare costs that are not covered by insurance",
                "universal healthcare":
                    "a system that guarantees healthcare coverage for "
                    "everyone", },
            "19.5": {
                "commodification":
                    "the changing of something not generally thought of as a "
                    "commodity into something that can be bought and sold in "
                    "a marketplace",
                "demedicalization":
                    "the social process that normalizes “sick” behavior",
                "legitimation":
                    "the act of a physician certifying that an illness is "
                    "genuine",
                "medicalization of deviance":
                    "the process that changes “bad” behavior into “sick” "
                    "behavior",
                "sick role":
                    "the pattern of expectations that define appropriate "
                    "behavior for the sick and for those who take care of "
                    "them", },
            "20": {
                "fracking":
                    "hydraulic fracturing, a method used to recover gas and "
                    "oil from shale by drilling down into the earth and "
                    "directing a high-pressure mixture of water, sand, and "
                    "proprietary chemicals into the rock", },
            "20.1": {
                "carrying capacity":
                    "the amount of people that can live in a given area "
                    "considering the amount of available resources",
                "cornucopian theory":
                    "a theory that asserts human ingenuity will rise to the "
                    "challenge of providing adequate resources for a growing "
                    "population",
                "demographic transition theory":
                    "a theory that describes four stages of population "
                    "growth, following patterns that connect birth and death "
                    "rates with stages of industrial development",
                "demography":
                    "the study of population",
                "fertility rate":
                    "a measure noting the actual number of children born",
                "Malthusian theory":
                    "a theory asserting that population is controlled through "
                    "positive checks (war, famine, disease) and preventive "
                    "checks (measures to reduce fertility)",
                "mortality rate":
                    "a measure of the number of people in a population who "
                    "die",
                "population composition":
                    "a snapshot of the demographic profile of a population "
                    "based on fertility, mortality, and migration rates",
                "population pyramid":
                    "a graphic representation that depicts population "
                    "distribution according to age and sex",
                "sex ratio":
                    "the ratio of men to women in a given population",
                "zero population growth":
                    "a theoretical goal in which the number of people "
                    "entering a population through birth or immigration is "
                    "equal to the number of people leaving it via death or "
                    "emigration", },
            "20.2": {
                "asylum-seekers":
                    "those whose claim to refugee status have not been "
                    "validated",
                "concentric zone model":
                    "a model of human ecology that views cities as a series "
                    "of circular rings or zones",
                "exurbs":
                    "communities that arise farther out than the suburbs and "
                    "are typically populated by residents of high "
                    "socioeconomic status",
                "gentrification":
                    "the entry of upper- and middle-class residents to city "
                    "areas or communities that have been historically less "
                    "affluent",
                "human ecology":
                    "a functional perspective that looks at the relationship "
                    "between people and their built and natural environment",
                "internally displaced person":
                    "someone who fled his or her home while remaining inside "
                    "the country’s borders",
                "megalopolis":
                    "a large urban corridor that encompasses several cities "
                    "and their surrounding suburbs and exurbs",
                "metropolis":
                    "the area that includes a city and its suburbs and exurbs",
                "NIMBY":
                    "“Not In My Back Yard,” the tendency of people to protest "
                    "poor environmental practices when those practices will "
                    "affect them directly",
                "refugee":
                    "an individual who has been forced to leave their country "
                    "in order to escape war, persecution, or natural disaster",
                "suburbs":
                    "the communities surrounding cities, typically close "
                    "enough for a daily commute",
                "sustainable development":
                    "development that occurs without depleting or damaging "
                    "the natural environment",
                "urban sociology":
                    "the subfield of sociology that focuses on the study of "
                    "urbanization",
                "urbanization":
                    "the study of the social, political, and economic "
                    "relationships of cities",
                "white flight":
                    "the migration of economically secure white people from "
                    "racially mixed urban areas toward the suburbs", },
            "20.3": {
                "cancer cluster":
                    "a geographic area with high levels of cancer within its "
                    "population",
                "climate change":
                    "long-term shifts in temperature and climate due to human "
                    "activity",
                "e-waste":
                    "the disposal of broken, obsolete, and worn-out "
                    "electronics",
                "environmental racism":
                    "the burdening of economically and socially disadvantaged "
                    "communities with a disproportionate share of "
                    "environmental hazards",
                "environmental sociology":
                    "the sociological subfield that addresses the "
                    "relationship between humans and the environment",
                "pollution":
                    "the introduction of contaminants into an environment at "
                    "levels that are damaging", },
            "21.1": {
                "acting crowds":
                    "crowds of people who are focused on a specific action or "
                    "goal",
                "assembling perspective":
                    "a theory that credits individuals in crowds as behaving "
                    "as rational thinkers and views crowds as engaging in "
                    "purposeful behavior and collective action",
                "casual crowds":
                    "people who share close proximity without really "
                    "interacting",
                "collective behavior":
                    "a noninstitutionalized activity in which several people "
                    "voluntarily engage",
                "conventional crowds":
                    "people who come together for a regularly scheduled event",
                "crowd":
                    "a fairly large number of people who share close "
                    "proximity",
                "emergent norm theory":
                    "a perspective that emphasizes the importance of social "
                    "norms in crowd behavior",
                "expressive crowds":
                    "crowds who share opportunities to express emotions",
                "flash mobs":
                    "a large group of people who gather together in a "
                    "spontaneous activity that lasts a limited amount of time",
                "mass":
                    "a relatively large group with a common interest, even if "
                    "they may not be in close proximity",
                "public":
                    "an unorganized, relatively diffuse group of people who "
                    "share ideas",
                "value-added theory":
                    "a functionalist perspective theory that posits that "
                    "several preconditions must be in place for collective "
                    "behavior to occur", },
            "21.2": {
                "alternative movements":
                    "social movements that limit themselves to self-"
                    "improvement changes in individuals",
                "diagnostic framing":
                    "a the social problem that is stated in a clear, easily "
                    "understood manner", }
        }
