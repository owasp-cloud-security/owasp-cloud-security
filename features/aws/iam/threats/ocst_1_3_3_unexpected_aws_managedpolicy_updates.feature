# Id: OCST-1.3.3
# Status: Confirmed
# Service: AWS IAM
# STRIDE: 
#   - Elevation of privilege
# Components:
#   - IAM ManagedPolicy
# References:
#   - https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_managed-vs-inline.html


Feature: Unexpected AWS ManagedPolicy updates 
  In order to automatically gain access to new resources when AWS releases new services and functionality
  As an attacker
  I want the target to use AWS managed policies


  Scenario: AWS ManagedPolicies are used
    Given an IAM role that uses AWS managed policies
    And a principal with access to that role
    When AWS adds additional actions to the managed policies
    Then the attacker uses the new actions and gains additional permissions to resources
