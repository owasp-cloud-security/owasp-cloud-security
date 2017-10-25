# OWASP Cloud Security

The OWASP Cloud Security project aims to help people secure their products and services running in the cloud by providing a set of easy to use threat model templates and security control BDD stories that pool together the expertise and experience of the development, operations, and security communities.

This project provides the following for an ever-expanding list of cloud providers and services:

* Threats stored as machine-parsable YAML files
* Threats stored as human-friendly README files (generated from YAML)
* Mitigating controls as BDD stories in Gherkin-like feature files
* Proof-of-concept attack scripts and tools

You can find the main OWASP Project page here: https://www.owasp.org/index.php/OWASP_Cloud_Security_Project

# Table of Contents

   * [Getting involved](#getting-involved)
      * [Ways to participate](#ways-to-participate)
         * [Join the discussion](#join-the-discussion)
         * [Github issues](#github-issues)
         * [Pull requests](#pull-requests)
      * [What needs doing](#what-needs-doing)
         * [Discovering new threats](#discovering-new-threats)
            * [Scope](#scope)
         * [Documenting threats](#documenting-threats)
         * [Identifying controls](#identifying-controls)
         * [Documenting controls](#documenting-controls)
         * [Community development](#community-development)
      * [Working with Github issues](#working-with-github-issues)
         * [Labels](#labels)
            * [Subject](#subject)
            * [Issue type](#issue-type)
            * [Cloud provider](#cloud-provider)
            * [Special](#special)
         * [Github projects](#github-projects)
         * [Creating Github issues](#creating-github-issues)
      * [Creating pull requests (PRs)](#creating-pull-requests-prs)
   * [Using the OWASP Cloud Security project](#using-the-owasp-cloud-security-project)
      * [Threat models](#threat-models)
      * [BDD stories](#bdd-stories)
   * [Project structure](#project-structure)
      * [Directory structure](#directory-structure)
      * [Threat model yaml files](#threat-model-yaml-files)
         * [Fields](#fields)
            * [id](#id)
            * [status](#status)
   * [Learning more](#learning-more)
      * [Threat modelling](#threat-modelling)
      * [Behaviour driven development](#behaviour-driven-development)
      * [Cloud](#cloud)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc)

# Getting involved

This project was created to pool together the experience and expertise of people just like you, so that others can build better and more secure products and services in the cloud. Your contributions are essential!

## Ways to participate

There are a number of different ways you can participate in the project.

### Join the discussion

The simplest way to get involved is to reach out to other members of the community. If you would like to ask questions, discuss ideas or problems, or even just share your thoughts you can do so in a number of ways:

* [@OWASP_CloudSec on Twitter](twitter.com/owasp_cloudsec)
* [#cloud-security on the OWASP Slack](https://owasp.slack.com/messages/C7FRASYET/)
* Email - mailing list coming soon!

If you would like to get in touch with the project leader directly, you can do so via email to fraser.scott@owasp.org

### Github issues

This project uses [Github issues](#working-with-github-issues) as the primary way of tracking tasks, problems and ideas etc. 

You can create a new Github issue for pretty much anything, including:

* You have an idea for a possible threat but don't have time to research or fully document it
* You want to propose an idea for how the community could collaborate more effectively
* You found a typo or some other error but are not able to submit a pull request with changes
* There's some key documentation missing

If you're looking for a way to help out, but you're not sure where to start, take a look at the list of issues for something you could work on.

For more information, see the [Working with Github issues](#working-with-github-issues) section.

### Pull requests

If you want to just get stuck straight in, you can create Github pull requests (PRs) with your changes. You don't need to create an issue first. Your PR will then be reviewed. If all is well, your PR will be merged into the repository. If there are questions, these will be done via the comments on the PR.

For more information, see the [Creating pull requests](#creating-pull-requests-prs) section.

## What needs doing

This project is still in its infancy, so there's plenty of things to do. Also, as cloud security is an ever-expanding landscape, there will always be plenty of things to do ;)

The following sections detail the different types of activities you can participate in.

### Discovering new threats

Whether you're new to the cloud, a cloud expert, a seasoned pentester, or a junior developer, there are plenty of ways of researching new threats. These include, but are not limited to:

* Formal threat modelling sessions
* Reading and researching documentation (for example, look for the notes, warnings and other edge cases)
* Identifying threats documented in standards, whitepapers etc (please credit and provide references)
* Simply having a play to see what you can do/break

If you think you've found a new threat, but don't have time to research or test it, that's fine. Please just create a [Github issue](#working-with-github-issues) for somebody else to continue the research and documentation.

For more information on threat modelling, see the [Learning more](#learning-more) section.

#### Scope

This project focuses on the threats associated with using and specifically relating to cloud services. 

The following types of threats are **in scope**:

* The way cloud services are used

The following types of threats are **not in scope**:

* Threats associated with the cloud provider itself. If you find a problem with their API authentication, please don't add it here - raise it to their security team directly ;)
* General, non-cloud threats. Although you may be running a Linux host on AWS EC2, this project does cover threat modelling Linux hosts.

**Please note:** If you're thinking about contributing threats that you discovered at work or while working with a client etc. please make sure you have permission to contribute them and that you don't expose proprietary or sensitive information.

### Documenting threats

In an ideal world you would identify a new threat, test and prove it, then document it so that it is immediately consumable by users of this project. However, that probably isn't always going to be realistic. So it makes sense to differentiate between discovering threats and documenting them.

You will find [Github issues](#working-with-github-issues) for new threats that need verifying and then documenting. For more information on how threats are documented, see the [Project structure](#project-structure) section.

### Identifying controls

Identifying and documenting threats is only half the story (pun intended). The true value of this project is helping understand what they can do about the threats. This project uses Behaviour Driven Development (BDD) feature stories as a way of expressing requirements for mitigating controls. People can then take these requirements stories and, as they see fit, implement as mitigating controls in their environments.

There are many different ways of dealing with a threat, and these are typically split into the following types of controls:

* Prevention
* Detection
* Remediation

If you have a currently undocumented way of mitigating against a particular threat you can create a [Github issue](#working-with-github-issues) with a summary of control requirements and any supporting documentation. The controls can then be turned into BDD feature stories (see the next section).

### Documenting controls

Behaviour Driven Development (BDD) expresses an idea such as a requirement or user experience in a way that is natural to read but can be tested as code. BDD seems to fit particularly well for security as it allows technical experts to express requirements for mitigating controls as something that can be easily understood by management and auditors, and then prove that those requirements are being met through the use of continuous testing. Gherkin, the language generally used for BDD, is mostly agnostic to the underlying implementation. This allows different organisations to take the exact same requirements story and them implement it in a way that best suits that organisation.

If you have identified a control that is missing from the project, you can either create a simple Github issue with the details, or write a new BDD story in an existing or new feature file.

For more information about BDD, see the [Learning more](#learning-more) section below.

### Community development

The community is the lifeblood of the project. Awesome people like you make projects awesome :)

There are many non-technical ways to get involved in the project, so if you need a rest from coding or if threat modelling isn't really your thing, you can still make a huge impact!

The goal of community development is to:

* Raise awareness
* Make sure the project is easy to use
* Make sure the project is easy to contribute to

These goals are achieved in a number of ways:

* Having great documentation
* Publishing informative blog posts about major developments or announcements
* Interacting with the community on social media platforms such as Twitter
* Talking at events about the project, threat modelling or using BDD for security
* Having a well managed project that allows contributors (who volunteer their time) to help out with minimal hassle

If you think you can help achieve these goals, take a look at the [community Github issues](#working-with-github-issues).

## Working with Github issues

Github issues are the primary way of tracking work for the project. You can find the list of all Github issues [here](https://github.com/owasp-cloud-security/owasp-cloud-security/issues), but you'll probably want to read the Github projects section below.

### Labels

Labels are used to group issues in a number of different ways and can be combined as needed. So an idea for a new AWS threat would be labelled with threat\_model, idea and aws.

#### Subject

* threat\_model
* bdd\_feature
* community
* documentation

#### Issue type

* idea
* bug
* enhancement
* question

#### Cloud provider

* aws
* azure
* gcp

#### Special

* help wanted

### Github projects

Github provides a Kanban board system that makes it easier to see issues group together at the various stages of their life. There are currently three boards:

* [AWS Threats](https://github.com/owasp-cloud-security/owasp-cloud-security/projects/1)
* [AWS BDD](https://github.com/owasp-cloud-security/owasp-cloud-security/projects/2)
* [Community](https://github.com/owasp-cloud-security/owasp-cloud-security/projects/3)

More boards can be added when required.

Each board is made up columns that represent the various stages of a issue's life. They are:

* Backlog - The list of all things that should be done at some point
* Ready - The issues that have been prioritized and will be worked on next
* Research - The issue is being researched (threats and BDD)
* Documentation - The research is complete and the threat or BDD story is being documented (threats and BDD)
* In progress - People are actively working on these issues (community)
* Review - These issues have been completed and require peer review from the community

Issues have to be added to a project first, then triaged to the backlog. There is no Done column as this is handled by closing the issues.

For more information on Google projects, see the [Github documentation](https://help.github.com/articles/about-project-boards/).

### Creating Github issues

When you create a new Github issue, please:

* Add a description so other other people have the full context and are able to pick up the issue if needed.
* If possible, use the labels to identify the issue type etc.
* If possible, assign the issue to the appropriate project

## Creating pull requests (PRs)

To contribute a change:

1. Fork the repository on Github
2. Clone your fork to your local machine
3. Commit your changes to your own branch
4. Push your changes back to your fork
5. Submit a pull request to merge your changes into this repository

For more information see the [Github documentation](https://help.github.com/articles/creating-a-pull-request/)

# Using the OWASP Cloud Security project

This project can be used in many different ways, but typically it will involve using the threat models in your SDLC, then using the BDD stories to ensure you mitigated against identified threats.

## Threat models

There is no single correct way to threat model. There are different methodologies, each with differing levels of formality and strengths etc.  Formal threat modelling as part of the SDLC can seem like a daunting task, so this project aims to make it easier to get started with threat modelling cloud based products and services by providing a library of threats that other people have idenitied.

If you're looking to do formal threat modelling sessions, you can reference the threats in the project as you work through the components of your cloud service. You may find that the threats in this project lead on to ideas for other cloud related threats, or perhaps they help you identified issues and assumptions in the design and architecture of your application. If you find new threats, please consider [contributing them back to the project](#discovering-new-threats)!

If you aren't running formal threat modelling sessions, then you can simply read through the threats and think about how they might apply to your product and service. If you think a threat is relevant, create a bug or story on your backlog to make sure you address it at some point.

For more information on threat modelling, take a look at the [Learning more](#learning-more) section.

## BDD stories

Once you have identified threats that are relevant to your environment, the next step is to think about what to do about those threats. This project provides mitigating controls in the form of Behaviour Driven Development (BDD) feature stories. BDD expresses an idea such as a requirement or user experience in a way that is natural to read but can be tested as code. BDD seems to fit particularly well for security as it allows technical experts to express requirements for mitigating controls as something that can be easily understood by management and auditors, and then prove that those requirements are being met through the use of continuous testing. Gherkin, the language generally used for BDD, is mostly agnostic to the underlying implementation. This allows different organisations to take the exact same requirements story and them implement it in a way that best suits that organisation.

Depending on your levels of automation, approaches to testing, and general engineering maturity, you have several options for using the BDD stories.

The simplest way to use the stories is to treat them as just another form of documentation and to then somehow check that you have controls in place that map to the stories. You could paste the relevent scenarios into issues on your project backlogs so that an engineer picks up the task of testing or implementing the control.

The more advanced way of using the BDD stories is to write test implementations that enable you to continuously test the assumption that you have controls in place and that they are indeed effective. Because different organisations prefer different techonology stacks, it is up to you to choose and development the test implementations for the BDD stories. For example, you could use Python's behave library from a Jenkins server, or use Cucumber on CircleCI. Use the technology that works best for you.

For more information on BDD, see the [Learning more](#learning-more) section.

# Project structure

## Directory structure

The root of this repository contains Cloud providers (e.g. aws). Within each directory you will find provider-specific services (e.g. ec2 for aws).

Each service directory contains the following files and directories:

* README.md - Generated by concatenating the below two files (plus using ocst2md.py - see below)
* threatmodel.md - Threat model overview and scope information
* platform\_service\_threats.yaml - Data file containing threats (process to markdown using ocst2md.py)
* features - Directory containing .feature BDD mitigation/control stories
* tools - Proof-of-concept attack scripts and tools

## Threat model yaml files

The threat model structures are loosely based off the advice in https://blogs.msdn.microsoft.com/adioltean/2005/01/17/ten-tips-how-to-write-a-well-structured-threat-model-document/

Threats are stored in YAML files:

    threats:
      - id: <OCST id>
        name: <short name>
        description: |
          <long description>
        service: <platform and service name>
        status: <status name>
        stride: <one or more of>
          - Spoofing
          - Tampering
          - Repudiation
          - Information disclosure
          - Denial of service
          - Elevation of privilege
        components:
          - <related platform/service components>
        mitigations:
          - <mitigation descriptions or references>
        references:
          - <relevant documentation>

The service threat model README.md files can be generated using the following command:

    $ ./scripts/generate_readmes.sh

### Fields

#### id

For threats the Id field is structured as follows:

    OCST-<platform_id>-<service_id>-<threat_id>

So if for example the Id is

    OCST-1.3.1

then the first 1 refers to the AWS platform, the 3 refers to the IAM service, and the second 1 refers to the threat number. In this case it is the first AWS IAM threat.

#### status

The status field is used to indicate the state of the threat. Some threats are simply a what-if that may in fact not be possible, whereas others have public attack tools/exploits. The following field values are used:

* Unconfirmed - The threat is a what-if and may not actually even be possible. Further research is required.
* Confirmed - The threat has been confirmed through research.
* Exploited - A known attack tool or exploit exists for the threat.

# Learning more

## Threat modelling

If you would like to learn more about threat modelling, take a look at the [OWASP Threat Modeling](https://www.owasp.org/index.php/Category:Threat_Modeling) pages.

## Behaviour driven development

For a bit of an overview of BDD, take a look at the [Wikipedia](https://en.wikipedia.org/wiki/Behavior-driven_development) page.

There are number of different BDD implementations:

* [Cucumber](https://cucumber.io/)
* [Python behave](https://pythonhosted.org/behave/)
* [JBehave](http://jbehave.org/)
* plus many more!

## Cloud

If you're just getting started with the cloud, your best starting point will be the documentation provided by your cloud provider.

* [Amazon Web Services](https://aws.amazon.com/documentation/)
* [Microsoft Azure](https://docs.microsoft.com/en-us/azure/)
* [Google Cloud Platform](https://cloud.google.com/docs/)
