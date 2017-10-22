# AWS Identity and Access Management (IAM) Threat Model

## See also

* https://docs.aws.amazon.com/IAM/latest/UserGuide/getting-started.html

# Assumptions

* A threat model exists for console and API access to service. This page does not include threat models of the TLS or authentication mechanism of the AWS API itself.

# Scope

This threat model is scoped to the IAM service itself, including for example roles and policies, but not to all the possible IAM actions of every single AWS service. The only IAM actions considered here are those of IAM itself (e.g. PassRole and AssumeRole).
