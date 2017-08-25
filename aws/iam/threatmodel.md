# AWS IAM Threat Model

# Assumptions

* A threat model exists for console and API access to service. This page does not include threat models of the TLS or authentication mechanism of the AWS API itself.

# Scope

This threat model is scoped to the IAM service itself, including for example roles and policies, but not to all the possible IAM actions of every single AWS service. The only IAM actions considered here are those of IAM itself (e.g. PassRole and AssumeRole).

# Threats

## Attacker can gain unauthorised access to resources using unprotected access keys

### Mitigations

* Access key rotation. Either fixed time or dynamic using SSO)
* Detection and clean up of unused access keys and users

## Attacker can gain unauthorised access to ALL resources using unprotected root access keys

### Mitigations

* Do not use root access keys, instead create administrator and other users

## Attacker can gain elevated permissions through unexpected AWS ManagedPolicy updates

If the organisation uses AWS provided ManagedPolicies, then they may not be aware of the updates made by AWS to those policies. If AWS introduces additional services or actions, then the organisation may have additional exposure that they're not aware of. An attacker that knows about the updates may be able to use this to their advantage.

### Mitigations

* Use custom policies (implicit denies)

## Attacker can guess a user's AWS console password through weak password policy

### Mitigations

* Use a complex password policy

## Attacker can perform the confused deputy attack by tricking a trusted third party into assuming the role of an ARN in another account

### Mitigations

* Use the optional ExternalId in a condition as a pre-shared key

## Where ExternalId is used, attacker can perform the confused deputy attack by tricking a trusted third party into assuming the role of an ARN in another account because the ExternalId lacked complexity and was easy to guess

### Mitigations

* Use a long, securely generated random value

