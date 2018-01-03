# Id: OCSC-1.1.1
# Status: Confirmed
# Service: AWS EC2
# Components:
#   - User Data
# Mitigates:
#   - OCST-1.1.1


@aws @ec2
Feature: User Data does not contain sensitive information
  In order to prevent exposure of sensitive or proprietary information
  As an engineer
  I want to avoid putting sensitive information in User Data


  @disabled
  Scenario Outline: Detecting sensitive information via lambda
    Given a lambda function triggered by CloudFormation stack creation
    When a new stack is created
    And the lambda function searches the stack's User Data for <data-type>
    Then no sensitive information should be found

    Examples: Data types
      | data-type         |
      | password          |
      | API key           |
      | X.509 private key |
      | SSH private key   |
      | Internal URL      |


  @disabled
  Scenario Outline: Verifying the point-in-time use of a secrets managements system
    Given a <secrets-management> system
    And a lambda function triggered by CloudFormation stack creation
    When a new stack is created
    And the lambda function search the stack's User Data for use of the <secrets-management> system
    Then a point-in-time use should be found

    Examples: Secrets management system
      | secrets-management |
      | AWS KMS            |
      | Hashicorp Vault    |
      | Keywhiz            |
