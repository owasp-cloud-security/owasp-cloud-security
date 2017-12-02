# Amazon Web Services

For more information:

* https://aws.amazon.com/

# Unstructured notes

* Permissive Ingress, egress and admin for security groups and NACLs
* Console logs exposed
* Cloudtrail, Cloudwatch and flowlogs not enabled
* Denial of Money due to elasticity
* High application load due to DoS and poor ASG configuration causing continuous rebuilds of instances
* Ephermeral servers with no central logging
* Overly permissive EC2 IAM access
* Reliance on host-based rules, ACLs to filter egress
* Instance uses API keys not assume role/instance profile
* Instance has ability to write to S3 allowing overwriting of build artefacts
* No monitoring of cloudtrail, cloudwatch or flowlogs
* "private" instance placed in a public subnet (e.g. even if behing and ELB)
* EBS not encrypted
* Re-route metadata service IP?
* API limits
* EC2 IAM conditions?
* Brute force IAM user?
* Reuse IAM user password (no MFA)
* Reuse API keys - not rotated
* Unexpected ability to assume an IAM role
* Deleting trails?
* Inherit EIP from previous account
* Attacker can modify tags
* Run command?
