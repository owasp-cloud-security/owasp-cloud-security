# Id: OCST-1.3.1
# Service: AWS IAM
# Status: Confirmed
# STRIDE:
#   - Information disclosure
#   - Elevation of privilege
# Components:
#   - IAM user
#   - Access Key
# References:
#   - https://docs.aws.amazon.com/general/latest/gr/managing-aws-access-keys.html
#   - https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html#lock-away-credentials


Feature: Unprotected access keys
  In order to gain additional access to resources
  As an attacker
  I want to find unprotected API access keys


  Scenario Outline: Finding exposed keys
    Given a principal with existing API access keys
    And a <storage-system>
    When the user stores their access keys in the <storage-system>
    And the attacker scans the <storage-system> for access keys
    Then the attacker finds the access keys
    And the attacker can use the access keys to access resources in the target account

    Examples: Non-exhaustive list of possible storage systems
      | storage-system                        |
      | S3 bucket                             |
      | Git repository                        |
      | Filesystem with weak protection       |
      | Wiki or documentation system          |
      | Email or other communication platform |


  Scenario: Finding globally exposed access keys
    Given a principal with existing API access keys
    And a world-readable global storage system
    And the fact that API keys can be used from anyway, even outside of the account
    When the user stores their access keys in the global storage system
    And teh attacker scans the storage system for access keys
    Then the attacker finds the access keys
    And the attacker can use the access keys to access resources in the target account from outside the target
