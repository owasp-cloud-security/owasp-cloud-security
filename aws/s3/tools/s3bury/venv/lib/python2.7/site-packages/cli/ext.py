"""Includes:
    argparse - 2010.02.01
        LICENSE:    Apache License 2.0
        URL:        http://argparse.googlecode.com/svn/tags/r101/argparse.py

    scripttest - 2010.03.04
        LICENSE:    MIT
        URL:        http://bitbucket.org/ianb/scripttest/src/tip/scripttest/__init__.py
"""
import os

# Add included module names to __all__.
__all__ = ["argparse", "scripttest"]
project = os.path.basename(os.path.dirname(__file__))
ext = project + "._ext"

name, module = None, None
for name in __all__:
    try:
        module = __import__(name)
    except ImportError:
        module = __import__('.'.join((ext, name)), {}, {}, [ext])
    locals()[name] = module

del(ext, module, name, project)
