# Epoch-2 Provenance Extension

## Overview
Epoch-2 extends the CERL-Preemptive provenance framework with enhanced security, validation, and transparency features aligned with CERL-1.0 §1.3, §2.0, and §4.2.

## Key Enhancements

### 1. Enhanced Validation Pipeline
- **Python Linting**: Integration of `ruff` and `flake8` for code quality checks
- **Security Scanning**: `bandit` for identifying security vulnerabilities in Python code
- **Dependency Auditing**: `pip-audit` for scanning dependencies against known CVEs
- **Configuration Linting**: `yamllint` for YAML validation and `markdownlint` for documentation quality

### 2. Artifact Provenance
- **SHA256 Receipts**: Every CI run generates cryptographic checksums for all artifacts
- **Receipt Storage**: Machine-readable receipts uploaded as `cerl-epoch2-receipt-<run_id>.zip`
- **Human-Readable Ledger**: Chain-of-custody records maintained in `receipts/epoch-2-ledger.md`

### 3. Sigstore Integration (Scaffold)
- **Cosign Signing**: Preparation for signing release artifacts with cosign
- **Rekor Transparency**: Planning for transparency log entries
- **Policy Framework**: Sign tags >= v1.x and all provenance receipts
- **OIDC Authentication**: GitHub OIDC-based signing policy

## Architecture Changes

### CI/CD Workflow (`ci-security.yml`)
The new security-focused CI workflow includes:
1. Repository structure validation
2. Python syntax and security checks
3. Dependency vulnerability scanning
4. Documentation and configuration linting
5. Artifact generation with SHA256 receipts
6. Automated provenance record creation

### Validation Rules v0.2.0
Enhanced validation rules documented in `validation-rules/v0.2.0.md`:
- Mandatory security scanning before merge
- Automated lint checks for all file types
- Dependency audit requirements
- SHA256 receipt generation for audit trail

## CERL Compliance Mapping

| Enhancement | CERL Clause | Purpose |
|-------------|-------------|---------|
| Security Scanning | §1.3 | Ensure code integrity and prevent vulnerabilities |
| Dependency Audit | §2.0 | Maintain supply chain security |
| Artifact Receipts | §4.2 | Enable verifiable audit trail |
| Sigstore Integration | §1.3, §4.2 | Cryptographic proof of authenticity |

## Implementation Timeline

### Phase 1: Foundation (v0.2.0) ✓
- [x] Validation rules v0.2.0 published
- [x] Receipt ledger template created
- [x] Sigstore plan scaffolded
- [x] CI security workflow implemented

### Phase 2: Integration (v0.3.0)
- [ ] Activate security scanning gates
- [ ] Integrate Sigstore cosign signing
- [ ] Enable Rekor transparency logging
- [ ] Automated receipt verification

### Phase 3: Hardening (v1.0.0)
- [ ] Multi-signature verification
- [ ] Cross-organization audit support
- [ ] Real-time provenance API
- [ ] Policy enforcement automation

## Usage

### Running Security Checks Locally
```bash
# Install dependencies
pip install ruff flake8 bandit pip-audit

# Run linting
ruff check cerl_preemptive/
flake8 cerl_preemptive/

# Run security scan
bandit -r cerl_preemptive/

# Audit dependencies
pip-audit
```

### Verifying Artifacts
```bash
# Download receipt from CI artifacts
# Extract and verify SHA256 checksums
sha256sum -c sha256s.txt
```

## Related Documentation
- [Validation Rules v0.2.0](../validation-rules/v0.2.0.md)
- [Epoch-2 Ledger](../receipts/epoch-2-ledger.md)
- [Sigstore Plan](../sigstore-plan.md)
- [CI Security Workflow](../../../.github/workflows/ci-security.yml)

## Governance
This provenance extension is governed under the CERL-1.0 license and maintained by the Commons Initiative. All changes require documented rationale and CERL clause mapping.

---
**Version**: 0.2.0  
**Last Updated**: 2025-11-06  
**Maintainer**: Commons Custodianship Trust Charter
