# Id: OCST-1.1.8
# Status: Confirmed
# Service: AWS EC2
# Components:
#   - EBS
#   - Snapshots
# STRIDE:
#   - Information disclosure
# References:


Feature: Restoring a snapshot that contains sensitive information
  In order to retrieve sensitive instance data
  As an attacker
  I want to restore snapshots into an instance I control


  Scenario: Restoring a snapshot
    Given an EBS snapshot for an instance containing sensitive information
    And an instance that the attacker controls
    And a principal with the allowed permissions needed to read and restore snapshots
      | action                | description                                 |
      | ec2:DescribeSnapshots | Get a list and details of the available snapshots |
      | ec2:CreateVolume      | Creates a new volume from the snapshot            |
      | ec2:AttachVolume      | Attach the new volume to the EC2 instance         |
    When the attacker restores the snapshot to the instance
    And the attacker searches the snapshot filesystem for interesting data
      | data         |
      | credentials  |
      | private keys |
      | log files    |
    Then the sensitive information is returned to the attacker
