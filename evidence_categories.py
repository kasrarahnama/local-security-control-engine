from __future__ import annotations

from typing import Dict, Any


EVIDENCE_CATEGORIES: Dict[str, Dict[str, Any]] = {
    "SCP": {
        "description": "Service Control Policies enforcing organization-wide restrictions",
        "examples": [
            "Deny unapproved AWS regions",
            "Deny disabling CloudTrail",
            "Deny creation of unrestricted IAM policies",
        ],
    },
    "IAM_POLICY": {
        "description": "IAM policies enforcing least privilege access",
        "examples": [
            "Read-only access policy",
            "Restricted admin policy",
            "Application role policy with scoped permissions",
        ],
    },
    "AWS_CONFIG": {
        "description": "AWS Config rules validating security configuration state",
        "examples": [
            "S3 bucket encryption enabled",
            "CloudTrail enabled",
            "Security groups do not allow unrestricted access",
        ],
    },
    "CLOUDTRAIL": {
        "description": "Audit logs capturing AWS API activity and management events",
        "examples": [
            "IAM policy changes",
            "Console login activity",
            "Changes to Config rules or CloudTrail settings",
        ],
    },
    "FLOW_LOGS": {
        "description": "VPC Flow Logs providing evidence of network traffic patterns",
        "examples": [
            "Traffic between application and database",
            "Blocked unauthorized network paths",
            "Unexpected inbound or outbound connections",
        ],
    },
}