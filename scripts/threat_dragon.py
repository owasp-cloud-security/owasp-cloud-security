#!/usr/bin/env python

from pprint import pprint
import os, fnmatch, yaml, json, re
from cli.log import LoggingApp
from bdd_threats import ThreatBdd

class ThreatDragonIntegrationApp(LoggingApp):
  
  def load_threats(self):
    print("[*] Loading threats")
    self.threats = {}
    self.service_threats = {}

    threatbdd = ThreatBdd(self.params.THREATS)
    threatbdd.run()

    for threat in threatbdd.threats:
      self.threats[threat["id"]] = threat
      service = threat["service"]
      if not service in self.service_threats:
        self.service_threats[service] = []
      self.service_threats[service].append(threat)

  def load_threat_dragon_file(self):
    print("[*] Loading OWASP Threat Dragon file %s" % self.params.file)
    with open(self.params.file) as fh:
      self.threat_dragon_data = json.load(fh)

  def discover_threats(self):
    for diagram in self.threat_dragon_data["detail"]["diagrams"]:
      for cell in diagram["diagramJson"]["cells"]:
        try:
          match = re.search(r"\[OCS:([a-zA-Z0-9\ \-\_]+)\]", cell["attrs"]["text"]["text"])
        except KeyError:
          continue

        if match:
          service = match.group(1)
          if service in self.service_threats:
            print("[*] Adding threats for service %s" % service)
            if not "threats" in cell:
              cell["threats"] = []
            
            for threat in self.service_threats[service]:
              threat_found = False
              for td_threat in cell["threats"]:
                if td_threat["title"].startswith(threat["id"]):
                  threat_found = True
                  break
              if not threat_found:
                cell["threats"].append({
                  "status": "Open",
                  "title": threat["id"],
                  "severity": "medium"
                })
          else:
            print("[*] Unknown service found %s" % service)

  def parse_threats(self):
    for diagram in self.threat_dragon_data["detail"]["diagrams"]:
      for cell in diagram["diagramJson"]["cells"]:
        if "threats" in cell:
          for threat in cell["threats"]:
            match = re.match(r"^(OCST\-\d+\.\d+\.\d+)", threat["title"])
            if match:
              threat_id = match.group(1)
              if threat_id in self.threats:
                print("[*] Found threat %s" % threat_id)
                found_threat = self.threats[threat_id]
                threat["title"] = "%s %s" % (threat_id, found_threat["name"])
                threat["description"] = ""
                for (depth, feature_line) in found_threat["feature"]:
                  print(feature_line)
                  threat["description"] += "%s%s\n" % ("  " * depth, feature_line)
                threat["type"] = found_threat["stride"][0].capitalize()
                threat["mitigation"] = ""
                if "mitigations" in found_threat:
                  for mitigation in found_threat["mitigations"]:
                    if mitigation.endswith(".feature"):
                      with open(mitigation) as fh:
                        threat["mitigation"] += fh.read()+"\n\n"
                    else:
                        threat["mitigation"] += mitigation+"\n\n"
              else:
                print("[*] Unknown threat id %s" % threat_id)

  def save_threat_dragon_file(self):
    with open(self.params.file, "w") as fh:
      print("[*] Saving OWASP Threat Dragon file %s" % self.params.file)
      json.dump(self.threat_dragon_data, fh, indent=4)

  def main(self):
    self.load_threats()
    self.load_threat_dragon_file()
    if self.params.discover:
      self.discover_threats()
    self.parse_threats()
    self.save_threat_dragon_file()

if __name__ == "__main__":
  app = ThreatDragonIntegrationApp(
    name="OWASP Threat Dragon Integration",
    description="Inserts threats into Threat Dragon files"
  )
  app.add_param("--file", help="OWASP Threat Dragon data file")
  app.add_param("--discover", help="Discover threats based on cloud provider and service", action="store_true", default=False)
  app.add_param("THREATS", help="Threats files")
  app.run()

