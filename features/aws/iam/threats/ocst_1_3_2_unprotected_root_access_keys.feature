# Id: OCST-1.3.2
# Status: Confirmed
# Service: AWS IAM
# STRIDE:
#   - Information disclosure
#   - Elevation of privilege
# Components:
#   - IAM User
#   - Access Key
#   - AWS Account (root user)
# References:
#   - https://docs.aws.amazon.com/general/latest/gr/managing-aws-access-keys.html
#   - https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html#lock-away-credentials


Feature: Unprotected root access keys
  In order to gain complete access to all resources in an account
  As an attacker
  I want to find unprotected root API access keys


  Scenario Outline: Finding exposed root access keys
    Given the root principal with existing API access keys
    And a <storage-system>
    When the user stores the root access keys in the <storage-system>
    And the attacker scans the <storage-system> for access keys
    Then the attacker finds the root access keys
    And the attacker can use the root access keys to access all resources in the target account
    And the access includes billing information
    And the access is completely unrestricted
  

    Examples: Non-exhaustive list of possible storage systems
      | storage-system                        |
      | S3 bucket                             |
      | Git repository                        |
      | Filesystem with weak protection       |
      | Wiki or documentation system          |
      | Email or other communication platform |


  Scenario: Finding globally exposed root access keys
    Given the root principal with existing API access keys
    And a world-readable global storage system
    And the fact that API keys can be used from anyway, even outside of the account
    When the user stores the root access keys in the global storage system
    And teh attacker scans the storage system for access keys
    Then the attacker finds the root access keys
    And the attacker can use the access keys to access all resources in the target account
    And the access includes billing information
    And the access is completely unrestricted

