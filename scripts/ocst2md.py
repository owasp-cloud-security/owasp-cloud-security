#!/usr/bin/env python

import sys, yaml

with open(sys.argv[1]) as fh:
  data = yaml.load(fh)

key_order = ["name", "description", "service", "status", "stride", "components", "mitigations", "references"]
print("# Threats\n")
for threat in data["threats"]:
  print("## %s" % threat["id"])

  for key in key_order:
    if key in threat:
      print("### %s" % key.capitalize())
      if isinstance(threat[key], str):
        print(threat[key])
      elif isinstance(threat[key], list):
        for elem in threat[key]:
          print("* %s" % elem)
  print
