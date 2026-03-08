import boto3
from typing import Any, Dict, List, Optional


class AWSEvidenceCollector:
    def __init__(self, region_name: str = "us-east-1"):
        self.iam = boto3.client("iam", region_name=region_name)
        self.cloudtrail = boto3.client("cloudtrail", region_name=region_name)
        self.config = boto3.client("config", region_name=region_name)

    def get_iam_policies(self) -> List[Dict[str, Any]]:
        response = self.iam.list_policies(Scope="Local")
        return response.get("Policies", [])

    def get_iam_policy_document(self, policy_arn: str) -> Optional[Dict[str, Any]]:
        policy = self.iam.get_policy(PolicyArn=policy_arn)
        default_version_id = policy["Policy"]["DefaultVersionId"]

        version = self.iam.get_policy_version(
            PolicyArn=policy_arn,
            VersionId=default_version_id,
        )

        return version["PolicyVersion"]["Document"]

    def get_cloudtrail_events(self) -> List[Dict[str, Any]]:
        response = self.cloudtrail.lookup_events(MaxResults=10)
        return response.get("Events", [])

    def get_config_compliance(self) -> List[Dict[str, Any]]:
        response = self.config.describe_compliance_by_resource()
        return response.get("ComplianceByResources", [])
