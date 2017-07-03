# Amazon Web Services - Elastic Compute Cloud - Threat Model

# Overview

## Data flow diagram (DFD)

![DFD](dfd.mmd.png)

## Related components

* Elastic IPs
* Availability Zones
* Security groups
* Scheduled events
* AMIs
* IAM Role (Instance profile)
* Key pair
* VPC
* Network interface
* Public IPs
* Private IPs
* Elastic IPs
* Subnets
* EBS volumes
* Tags
* Tenancy
* CloudWatch
* CloudTrail
* Flowlog

## References

* http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html
* http://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_Operations.html

# Assumptions

* A threat model exists for console and API access to service. This page does not include threat models of the TLS or authentication mechanism of the AWS API itself.
* A threat model exists for the operating system and application stacks. This page does include threat models of for example SSH access or web services that may be running on the EC2 instance.

# Threats
