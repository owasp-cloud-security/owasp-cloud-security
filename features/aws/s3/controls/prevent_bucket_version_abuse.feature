@wip @aws @s3
Feature: Malicious data cannot be hidden inside a bucket
  In order to prevent a spoofing attack
  An attacker
  Must not be able to hide malicious data within an S3 bucket
  Mitigating against OCST-1.2.1

  @disabled
  Scenario: Detecting VersionId usage
    Given a bucket with versioning enabled
    And rare use of VersionId in GET Object requests
    When a GET Object request is made with VersionId as a parameter
    Then an alert should be generated

  @disabled
  Scenario: Prevent unauthorized users writing to a bucket
    Given a bucket
    And the list of permitted write actions
    And the list of authorized IAM principals
    And the list of all IAM entities
    When we simulate the write actions for each IAM principal
    Then only the authorized principals should allowed responses
    
    
