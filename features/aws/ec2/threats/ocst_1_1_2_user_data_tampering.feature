# Id: OCST-1.1.2
# Status: Confirmed
# Service: AWS EC2
# Components:
#   - User Data
# STRIDE:
#   - Tampering
#   - Elevation of privilege
# References:
#   - https://docs.aws.amazon.com/autoscaling/latest/userguide/LaunchConfiguration.html
#   - https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html


Feature: Tampering of User Data
  In order to run arbitrary code on EC2 instances at build time
  As an attacker
  I want to tamper with User Data


  Scenario: Updating Auto Scaling launch configurations
    Given one or more existing Auto Scaling launch configurations
    And a principal with the ability to update launch configurations
    When the attacker adds malicious code to the launch configuration user data
    Then the malicious code will execute the next time an EC2 instance is created in the Auto Scaling group


  Scenario: Insufficiently protected user data script file
    Given a user data script stored as a file on a filesystem
    And a user with the ability to write to the user data script file
    When the attacker adds malicious code to the user data script
    Then the malicious code will execute when the user data script is used in the AWS account
    

  Scenario: Unprotected CI/CD job
    Given a CI/CD job that processes user data
    And a user with the ability to update the CI/CD job
    When the attacker updates the job to inject malicious code into the user data
    Then the malicious code will execute when the CI/CD job deploys the user data to the AWS account
