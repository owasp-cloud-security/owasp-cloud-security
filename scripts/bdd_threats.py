#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os.path

from pprint import pprint
from behave.configuration import Configuration
from behave.runner import *

class ThreatRunner(ModelRunner):
    def __init__(self, config):
        super(ThreatRunner, self).__init__(config)
        self.path_manager = PathManager()
        self.base_dir = None


    def setup_paths(self):
        if self.config.paths:
            if self.config.verbose:
                print('Supplied path:', \
                      ', '.join('"%s"' % path for path in self.config.paths))
            first_path = self.config.paths[0]
            if hasattr(first_path, "filename"):
                # -- BETTER: isinstance(first_path, FileLocation):
                first_path = first_path.filename
            base_dir = first_path
            if base_dir.startswith('@'):
                # -- USE: behave @features.txt
                base_dir = base_dir[1:]
                file_locations = self.feature_locations()
                if file_locations:
                    base_dir = os.path.dirname(file_locations[0].filename)
            base_dir = os.path.abspath(base_dir)

            # supplied path might be to a feature file
            if os.path.isfile(base_dir):
                if self.config.verbose:
                    print('Primary path is to a file so using its directory')
                base_dir = os.path.dirname(base_dir)
        else:
            if self.config.verbose:
                print('Using default path "./features"')
            base_dir = os.path.abspath('features')

        # Get the root. This is not guaranteed to be '/' because Windows.
        root_dir = path_getrootdir(base_dir)
        new_base_dir = base_dir
        steps_dir = self.config.steps_dir
        environment_file = self.config.environment_file

        while True:
            if self.config.verbose:
                print('Trying base directory:', new_base_dir)

            if os.path.isdir(os.path.join(new_base_dir, steps_dir)):
                break
            if os.path.isfile(os.path.join(new_base_dir, environment_file)):
                break
            if new_base_dir == root_dir:
                break

            new_base_dir = os.path.dirname(new_base_dir)

        if new_base_dir == root_dir:
            if self.config.verbose:
                if not self.config.paths:
                    print('ERROR: Could not find "%s" directory. '\
                          'Please specify where to find your features.' % \
                                steps_dir)
                else:
                    print('ERROR: Could not find "%s" directory in your '\
                        'specified path "%s"' % (steps_dir, base_dir))

            message = 'No %s directory in "%s"' % (steps_dir, base_dir)
            raise ConfigError(message)

        base_dir = new_base_dir
        self.config.base_dir = base_dir

        for dirpath, dirnames, filenames in os.walk(base_dir):
            if [fn for fn in filenames if fn.endswith('.feature')]:
                break
        else:
            if self.config.verbose:
                if not self.config.paths:
                    print('ERROR: Could not find any "<name>.feature" files. '\
                        'Please specify where to find your features.')
                else:
                    print('ERROR: Could not find any "<name>.feature" files '\
                        'in your specified path "%s"' % base_dir)
            raise ConfigError('No feature files in "%s"' % base_dir)

        self.base_dir = base_dir
        self.path_manager.add(base_dir)
        if not self.config.paths:
            self.config.paths = [base_dir]

        if base_dir != os.getcwd():
            self.path_manager.add(os.getcwd())

    def before_all_default_hook(self, context):
        """
        Default implementation for :func:`before_all()` hook.
        Setup the logging subsystem based on the configuration data.
        """
        context.config.setup_logging()

    def load_hooks(self, filename=None):

        source = """
import re, yaml

def before_feature(context, feature):
  match = re.match(r'^(OCST-\d+\.\d+\.\d+) (.*)$', feature.name)
  if match:
    context.threat = {
      "id": match.group(1),
      "name": match.group(2)
    }
    feature_story = []
    feature_story.append((0, "%s: %s" % (feature.keyword, feature.name)))
    for desc in feature.description:
      feature_story.append((1, desc))

    feature_story.append((1, "%s:" % feature.background.keyword))
    for step in feature.background.steps:
      feature_story.append((2, "%s %s" % (step.keyword, step.name)))

    for scenario in feature.scenarios:
      feature_story.append((1, "%s: %s" % (scenario.keyword, scenario.name)))
      for step in scenario.steps:
        feature_story.append((2, "%s %s" % (step.keyword, step.name)))
    
    context.threat["feature"] = feature_story

def after_feature(context, feature):
  if not context.failed:
    if not "threats" in context.dirty_hack:
      context.dirty_hack["threats"] = []
    context.dirty_hack["threats"].append(context.threat)
    #filename = "%s.yaml" % context.threat["id"]
    #with open(filename, "w") as fh:
      #yaml.dump(context.threat, fh)

        """
        code = compile(source, "hooks", 'exec')
        exec(code, self.hooks, self.hooks)

        if 'before_all' not in self.hooks:
            self.hooks['before_all'] = self.before_all_default_hook

    def load_step_definitions(self, extra_step_paths=[]):
        step_globals = {
            'use_step_matcher': matchers.use_step_matcher,
            'step_matcher':     matchers.step_matcher, # -- DEPRECATING
        }
        setup_step_decorators(step_globals)

        default_matcher = matchers.current_matcher

        source = """
@given(u'the {service} service')
def step_impl(context, service):
    context.threat["service"] = service

@given(u'the {component} component')
def step_impl(context, component):
  if not "components" in context.threat:
      context.threat["components"] = []
  context.threat["components"].append(component)

@then(u'the result is a successful {stride} attack')
def step_impl(context, stride):
    if not "stride" in context.threat:
        context.threat["stride"] = []
    context.threat["stride"].append(stride)

@given(u'{ignore}[x]')
@when(u'{ignore}[x]')
@then(u'{ignore}[x]')
def step_impl(context, ignore):
    pass
        """

        step_module_globals = step_globals.copy()
        code = compile(source, "steps", 'exec')
        exec(code, step_module_globals, step_module_globals)
        matchers.current_matcher = default_matcher

    def feature_locations(self):
        return collect_feature_locations(self.config.paths)


    def run(self):
        with self.path_manager:
            self.setup_paths()
            return self.run_with_paths()


    def run_with_paths(self):
        self.context = Context(self)
        self.context.dirty_hack = {}

        self.load_hooks()
        self.load_step_definitions()

        # -- ENSURE: context.execute_steps() works in weird cases (hooks, ...)
        # self.setup_capture()
        # self.run_hook('before_all', self.context)

        # -- STEP: Parse all feature files (by using their file location).
        feature_locations = [ filename for filename in self.feature_locations()
                                    if not self.config.exclude(filename) ]
        features = parse_features(feature_locations, language=self.config.lang)
        self.features.extend(features)

        # -- STEP: Run all features.
        stream_openers = self.config.outputs
        self.formatters = make_formatters(self.config, stream_openers)
        return self.run_model()

    def threats(self):
        return self.context.dirty_hack["threats"]

class ThreatBdd:

    def __init__(self, threats_path):
        self.threats_path = threats_path
 
    def run(self):
        config = Configuration(self.threats_path)
        config.format = [ config.default_format ]
        runner = ThreatRunner(config)
        failed = runner.run()
        self.threats = runner.threats()

if __name__ == "__main__":
    threatbdd = ThreatBdd()
    threatbdd.run()
    pprint(threatbdd.threats)
