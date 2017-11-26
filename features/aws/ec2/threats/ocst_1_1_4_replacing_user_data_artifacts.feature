# Id: OCST-1.1.4
# Status: Confirmed
# Service: AWS EC2
# STRIDE:
#   - Tampering
#   - Elevation of privilege
# Components:
#   - User Data
# References:
#   - https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html


Feature: Replacing user data artifacts
  In order to run arbitrary code on EC2 instances at build time
  As an attacker
  I want to replace user data atrifacts with ones I control


  Scenario Outline: Files stored in a repository
    Given a <repository> containing build artifacts
    And a principal with the permission to write to the <repository>
    And a user data script that pulls down and executes artifacts in the <repository>
    When I replace an existing artifact stored in the <repository> with a malicious one
    Then the malicious code will execute the next time an EC2 instance is created 

    Examples: Non-exhaustive list of possible repository types
      | repository            | description                           |
      | s3 bucket             | Amazons general-use object storage    |
      | YUM package mirror    | RHEL/CenOS .rpm packages              |
      | Debian package mirror | Debian .deb packages                  |
      | NPM                   | Node.js software repository           |
      | Commercial repo       | Any commmercial software/package repo |
