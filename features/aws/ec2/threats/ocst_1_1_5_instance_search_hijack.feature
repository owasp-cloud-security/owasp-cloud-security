# Id: OCST-1.1.5
# Status: Confirmed
# Service: AWS EC2
# STRIDE:
#   - Spoofing
# Components:
#   - Instances
#   - Tagging
# References:
#   - https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html


Feature: Instance search hijack
  In order to spoof existing instances
  As an attacker
  I want manipulate instance search results to include an instance I control


  Scenario: Name tag search
    Given an existing set of instances with consistent and shared Name tags
    And a principal with the ability to set the Name tag on a malicious instance
    When the attacker sets the Name tag on the malicious instance to match those of the target instance
    And a user searches for instances based on the Name tag
    Then the malicious instance will be included in the search results
    

  Scenario: A malicious SSH daemon
    Given a successful search injection
    And a malicious instance running an SSH daemon that captures credentials
    When the user SSH's into the found malicious instance using a username and password
    Then the attacker will have access to the user's credentials
