# Id: OCST-1.3.4
# Status: Confirmed
# Service: AWS IAM
# STRIDE:
#   - Elevation of privilege
# Components:
#   - IAM User
#   - Account Password Policy
# References:
#   - https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_passwords_account-policy.html


Feature: Weak password policy
  In order to get access to a console users account
  As an attacker
  I want the account to have a weak password policy


  Scenario:
    Given an account with a weak IAM password policy set
    And a user that have weak passwords permitted by the policy
    When the attacker tries to guess the password
    Then the attacker successfully finds the password
    And the attacker logs in to the account as the user
