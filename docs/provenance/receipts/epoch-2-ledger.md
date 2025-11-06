# Epoch-2 Ledger (Human-Readable Receipt)

This file catalogs each CI run for Epoch-2:
- Commit SHA
- Tag (when present)
- SHA256 bundle summary
- Links to run logs and artifacts
- CERL clause references

Machine receipts (sha256s.txt) are uploaded per run as CI artifacts named:
`cerl-epoch2-receipt-<run_id>.zip`

## Chain-of-Custody Block (Template)
- Repo: mommommy1960-lang/CERL-Preemptive
- Branch: main
- Tag: v0.2.0
- Commit: <populated by CI>
- Run ID: <populated by CI>
- SHA bundle: artifact `cerl-epoch2-receipt-<run_id>.zip`
- CERL: §1.3, §2.0, §4.2
- Notes: Security & lint checks executed; see CI logs.