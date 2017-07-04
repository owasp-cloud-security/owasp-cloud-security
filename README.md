# OWASP Cloud Security

**Threat models and BDD stories**

This project contains a growing library of threat models for Cloud services as well as BDD stores for the mitigations and controls that result from the threat models.

This project was borne out of the [OWASP Summit 2017](https://owaspsummit.org/).

# Project structure

The root of this repository contains Cloud providers (e.g. aws). Within each directory you will find provider-specific services (e.g. ec2 for aws).

Each service directory contains the following files and directories:

* README.md - A very brief overview of the service with links to relevant documentation
* threatmodel.md - The threat model for the service
* dfd.mmd - mermaid data flow diagram source file
* dfd.mmd.png - Data flow diagram image file
* components.mmd - mermaid components diagram source file
* components.mmd.png - Components diagram image file
* features - Directory containing .feature BDD mitigation/control stories

# See also

* https://knsv.github.io/mermaid/
* https://en.wikipedia.org/wiki/Behavior-driven_development

# Contributing

PRs and issues are welcome!
