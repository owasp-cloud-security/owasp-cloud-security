# Id: OCSC-1.1.2
# Status: Confirmed
# Service: AWS EC2
# Components:
#   - User Data
# Mitigates:
#   - OCST-1.1.2 


@aws @ec2
Feature: User data is protected by restricted access permissions
  In order to protect User Data from being tampered with
  As an engineer
  I want to sufficiently restrict access permissions to the User Data


  @disabled
  Scenario: Verifying permissions on user data source
    When we look at the user data source permissions
    Then they will only allow authorized entities to make changes to user data


  @disabled
  Scenario: Authorized change to user data is successful
    Given a user data source
    When an authorized enitiy tries to change the content
    Then the user data should be updated


  @disabled
  Scenario: Unauthorized change to user data fails
    Given a user data source
    When an unauthorized entity tries to change the content
    Then the user data is not updated and a permission error occurs
