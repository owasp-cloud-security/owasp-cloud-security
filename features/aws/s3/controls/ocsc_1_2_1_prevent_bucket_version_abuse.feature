# Id: OCSC-1.2.1
# Status: Confirmed
# Service: AWS S3
# Components:
#   - Versioning
# Mitigates:
#   - OCST-1.2.1

@aws @s3
Feature: Malicious data cannot be hidden inside a bucket
  In order to prevent a spoofing attack
  An an engineer
  I want to prevent malicious files from being hidden within an S3 bucket


  @disabled
  Scenario: Detecting VersionId usage
    Given a bucket with versioning enabled
    And infrequent use of VersionId in GET Object requests
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
