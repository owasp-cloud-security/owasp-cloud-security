# Id: OCST-1.3.7
# Status: Confirmed
# Service: AWS IAM
# Components:
#   - IAM AssumeRole
#   - Principals
# STRIDE:
#   - Elevation of privilege
# References:
#   - https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements.html
#   - http://docs.aws.amazon.com/AmazonS3/latest/dev/s3-bucket-user-policy-specifying-principal-intro.html


Feature: Use of wildcard principals
  In order to gain access to resources in the target account
  As an attacker
  I want the target to use wildcard ("*") principals in their roles


  Scenario:
    Given an IAM role in the target account
    And the IAM role allows access using the wildcard ("*") principal
    And there are insufficient conditions to restrict access
    And a principal outside of the target account that the attacker controls
    When the attacker uses the target role from their role outside the account
    Then the attacker gains access to the resources defined in the target role
    
