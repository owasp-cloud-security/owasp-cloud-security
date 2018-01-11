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
  I want the target to use AWS managed policies in their IAM roles


  Scenario: AWS ManagedPolicies are used
    Given an IAM role that uses AWS managed policies
    And a principal with access to that role
    When AWS adds additional privileged actions to the managed policies
    And the added actions become available to users of the role
    Then the attacker principal uses the role
    And can use the additional permissions to gain more access to resources
