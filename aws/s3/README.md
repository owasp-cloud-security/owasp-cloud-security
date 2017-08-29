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

* An attacker can hide a malicious file in the version history of a benign object and can later reference that file using the VersionId.
* Attacker can create an object version history with millions of objects resulting in 503 "Slow Down" errors for PUT and DELETE object actions on the bucket, effectively causing a denial of service.
* An attacker can update or manipulate object tags which affects business logic that relies on those tags (e.g. IAM permissions to read only objects with the specific tags).
* Object tags contain sensitive information (e.g. PII)
* Bucket names are globally namespaced, so an attacker can do typo-squatting or hijack deleted bucket names.
* Creating objects with non-printable characters in the object key results in strange effects in the AWS console, including the apparent rendering of only a subset of the available pages.
* An attacker can determine whether an object exists for a bucket that has website enabled by looking for 403 errors which are returned if the object exists, and 404 if the object does not exist, regardless of the attackers ACL/IAM permissions.
* Due to the nature of S3 log delivery, there is no way to know whether all logs have been delivered to a bucket, leading to a potential repudation attack window.
* "Can affect destination log bucket to turn off logging, eg. object ACL" - not sure what I meant here in my notes
* Attacker can edit CORS configuration to allow code injection from a malicious website.
* Logging bucket is world-readable.
* A bucket owner can delete an object regardless of object ACL, allowing for possible denial of service if the attack can become the bucket owner.
* Sensitive date is stored unencrypted in buckets leading to potential information disclosure.
* Buckets containing private or proprietary data are accidentally made public.
* An attacker can over-write code/build artifacts stored in an S3 buckets leading to code execution on the destination system.
* An attacker can set a website redirect rule for an object path to arbitrarily redirect a file to on the attacker controls.
* An attack with bucket owner permissions can delete an object (bypassing the object ACL) and set a 404 redirect to a malicious version.
* Attacker can create a lambda to remove their logs from a logging destination bucket triggered by an object creation event during a given time window.
* A lack of centralised or automated pipelines leads to inconsistencies between the bucket policies for different buckets across the organisation, resulting in some buckets having poorly configured bucket policies.
