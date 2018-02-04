# Id: OCST-1.2.2
# Status: Exploited
# Service: AWS S3
# STRIDE:
#   - Information disclosure
# Components:
#   - Objects
#   - Bucket policies
#   - ACLs
# References:
#   - https://blog.rapid7.com/2013/03/27/open-s3-buckets/
#   - https://digi.ninja/blog/analysing_amazons_buckets.php


Feature: S3 buckets containing proprietry or sensitive information are public
  In order to get access to secret, sensitive or customer data
  As an attacker
  I want companies to accidentally make private S3 buckets public

  
  Scenario: Discovering public buckets using Bucket Finder
    Given an S3 bucket containing sensitive information
    And the bucket has a predictable global name
    And a wordlist of possible bucket names
    When Bucket Finder is executed using the wordlist
    Then the public bucket is found
    And the contents is available to download
