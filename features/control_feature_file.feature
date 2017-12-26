@ocsc
Feature: Control feature files
  In order to improve collaboration
  As an OWASP Cloud Security project contributor
  I want the control feature files to contain the necessary metadata


  Background: Locating and loading the control feature file
    Given the filename in the "OCSC_FILE" environment variable
    And the control feature file has been loaded


  Scenario: Control files live inside a controls directory for each service
    Then the parent directory must be "controls"


  Scenario: Control files follow a pattern that includes the OCSC Id and a brief summary
    Then the file must match the pattern "^(?P<ocsc_id>ocsc_\d{1,3}_\d{1,3}_\d{1,3})(?P<name>[a-z0-9_]{0,50})\.feature$"


  Scenario: The OCSC Id field is used as a unique reference for each control
    Then the "Id" field must exist
    And the "Id" field must be a "string"
    And the "Id" field must match the pattern "^OCSC-(?P<provider_id>\d+)\.(?P<service_id>\d+)\.(?P<control_id>\d+)$"
    And the Id must be the same as the filename Id


  Scenario: A short but descriptive name must be given
    Then the "Name" field must exist
    And the "Name" field must be a "string"
    And the "Name" field must match the pattern "^(?P<name>[a-zA-Z0-9\ ]{10,80})$"


  Scenario: The status field describes the maturity of the control
    Given the set of allowed values
      | value       | description                                                         |
      | Unconfirmed | A theoretical control that requires further research                |
      | Confirmed   | A control that has been confirmed through research or documentation |
      | Mitigated   | A control that also includes proof of concept mitigation   code     |
    Then the "Status" field must exist
    And the "Status" field must be a "string"
    And the "Status" field must be one of the allowed values


  Scenario: The service is captured so that the control can be related to other controls for the same service
    Then the "Service" field must exist
    And the "Service" field must be a "string"
    And the "Service" field must match the pattern "^(?P<provider>[a-zA-Z0-9]{2,10}) (?P<service>[a-zA-Z0-9]{2,10})$"


  Scenario: The service components are captured so that the control can be related to other services with related components
    Then the "Components" field must exist
    And the "Components" field must be a "list"


  Scenario: The story is captured
    Then the "Story" field must exist
    And the "Story" field must be a "string"
