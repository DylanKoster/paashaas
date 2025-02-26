#!/usr/bin/env python
"""
Parses a SAM template.yaml, searches for any SES EmailIdentity specifications, and configures AWS SES automatically.
"""

import boto3
import yaml
import time

# AWS Clients
ses_client = boto3.client("ses", region_name="us-east-1")
route53_client = boto3.client("route53")

# Constants
TEMPLATE_PATH = "paas-haas/template.yaml"
HOSTED_ZONE_ID = "Z123456789EXAMPLE"  # Replace with actual Route 53 Hosted Zone ID


# Custom YAML tag handlers
def ref_constructor(loader, node):
    return f"REF_{node.value}"


def sub_constructor(loader, node):
    if isinstance(node, yaml.ScalarNode):
        return node.value
    return node.value[0]


def getatt_constructor(loader, node):
    return f"GETATT_{'.'.join(node.value)}"


def load_template(file_path=TEMPLATE_PATH):
    """
    Initialize PyYAML custom constructors and parse the file stored at file_path.
    """
    yaml.add_constructor("!Ref", ref_constructor)
    yaml.add_constructor("!Sub", sub_constructor)
    yaml.add_constructor("!GetAtt", getatt_constructor)

    with open(file_path, "r") as file:
        return yaml.load(file, Loader=yaml.FullLoader)


def setup_ses(template):
    """
    Extract SES configurations and set them up automatically.
    """
    resources = template.get("Resources", {})

    for resource_name, resource in resources.items():
        if resource.get("Type") == "AWS::SES::EmailIdentity":
            email_identity = resource["Properties"]["EmailIdentity"]

            # Step 1: Verify Domain in SES
            response = ses_client.verify_domain_identity(Domain=email_identity)
            verification_token = response["VerificationToken"]
            print(f"SES Domain Verification Token for {email_identity}: {verification_token}")

            # Step 2: Get DKIM Records
            dkim_response = ses_client.verify_domain_dkim(Domain=email_identity)
            dkim_tokens = dkim_response["DkimTokens"]

            # Step 3: Add DNS Records to Route 53
            dns_changes = [
                {
                    "Action": "UPSERT",
                    "ResourceRecordSet": {
                        "Name": f"_amazonses.{email_identity}",
                        "Type": "TXT",
                        "TTL": 300,
                        "ResourceRecords": [{"Value": f'"{verification_token}"'}],
                    },
                }
            ]

            for token in dkim_tokens:
                dns_changes.append(
                    {
                        "Action": "UPSERT",
                        "ResourceRecordSet": {
                            "Name": f"{token}._domainkey.{email_identity}",
                            "Type": "CNAME",
                            "TTL": 300,
                            "ResourceRecords": [{"Value": f"{token}.dkim.amazonses.com"}],
                        },
                    }
                )

            # Apply DNS changes
            route53_client.change_resource_record_sets(
                HostedZoneId=HOSTED_ZONE_ID,
                ChangeBatch={"Changes": dns_changes},
            )
            print(f"DNS records added for {email_identity}. Waiting for verification...")

            # Step 4: Wait for Verification
            while True:
                verification_status = ses_client.get_identity_verification_attributes(
                    Identities=[email_identity]
                )["VerificationAttributes"].get(email_identity, {}).get("VerificationStatus", "Pending")

                print(f"Verification Status: {verification_status}")

                if verification_status == "Success":
                    print(f"Domain {email_identity} successfully verified!")
                    break

                time.sleep(30)  # Wait before checking again


if __name__ == "__main__":
    template_data = load_template()
    setup_ses(template_data)
