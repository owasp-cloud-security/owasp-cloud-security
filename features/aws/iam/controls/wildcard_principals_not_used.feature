@wip @aws @iam
Feature: Wildcard principals are not used
  In order to prevent an elevation of privilege attack
  IAM Policies
  Must not use wildcard ("*") principals
  Mitigating against OCST-1.3.8

  @disabled
  Scenario: Detecting wildcard principals
    Given the list of all IAM policies
    When we look at all principals in each policy
    Then no principals should be the wildcard
