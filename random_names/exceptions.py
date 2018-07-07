

class NameSetError(Exception):
    """Base exception for name sets."""


class MissingIdError(NameSetError):
    """A mandatory field is missing."""


class InvalidTemplateError(NameSetError):
    """A template is missing a field or has invalid content."""


class InvalidNameListError(NameSetError):
    """A name list is missing a field or has invalid content."""


class NameListMissingError(NameSetError):
    """A name has no list."""


# TODO: change this to type error...
class InvalidValueError(NameSetError):
    """"""

    def __init__(self, field_name, encountered_type='', expected_type='', value=''):
        self.field_name = field_name
        self.encountered_type = encountered_type
        self.expected_type = expected_type
        self.value = value


class UnexpectedFieldError(NameSetError):
    """The parser has encountered a field, which does nothing."""
