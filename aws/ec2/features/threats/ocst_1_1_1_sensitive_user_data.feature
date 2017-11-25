# Id: OCST-1.1.1
# Status: Confirmed
# Service: AWS EC2
# Components:
#   - User Data
# STRIDE:
#   - Elevation of privilege
#   - Information disclosure
# References:
#   - https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html


Feature: User Data contains sensitive information
  In order to obtain sensitive information about the target
  As an attacker
  I want the target to have inappropriately placed sensitive information in User Data that I can access


  Scenario Outline: Access via instance attribute
    Given an instance with sensitive information in the User Data attribute
    And a principal with the ability to read the instance attributes
    When the attacker searches the User Data for the "<data-type>"
    Then the sensitive information is returned to the attacker

    Examples: Data types
      | data-type         |
      | password          |
      | API key           |
      | X.509 private key |
      | SSH private key   |
      | Internal URL      |


  Scenario: Access via CloudFormation
    Given an instance built using CloudFormation
    And a principal with the ability to read CloudFormation templates
    When the attacker searches the CloudFormation templates
    Then the sensitive information is returned to the attacker


  Scenario: Access via AutoScaling LaunchConfiguration
    Given an instance built inside an Autoscaling group
    And a principal with the ability to read Autoscaling launch configurations
    When the attacker searches the launch configurations
    Then the sensitive information is returned to the attacker
