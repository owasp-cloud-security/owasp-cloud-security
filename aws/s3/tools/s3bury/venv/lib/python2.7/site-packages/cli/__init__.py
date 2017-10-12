"""\
The cli package is a framework for making simple, correct command
line applications in Python. With cli, you can quickly add standard
`command line parsing`_; `logging`_; `unit`_ and `functional`_ testing;
and `profiling`_ to your CLI apps. To make it easier to do the right 
thing, cli wraps all of these tools into a single, consistent application 
interface.

.. _command line parsing:   http://www.python.org/dev/peps/pep-0389/#deprecation-of-optparse
.. _logging:                http://docs.python.org/library/logging.html
.. _unit:                   http://docs.python.org/library/unittest.html
.. _functional:             http://pythonpaste.org/scripttest/
.. _profiling:              http://docs.python.org/library/profile.html
"""

# pragma: no cover

__project__ = "pyCLI"
__version__ = "2.0.3"
__package__ = "cli"
__description__ = "Simple, object-oriented approach to Python CLI apps"
__author__ = "Will Maier"
__author_email__ = "wcmaier@m.aier.us"
__url__ = "http://packages.python.org/pyCLI/"

# See http://pypi.python.org/pypi?%3Aaction=list_classifiers.
__classifiers__ = [
    "Programming Language :: Python :: 2.4",
    "Programming Language :: Python :: 2.5",
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Topic :: Software Development :: Libraries :: Application Frameworks",
    "Environment :: Console",
    "Development Status :: 5 - Production/Stable",
] 
__keywords__ = "command line application framework"

__requires__ = []

# The following is modeled after the ISC license.
__copyright__ = """\
2009-2012 Will Maier <wcmaier@m.aier.us>

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
* cli.app:
    * more tests
    * add Windows registry/OS X plist support (sekhmet)
"""
