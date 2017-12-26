@ocst
Feature: Threat feature files
  In order to improve collaboration
  As an OWASP Cloud Security project contributor
  I want the threat feature files to contain the necessary metadata


  Background: Locating and loading the threat feature file
    Given the filename in the "OCST_FILE" environment variable
    And the threat feature file has been loaded


  Scenario: Threat files live inside a threats directory for each service
    Then the parent directory must be "threats"


  Scenario: Threat files follow a pattern that includes the OCST Id and a brief summary
    Then the file must match the pattern "^(?P<ocst_id>ocst_\d{1,3}_\d{1,3}_\d{1,3})(?P<name>[a-z0-9_]{0,50})\.feature$"


  Scenario: The OCST Id field is used as a unique reference for each threat
    Then the "Id" field must exist
    And the "Id" field must be a "string"
    And the "Id" field must match the pattern "^OCST-(?P<provider_id>\d+)\.(?P<service_id>\d+)\.(?P<threat_id>\d+)$"
    And the Id must be the same as the filename Id


  Scenario: A short but descriptive name must be given
    Then the "Name" field must exist
    And the "Name" field must be a "string"
    And the "Name" field must match the pattern "^(?P<name>[a-zA-Z0-9\ ]{10,80})$"


  Scenario: The status field describes the maturity of the threat
    Given the set of allowed values
      | value       | description                                                        |
      | Unconfirmed | A theoretical threat that requires further research                |
      | Confirmed   | A threat that has been confirmed through research or documentation |
      | Exploited   | A threat that also includes proof of concept exploitation code     |
    Then the "Status" field must exist
    And the "Status" field must be a "string"
    And the "Status" field must be one of the allowed values


  Scenario: STRIDE is used to identify related threats by threat type
    Given the set of allowed values
      | value                  |
      | Spoofing               |
      | Tampering              |
      | Repudiation            |
      | Information disclosure |
      | Denial of service      |
      | Elevation of privilege |
    Then the "STRIDE" field must exist
    And the "STRIDE" field must be a "list"
    And the "STRIDE" field must be one or more of the allowed values


  Scenario: The service is captured so that the threat can be related to other threats for the same service
    Then the "Service" field must exist
    And the "Service" field must be a "string"
    And the "Service" field must match the pattern "^(?P<provider>[a-zA-Z0-9]{2,10}) (?P<service>[a-zA-Z0-9]{2,10})$"


  Scenario: The service components are captured so that the threat can be related to other services with related components
    Then the "Components" field must exist
    And the "Components" field must be a "list"


  Scenario: The story is captured
    Then the "Story" field must exist
    And the "Story" field must be a "string"


  Scenario: Documentation, standards and credit must be referenced
    Then the "References" field must exist
    And the "References" field must be a "list"


