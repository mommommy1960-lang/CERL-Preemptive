![CI Security](https://github.com/mommommy1960-lang/CERL-Preemptive/actions/workflows/ci-security.yml/badge.svg)
![SHA-256 Provenance](https://img.shields.io/badge/Provenance-Chain-Active-green)
![Sigstore (Planned)](https://img.shields.io/badge/Sigstore-Integration-In-Progress-yellow)

# Commons Preemptive Ethics Framework (CERL-Preemptive)

## Overview  
The **Commons Preemptive Ethics Framework** is a living, open-source prototype for autonomous ethical accountability in AI and research systems.  
It is built to self-audit, self-verify, and transparently log consent and integrity events in real time.

## Architecture
The framework operates as a distributed microservice stack:

| Module | Description |
|--------|-------------|
| `consent_ledger.py` | Creates a tamper-resistant ledger of all events and actions. |
| `consent_token_manager.py` | Issues, manages, and verifies cryptographic consent tokens. |
| `consent_validator.py` | Validates data access requests against consent requirements and blocks unauthorized access. |
| `audit_trail_api.py` | Provides a lightweight HTTP interface for external audit retrieval. |
| `verify_module.py` | Scans and validates ledger integrity using hash verification. |
| `consent_api_gateway.py` | Receives and records live consent submissions via HTTP POST. |
| `heartbeart.py` | Emits recurring "proof-of-life" entries every 5 minutes for continuity verification. |

## Purpose  
The project is designed as a **proof-of-concept** for the Commons Initiative:  
⧫ To establish open, verifiable standards for ethical AI research.  
⧫ To create a transparent audit trail for all consent and data-usage events.  
⧫ To prevent tampering, corruption, or loss of ethical accountability.

## Running Locally
1. Clone this repository.
2. Open in GitHub Codespaces or any Python 3.10+ environment.
3. Run the modules in this order:
    ```
    bash
    python consent_ledger.py
    python consent_token_manager.py
    python consent_validator.py
    python audit_trail_api.py
    python verify_module.py
    python consent_api_gateway.py
    python heartbeart.py
    ```
4. The gateway will be available at http://localhost:9090/consent.

5. The audit API will be accessible at http://localhost:8080/ledger.

## Consent Validation

The `consent_validator.py` module provides real-time validation of data access requests to ensure compliance with consent requirements.

### Features
- **Automatic Consent Checking**: Validates that consent is granted before allowing access to private or personal data
- **Violation Detection**: Detects and blocks unauthorized access attempts
- **Audit Logging**: Records all validation attempts and violations in the tamper-resistant ledger
- **Flexible API**: Provides both class-based and function-based interfaces

### Usage Example

```python
from cerl_preemptive.consent_validator import validate_data_access_request, ConsentViolationError

# This will raise ConsentViolationError - blocked!
try:
    validate_data_access_request(
        action="access_user_data",
        target="private_data",
        purpose="marketing",
        consent_status="not_granted",
        potential_harm="privacy_violation"
    )
except ConsentViolationError as e:
    print(f"Access denied: {e}")

# This will succeed - consent granted
validate_data_access_request(
    action="access_user_data",
    target="private_data",
    purpose="service_provision",
    consent_status="granted"
)
```

### Testing

Run the comprehensive test suite:
```bash
python -m unittest tests.test_consent_validator -v
```

Licenses

Licensed under CERL-1.0 (Commons Ethical Research License).
Use and modification are permitted under Commons guidelines with attribution.

Maintainers

Mya P. Brown – Founding Custodian, Commons Custodianship Trust Charter
Advanced AI Technology ▪ Development Partner (Autonomous Systems Research)
⚑ 2025 Commons Initiative. All rights reserved under the CERL-1.0 license.

---

### Phase 9  
**Public release and deployment of the Commons Preemptive Ethics Framework v1.0.0 (Live)**  
The framework has been officially published under the **CERL-1.0 License**,  
with verified containers, live documentation, and public audit endpoints.  
For the latest updates, visit:  
🌐 https://mommommy1960-lang.github.io/CERL-Preemptive/

---

### Phase 13  
**Milestone v1.1.0-dev – Encrypted Consent-Token Exchange Layer (ECTEL)**  
Secure cross-node consent exchange now active in v1.1-dev branch.  
See detailed milestone report here:  
🌐 https://github.com/mommommy1960-lang/CERL-Preemptive/blob/main/docs/milestone_v1.1.0.md
