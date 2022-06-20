import unicodedata

import icu
import regex


# FIXME: Determine if we hould prefer Punct vs Mark
# UNICODE_MARK_CATEGORY_REGEX = regex.compile(r"\p{Punct}")
UNICODE_MARK_CATEGORY_REGEX = regex.compile(r"\p{M}")
DIGITS_REGEX = regex.compile(r"\d")


def nfkc(s):
    return unicodedata.normalize("NFKC", s)


def nfd(s):
    return unicodedata.normalize("NFD", s)


def strip_marks(s):
    """
    https://unicode.org/reports/tr18/#General_Category_Property
    """
    cps = nfd(s)
    return nfkc(UNICODE_MARK_CATEGORY_REGEX.sub("", cps))


def normalize_and_strip_marks(s):
    """
    Strip marks and return the case-folded representation of string
    """
    return strip_marks(s).lower()


# FIXME: Deprecate this in favor of normalize_and_strip_marks
def normalize_string(s):
    return normalize_and_strip_marks(s)


# FIXME: Get a code review on this as our
# normalization pattern
def normalize_value(value):
    return nfkc(nfd(value)).lower()


def normalized_no_digits(value):
    return DIGITS_REGEX.sub("", normalize_value(value))


# FIXME: Wrap as a lazy instantiation
# or allow multiple flags for ICU IDs
icu_transliterator = icu.Transliterator.createInstance("Any-Latin")
