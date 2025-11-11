"""
CERL-Preemptive Consent Validator
Validates data access requests against consent requirements.
"""

import time
from typing import Dict, Any

# Handle both relative and absolute imports
try:
    from .consent_ledger import append_event
except ImportError:
    from consent_ledger import append_event


class ConsentViolationError(Exception):
    """Raised when a consent requirement is violated."""
    pass


class ConsentValidator:
    """
    Validates requests for data access against consent requirements.
    Ensures that private data is only accessed with proper consent.
    """

    def __init__(self):
        self.violation_count = 0

    def validate_request(self, request: Dict[str, Any]) -> bool:
        """
        Validate a data access request.

        Args:
            request: Dictionary containing:
                - action: The action being requested
                - target: The target of the action
                - purpose: The purpose of the action
                - consent_status: Status of consent ("granted" or "not_granted")
                - urgency: Urgency level
                - potential_harm: Potential harm description
                - actor: (optional) The actor making the request

        Returns:
            True if the request is valid and should be allowed
            False if the request violates consent requirements

        Raises:
            ConsentViolationError: If consent is not granted for private data access
        """
        action = request.get("action", "")
        target = request.get("target", "")
        purpose = request.get("purpose", "")
        consent_status = request.get("consent_status", "not_granted")
        potential_harm = request.get("potential_harm", "")
        actor = request.get("actor", "unknown")
        urgency = request.get("urgency", "none")

        # Log the validation attempt
        validation_payload = {
            "action": action,
            "target": target,
            "purpose": purpose,
            "consent_status": consent_status,
            "urgency": urgency,
            "potential_harm": potential_harm
        }

        # Check if this is a request for private data
        is_private_data = "private" in target.lower() or "personal" in target.lower()

        # Check consent status
        consent_granted = consent_status == "granted"

        # Validate the request
        if is_private_data and not consent_granted:
            # This is a consent violation - log it
            self.violation_count += 1
            append_event(
                actor=actor,
                action="consent_violation_detected",
                payload={
                    **validation_payload,
                    "violation_type": "access_without_consent",
                    "blocked": True,
                    "timestamp": time.time()
                }
            )

            error_msg = (
                f"Consent violation: Attempt to {action} on {target} "
                f"for {purpose} without consent. "
                f"Potential harm: {potential_harm}"
            )
            raise ConsentViolationError(error_msg)

        # Request is valid - log successful validation
        append_event(
            actor=actor,
            action="consent_validation_passed",
            payload={
                **validation_payload,
                "validated": True,
                "timestamp": time.time()
            }
        )

        return True

    def check_consent_status(self, consent_status: str) -> bool:
        """
        Check if a consent status is valid.

        Args:
            consent_status: The consent status to check

        Returns:
            True if consent is granted, False otherwise
        """
        return consent_status == "granted"

    def get_violation_count(self) -> int:
        """Get the total number of consent violations detected."""
        return self.violation_count


def validate_data_access_request(
    action: str,
    target: str,
    purpose: str,
    consent_status: str,
    actor: str = "unknown",
    urgency: str = "none",
    potential_harm: str = "unknown"
) -> bool:
    """
    Convenience function to validate a data access request.

    Args:
        action: The action being requested
        target: The target of the action
        purpose: The purpose of the action
        consent_status: Status of consent ("granted" or "not_granted")
        actor: The actor making the request
        urgency: Urgency level
        potential_harm: Potential harm description

    Returns:
        True if the request is valid

    Raises:
        ConsentViolationError: If consent is not granted for private data access
    """
    validator = ConsentValidator()
    request = {
        "action": action,
        "target": target,
        "purpose": purpose,
        "consent_status": consent_status,
        "actor": actor,
        "urgency": urgency,
        "potential_harm": potential_harm
    }
    return validator.validate_request(request)


if __name__ == "__main__":
    print("CERL-Preemptive Consent Validator initialized.")

    # Example: Test the validator with the problem statement case
    validator = ConsentValidator()

    print("\nTest Case 1: Attempting to access private data without consent...")
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
        print("✗ Request was allowed (UNEXPECTED)")
    except ConsentViolationError as e:
        print(f"✓ Request blocked: {e}")

    print("\nTest Case 2: Accessing private data with consent...")
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
        print("✓ Request allowed with proper consent")
    except ConsentViolationError as e:
        print(f"✗ Request blocked (UNEXPECTED): {e}")

    print(f"\nTotal violations detected: {validator.get_violation_count()}")
