# (c) 2005-2007 Ian Bicking and contributors; written for Paste (http://pythonpaste.org)
# Licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php
"""
Helpers for testing command-line scripts
"""
import sys
import os
import shutil
import shlex
import subprocess
import re

# From pathutils by Michael Foord: http://www.voidspace.org.uk/python/pathutils.html
def onerror(func, path, exc_info):
    """
    Error handler for ``shutil.rmtree``.

    If the error is due to an access error (read only file)
    it attempts to add write permission and then retries.

    If the error is for another reason it re-raises the error.

    Usage : ``shutil.rmtree(path, onerror=onerror)``

    """
    import stat
    if not os.access(path, os.W_OK):
        # Is the error an access error ?
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise

__all__ = ['TestFileEnvironment']

class TestFileEnvironment(object):

    """
    This represents an environment in which files will be written, and
    scripts will be run.
    """

    # for py.test
    disabled = True

    def __init__(self, base_path=None, template_path=None,
                 script_path=None,
                 environ=None, cwd=None, start_clear=True,
                 ignore_paths=None, ignore_hidden=True):
        """
        Creates an environment.  ``base_path`` is used as the current
        working directory, and generally where changes are looked for.
        If not given, it will be the directory of the calling script plus
        ``test-output/``.

        ``template_path`` is the directory to look for *template*
        files, which are files you'll explicitly add to the
        environment.  This is done with ``.writefile()``.

        ``script_path`` is the PATH for finding executables.  Usually
        grabbed from ``$PATH``.

        ``environ`` is the operating system environment,
        ``os.environ`` if not given.

        ``cwd`` is the working directory, ``base_path`` by default.

        If ``start_clear`` is true (default) then the ``base_path``
        will be cleared (all files deleted) when an instance is
        created.  You can also use ``.clear()`` to clear the files.

        ``ignore_paths`` is a set of specific filenames that should be
        ignored when created in the environment.  ``ignore_hidden``
        means, if true (default) that filenames and directories
        starting with ``'.'`` will be ignored.
        """
        if base_path is None:
            base_path = self._guess_base_path(1)
        self.base_path = base_path
        self.template_path = template_path
        if environ is None:
            environ = os.environ.copy()
        self.environ = environ
        if script_path is None:
            if sys.platform == 'win32':
                script_path = environ.get('PATH', '').split(';')
            else:       
                script_path = environ.get('PATH', '').split(':')
        self.script_path = script_path
        if cwd is None:
            cwd = base_path
        self.cwd = cwd
        if start_clear:
            self.clear()
        elif not os.path.exists(base_path):
            os.makedirs(base_path)
        self.ignore_paths = ignore_paths or []
        self.ignore_hidden = ignore_hidden

    def _guess_base_path(self, stack_level):
        frame = sys._getframe(stack_level+1)
        file = frame.f_globals.get('__file__')
        if not file:
            raise TypeError(
                "Could not guess a base_path argument from the calling scope "
                "(no __file__ found)")
        dir = os.path.dirname(file)
        return os.path.join(dir, 'test-output')

    def run(self, script, *args, **kw):
        """
        Run the command, with the given arguments.  The ``script``
        argument can have space-separated arguments, or you can use
        the positional arguments.

        Keywords allowed are:

        ``expect_error``: (default False)
            Don't raise an exception in case of errors
        ``expect_stderr``: (default ``expect_error``)
            Don't raise an exception if anything is printed to stderr
        ``stdin``: (default ``""``)
            Input to the script
        ``cwd``: (default ``self.cwd``)
            The working directory to run in (default ``base_path``)
        ``quiet``: (default False)
            When there's an error (return code != 0), do not print stdout/stderr

        Returns a `ProcResult
        <class-paste.fixture.ProcResult.html>`_ object.
        """
        __tracebackhide__ = True
        expect_error = _popget(kw, 'expect_error', False)
        expect_stderr = _popget(kw, 'expect_stderr', expect_error)
        cwd = _popget(kw, 'cwd', self.cwd)
        stdin = _popget(kw, 'stdin', None)
        quiet = _popget(kw, 'quiet', False)
        args = map(str, args)
        assert not kw, (
            "Arguments not expected: %s" % ', '.join(kw.keys()))
        if ' ' in script:
            assert not args, (
                "You cannot give a multi-argument script (%r) "
                "and arguments (%s)" % (script, args))
            script, args = script.split(None, 1)
            args = shlex.split(args)
        # We don't want to resolve $PATH for this:
        all_proc_results = [script] + args
        script = self._find_exe(script)
        all = [script] + args
        files_before = self._find_files()
        proc = subprocess.Popen(all, stdin=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                cwd=cwd,
                                env=self.environ)
        stdout, stderr = proc.communicate(stdin)
        files_after = self._find_files()
        result = ProcResult(
            self, all_proc_results, stdin, stdout, stderr,
            returncode=proc.returncode,
            files_before=files_before,
            files_after=files_after)
        if not expect_error:
            result.assert_no_error(quiet)
        if not expect_stderr:
            result.assert_no_stderr(quiet)
        return result

    def _find_exe(self, script_name):
        if self.script_path is None:
            script_name = os.path.join(self.cwd, script_name)
            if not os.path.exists(script_name):
                raise OSError(
                    "Script %s does not exist" % script_name)
            return script_name
        for path in self.script_path:
            fn = os.path.join(path, script_name)
            if os.path.exists(fn):
                return fn
        raise OSError(
            "Script %s could not be found in %s"
            % (script_name, ':'.join(self.script_path)))

    def _find_files(self):
        result = {}
        for fn in os.listdir(self.base_path):
            if self._ignore_file(fn):
                continue
            self._find_traverse(fn, result)
        return result

    def _ignore_file(self, fn):
        if fn in self.ignore_paths:
            return True
        if self.ignore_hidden and os.path.basename(fn).startswith('.'):
            return True
        return False

    def _find_traverse(self, path, result):
        full = os.path.join(self.base_path, path)
        if os.path.isdir(full):
            result[path] = FoundDir(self.base_path, path)
            for fn in os.listdir(full):
                fn = os.path.join(path, fn)
                if self._ignore_file(fn):
                    continue
                self._find_traverse(fn, result)
        else:
            result[path] = FoundFile(self.base_path, path)

    def clear(self, force=False):
        """
        Delete all the files in the base directory.
        """
        marker_file = os.path.join(self.base_path, '.scripttest-test-dir.txt')
        if os.path.exists(self.base_path):
            if not force and not os.path.exists(marker_file):
                print >> sys.stderr, 'The directory %s does not appear to have been created by ScriptTest' % self.base_path
                print >> sys.stderr, 'The directory %s must be a scratch directory; it will be wiped after every test run' % self.base_path
                print >> sys.stderr, 'Please delete this directory manually'
                raise AssertionError(
                    "The directory %s was not created by ScriptTest; it must be deleted manually" % self.base_path)
            shutil.rmtree(self.base_path, onerror=onerror)
        os.mkdir(self.base_path)
        f = open(marker_file, 'w')
        f.write('placeholder')
        f.close()

    def writefile(self, path, content=None,
                  frompath=None):
        """
        Write a file to the given path.  If ``content`` is given then
        that text is written, otherwise the file in ``frompath`` is
        used.  ``frompath`` is relative to ``self.template_path``
        """
        full = os.path.join(self.base_path, path)
        if not os.path.exists(os.path.dirname(full)):
            os.makedirs(os.path.dirname(full))
        f = open(full, 'wb')
        if content is not None:
            f.write(content)
        if frompath is not None:
            if self.template_path:
                frompath = os.path.join(self.template_path, frompath)
            f2 = open(frompath, 'rb')
            f.write(f2.read())
            f2.close()
        f.close()
        return FoundFile(self.base_path, path)

