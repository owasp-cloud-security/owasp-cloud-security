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
import logging
logging.logMultiprocessing = 0

from cli.ext import argparse
from cli.log import CommandLineLogger, LoggingApp

from cli import tests

class FakeLoggingApp(LoggingApp):
    
    def main(self):
        pass

class TestCommandLineLogger(tests.BaseTest):
    
    def setUp(self):
        self.fakens = argparse.Namespace()
        self.logger = CommandLineLogger("foo")

    def test_setLevel(self):
        self.fakens.verbose = 0
        self.fakens.silent = False
        self.fakens.quiet = 0

        # The logger should start at 0.
        self.assertEqual(self.logger.level, 0)

        # Given the default input, it should be set to WARNING.
        self.logger.setLevel(self.fakens)
        self.assertEqual(self.logger.level, logging.WARNING)

        # Incrementing verbose should increase the logger's verbosity.
        self.fakens.verbose = 1
        self.logger.setLevel(self.fakens)
        self.assertEqual(self.logger.level, logging.INFO)

        # Incrementing quiet should decrease it.
        self.fakens.quiet = 1
        self.logger.setLevel(self.fakens)
        self.assertEqual(self.logger.level, logging.WARNING)
        self.fakens.quiet = 2
        self.logger.setLevel(self.fakens)
        self.assertEqual(self.logger.level, logging.ERROR)

        # And setting silent should shut it up completely.
        self.fakens.silent = True
        self.logger.setLevel(self.fakens)
        self.assertEqual(self.logger.level, logging.CRITICAL)

class TestLoggingApp(tests.AppTest):
    app_cls = FakeLoggingApp

    def test_setup_log(self):
        _, app = self.runapp(self.app_cls, "test -vvv")
        self.assertEqual(app.params.verbose, 3)
        self.assertEqual(app.log.level, logging.DEBUG)

        _, app = self.runapp(self.app_cls, "test -vvv -qqq")
        self.assertEqual(app.log.level, logging.WARNING)

    def test_no_stream_or_logfile(self):
        self.app.logfile = None
        self.app.stream = None

        self.app.run()

        # We shouldn't see anything here.
        self.app.log.critical("foo")
