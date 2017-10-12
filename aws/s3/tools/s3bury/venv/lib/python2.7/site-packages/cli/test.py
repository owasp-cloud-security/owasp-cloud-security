"""\
:mod:`cli.test` -- functional and unit test support
---------------------------------------------------

This module provides support for easily writing both functional and
unit tests for your scripts.

.. versionadded:: 1.0.2
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

import os
import shlex

from shutil import rmtree
from tempfile import mkdtemp

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from cli.app import Abort
from cli.ext import scripttest
from cli.util import StringIO, trim

__all__ = ["AppTest", "FunctionalTest"]

class AppTest(unittest.TestCase):
    """An application test, based on :class:`unittest.TestCase`.

    :class:`AppTest` provides a simple :meth:`setUp` method
    to instantiate :attr:`app_cls`, your application's class.
    :attr:`default_kwargs` will be passed to the new application then.

    .. deprecated:: 1.1.1
        Use :class:`AppMixin` instead.
    """
    app_cls = None
    """An application, usually descended from :class:`cli.app.Application`."""

    default_kwargs = {
        "argv": [],
        "exit_after_main": False
    }
    """Default keyword arguments that will be passed to the new :class:`cli.app.Application` instance.

    By default, the application won't see any command line arguments and
    will not raise SystemExit when the :func:`main` function returns.
    """

    def setUp(self):
        """Set up the application.

        :meth:`setUp` instantiates :attr:`app_cls` and
        stores it at :attr:`app`. Test methods should call
        the application's :meth:`cli.app.Application.setup`,
        :meth:`cli.app.Application.pre_run` and
        :meth:`cli.app.Application.run` methods as necessary.
        """
        kwargs = self.default_kwargs.copy()
        kwargs.update(getattr(self, "kwargs", {}))
        @self.app_cls(**kwargs)
        def app(app):
            pass
        self.app = app

    def runapp(self, cmd, environ={}, **kwargs):
        _kwargs = self.default_kwargs.copy()
        _kwargs.update(kwargs)
        self.app_cls(**kwargs)

class AppMixin(object):
    """Useful methods for testing App classes.

    Note: This won't help for testing App _instances_.
    """
    app_cls = None
    """The Application class to test."""
    args = ()
    """The arguments to pass when instantiating the test Application."""
    kwargs = {
        "exit_after_main": False,
    }
    """The keyword arguments to pass when instantiating the test Application."""

    def runapp(self, app_cls, cmd, **kwargs):
        """Run the application.

        *app_cls* is a class that inherits from :class:`cli.app.Application`.
        *cmd* may be a string with command line arguments. If present, *cmd*
        will be parsed by :func:`shlex.split` and passed to the application
        as its *argv* keyword argument (overriding *argv* keys in both
        :attr:`default_kwargs` and *kwargs*). *kwargs* will be merged with
        :attr:`default_kwargs` and passed to the application as well.

        If *stdout* or *stderr* keys are not set in either *kwargs* or
        :attr:`default_kwargs`, new :class:`StringIO` instances will be
        used as temporary buffers for application output.

        Returns (status, app), where *status* is the application's return code
        and *app* is the application instance.
        """
        _kwargs = self.kwargs.copy()
        _kwargs.update(kwargs)
        _kwargs["stdout"] = _kwargs.get("stdout", StringIO())
        _kwargs["stderr"] = _kwargs.get("stderr", StringIO())
        if cmd:
            _kwargs["argv"] = shlex.split(cmd)
        app = app_cls(**_kwargs)
        app.setup()
        status = app.run()
        return status, app

    def assertAppDoes(self, app_cls, cmd, kwargs={}, stdout='', stderr='', status=0,
            raises=(), trim_output=trim):
        """Fail the test if the app behaves unexpectedly.

        *app_cls*, *cmd* and *kwargs* will be passed to :meth:`runapp`. If the
        application raises an :class:`Exception` instance contained in the
        *raises* tuple, the test will pass. Otherwise, the application's stdout,
        stderr and return status will be compared with *stdout*, *stderr* and
        *status*, respectively (using :meth:`assertEqual`).
        """
        try:
            returned, app = self.runapp(app_cls, cmd, **kwargs)
        except raises, e:
            return True
        if trim:
            stdout, stderr = trim(stdout), trim(stderr)
        self.assertEqual(status, returned)
        self.assertEqual(stdout, app.stdout)
        self.assertEqual(stderr, app.stderr)

    def assertAppAborts(self, app_cls, cmd, status=0, **kwargs):
        """Fail unless the app aborts.

        *app_cls* must raise :class:`Abort` with a :data:`Abort.status` value
        equal to *status*.
        """
        try:
            self.runapp(app_cls, cmd, **kwargs)
        except Abort, e:
            self.assertEqual(status, e.status)
            return True

        raise self.failureException("Abort not raised")

class FunctionalTest(unittest.TestCase):
    """A functional test, also based on :class:`unittest.TestCase`.

    Functional tests monitor an application's 'macro' behavior, making
    it easy to spot regressions. They can also be simpler to write and
    maintain as they don't rely on any application internals.

    The :class:`FunctionalTest` will look for scripts to run under
    :attr:`scriptdir`. It uses :class:`scripttest.TestFileEnvironment`
    to provide temporary working areas for the scripts; these scratch
    areas will be created under :attr:`testdir` (and are created and
    removed before and after each test is run).
    """
    testdir = None
    scriptdir = None
    run_kwargs = {
        "expect_stderr": True,
        "expect_error": True,
    }

    def setUp(self):
        """Prepare for the functional test.

        :meth:`setUp` creates the test's working directory. If
        the :mod:`unittest2` package is present, it also makes sure that
        differences in the test's standard err and output are presented
        using :class:`unittest2.TestCase.assertMultiLineEqual`. Finally,
        :meth:`setUp` instantiates the
        :class:`scripttest.TestFileEnvironment` and stores it at
        :attr:`env`.
        """
        self._testdir = self.testdir
        if self._testdir is None:
            self._testdir = mkdtemp(prefix="functests-")
        if not os.path.isdir(self._testdir):
            os.mkdir(self._testdir)
        path = os.environ.get("PATH", '').split(':')
        path.append(self.scriptdir)
        self.env = scripttest.TestFileEnvironment(
            base_path=os.path.join(self._testdir, "scripttest"),
            script_path=path,
        )

        addTypeEqualityFunc = getattr(self, "addTypeEqualityFunc", None)
        if callable(addTypeEqualityFunc):
            addTypeEqualityFunc(str, "assertMultiLineEqual")

    def tearDown(self):
        """Clean up after the test.

        :meth:`tearDown` removes the temporary working directory created
        during :meth:`setUp`.
        """
        rmtree(self._testdir)

    def run_script(self, script, *args, **kwargs):
        """Run a test script.

        *script*, *args* and *kwargs* are passed to :attr:`env`. Default keyword
        arguments are specified in :attr:`run_kwargs`.

        .. versionchanged:: 1.1.1
            :attr:`scriptdir` is no longer prepended to *script* before passing it
            to :attr:`env`. Instead, it is added to the env's *script_path* during
            :meth:`setUp`.
        """
        _kwargs = self.run_kwargs.copy()
        _kwargs.update(kwargs)
        return self.env.run(script, *args, **_kwargs)

    def assertScriptDoes(self, result, stdout='', stderr='', returncode=0, trim_output=True):
        """Fail if the result object's stdout, stderr and returncode are unexpected.

        *result* is usually a :class:`scripttest.ProcResult` with
        stdout, stderr and returncode attributes.
        """
        if trim_output:
            stdout, stderr = trim(stdout), trim(stderr)
        self.assertEqual(returncode, result.returncode,
            "expected returncode %d, got %d" % (returncode, result.returncode))
        self.assertEqual(result.stdout, stdout,
            "unexpected output on stdout")
        self.assertEqual(result.stderr, stderr,
            "unexpected output on stderr")
