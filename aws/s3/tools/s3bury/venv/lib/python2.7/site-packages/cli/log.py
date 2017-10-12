"""\
:mod:`cli.log` -- logging applications
--------------------------------------

Logging applications use the standard library :mod:`logging` module to
handle log messages.
"""

__license__ = """Copyright (c) 2008-2010 Will Maier <will@m.aier.us>

Permission to use, copy, modify, and distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

"""

import logging
import sys

from logging import Formatter, StreamHandler

from cli.app import CommandLineApp, CommandLineMixin, Application

__all__ = ["LoggingApp", "LoggingMixin", "CommandLineLogger"]

# Silence multiprocessing errors.
logging.logMultiprocessing = 0

class FileHandler(logging.FileHandler):

    def close(self):
        """Override close().
        
        We leave the file open because the application may have
        multiple threads that still need to write to it. Python
        should GC the fd when it goes out of scope, anyway.
        """
        pass    # pragma: no cover

class NullHandler(logging.Handler):
    """A blackhole handler.

    NullHandler simply ignores all messages it receives.
    """

    def emit(self, record):
        """Ignore the record."""
        pass

class CommandLineLogger(logging.Logger):
    """Provide extra configuration smarts for loggers.

    In addition to the powers of a regular logger, a
    :class:`CommandLineLogger` can set its verbosity levels based on a
    populated :class:`argparse.Namespace`.
    """
    default_level = logging.WARN
    """An integer representing the default logging level.

    Default: :data:`logging.WARN` (only warning messages will be
    shown).
    """
    silent_level = logging.CRITICAL
    """An integer representing the silent logging level.

    Default: :data:`logging.CRITICAL` (only critical messages will
    be shown).
    """

    def setLevel(self, ns):
        """Set the logger verbosity level.

        *ns* is an object with :attr:`verbose`, :attr:`quiet` and
        :attr:`silent` attributes. :attr:`verbose` and :attr:`quiet` may
        be positive integers or zero; :attr:`silent` is ``True`` or ``False``.
        If :attr:`silent` is True, the logger's level will be set to
        :attr:`silent_level`. Otherwise, the difference between
        :attr:`quiet` and :attr:`verbose` will be multiplied by 10 so it
        fits on the standard logging scale and then added to
        :attr:`default_level`.
        """
        if not hasattr(ns, "quiet"):
            return logging.Logger.setLevel(self, ns)
        level = self.default_level + (10 * (ns.quiet - ns.verbose))

        if ns.silent:
            level = self.silent_level
        elif level <= logging.NOTSET:
            level = logging.DEBUG

        self.level = level

class LoggingMixin(object):
    """A mixin for command-line applications that knows how to log.

    The :class:`LoggingMixin` requires :class:`cli.app.CommandLineMixin`
    and allows command line configuration of the application logger. In
    addition to those supported by the standard :class:`cli.app.Application` and
    :class:`cli.app.CommandLineMixin`, arguments are:

    *stream* is an open file object to which the log messages will be
    written. By default, this is standard output (not standard error, as
    might be expected).

    *logfile* is the name of a file which will be opened by the
    :class:`logging.FileHandler`.

    *message_format* and *date_format* are passed directly to the 
    :class:`CommandLineLogger` and are interpreted as in the 
    :mod:`logging` package.

    If *root* is True, the :class:`LoggingMixin` will make itself the root
    logger. This means that, for example, code that knows nothing about
    the :class:`LoggingMixin` can inherit its verbosity level, formatters
    and handlers.
    """

    def __init__(self, stream=sys.stdout, logfile=None,
            message_format="%(asctime)s %(message)s", 
            date_format="%Y-%m-%dT%H:%M:%S", root=True, **kwargs):
        self.logfile = logfile
        self.stream = stream
        self.message_format = message_format
        self.date_format = date_format
        self.root = root

    def setup(self):
        """Configure the :class:`LoggingMixin`.

        This method adds the :option:`-l`, :option:`q`,
        :option:`-s` and :option:`-v` parameters to the
        application and instantiates the :attr:`log` attribute.
        """
        # Add logging-related options.
        self.add_param("-l", "--logfile", default=self.logfile, 
                help="log to file (default: log to stdout)")
        self.add_param("-q", "--quiet", default=0, help="decrease the verbosity",
                action="count")
        self.add_param("-s", "--silent", default=False, help="only log warnings",
                action="store_true")
        self.add_param("-v", "--verbose", default=0, help="raise the verbosity",
                action="count")

        # Create logger.
        logging.setLoggerClass(CommandLineLogger)
        self.log = logging.getLogger(self.name)
        self.formatter = Formatter(fmt=self.message_format, datefmt=self.date_format)

        self.log.level = self.log.default_level

        # If requested, make our logger the root.
        if self.root:
            logging.root = self.log
            logging.Logger.root = self.log
            logging.Logger.manager = logging.Manager(self.log)

    def pre_run(self):
        """Set the verbosity level and configure the logger.

        The application passes the :attr:`params` object
        to the :class:`CommandLineLogger`'s special
        :meth:`CommandLineLogger.setLevel` method to set the logger's
        verbosity and then initializes the logging handlers. If the
        :attr:`logfile` attribute is not ``None``, it is passed to a
        :class:`logging.FileHandler` instance and that is added to the
        handler list. Otherwise, if the :attr:`stream` attribute is
        not ``None``, it is passed to a :class:`logging.StreamHandler`
        instance and that becomes the main handler.

        """
        self.log.setLevel(self.params)

        self.log.handlers = []
        if self.params.logfile is not None:
            file_handler = FileHandler(self.params.logfile)
            file_handler.setFormatter(self.formatter) # pragma: no cover
            self.log.addHandler(file_handler)
        elif self.stream is not None:
            stream_handler = StreamHandler(self.stream)
            stream_handler.setFormatter(self.formatter)
            self.log.addHandler(stream_handler)

        # The null handler simply drops all messages.
        if not self.log.handlers:
            self.log.addHandler(NullHandler())

class LoggingApp(LoggingMixin, CommandLineMixin, Application):
    """A logging application.

    This class simply glues together the base :class:`Application`,
    :class:`LoggingMixin` and other mixins that provide necessary functionality.

    .. versionchanged:: 1.0.4
        Actual functionality moved to :class:`LoggingMixin`.
    """
    
    def __init__(self, main=None, **kwargs):
        CommandLineMixin.__init__(self, **kwargs)
        LoggingMixin.__init__(self, **kwargs)
        Application.__init__(self, main, **kwargs)

    def setup(self):
        Application.setup(self)
        CommandLineMixin.setup(self)
        LoggingMixin.setup(self)

    def pre_run(self):
        Application.pre_run(self)
        CommandLineMixin.pre_run(self)
        LoggingMixin.pre_run(self)
