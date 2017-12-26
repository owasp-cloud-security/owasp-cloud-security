# Id: OCSC-1.1.4
# Status: Confirmed
# Service: AWS EC2
# Components:
#   - User Data
# Mitigates:
#   - OCST-1.1.4


@aws @ec2
Feature: Artifacts used by user data are protected
  In order to prevent a tampering or an information disclosure attack
  As an engineer
  I want all artifacts used in the AWS EC2 user data to be protected from tampering


  @disabled
  Scenario: Only authorized users can overwrite artifacts
    Given a User Data script that downloads artifacts from an artifact repository
    When we look at the permissions of all the artifacts used by the User Data
    Then only authorised entities are able to overwrite the artifacts
