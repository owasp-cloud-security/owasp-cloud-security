# AWS Simple Storage Service (S3)

Amazon Web Service's highly-scalable object storage.

# See also

* https://aws.amazon.com/s3/
* https://docs.aws.amazon.com/IAM/latest/UserGuide/list_s3.html
# AWS S3 Threat Model

# Overview

## Data flow diagram (DFD)

![DFD](dfd.mmd.png)

## Related components

![Components](components.mmd.png)

# Assumptions

* A threat model exists for console and API access to service. This page does not include threat models of the TLS or authentication mechanism of the AWS API itself.
# Threats

## OCST-1.2.1
### Name
Hiding malicious data within object version history
### Description
An attacker can hide a malicious file in the version history of a
benign object and can later reference that file using the VersionId
and a PreSigned URL.

### Service
AWS S3
### Status
Exploited
### Stride
* Spoofing
### Components
* Bucket versioning
### Mitigations
* [aws/s3/features/prevent_bucket_version_abuse.feature](https://github.com/owasp-cloud-security/owasp-cloud-security/blob/master/aws/s3/features/prevent_bucket_version_abuse.feature)
### References
* http://docs.aws.amazon.com/AmazonS3/latest/dev/Versioning.html
* aws/s3/tools/s3bury

