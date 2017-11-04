Feature: Threat YAML files
  In order to improve collaboration
  As an OWASP Cloud Security project contributor
  I want the threat YAML files to be well structured

  Background: Locating and loading the threat YAML file
    Given the filename in the "OCST_FILE" environment variable
    And the yaml file has been loaded

  Scenario: Threat files live inside a threats directory for each service
    Then the parent directory must be "threats"

  Scenario: Threat files follow a pattern that includes the OCST id and a brief summary
    Then the file must match the pattern "^(?P<ocst_id>ocst_\d{1,3}_\d{1,3}_\d{1,3})(?P<name>[a-z0-9_]{0,40})\.yaml$"

  Scenario: The OCST id field is used as a unique reference for each threat
    Then the "id" field must exist
    And the "id" field must be a "string"
    And the "id" field must match the pattern "^OCST-(?P<provider_id>\d+)\.(?P<service_id>\d+)\.(?P<threat_id>\d+)$"
    And the id must be the same as the filename id

  Scenario: A short but descriptive name must be given
    Then the "name" field must exist
    And the "name" field must be a "string"
    And the "name" field must match the pattern "^(?P<name>[a-zA-Z0-9\ ]{10,80})$"

  Scenario: A longer description should explain the threat fully
    Then the "description" field must exist
    And the "description" field must be a "string"
    And the "description" field length must be greater than or equal to "200" characters

  Scenario: The status field describes the maturity of the threat
    Given the set of allowed values
      | value       | description                                                        |
      | Unconfirmed | A theoretical threat that requires further research                |
      | Confirmed   | A threat that has been confirmed through research or documentation |
      | Exploited   | A threat that also includes proof of concept exploitation code     |
    Then the "status" field must exist
    And the "status" field must be a "string"
    And the "status" field must be one of the allowed values

  Scenario: STRIDE is used to identify related threats by threat type
    Given the set of allowed values
      | value                  |
      | Spoofing               |
      | Tampering              |
      | Repudiation            |
      | Information disclosure |
      | Denial of service      |
      | Elevation of privilege |
    Then the "stride" field must exist
    And the "stride" field must be a "list"
    And the "stride" field must be one or more of the allowed values

  Scenario: The service is captured so that the threat can be related to other threats for the same service
    Then the "service" field must exist
    And the "service" field must be a "string"
    And the "service" field must match the pattern "^(?P<provider>[a-zA-Z0-9]{2,10}) (?P<service>[a-zA-Z0-9]{2,10})$"

  Scenario: The service components are captured so that the threat can be related to other services with related components
    Then the "components" field must exist
    And the "components" field must be a "list"

  Scenario: Mitigations are actionable and testable BDD features
    Then the "mitigations" field must exist
    And the "mitigations" field must be a "list"
    #And each "mitigations" value must match the pattern "^(?P<path>[a-zA-Z0-9\/\_]+)/features/(?P<file>[a-zA-Z0-9\_]+\.feature)$"

  Scenario: Documentation, standards and credit must be referenced
    Then the "references" field must exist
    And the "references" field must be a "list"


