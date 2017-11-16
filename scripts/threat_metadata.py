#!/usr/bin/env python

import sys, re, yaml
from pprint import pprint

process_comments = True
metadata_lines = []
story_lines = []
with open(sys.argv[1]) as fh:
  for line in fh.readlines():
    match = re.match(r'^\s*#\s*(.*)$', line)
    if process_comments and match:
      metadata_lines.append(match.group(1))
    else:
      match = re.match(r'^\s*Feature:\s*(.*)$', line)
      if match:
        process_comments = False
        metadata_lines.append("Name: %s" % match.group(1))
    if not process_comments:
      story_lines.append(line)

metadata = yaml.load("\n".join(metadata_lines))
metadata["Story"] = "\n".join(story_lines)
pprint(metadata)
