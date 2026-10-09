"""Print a denied local policy proposal; review and explicitly select approval.

No file is written and no dependency is imported by identity discovery. The
printed deny setting prevents this proposal from satisfying strict admission.
"""
import json
from pyalamode.integration_contracts import integration_snapshot


def main():
    snapshot = integration_snapshot()
    if snapshot["errors"] or any(row["installed_identity"] is None for row in snapshot["catalog"]):
        raise SystemExit("Installed integration identity is unavailable; inspect pyalamode explain integrations --json")
    print("# Review actual paths, installed version, artifact bytes and the finite contracts.")
    print("# Replace review text and choose expiry; explicitly select approved after review.")
    print('[tool.pyalamode]\nexternal_trust = "deny"')
    for row in snapshot["catalog"]:
        print("\n# " + row["identity"])
        print("# Installed identity: " + json.dumps(row["installed_identity"], sort_keys=True))
        print("[[tool.pyalamode.integration_approvals]]")
        for key, value in {"operation": row["identity"], "contract_sha256": row["contract_sha256"], "dependency_sha256": row["dependency_sha256"],
                           "owner": "REVIEW REQUIRED", "rationale": "REVIEW REQUIRED", "provenance": "REVIEW REQUIRED"}.items():
            print(key + " = " + json.dumps(value))


if __name__ == "__main__":
    main()
