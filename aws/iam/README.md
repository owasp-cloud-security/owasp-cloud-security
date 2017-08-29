# AWS Identity and Access Management (IAM)

Controlling access to AWS resources

# See also

* https://docs.aws.amazon.com/IAM/latest/UserGuide/getting-started.html
# AWS IAM Threat Model

# Assumptions

* A threat model exists for console and API access to service. This page does not include threat models of the TLS or authentication mechanism of the AWS API itself.

# Scope

This threat model is scoped to the IAM service itself, including for example roles and policies, but not to all the possible IAM actions of every single AWS service. The only IAM actions considered here are those of IAM itself (e.g. PassRole and AssumeRole).

# Threats

## Notes

* No MFA?
* Using AWS accounts as principals exposes it to all principals in the account
* Policy VersionId defaults to 2008 - is that bad?
* Non-unique PolicyId?
* Deny overrides allow which overrides implicit deny
* What happens when you use principal in policy attached to a user or group? - Docs state "Do not use the Principal element in policies that you attach to IAM users or groups"
* Wildcard principal means everyone/anonymous. A poorly defined condition could expose the policy to any user/role in any account.
* Root is entire account - nice idea for a tool perhaps to look for uses of :root arns
* Principal for specific users and roles uses canonical ids to prevent removal + addition
* Assume role session id?
* "Warning - When you use NotPrincipal in the same policy statement as Effect Allow the permissions specified in the policy statement will be granted to all principals except the ones specified, including anonymous". For example, an administrative policy that includes NonPrincipal:NormalUsers, Effect:Allow, Actions:Dangerous stuff would actually expose those actions to anonymous users
* Apparently NonPrincipal + Effect:Deny is order dependant
* NotAction results in exposure to new actions

## OCSTM-3.1

### Name

Attacker can gain unauthorised access to resources using unprotected access keys

### Description

aklkaalslkaslklkj

### Status

To be confirmed

### STRIDE Classification

STRIDE

### Components

### Mitigations

* Access key rotation. Either fixed time or dynamic using SSO)
* Detection and clean up of unused access keys and users

# OLD

### Attacker can gain unauthorised access to ALL resources using unprotected root access keys

#### Mitigations

* Do not use root access keys, instead create administrator and other users

### Attacker can gain elevated permissions through unexpected AWS ManagedPolicy updates

If the organisation uses AWS provided ManagedPolicies, then they may not be aware of the updates made by AWS to those policies. If AWS introduces additional services or actions, then the organisation may have additional exposure that they're not aware of. An attacker that knows about the updates may be able to use this to their advantage.

#### Mitigations

* Use custom policies (implicit denies)

### Attacker can guess a user's AWS console password through weak password policy

#### Mitigations

* Use a complex password policy

### Attacker can perform the confused deputy attack by tricking a trusted third party into assuming the role of an ARN in another account

#### Mitigations

* Use the optional ExternalId in a condition as a pre-shared key

### Where ExternalId is used, attacker can perform the confused deputy attack by tricking a trusted third party into assuming the role of an ARN in another account because the ExternalId lacked complexity and was easy to guess

#### Mitigations

* Use a long, securely generated random value

