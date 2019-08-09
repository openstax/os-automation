"""A term and definition selector for OpenStax Tutor Beta books."""

from __future__ import annotations

import os
from random import randint
from typing import Tuple, Union

from yaml import safe_load as load_yaml

Term = Tuple[str, str]

Biology_2e = 'biology_2e.yaml'
College_Physics = 'college_physics.yaml'
Sociology_2e = 'introduction_to_sociology_2e.yaml'


class BookIndexError(IndexError):
    """A error for when a book section index is not found."""

    pass


class OpenStaxBook(object):
    """An index of book terms for use in free response questions."""

    # Default to Biology
    BOOK = Biology_2e
    TITLE = 'Biology 2e'

    def __init__(self) -> None:
        """Initialize the term group."""
        current_dir = os.getcwd()
        slash = '/' if '/' in current_dir else '\\'
        file_path = f'{current_dir}{slash}utils{slash}{self.BOOK}'
        self._book_title = self.TITLE
        with open(file_path) as file:
            book = file.read()
            self._terms = load_yaml(book)

    @property
    def book_title(self) -> str:
        """Return the book title."""
        return self._book_title

    def get_term(self, section: Union[int, float, str]) -> Term:
        """Return a random term and definition from a specific section.

        :param section: the book section to pull a term from
        :type section: int or float or str
        :return: a book term and definition
        :rtype: tuple(str, str)

        :raises :py:class:`~utils.bookterm.BookIndexError`: if the section
            number does not exist within the book or the requested section does
            not contain any defined terms

        """
        if isinstance(section, str):
            if '.' in section:
                section = float(section)
            else:
                section = int(section)
        terms = self._terms.get(section)
        if not terms:
            raise BookIndexError('No terms found in section {0} of {1}'
                                 .format(section, self.book_title))
        keys = list(terms.keys())
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

    # Use the OpenStaxBook default for book and title


class CollegePhysics(OpenStaxBook):
    """College Physics."""

    BOOK = College_Physics
    TITLE = 'College Physics'


class IntroductionToSociology2e(OpenStaxBook):
    """Introduction to Sociology 2e."""

    BOOK = Sociology_2e
    TITLE = 'Introduction to Sociology 2e'
