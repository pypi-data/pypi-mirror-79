"""
Exception types raised by PugSQL. PugSQL will also raise built-in exceptions
when they're appropriate.
"""

__pdoc__ = {}


class ParserError(ValueError):
    """
    Exception raised when syntax errors are encountered parsing PugSQL files.
    """
    token = None

    def __init__(self, message, token):
        """
        Creates a new ParserError given a message and the token indicating the
        position of the error. Builds a user-facing error message indicating
        the file, line, and column of the error.
        """
        super(ParserError, self).__init__(
            'Error in %s:%s:%s - %s' % (
                token.context.sqlfile,
                token.context.line,
                token.context.col,
                message))
        self.token = token


__pdoc__['ParserError.token'] = (
    'The `pugsql.lexer.Token` indicating the position of the error '
    'encountered during parsing.')


class NoConnectionError(RuntimeError):
    """
    Exception raised when a PugSQL module is not connected to a database.
    """
    def __init__(self):
        super(NoConnectionError, self).__init__(
            'No connection engine is configured. Pass a connection string '
            "to the module's connect method, or pass a SQLAlchemy engine "
            'to the set_engine method.')


class InvalidArgumentError(AttributeError):
    """
    Exception raised when a PugSQL statement is called with incorrect
    arguments.
    """