class ProcResult(object):

    """
    Represents the results of running a command in
    `TestFileEnvironment
    <class-paste.fixture.TestFileEnvironment.html>`_.

    Attributes to pay particular attention to:

    ``stdout``, ``stderr``:
        What is produced on those streams.

    ``returncode``:
        The return code of the script.

    ``files_created``, ``files_deleted``, ``files_updated``:
        Dictionaries mapping filenames (relative to the ``base_path``)
        to `FoundFile <class-paste.fixture.FoundFile.html>`_ or
        `FoundDir <class-paste.fixture.FoundDir.html>`_ objects.
    """

    def __init__(self, test_env, args, stdin, stdout, stderr,
                 returncode, files_before, files_after):
        self.test_env = test_env
        self.args = args
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode
        self.files_before = files_before
        self.files_after = files_after
        self.files_deleted = {}
        self.files_updated = {}
        self.files_created = files_after.copy()
        for path, f in files_before.items():
            if path not in files_after:
                self.files_deleted[path] = f
                continue
            del self.files_created[path]
            if f.mtime < files_after[path].mtime:
                self.files_updated[path] = files_after[path]

    def assert_no_error(self, quiet):
        __tracebackhide__ = True
        if self.returncode != 0:
            if not quiet:
                print self
            raise AssertionError(
                "Script returned code: %s" % self.returncode)

    def assert_no_stderr(self, quiet):
        __tracebackhide__ = True
        if self.stderr:
            if not quiet:
                print self
            else:
                print 'Error output:'
                print self.stderr
            raise AssertionError("stderr output not expected")

    def wildcard_matches(self, wildcard):
        """Return all the file objects whose path matches the given wildcard.

        You can use ``*`` to match any portion of a filename, and
        ``**`` to match multiple segments/directories.
        """
        regex_parts = []
        for index, part in enumerate(wildcard.split('**')):
            if index:
                regex_parts.append('.*')
            for internal_index, internal_part in enumerate(part.split('*')):
                if internal_index:
                    regex_parts.append('[^/\\\\]*')
                regex_parts.append(re.escape(internal_part))
        regex = ''.join(regex_parts) + '$'
        #assert 0, repr(regex)
        regex = re.compile(regex)
        results = []
        for container in self.files_updated, self.files_created:
            for key, value in sorted(container.items()):
                if regex.match(key):
                    results.append(value)
        return results

    def __str__(self):
        s = ['Script result: %s' % ' '.join(self.args)]
        if self.returncode:
            s.append('  return code: %s' % self.returncode)
        if self.stderr:
            s.append('-- stderr: --------------------')
            s.append(self.stderr)
        if self.stdout:
            s.append('-- stdout: --------------------')
            s.append(self.stdout)
        for name, files, show_size in [
            ('created', self.files_created, True),
            ('deleted', self.files_deleted, True),
            ('updated', self.files_updated, True)]:
            if files:
                s.append('-- %s: -------------------' % name)
                files = files.items()
                files.sort()
                last = ''
                for path, f in files:
                    t = '  %s' % _space_prefix(last, path, indent=4,
                                               include_sep=False)
                    last = path
                    if show_size and f.size != 'N/A':
                        t += '  (%s bytes)' % f.size
                    s.append(t)
        return '\n'.join(s)

