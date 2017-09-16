Feature: User data does not contain sensitive information
  In order to prevent an information disclosure attack
  User data
  Must not contain sensitive information 
  Mitigating against OCST-1.1.1

  Scenario: Detecting sensitive information in user data
    When we look at the user data
    Then no sensitive information must be found # E.g. passwords, API keys, private keys, PII

  Scenario: Using a secret managements system
    Given a secrets management system # E.g. KMS, HashiCorp Vault
    When user data needs access to sensitive information
    Then it should retrieve the data it needs at the point of use
