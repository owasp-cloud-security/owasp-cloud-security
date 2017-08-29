# OWASP Cloud Security

**Threat models and BDD stories**

This project contains a growing library of threat models for Cloud services as well as BDD stories for the mitigations and controls that result from the threat models.

This project was borne out of the [OWASP Summit 2017](https://owaspsummit.org/).

# Project structure

## Directory structure

The root of this repository contains Cloud providers (e.g. aws). Within each directory you will find provider-specific services (e.g. ec2 for aws).

Each service directory contains the following files and directories:

* README.md - Overview and threat model
* dfd.mmd - mermaid data flow diagram source file
* dfd.mmd.png - Data flow diagram image file
* components.mmd - mermaid components diagram source file
* components.mmd.png - Components diagram image file
* features - Directory containing .feature BDD mitigation/control stories

## Threat model structure

The threat model structures are loosely based off the advice in https://blogs.msdn.microsoft.com/adioltean/2005/01/17/ten-tips-how-to-write-a-well-structured-threat-model-document/

## Id field

For threats the Id field is structured as follows:

    OCST-<platform_id>-<service_id>-<threat_id>

So if for example the Id is

    OCST-1.3.1

then the first 1 refers to the AWS platform, the 3 refers to the IAM service, and the second 1 refers to the threat number. In this case it is the first AWS IAM threat.

For mitigations the Id field is structured as follows:

    OCSM-<platform_id>-<service_id>-<mitigation_id>

If the Id is

    OCSM-1.3.4

then the first 1 and the 3 are as above, and the 4 shows that it is the fourth AWS IAM mitigation. Note that the mitigation Ids are not directly associated with threats because one mitigation might address multiple threats. In the event that a mitigation addresses threats in multiple services, this will be noted but the mitigation Id will reference the most appropriate service.

## Status field

The status field is used to indicate the state of the threat. Some threats are simply a what-if that may in fact not be possible, whereas others have public attack tools/exploits. The following field values are used:

* Unconfirmed - The threat is a what-if and may not actually even be possible. Further research is required.
* Confirmed - The threat has been confirmed through research.
* Exploited - A known attack tool or exploit exists for the threat.

# Roadmap

## Short term goals

Target date: 1st September 2017

* ~~Set up project repository and define repo structure~~
* Engage and on-board contributors
* Set up official OWASP project
* Set up community support and communication channels (e.g. Wiki, mailing list, IRC channel)
* A basic collection of threat models for 10 most popular AWS services (EC2, S3, SQS, RDS etc.)
* A basic collection of BDD stories for identified mitigations and controls of 10 most popular AWS services

## Medium term goals

Target date: 1st April 2018

* Mature collection of threat models for 10 most popular AWS services
* Mature collection of BDD stories for 10 most popular AWS services
* Basic threat models for at least 50% of AWS services (e.g. Cloudfront, Lambda, Elasticache)
* Basic BDD stories for indentified mitigations and controls of at least 50% of AWS services

## Long term goals

Target date: 2018 onwards

* Threat model and BDD additional cloud services (Azure, Google Compute Engine)
* Write vendor agnostic BDD stories (e.g. IaaS compute)

# See also

* https://knsv.github.io/mermaid/
* https://en.wikipedia.org/wiki/Behavior-driven_development
* http://www.networkworld.com/article/3074508/cloud-computing/top-30-aws-cloud-services.html

# Contributing

PRs and issues are welcome!
