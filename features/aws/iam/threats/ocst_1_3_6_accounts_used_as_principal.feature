# Id: OCST-1.3.6
# Status: Confirmed
# Service: AWS IAM
# STRIDE:
#   - Elevation of privilege
# Components:
#   - IAM AssumeRole
#   - Principals
#   - AWS Accounts
# References:
#   - https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements.html#Principal


Feature: Accounts used as principals
  In order to gain elevated privileges in a trusting account
  As an attacker
  I want the trusting account to use the trusted account as a principal (:root)


  Scenario: Elevated privilege due to trusted account
    Given a privileged IAM role in the target (trusting) account
    And a non-privileged IAM role in the attackers (trusted) account
    And the target IAM role has a trust for the :root principal of the attacker account
    When the attacker assumes the privileged role in the target account using their non-privileged role
    Then the attacker successfully assumes the privileged role
    And the attacker gains access to privileged resources in the target account
