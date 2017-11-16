Feature: User data does not contain sensitive information
  In order to prevent an information disclosure attack
  User data
  Must not contain sensitive information 
  Mitigating against OCST-1.1.1

  @disabled
  Scenario: Detecting sensitive information via lambda
    Given the classification of sensitive information in sensitive_info.yaml
    And a lambda function triggered by CloudFormation stack creation
    When a new stack is created
    Then the lambda function should not find any sensitive information in the user data of the stack

  @disabled
  Scenario: Using a secrets managements system
    Given a secrets management system # E.g. KMS, HashiCorp Vault
    And a lambda function triggered by CloudFormation stack creation
    When a new stack is created
    Then the lambda function should find the secrets management client at the point of use
