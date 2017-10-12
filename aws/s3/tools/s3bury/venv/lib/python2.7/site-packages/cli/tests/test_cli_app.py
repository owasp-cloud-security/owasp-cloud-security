"""CLI tools for Python.

Copyright (c) 2009-2010 Will Maier <will@m.aier.us>

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

from cli.app import Abort, Application, CommandLineApp
from cli.util import StringIO

from cli import tests

class FakeApp(Application):
    
    def main(self):
        pass

class FakeCommandLineApp(CommandLineApp):
    
    def main(self):
        pass

class TestApplication(tests.AppTest):
    app_cls = FakeApp
    
    def test_discover_name(self):
        self.assertEqual(self.app.name, "main")

    def test_exit(self):
        @self.app_cls
        def app(app):
            pass

        self.assertRaises(SystemExit, app.run)

    def test_returns(self):
        self.assertEqual(self.app.run(), 0)

    def test_returns_value(self):
        @self.app_cls(exit_after_main=False)
        def app(app):
            return 1

        self.assertEqual(app.run(), 1)
        app.main = lambda app: "foo"
        self.assertEqual(app.run(), 1)

    def test_raise_exception1(self):
        @self.app_cls(exit_after_main=False, reraise=Exception)
        def app(app):
            raise RuntimeError("Just testing.")

        self.assertRaises(RuntimeError, app.run)

    def test_raise_exception2(self):
        @self.app_cls(exit_after_main=False,
                      reraise=(RuntimeError, AssertionError))
        def app(app):
            raise RuntimeError("Just testing.")

        self.assertRaises(RuntimeError, app.run)

    def test_swallow_exception(self):
        @self.app_cls(exit_after_main=False, reraise=(ValueError, TypeError))
        def app(app):
            raise RuntimeError("Just testing.")

        self.assertEqual(app.run(), 1)

            
class TestCommandLineApp(tests.AppTest):
    app_cls = FakeCommandLineApp

    def test_parse_args(self):
        app_cls = self.app_cls
        class Test(app_cls):
            
            def setup(self):
                app_cls.setup(self)
                self.add_param("-f", "--foo", default=None)

        status, app = self.runapp(Test, "test -f bar")
        self.assertEqual(app.params.foo, "bar")

    def test_parse_args_version(self):
        class Test(self.app_cls): pass

        status = None
        try:
            self.runapp(Test, "test -V", version="1.0")
        except Abort, e:
            status = e.status
        self.assertEqual(status, 0)

    def test_version(self):
        self.app.version = "0.1"
        self.app.run()
