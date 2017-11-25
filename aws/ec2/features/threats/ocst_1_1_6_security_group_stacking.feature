# Id: OCST-1.1.6
# Status: Confirmed
# Service: AWS EC2
# STRIDE:
#   - Tampering
# Components:
#   - Security Groups
#   - Instances
# References:
#   - https://docs.aws.amazon.com/AmazonVPC/latest/UserGuide/VPC_SecurityGroups.html


Feature: Security Group stacking
  In order to gain additional network access
  As an attacker
  I want to be able to attach security groups to running instances


  Scenario: Extend inbound connectivity
    Given an instance with inbound connectivity restricted by security groups
    And an existing security group with weaker access restrictions
    And a principal that can attach security groups to instances
    When the attacker attaches the permissive security group to the instance
    Then the attacker can reach additional network services on the instance


  Scenario: Extend outbound connectivity
    Given an instance with outbound connectivity restricted by security groups
    And an existing security group with weaker access restrictions
    And a principal that can attach security groups to instances
    When the attacker attaches the permissive security group to the instance
    Then the attacker can reach additional network services from the instance
