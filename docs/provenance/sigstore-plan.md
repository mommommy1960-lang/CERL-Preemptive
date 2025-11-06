# Sigstore Plan (Scaffold)
Targets:
- Sign release artifacts with cosign
- Rekor transparency log entries
- Policy: sign tags >= v1.x and all provenance receipts
Prereqs:
- Create OIDC-based signing policy on repo
- Add cosign step to CI on release workflow
