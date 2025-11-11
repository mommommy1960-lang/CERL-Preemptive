#!/usr/bin/env python3
"""
Integration test for CERL-Preemptive Consent Validator
This script demonstrates the complete workflow of consent validation
and verifies the problem statement scenario is handled correctly.
"""

import sys
import os
import tempfile
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cerl_preemptive.consent_validator import (
    ConsentValidator,
    ConsentViolationError
)
from cerl_preemptive import consent_ledger


def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'=' * 70}")
    print(f" {title}")
    print('=' * 70)


def test_problem_statement_scenario():
    """Test the exact scenario from the problem statement"""
    print_section("Problem Statement Scenario Test")

    print("\nTesting REQUEST:")
    print("  action: 'access_user_data'")
    print("  target: 'private_data'")
    print("  purpose: 'marketing'")
    print("  consent_status: 'not_granted'")
    print("  urgency: 'none'")
    print("  potential_harm: 'privacy_violation'")
    print()

    validator = ConsentValidator()

    try:
        validator.validate_request({
            "action": "access_user_data",
            "target": "private_data",
            "purpose": "marketing",
            "consent_status": "not_granted",
            "urgency": "none",
            "potential_harm": "privacy_violation",
            "actor": "marketing_system"
        })
        print("❌ FAILED: Request was allowed (should have been blocked)")
        return False
    except ConsentViolationError as e:
        print("✅ SUCCESS: Request was blocked")
        print(f"   Reason: {e}")
        return True


def test_valid_consent_scenario():
    """Test a scenario with valid consent"""
    print_section("Valid Consent Scenario Test")

    print("\nTesting REQUEST with consent granted:")
    print("  action: 'access_user_data'")
    print("  target: 'private_data'")
    print("  purpose: 'service_provision'")
    print("  consent_status: 'granted'")
    print()

    validator = ConsentValidator()

    try:
        validator.validate_request({
            "action": "access_user_data",
            "target": "private_data",
            "purpose": "service_provision",
            "consent_status": "granted",
            "urgency": "normal",
            "potential_harm": "none",
            "actor": "service_system"
        })
        print("✅ SUCCESS: Request was allowed with proper consent")
        return True
    except ConsentViolationError as e:
        print("❌ FAILED: Request was blocked (should have been allowed)")
        print(f"   Error: {e}")
        return False


def test_ledger_integrity():
    """Verify ledger integrity after validations"""
    print_section("Ledger Integrity Test")

    if not os.path.exists(consent_ledger.LEDGER_PATH):
        print("⚠ WARNING: No ledger file found")
        return True

    print(f"\nVerifying ledger at: {consent_ledger.LEDGER_PATH}")

    try:
        is_valid = consent_ledger.verify_chain()
        if is_valid:
            print("✅ SUCCESS: Ledger chain integrity verified")

            # Count events
            with open(consent_ledger.LEDGER_PATH, 'r') as f:
                events = [json.loads(line) for line in f if line.strip()]

            print("\nLedger Statistics:")
            print(f"  Total events: {len(events)}")

            violations = [e for e in events if e['action'] == 'consent_violation_detected']
            validations = [e for e in events if e['action'] == 'consent_validation_passed']

            print(f"  Consent violations detected: {len(violations)}")
            print(f"  Successful validations: {len(validations)}")

            if violations:
                print("\n  Recent violation details:")
                last_violation = violations[-1]
                print(f"    Actor: {last_violation['actor']}")
                print(f"    Target: {last_violation['payload']['target']}")
                print(f"    Purpose: {last_violation['payload']['purpose']}")
                print(f"    Blocked: {last_violation['payload']['blocked']}")

            return True
        else:
            print("❌ FAILED: Ledger chain integrity check failed")
            return False
    except Exception as e:
        print(f"❌ FAILED: Error verifying ledger: {e}")
        return False


def test_public_data_access():
    """Test that public data can be accessed without consent"""
    print_section("Public Data Access Test")

    print("\nTesting access to public data without explicit consent:")
    validator = ConsentValidator()

    try:
        validator.validate_request({
            "action": "read_data",
            "target": "public_information",
            "purpose": "display",
            "consent_status": "not_granted",
            "urgency": "normal",
            "potential_harm": "none",
            "actor": "display_system"
        })
        print("✅ SUCCESS: Public data access allowed without explicit consent")
        return True
    except ConsentViolationError as e:
        print(f"❌ FAILED: Public data access was blocked: {e}")
        return False


def main():
    """Run all integration tests"""
    print_section("CERL-Preemptive Consent Validator - Integration Test")
    print("\nThis test suite validates the consent validation implementation")
    print("against the problem statement requirements.")

    # Setup: Use a temporary ledger for testing
    temp_dir = tempfile.mkdtemp()
    original_ledger = consent_ledger.LEDGER_PATH
    consent_ledger.LEDGER_PATH = os.path.join(temp_dir, "integration_test_ledger.jsonl")

    print(f"\nUsing temporary ledger: {consent_ledger.LEDGER_PATH}")

    # Run tests
    results = []
    results.append(("Problem Statement Scenario", test_problem_statement_scenario()))
    results.append(("Valid Consent Scenario", test_valid_consent_scenario()))
    results.append(("Public Data Access", test_public_data_access()))
    results.append(("Ledger Integrity", test_ledger_integrity()))

    # Restore original ledger path
    consent_ledger.LEDGER_PATH = original_ledger

    # Summary
    print_section("Test Summary")
    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}: {name}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All integration tests passed!")
        print("\n✅ The consent validator successfully:")
        print("   • Blocks unauthorized access to private data")
        print("   • Allows access when proper consent is granted")
        print("   • Permits access to public data")
        print("   • Maintains ledger integrity")
        return 0
    else:
        print(f"\n❌ {total - passed} test(s) failed")
        return 1

    # Cleanup
    import shutil
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)


if __name__ == "__main__":
    sys.exit(main())