class FoundFile(object):

    """
    Represents a single file found as the result of a command.

    Has attributes:

    ``path``:
        The path of the file, relative to the ``base_path``

    ``full``:
        The full path

    ``bytes``:
        The contents of the file.

    ``stat``:
        The results of ``os.stat``.  Also ``mtime`` and ``size``
        contain the ``.st_mtime`` and ``.st_size`` of the stat.

    ``mtime``:
        The modification time of the file.

    ``size``:
        The size (in bytes) of the file.

    You may use the ``in`` operator with these objects (tested against
    the contents of the file), and the ``.mustcontain()`` method.
    """

    file = True
    dir = False

    def __init__(self, base_path, path):
        self.base_path = base_path
        self.path = path
        self.full = os.path.join(base_path, path)
        self.stat = os.stat(self.full)
        self.mtime = self.stat.st_mtime
        self.size = self.stat.st_size
        self._bytes = None

    def bytes__get(self):
        if self._bytes is None:
            f = open(self.full, 'rb')
            self._bytes = f.read()
            f.close()
        return self._bytes
    bytes = property(bytes__get)

    def __contains__(self, s):
        return s in self.bytes

    def mustcontain(self, s):
        __tracebackhide__ = True
        bytes = self.bytes
        if s not in bytes:
            print 'Could not find %r in:' % s
            print bytes
            assert s in bytes

    def __repr__(self):
        return '<%s %s:%s>' % (
            self.__class__.__name__,
            self.base_path, self.path)

class FoundDir(object):

    """
    Represents a directory created by a command.
    """

    file = False
    dir = True

    def __init__(self, base_path, path):
        self.base_path = base_path
        self.path = path
        self.full = os.path.join(base_path, path)
        self.stat = os.stat(self.full)
        self.size = 'N/A'
        self.mtime = self.stat.st_mtime

    def __repr__(self):
        return '<%s %s:%s>' % (
            self.__class__.__name__,
            self.base_path, self.path)

def _popget(d, key, default=None):
    """
    Pop the key if found (else return default)
    """
    if key in d:
        return d.pop(key)
    return default

def _space_prefix(pref, full, sep=None, indent=None, include_sep=True):
    """
    Anything shared by pref and full will be replaced with spaces
    in full, and full returned.
    """
    if sep is None:
        sep = os.path.sep
    pref = pref.split(sep)
    full = full.split(sep)
    padding = []
    while pref and full and pref[0] == full[0]:
        if indent is None:
            padding.append(' ' * (len(full[0]) + len(sep)))
        else:
            padding.append(' ' * indent)
        full.pop(0)
        pref.pop(0)
    if padding:
        if include_sep:
            return ''.join(padding) + sep + sep.join(full)
        else:
            return ''.join(padding) + sep.join(full)
    else:
        return sep.join(full)
