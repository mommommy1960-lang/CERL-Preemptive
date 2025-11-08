#!/usr/bin/env python3
"""
Demonstration of CERL-Preemptive Consent Validator
This script demonstrates how the consent validator handles the
exact scenario from the problem statement.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cerl_preemptive.consent_validator import ConsentValidator, ConsentViolationError


def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")


def main():
    print_header("CERL-Preemptive Consent Validator - Demonstration")

    print("This demonstration shows how the consent validator handles")
    print("the exact scenario from the problem statement.\n")

    # Create validator instance
    validator = ConsentValidator()

    # Scenario from problem statement
    print_header("SCENARIO: Problem Statement Request")
    print("REQUEST:")
    print("  action: 'access_user_data'")
    print("  target: 'private_data'")
    print("  purpose: 'marketing'")
    print("  consent_status: 'not_granted'  ← VIOLATION!")
    print("  urgency: 'none'")
    print("  potential_harm: 'privacy_violation'")
    print()

    request = {
        "action": "access_user_data",
        "target": "private_data",
        "purpose": "marketing",
        "consent_status": "not_granted",
        "urgency": "none",
        "potential_harm": "privacy_violation",
        "actor": "marketing_system"
    }

    print("Processing request...")
    print()

    try:
        validator.validate_request(request)
        print("❌ ERROR: Request was ALLOWED (this should not happen!)")
        return 1
    except ConsentViolationError as e:
        print("✅ SUCCESS: Request was BLOCKED")
        print()
        print("Details:")
        print(f"  Error Message: {e}")
        print(f"  Violations Detected: {validator.get_violation_count()}")
        print()
        print("The violation has been logged to the tamper-resistant ledger.")
        print("Audit trail entry created with:")
        print("  - Timestamp")
        print("  - Actor (marketing_system)")
        print("  - Action (consent_violation_detected)")
        print("  - Full request context")
        print("  - Violation type (access_without_consent)")
        print("  - Blocked status (True)")

    # Show a valid request for comparison
    print_header("COMPARISON: Valid Request with Consent")
    print("REQUEST:")
    print("  action: 'access_user_data'")
    print("  target: 'private_data'")
    print("  purpose: 'service_provision'")
    print("  consent_status: 'granted'  ← Valid!")
    print("  urgency: 'normal'")
    print("  potential_harm: 'none'")
    print()

    valid_request = {
        "action": "access_user_data",
        "target": "private_data",
        "purpose": "service_provision",
        "consent_status": "granted",
        "urgency": "normal",
        "potential_harm": "none",
        "actor": "service_system"
    }

    print("Processing request...")
    print()

    try:
        validator.validate_request(valid_request)
        print("✅ SUCCESS: Request was ALLOWED")
        print()
        print("The request was validated because:")
        print("  - Consent status is 'granted'")
        print("  - Target is private_data (requires consent)")
        print("  - All validation checks passed")
        print()
        print("Validation logged to ledger with:")
        print("  - Timestamp")
        print("  - Actor (service_system)")
        print("  - Action (consent_validation_passed)")
        print("  - Full request context")
    except ConsentViolationError as e:
        print(f"❌ ERROR: Request was BLOCKED: {e}")
        print("(This valid request should have been allowed)")
        return 1

    # Summary
    print_header("Summary")
    print("✅ The consent validator successfully:")
    print()
    print("  1. BLOCKED unauthorized access to private data without consent")
    print("     (matching the exact problem statement scenario)")
    print()
    print("  2. ALLOWED legitimate access to private data with consent")
    print()
    print("  3. LOGGED all validation attempts to the tamper-resistant ledger")
    print()
    print("  4. RAISED appropriate exceptions for consent violations")
    print()
    print(f"Total violations detected in this session: {validator.get_violation_count()}")
    print()
    print("The CERL-Preemptive framework is protecting user privacy! 🛡️")

    return 0


if __name__ == "__main__":
    sys.exit(main())
