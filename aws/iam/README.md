# AWS Identity and Access Management (IAM) Threat Model

## See also

* https://docs.aws.amazon.com/IAM/latest/UserGuide/getting-started.html

# Assumptions

* A threat model exists for console and API access to service. This page does not include threat models of the TLS or authentication mechanism of the AWS API itself.

# Scope

This threat model is scoped to the IAM service itself, including for example roles and policies, but not to all the possible IAM actions of every single AWS service. The only IAM actions considered here are those of IAM itself (e.g. PassRole and AssumeRole).

# Threats

## OCST-1.3.1

### Name

Unprotected access keys

### Description

Attacker can gain unauthorised access to resources using unprotected AWS access keys.

If an AWS user doesn't sufficiently protect their access keys, for example by leaving them on a server, then an attacker could use those keys to gain access to any resources assigned to those keys.

Because the use of the API access keys is global, the attacker doesn't need to be an account already if the keys are exposed outside of AWS. 

### Service

AWS IAM

### Status

Confirmed

### STRIDE Classification

* Information disclosure
* Elevation of privilege

### Components

* IAM User
* Access Key

### Mitigations

* Access key rotation. Either fixed time or dynamic using SSO
* Detection and clean up of unused access keys and users
* Assume roles where possible

### References

* https://docs.aws.amazon.com/general/latest/gr/managing-aws-access-keys.html
* https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html#lock-away-credentials

## OCST-1.3.2

### Name

Unprotected root access keys

### Description

Attacker can gain unauthorised access to ALL resources using unprotected root access keys.

The account root user has full access to all resources, including billing, and cannot be restricted.

### Service

AWS IAM

### Status

Confirmed

### STRIDE Classification

* Information disclosure
* Elevation of privilege

### Components

* IAM User
* Access Key
* AWS Account (root user)

### Mitigations

* Do not use root access keys. Instead create separate administrative users or ideally users with the least privilege required for the use case.

### References

* https://docs.aws.amazon.com/general/latest/gr/managing-aws-access-keys.html
* https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html#lock-away-credentials

## OCST-1.3.3

### Name

Unexpected AWS ManagedPolicy updates

### Description

An attacker can gain elevated permissions through unexpected AWS ManagedPolicy updates.

If the organisation uses AWS provided ManagedPolicies, then they may not be aware of the updates made by AWS to those policies. If AWS introduces additional services or actions, then the organisation may have additional exposure that they're not aware of. An attacker that knows about the updates may be able to use this to their advantage.

### Service

AWS IAM

### Status

Confirmed

### STRIDE Classification

* Elevation of privilege

### Components

* IAM ManagedPolicy

### Mitigations

* Use customer managed policies with non-wildcard actions.

### References

* https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_managed-vs-inline.html

## OCST-1.3.4

### Name

Weak password policy

### Description

An attacker can guess a user's AWS console password through weak password policy.

If an account password policy is not used, or is configured to be weak, then an attacker might be able to guess a user's password.

### Service

AWS IAM

### Status

Confirmed

### STRIDE Classification

* Elevation of privilege

### Components

* IAM User
* Account Password Policy

### Mitigations

* Use a complex password policy such as having a minimum length and/or requiring specific character types.
* Use federation (SSO)

### References

* https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_passwords_account-policy.html

## OCST-1.3.5

### Name

Confused deputy

### Description

An attacker can perform the confused deputy attack by tricking a trusted third party into assuming the role of an ARN in another account.

### Service

AWS IAM

### Status

Confirmed

### STRIDE Classification

* Elevation of privilege

### Components

* IAM AssumeRole

### Mitigations

* Use the optional ExternalId in a condition as a pre-shared key

### References

* https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user_externalid.html
* https://aws.amazon.com/blogs/security/tag/confused-deputy/

## OCST-1.3.6

### Name

Weak ExternalId

### Description

Where ExternalId is used, attacker can perform the confused deputy attack by tricking a trusted third party into assuming the role of an ARN in another account because the ExternalId lacked complexity and was easy to guess

### Service

AWS IAM

### Status

Confirmed

### STRIDE Classification

* Elevation of privilege

### Components

* IAM AssumeRole
* ExternalId

### Mitigations

* Use a long, securely generated random ExternalId

### References

* https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user_externalid.html
* https://aws.amazon.com/blogs/security/tag/confused-deputy/

# Notes

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
# Threats
## OCST-1.3.1
### Name
Unprotected access keys
### Description
Attacker can gain unauthorised access to resources using unprotected AWS access keys.

If an AWS user doesn't sufficiently protect their access keys, for example by leaving them on a server, then an attacker could use those keys to gain access to any resources assigned to those keys.

Because the use of the API access keys is global, the attacker doesn't need to be an account already if the keys are exposed outside of AWS.  

### Service
AWS IAM
### Status
Confirmed
### Stride
* Information Disclosure
* Elevation of Privilege
### Components
* IAM user
* Access Key
### Mitigations
* Access key rotation. Either fixed time or dynamic using SSO
* Detection and clean up of unused access keys and users
* Assume roles where possible
