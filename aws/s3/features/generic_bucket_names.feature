Feature: Sensitive data should not be stored inside a public bucket.
  In order to prevent sensitive information leakage
  As a Security Officer
  I want S3 buckets containing sensitive information to not be public
  
  In order to reduce the chances of discovery of an S3 bucket and prevent sensitive information leakage via their names
  As a Security Officer
  I want the bucket name to be generic
  Mitigating against OCST-1.2.2
  
  Scenario: S3 buckets containing sensitive information should not be public
    Given an S3 bucket
    And the bucket contains sentivite informaiton
    When we look at the permissions
    Then the permissions should not allow public access
    
  Scenario: S3 bucket names should be generic
    Given an S3 bucket
    When we look at the bucket name
    Then it should be generic and should not disclose sensitive information
