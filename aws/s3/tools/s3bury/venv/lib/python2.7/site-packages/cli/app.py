"""\
:mod:`cli.app` -- basic applications
------------------------------------

The :mod:`cli.app` module establishes the basis for all of the other
applications and is a good place to start when looking to extend
:class:`Application` functionality or to understand the basic API.
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

__todo__ = """\
""".split(" * ")

import os
import sys

from cli._ext import argparse
from cli.util import ifelse, ismethodof

__all__ = ["Application", "CommandLineApp", "CommandLineMixin"]

class Error(Exception):
    pass

class Abort(Error):
    """Raised when an application exits unexpectedly.

    :class:`Abort` takes a single integer argument indicating the exit status of
    the application.

    .. versionadded:: 1.0.4
    """

    def __init__(self, status):
        self.status = status
        message = "Application terminated (%s)" % self.status
        super(Abort, self).__init__(message, self.status)

class Application(object):
    """An application.
    
    :class:`Application` constructors should always be called with
    keyword arguments, though the *main* argument may be passed
    positionally (as when :class:`Application` or its subclasses are
    instantiated as decorators). Arguments are:

    *main* is the callable object that performs the main work of the
    application. The callable must accept an :class:`Application`
    instance as its sole argument. If *main* is ``None``, it is assumed that
    a valid callable will be passed to the :meth:`__call__` method (when
    using an :class:`Application` instance as a decorator). If *main* is
    not None, the :meth:`setup` method will be called, allowing
    subclasses to customize the order in which certain setup steps are
    executed.

    *name* is the name of the application itself. If *name* is not ``None``,
    the :attr:`name` property will inspect the :attr:`main` callable and
    use its function or class name.

    *exit_after_main* determines whether the application will call
    :func:`sys.exit` after :attr:`main` completes.

    *stdin*, *stderr* and *stdout* are file objects that represent the 
    usual application input and outputs. If they are ``None``, they will
    be replaced with :data:`sys.stdin`, :data:`sys.stderr` and
    :data:`sys.stdout`, respectively.

    *version* is a string representing the application's version.

    *description* is a string describing the application. If
    *description* is ``None``, the :attr:`description` property will use
    the :attr:`main` callable's :attr:`__doc__` attribute instead.

    *argv* is a list of strings representing the options passed on the
    command line. If *argv* is ``None``, :data:`sys.argv` will be used
    instead.

    *profiler* is a :class:`cli.profiler.Profiler` instance, or ``None`` (default).
    If not ``None``, the profiler will be available to the running application.

    *reraise* is a tuple of exception classes: if an exception is
    raised by :attr:`main` and it is listed here, then it will be
    propagated upwards by :attr:`post_run`; otherwise it will just
    cause :attr:`post_run` to exit with return code 1.

    In all but a very few cases, subclasses that override the constructor
    should call :meth:`Application.__init__` at the end of the
    overridden method to ensure that the :meth:`setup` method is
    called.
    """
    main = None

    def __init__(self, main=None, name=None, exit_after_main=True, stdin=None, stdout=None,
            stderr=None, version=None, description=None, argv=None,
            profiler=None, reraise=(Exception,), **kwargs):
        self._name = name
        self.exit_after_main = exit_after_main
        self.stdin = stdin and stdin or sys.stdin
        self.stdout = stdout and stdout or sys.stdout
        self.stderr = stderr and stderr or sys.stderr
        self.version = version
        self.argv = argv
        if argv is None:
            self.argv = sys.argv
        self._description = description

        self.profiler = profiler
        self.reraise = reraise
        
        if main is not None:
            self.main = main

        if getattr(self, "main", None) is not None:
            self.setup()

    def __call__(self, main):
        """Wrap the *main* callable and return an :class:`Application` instance.
    
        This method is useful when it is necessary to pass keyword
        arguments to the :class:`Application` constructor when
        decorating callables. For example::
    
            @cli.Application(stderr=None)
            def foo(app):
                pass
    
        In this case, :meth:`setup` will occur during :meth:`__call__`,
        not when the :class:`Application` is first constructed.
        """
        self.main = main

        self.setup()

        return self

    def setup(self):
        """Configure the :class:`Application`.

        This method is provided so that subclasses can easily customize
        the configuration process without having to reimplement the base
        constructor. :meth:`setup` is called once, either by the base
        constructor or :meth:`__call__`.
        """
        pass

    @property
    def name(self):
        """A string identifying the application.

        Unless specified when the :class:`Application` was created, this
        property will examine the :attr:`main` callable and use its
        name (:attr:`__name__` or :attr:`func_name` for classes or
        functions, respectively).
        """
        name = self._name
        if name is None:
            name = getattr(self.main, 'func_name', self.main.__name__)
        return name

    @property
    def description(self):
        """A string describing the application.

        Unless specified when the :class:`Application` was created, this
        property will examine the :attr:`main` callable and use its
        docstring (:attr:`__doc__` attribute).
        """
        if self._description is not None:
            return self._description
        else:
            return getattr(self.main, "__doc__", "")

    def pre_run(self):
        """Perform any last-minute configuration.

        The :meth:`pre_run` method is called by the :meth:`run` method
        before :attr:`main` is executed. This is a good time to do
        things like read a configuration file or parse command line
        arguments. The base implementation does nothing.
        """
        pass

    def post_run(self, returned):
        """Clean up after the application.

        After :attr:`main` has been called, :meth:`run` passes the return value
        (or :class:`Exception` instance raised) to this method. By default,
        :meth:`post_run` decides whether to call :func:`sys.exit` (based on the
        value of the :attr:`exit_after_main` attribute) or pass the value back
        to :meth:`run`. Subclasses should probably preserve this behavior.
        """
        # Interpret the returned value in the same way sys.exit() does.
        if returned is None:
            returned = 0
        elif isinstance(returned, Abort):
            returned = returned.status
        elif isinstance(returned, self.reraise):
            # raising the last exception preserves traceback
            raise
        else:
            try:
                returned = int(returned)
            except:
                returned = 1
            
        if self.exit_after_main:
            sys.exit(returned)
        else:
            return returned

    def run(self):
        """Run the application, returning its return value.

        This method first calls :meth:`pre_run` and then calls :attr:`main`,
        passing it an instance of the :class:`Application` itself as its only
        argument. The return value (or :class:`Exception` instance raised) is
        then passed to :meth:`post_run` which may modify it (or terminate the
        application entirely).
        """
        self.pre_run()

        args = (self,)
        if ismethodof(self.main, self):
            args = ()
        try:
            returned = self.main(*args)
        except Exception, e:
            returned = e

        return self.post_run(returned)

class ArgumentParser(argparse.ArgumentParser):
    """This subclass makes it easier to test ArgumentParser.

    Unwrapped, :class:`argparse.ArgumentParser` checks the sys module for
    stdout, stderr and argv at several points. This wrapper class moves all of
    these checks into instantiation (except for :attr:`prog`, which is a
    property).

    .. versionchanged:: 1.1.1
        The *stdout* and *stderr* options replace *file* (which was present until 1.1.1);
        *argv* is added.
    """

    def __init__(self, stdout=None, stderr=None, argv=None, **kwargs):
        self.stdout = ifelse(stdout, stdout is not None, sys.stdout)
        self.stderr = ifelse(stderr, stderr is not None, sys.stderr)
        self.argv = ifelse(argv, argv is not None, sys.argv)
        self._prog = kwargs.get("prog", None)
        super(ArgumentParser, self).__init__(**kwargs)

    def get_prog(self):

        prog = self._prog
        if prog is None:
            prog = os.path.basename(self.argv[0])
        return prog

    def set_prog(self, value):
        self._prog = value

    prog = property(get_prog, set_prog, doc= """\
        Return or lookup the program's name.

        If :attr:`_prog` is None, returns the first element in the :attr:`argv`
        list.
        """)
    del(get_prog, set_prog)

    def parse_known_args(self, args=None, namespace=None):
        """If *args* is None, use :attr:`argv`, not :data:`sys.argv`."""
        if args is None:
            args = self.argv[1:]
        return super(ArgumentParser, self).parse_known_args(args, namespace)

    def _print_message(self, message, file=None):
        """If *file* is None, use :attr:`stdout` instead of :data:`sys.stdout`.

        .. versionchanged:: 1.1.1
            Previously used :attr:`file`, which is now :attr:`stdout`.
        """
        if file is None:    # pragma: no cover
            file = self.stdout
        if message:
            message = unicode(message)
        super(ArgumentParser, self)._print_message(message, file)

    def exit(self, status=0, message=None):
        """If *message* is not None, write it to :attr:`stderr` instead of :data:`sys.stderr`."""
        if message:
            self.stderr.write(unicode(message))
        super(ArgumentParser, self).exit(status, message=None)

    def error(self, message):
        """Write *message* to :attr:`stderr` instead of :data:`sys.stderr`."""
        self.print_usage(self.stderr)
        self.exit(2, u"%s: error: %s\n" % (self.prog, message))

class CommandLineMixin(object):
    """A command line application.

    Command line applications extend the basic :class:`Application`
    framework to support command line parsing using the :mod:`argparse`
    module. As with :class:`Application` itself, *main* should be a
    callable. Other arguments are:

    *usage* is a string describing command line usage of the
    application. If it is not supplied, :mod:`argparse` will
    automatically generate a usage statement based on the application's
    parameters.

    *epilog* is text appended to the argument descriptions.

    The rest of the arguments are passed to the :class:`Application`
    constructor.
    """
    prefix = '-'
    argparser_factory = ArgumentParser
    formatter = argparse.HelpFormatter

    params = None
    """The :attr:`params` attribute is an object with attributes
    containing the values of the parsed command line arguments.
    Specifically, its an instance of :class:`argparse.Namespace`,
    but only the mapping of attributes to argument values should be
    relied upon.
    """

    def __init__(self, usage=None, epilog=None, **kwargs):
        self.usage = usage
        self.epilog = epilog
        self.actions = {}
        self.params = argparse.Namespace()

    def setup(self):
        """Configure the :class:`CommandLineMixin`.

        During setup, the application instantiates the
        :class:`argparse.ArgumentParser` and adds a version parameter
        (:option:`-V`, to avoid clashing with :option:`-v`
        verbose).
        """
        self.argparser = self.argparser_factory(
            prog=self.name,
            usage=self.usage,
            description=self.description,
            epilog=self.epilog,
            prefix_chars=self.prefix,
            argv=self.argv,
            stdout=self.stdout,
            stderr=self.stderr,
            )

        # We add this ourselves to avoid clashing with -v/verbose.
        if self.version is not None:
            self.add_param(
                "-V", "--version", action="version", 
                version=("%%(prog)s %s" % self.version),
                help=("show program's version number and exit"))

    def add_param(self, *args, **kwargs):
        """Add a parameter.

        :meth:`add_param` wraps
        :meth:`argparse.ArgumentParser.add_argument`, storing the
        parameter options in a dictionary. This information can be used
        later by other subclasses when deciding whether to override
        parameters.
        """
        action = self.argparser.add_argument(*args, **kwargs)
        self.actions[action.dest] = action
        return action

    def update_params(self, params, newparams):
        """Update a parameter namespace.

        The *params* instance will be updated with the names and values
        from *newparams* and then returned.

        .. versionchanged:: 1.0.2
            :meth:`update_params` expects and returns
            :class:`argparse.Namespace` instances; previously, it took
            keyword arguments and updated :attr:`params` itself. This is
            now left to the caller.
        """
        for k, v in vars(newparams).items():
            setattr(params, k, v)

        return params

    def pre_run(self):
        """Parse command line.

        During :meth:`pre_run`, :class:`CommandLineMixin`
        calls :meth:`argparse.ArgumentParser.parse_args`. The results are
        stored in :attr:`params`. 

        ..versionchanged:: 1.1.1

        If :meth:`argparse.ArgumentParser.parse_args` raises SystemExit but
        :attr:`exit_after_main` is not True, raise Abort instead.
        """
        try:
            ns = self.argparser.parse_args()
        except SystemExit, e:
            if self.exit_after_main:
                raise
            else:
                raise Abort(e.code)
        self.params = self.update_params(self.params, ns)

class CommandLineApp(CommandLineMixin, Application):
    """A command line application.

    This class simply glues together the base :class:`Application` and
    :class:`CommandLineMixin`.

    .. versionchanged: 1.0.4

    Actual functionality moved to :class:`CommandLineMixin`.
    """
    
    def __init__(self, main=None, **kwargs):
        CommandLineMixin.__init__(self, **kwargs)
        Application.__init__(self, main, **kwargs)

    def setup(self):
        Application.setup(self)
        CommandLineMixin.setup(self)
