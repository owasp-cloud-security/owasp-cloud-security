# AWS EC2 Threat Model

# Overview

## Data flow diagram (DFD)

![DFD](dfd.mmd.png)

## Related components

![Components](components.mmd.png)

## References

* http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html
* http://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_Operations.html

# Assumptions

* A threat model exists for console and API access to service. This page does not include threat models of the TLS or authentication mechanism of the AWS API itself.
* A threat model exists for the operating system and application stacks. This page does include threat models of for example SSH access or web services that may be running on the EC2 instance.

# Threats

* Userdata contains sensitive data and is world readable. E.g. API keys, passwords. (Information Disclosure)
* Weak file permssions on Userdata script allowing attacker to add malicious commands. (Tampering)
* Metadata service is exposed via Server Side Request Forgery (SSRF) - See https://blog.christophetd.fr/abusing-aws-metadata-service-using-ssrf-vulnerabilities/ (Information Disclosure)
* Attacker can replace AMI ID during instance creation with a malicious one (Tampering)
* Attacker can write to S3 or other asset data stores used during instance configuration, replacing valid files with malicious ones (Tampering)
* Attacker can create a similarly named or tagged instance which is included in a search. For example, the attacker creates an instance with the tag "Name:WebService" that runs a modified sshd that collects usernames and passwords. A user ssh'es  to each "Name:WebService" instance, including the attackers thereby exposing the user's credentials. (Information Disclosure)
* Attacker can replace key pair to one they control
* Attacker is able to attach additional Securit Groups exposing the instance to other network sources
* In a shared tenancy environment, attacker is able to escape their guest VM and influence the instance
* In a shared tenancy environment, attacker is able to read sensitive data through the VM host (e.g. CPU cache)
* Flowlog data exposes potentially sensitive metadata about connections
* Attacker is able to restore a snapshot, thereby recovering all the data that is in the snapshot
