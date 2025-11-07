# Epoch-3: Identity, Attestation & Key Continuity

## Overview
Epoch-3 extends the CERL-Preemptive provenance framework with cryptographic identity enforcement, Sigstore key lifecycle management, and attestation pipeline capabilities aligned with CERL-1.0 §1.3, §2.0, §4.2, and future §7.x provisions.

## Key Enhancements

### 1. Cryptographic Identity Enforcement
- **Identity Binding**: Linking cryptographic signatures to verified maintainer identities
- **Multi-Factor Authentication**: Enhanced authentication mechanisms for signing operations
- **Key Rotation Policy**: Structured approach to key lifecycle and expiration
- **Identity Verification**: Integration with trusted identity providers (GitHub OIDC)

### 2. Sigstore Key Lifecycle Plan
- **Key Generation**: Automated ephemeral key generation via Sigstore cosign
- **Key Storage**: Secure key management using OIDC-based keyless signing
- **Key Rotation**: Scheduled key rotation aligned with security best practices
- **Key Revocation**: Process for invalidating compromised or expired keys
- **Transparency**: All signing events logged to Rekor transparency log

### 3. Attestation Pipeline (Draft Stage)
- **Artifact Attestation**: Cryptographic proofs for all release artifacts
- **Build Provenance**: SLSA-compliant build provenance generation
- **In-Toto Layout**: Structured supply chain attestation framework
- **Verification Workflow**: Automated verification of signed artifacts
- **Policy Enforcement**: Signature verification requirements for deployments

### 4. CERL Cross-Compliance Clause Hooks
- **§1.3**: Code integrity enforcement through cryptographic signatures
- **§2.0**: Supply chain security via attestation and provenance tracking
- **§4.2**: Enhanced audit trail with signed receipts and transparency logs
- **§7.x (Future)**: Placeholder for upcoming cross-organizational compliance requirements

## Architecture Changes

### CI/CD Workflow Extensions
The Epoch-3 enhancements will include:
1. Sigstore cosign integration for artifact signing
2. Rekor transparency log submission
3. Attestation generation for all CI runs
4. Signature verification gates for deployments
5. Key lifecycle automation

### Validation Rules v0.3.0
Enhanced validation rules to be documented in `validation-rules/v0.3.0.md`:
- Mandatory signing for all release artifacts (>= v0.3.0)
- Attestation generation for provenance receipts
- Signature verification in deployment pipelines
- Key rotation compliance checks
- Transparency log verification

## CERL Compliance Mapping

| Enhancement | CERL Clause | Purpose |
|-------------|-------------|---------|
| Identity Enforcement | §1.3 | Cryptographic proof of maintainer identity |
| Key Lifecycle | §1.3, §2.0 | Secure key management and rotation |
| Attestation Pipeline | §4.2 | Verifiable build and release provenance |
| Transparency Logging | §1.3, §4.2 | Public audit trail for all signing events |
| Cross-Compliance Hooks | §7.x (future) | Multi-organization audit coordination |

## Implementation Timeline

### Phase 1: Foundation (v0.3.0) 🚧
- [ ] Validation rules v0.3.0 published
- [ ] Epoch-3 ledger template created
- [ ] Sigstore integration plan finalized
- [ ] Identity enforcement framework scaffolded

### Phase 2: Live Signing (v0.4.0)
- [ ] Activate cosign signing for releases
- [ ] Enable Rekor transparency logging
- [ ] Implement attestation generation
- [ ] Automated signature verification

### Phase 3: Full Attestation (v1.0.0)
- [ ] SLSA Level 2+ provenance
- [ ] In-Toto supply chain security
- [ ] Multi-party signing support
- [ ] Cross-organization audit federation

## Next Milestone: Live Signing Enforcement

The primary goal of Epoch-3 is to establish **live signing enforcement** for all release artifacts. This includes:

1. **Immediate Actions** (v0.3.0):
   - Finalize Sigstore integration configuration
   - Establish key lifecycle policies
   - Create attestation pipeline scaffolding
   - Document signing procedures

2. **Next Steps** (v0.4.0):
   - Enable automatic signing in CI/CD
   - Deploy signature verification requirements
   - Activate transparency log submission
   - Implement key rotation automation

3. **Long-term Vision** (v1.0.0+):
   - Full SLSA compliance
   - Multi-signature workflows
   - Cross-organizational provenance federation
   - Advanced policy-based verification

## Usage

### Preparing for Sigstore Integration
```bash
# Install cosign (when ready for activation)
curl -O -L "https://github.com/sigstore/cosign/releases/latest/download/cosign-linux-amd64"
sudo mv cosign-linux-amd64 /usr/local/bin/cosign
sudo chmod +x /usr/local/bin/cosign

# Verify cosign installation
cosign version
```

### Future: Verifying Signed Artifacts
```bash
# This will be activated in v0.4.0
# cosign verify-blob --signature <artifact>.sig <artifact>
# cosign verify-blob --bundle <artifact>.bundle <artifact>
```

## Related Documentation
- [Validation Rules v0.3.0](../validation-rules/v0.3.0.md) (to be created)
- [Epoch-3 Ledger](../receipts/epoch-3-ledger.md) (to be created)
- [Sigstore Plan](../sigstore-plan.md)
- [CI Security Workflow](../../../.github/workflows/ci-security.yml)
- [Epoch-2 README](../epoch-2/README.md)

## Governance
This provenance extension is governed under the CERL-1.0 license and maintained by the Commons Initiative. All changes require documented rationale and CERL clause mapping.

---
**Version**: 0.3.0  
**Last Updated**: 2025-11-07  
**Maintainer**: Commons Custodianship Trust Charter  
**Status**: Initialization Phase — Signing Not Yet Active
