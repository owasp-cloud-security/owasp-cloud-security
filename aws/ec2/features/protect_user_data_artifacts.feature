Ensure all external artifacts used by a User Data script are sufficiently protected

Feature: Artifacts used by user data are protected
  In order to prevent a tampering and an information disclosure attack
  Artifacts used by AWS EC2 user data
  Must be protected from tampering
  Mitigating against OCST-1.1.4

  Scenario: 
    When we look at the permissions of all the artifacts used by user data # e.g. rpm or deb files
    Then only authorised entities are able to update them
