# AWS Elastic Compute Cloud (EC2)

Amazon Web Service's virtual computing service.

# See also

* http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html
* http://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_Operations.html
# AWS EC2 Threat Model

# Overview

## Data flow diagram (DFD)

![DFD](dfd.mmd.png)

## Related components

![Components](components.mmd.png)

# Assumptions

* A threat model exists for console and API access to service. This page does not include threat models of the TLS or authentication mechanism of the AWS API itself.
* A threat model exists for the operating system and application stacks. This page does include threat models of for example SSH access or web services that may be running on the EC2 instance.

# Notes

* Attacker can replace AMI ID during instance creation with a malicious one (Tampering)
* Attacker can replace key pair to one they control
* In a shared tenancy environment, attacker is able to escape their guest VM and influence the instance
* In a shared tenancy environment, attacker is able to read sensitive data through the VM host (e.g. CPU cache)
* Flowlog data exposes potentially sensitive metadata about connections
* Attacker is able to restore a snapshot, thereby recovering all the data that is in the snapshot
* Where instances in an AutoScaling Group have been hot-fixed, an attacker is able to revert an instance to an insecure stay using a DoS attack that causes health checks to fail, resulting in the AutoScaling Group removing the current hot-patched instance and replacing it with new un-patched ones.
* Where instances in an AutoScaling Group fail to log to a centralised service, an attacker is able to destroy the logs using a DoS attack that causes health checks to fail, resuling in the AutoScaling Group removing the current instance with all the logs, and replacing it with a new instance without logs.

