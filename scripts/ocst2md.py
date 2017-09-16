#!/usr/bin/env python

import sys, yaml

base_path = "https://github.com/owasp-cloud-security/owasp-cloud-security/blob/master/"
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
        elems = [threat[key]]
      elif isinstance(threat[key], list):
        elems = threat[key]

      for elem in elems:
        if key == "mitigations":
          print("* [%s](%s%s)" % (elem, base_path, elem))
        else:
          print("* %s" % elem)
  print
