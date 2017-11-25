Feature: User data is protected by restricted access permissions
  In order to prevent a tampering attack
  User data
  Must be protected with sufficiently restricted access permissions
  Mitigating against OCST-1.1.2

  Scenario: Verifying permissions on user data source
    When we look at the user data source permissions
    Then they will only allow authorized entities to make changes to user data

  Scenario: Authorized change to user data is successful
    Given a user data source
    When an authorized enitiy tries to change the content
    Then the user data should be updated

  Scenario: Unauthorized change to user data fails
    Given a user data source
    When an unauthorized entity tries to change the content
    Then the user data is not updated and a permission error occurs
    
  
