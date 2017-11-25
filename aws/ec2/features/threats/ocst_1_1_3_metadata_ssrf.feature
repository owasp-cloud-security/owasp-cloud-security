# Id: OCST-1.1.3
# Status: Confirmed
# Service: AWS EC2
# Components:
#  - Metadata
# STRIDE:
# - Information disclosure
# References:
#  - https://blog.christophetd.fr/abusing-aws-metadata-service-using-ssrf-vulnerabilities/
#  - https://www.owasp.org/index.php/Server_Side_Request_Forgery
#  - https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-metadata.html


Feature: Metadata Server Side Request Forgery
  In order to get access to data about the EC2 instances and AWS environment
  As an attacker
  I want to access the AWS metadata service via a server side request forgery attack


  Background:
    Given a service running on EC2
    And the service is vulnerable to Server Side Request Forgery


  Scenario: Getting the AMI Id
    When the attacker injects a request to http://169.254.169.254/latest/meta-data/ami-id
    Then the AMI Id of the instance is returned


  Scenario: Getting the security credentials
    When the attacker injects a request to http://169.254.169.254/latest/meta-data/iam/security-credentials/ROLE_NAME
    Then the temporary security credentials for ROLE_NAME are returned


  Scenario: Getting the user data
    When the attacker injects a request to http://169.254.169.254/latest/user-data/
    Then the user data for the instance is returned
