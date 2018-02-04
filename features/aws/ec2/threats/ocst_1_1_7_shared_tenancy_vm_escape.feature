# Id: OCST-1.1.7
# Status: Confirmed
# Service: AWS EC2
# Components:
#   - Hypervisor
# STRIDE:
#   - Information disclosure
# References:
#   - https://www.theverge.com/2018/1/4/16850120/meltdown-spectre-vulnerability-cloud-aws-google-cpu
#   - https://aws.amazon.com/security/security-bulletins/AWS-2018-013/


Feature: Interacting with other instances on the same shared tenancy EC2 host
  In order to access or manipulate data in a target EC2 instance
  As an attacker
  I want the host server to be vulnerable to a vm escape bug


  Scenario: Read data across instances using Meltdown
    Given a target EC2 instance running on an EC2 host machine
    And an attacker instance running on the same host machine
    And the host machine is vulnerable to Meltdown
    When the attacker uses a Meltdown exploit tool on their instance
    Then the attacker can read data from the target instance
