

class NameSetError(Exception):
    """Base exception for name sets."""


class UnknownNameSet(NameSetError):
    """The given name set could not be found."""


class UnknownNameList(NameSetError):
    """The given name list could no be found."""


class UnknownTemplate(NameSetError):
    """The given template could not be found."""


class NoIdError(NameSetError):
    """The name set has no ID."""

