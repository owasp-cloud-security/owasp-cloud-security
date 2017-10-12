import os

from cli.test import FunctionalTest

FunctionalTest.scriptdir = os.path.join(os.path.dirname(__file__), "scripts")
