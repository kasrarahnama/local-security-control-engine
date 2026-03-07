from typing import Dict

SHARED_RESPONSIBILITY = {
    "AC-2/AC-3": {
        "provider": "Cloud provider ensures secure IAM infrastructure",
        "customer": "Customer manages identities, roles, and policies"
    },
    "LeastPrivilege": {
        "provider": "Cloud provider supplies IAM capability",
        "customer": "Customer defines least-privilege policies and roles"
    },
    "SC-28": {
        "provider": "Cloud provider secures underlying storage infrastructure",
        "customer": "Customer enables encryption at rest and manages keys"
    },
    "SI-10": {
        "provider": "Cloud provider supplies logging and monitoring infrastructure",
        "customer": "Customer implements application-level input validation"
    }
}