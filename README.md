# OWASP Cloud Security

The OWASP Cloud Security project aims to help people secure their products and services running in the cloud by providing a set of easy to use threat model templates and security control BDD stories that pool together the expertise and experience of the development, operations, and security communities.

You can find the main OWASP Project page here: https://www.owasp.org/index.php/OWASP_Cloud_Security_Project

# Using the project

This project provides the following for an ever-expanding list of cloud providers and services:

## Threats stored as machine-parsable YAML files and human-friendly README files (generated from YAML)

![threats](/images/threats.png)

## Mitigating controls as BDD stories in Gherkin-like feature files

![bdd stories](/images/bdd.png)

## Proof-of-concept attack scripts and tools

Check out the tools directory in the provider/service directories.

For more information, take a look at the [Using the project](https://github.com/owasp-cloud-security/owasp-cloud-security/wiki/Using-the-project) and [Project structure](https://github.com/owasp-cloud-security/owasp-cloud-security/wiki/Project-structure) Wiki pages.

# Getting involved

This project was created to pool together the experience and expertise of people just like you, so that others can build better and more secure products and services in the cloud. Your contributions are essential!


## Join the discussion

The simplest way to get involved is to reach out to other members of the community. If you would like to ask questions, discuss ideas or problems, or even just share your thoughts you can do so in a number of ways:

* [@OWASP_CloudSec on Twitter](https://twitter.com/OWASP_CloudSec)
* [#cloud-security on the OWASP Slack](https://owasp.slack.com/messages/C7FRASYET/)
* Email - mailing list coming soon!

If you would like to get in touch with the project leader directly, you can do so via email to fraser.scott@owasp.org

## Github issues and Pull Requests

This project uses [Github issues](https://github.com/owasp-cloud-security/owasp-cloud-security/wiki/Working-with-Github-issues) as the primary way of tracking tasks, problems and ideas etc. If you're looking for a way to help out, but you're not sure where to start, take a look at the list of issues for something you could work on.

If you want to just get stuck straight in, you can create Github pull requests (PRs) with your changes. You don't need to create an issue first. Your PR will then be reviewed. If all is well, your PR will be merged into the repository. If there are questions, these will be done via the comments on the PR. For more information, see the [Creating pull requests](https://github.com/owasp-cloud-security/owasp-cloud-security/wiki/Creating-pull-requests) section.

## What needs doing

This project is still in its infancy, so there's plenty of things to do. Also, as cloud security is an ever-expanding landscape, there will always be plenty of things to do ;)

* Discovering new threats
* Documenting threats
* Identifying controls
* Documenting controls
* Community development

For more information on how to get involved, see the [Getting involved](https://github.com/owasp-cloud-security/owasp-cloud-security/wiki/Getting-involved) Wiki page.

# Using the OWASP Cloud Security project

This project can be used in many different ways, but typically it will involve using the threat models in your SDLC, then using the BDD stories to ensure you mitigated against identified threats.

## Threat models

There is no single correct way to threat model. There are different methodologies, each with differing levels of formality and strengths etc.  Formal threat modelling as part of the SDLC can seem like a daunting task, so this project aims to make it easier to get started with threat modelling cloud based products and services by providing a library of threats that other people have idenitied.

If you're looking to do formal threat modelling sessions, you can reference the threats in the project as you work through the components of your cloud service. You may find that the threats in this project lead on to ideas for other cloud related threats, or perhaps they help you identified issues and assumptions in the design and architecture of your application. If you find new threats, please consider [contributing them back to the project](https://github.com/owasp-cloud-security/owasp-cloud-security/wiki/Getting-involved)!

If you aren't running formal threat modelling sessions, then you can simply read through the threats and think about how they might apply to your product and service. If you think a threat is relevant, create a bug or story on your backlog to make sure you address it at some point.

For more information on threat modelling, take a look at the [Learning more](https://github.com/owasp-cloud-security/owasp-cloud-security/wiki/Learning-more) section.

## BDD stories

Once you have identified threats that are relevant to your environment, the next step is to think about what to do about those threats. This project provides mitigating controls in the form of Behaviour Driven Development (BDD) feature stories. BDD expresses an idea such as a requirement or user experience in a way that is natural to read but can be tested as code. BDD seems to fit particularly well for security as it allows technical experts to express requirements for mitigating controls as something that can be easily understood by management and auditors, and then prove that those requirements are being met through the use of continuous testing. Gherkin, the language generally used for BDD, is mostly agnostic to the underlying implementation. This allows different organisations to take the exact same requirements story and them implement it in a way that best suits that organisation.

Depending on your levels of automation, approaches to testing, and general engineering maturity, you have several options for using the BDD stories.

The simplest way to use the stories is to treat them as just another form of documentation and to then somehow check that you have controls in place that map to the stories. You could paste the relevent scenarios into issues on your project backlogs so that an engineer picks up the task of testing or implementing the control.

The more advanced way of using the BDD stories is to write test implementations that enable you to continuously test the assumption that you have controls in place and that they are indeed effective. Because different organisations prefer different techonology stacks, it is up to you to choose and development the test implementations for the BDD stories. For example, you could use Python's behave library from a Jenkins server, or use Cucumber on CircleCI. Use the technology that works best for you.

For more information on BDD, see the [Learning more](https://github.com/owasp-cloud-security/owasp-cloud-security/wiki/Learning-more) section.
