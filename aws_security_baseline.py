AWS_SECURITY_BASELINE = {

    "multi_account_required": True,

    "expected_accounts": [
        "security",
        "logging",
        "workload"
    ],

    "guardrails": [
        "scp_enabled",
        "config_rules_enabled"
    ],

    "centralized_logging": {
        "cloudtrail": True,
        "vpc_flow_logs": True
    }

}