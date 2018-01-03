# Id: OCSC-1.1.3
# Status: Confirmed
# Service: AWS EC2
# Components:
#   - Metadata service
# Mitigates:
#   - OCST-1.1.3


@aws @ec2
Feature: Access to the metadata service is restricted
  In order to prevent an information disclosure attack
  As an engineer
  I want to ensure that the metadata service is not be exposed outside of the EC2 instance


  @disabled
  Scenario: Application is protected against Server Side Request Forgery
    Given an EC2 instance with access to the metadata service
    And an application running on the instance
    When we inject a request to the http:/169.254.169.254 metadata service URL
    Then the application must not call the provided metadata service URL
    And the application must not return any results of a call to the metadata service
