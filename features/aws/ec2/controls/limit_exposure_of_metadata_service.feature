Feature: Access to the metadata service is restricted
  In order to prevent an information disclosure attack
  The AWS EC2 metadata service
  Must not be exposed outside of the EC2 instance
  Mitigating against OCST-1.1.3

  Scenario: Application is not vulnerable to Server Side Request Forgery
    When we test the application running on EC2
    Then it must not be vulnerable to SSRF
    And the http:/169.254.169.254 host must not be callable through the application
