"""\
:mod:`cli.daemon` -- daemonizing applications
---------------------------------------------

Daemonizing applications run in the background, forking themselves off.
"""

__license__ = """
Copyright (c) 2008-2010 Will Maier <will@m.aier.us>

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
 * when daemonized, catch exceptions and write them to app.log
""".split(" * ")

import os
import sys

from cli.app import CommandLineApp, CommandLineMixin, Application
from cli.log import LoggingMixin

__all__ = ["DaemonizingApp", "DaemonizingMixin"]

class DaemonizingMixin(object):
    """A command-line application that knows how to daemonize.

    The :class:`DaemonizingMixin` requires the :class:`cli.log.LoggingMixin`
    (for it's not very helpful to daemonize without being able to log
    messages somewhere). In addition to those supported by the standard
    :class:`cli.app.Application`, :class:`cli.app.CommandLineMixin` and
    :class:`cli.log.LoggingMixin`, arguments are:

    *pidfile* is a string pointing to a file where the application will
    write its process ID after it daemonizes. If it is ``None``, no such
    file will be created.

    *chdir* is a string pointing to a directory to which the application
    will change after it daemonizes.

    *null* is a string representing a file that will be opened to
    replace stdin, stdout and stderr when the application daemonizes. By
    default, this :data:`os.path.devnull`.
    """

    def __init__(self, pidfile=None, chdir='/', null=os.path.devnull, **kwargs):
        self.pidfile = pidfile
        self.chdir = chdir
        self.null = null

    def setup(self):
        """Configure the :class:`DaemonizingMixin`.

        This method adds the :option:`-d`, :option:`u`,
        and :option:`-p` parameters to the application.
        """
        # Add daemonizing options.
        self.add_param("-d", "--daemonize", default=False, action="store_true",
                help="run the application in the background")
        self.add_param("-u", "--user", default=None, 
                help="change to USER[:GROUP] after daemonizing")
        self.add_param("-p", "--pidfile", default=None, 
                help="write PID to PIDFILE after daemonizing")

    def daemonize(self):
        """Run in the background.

        :meth:`daemonize` must be called explicitly by the application
        when it's ready to fork into the background. It forks, flushes
        and replaces stdin, stderr and stdout with the open :attr:`null`
        file and, if requested on the command line, writes its PID to a
        file and changes user/group.
        """
        if os.fork(): sys.exit(0)
        os.umask(0) 
        os.setsid() 
        if os.fork(): sys.exit(0)

        self.stdout.flush()
        self.stderr.flush()
        si = open(self.null, 'r')
        so = open(self.null, 'a+')
        se = open(self.null, 'a+', 0)
        os.dup2(si.fileno(), self.stdin.fileno())
        os.dup2(so.fileno(), self.stdout.fileno())
        os.dup2(se.fileno(), self.stderr.fileno())

        if self.params.pidfile:
            self.log.debug("Writing pidfile %s", self.params.pidfile)
            pidfile = open(self.params.pidfile, 'w')
            pidfile.write('%i\n' % os.getpid())
            pidfile.close()

        if self.params.user:
            import grp
            import pwd
            delim = ':'
            user, sep, group = self.params.user.partition(delim)

            # If group isn't specified, try to use the username as
            # the group.
            if delim != sep:
                group = user
            self.log.debug("Changing to %s:%s", user, group)
            os.setgid(grp.getgrnam(group).gr_gid)
            os.setuid(pwd.getpwnam(user).pw_uid)

        self.log.debug("Changing directory to %s", self.chdir)
        os.chdir(self.chdir)

        return True

class DaemonizingApp(
    DaemonizingMixin, LoggingMixin, CommandLineMixin, Application):
    """A daemonizing application.

    This class simply glues together the base :class:`Application`,
    :class:`DaemonizingMixin` and other mixins that provide necessary
    functionality.

    .. versionchanged:: 1.0.4
        Actual functionality moved to :class:`DaemonizingMixin`.
    """

    def __init__(self, main=None, **kwargs):
        DaemonizingMixin.__init__(self, **kwargs)
        LoggingMixin.__init__(self, **kwargs)
        CommandLineMixin.__init__(self, **kwargs)
        Application.__init__(self, main, **kwargs)

    def setup(self):
        Application.setup(self)
        CommandLineMixin.setup(self)
        LoggingMixin.setup(self)
        DaemonizingMixin.setup(self)

    def pre_run(self):
        Application.pre_run(self)
        CommandLineMixin.pre_run(self)
        LoggingMixin.pre_run(self)
