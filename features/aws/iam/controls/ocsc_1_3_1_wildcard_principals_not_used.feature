# Id: OCSC-1.3.1
# Status: Confirmed
# Service: AWS IAM
# Components:
#   - IAM Principal
# Mitigates:
#   - OCST-1.3.7


@aws @iam
Feature: Wildcard principals are not used
  In order to prevent an elevation of privilege attack
  As an engineer
  I want to ensure that wildcard ("*") principals are never used


  @disabled
  Scenario: Detecting wildcard principals
    Given the list of all IAM policies
    When we look at all principals in each policy
    Then no principals should be the wildcard principal
