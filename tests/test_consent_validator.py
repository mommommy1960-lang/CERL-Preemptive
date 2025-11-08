"""
Unit tests for CERL-Preemptive Consent Validator
"""

import unittest
import sys
import os
import tempfile
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from cerl_preemptive.consent_validator import (
    ConsentValidator,
    ConsentViolationError,
    validate_data_access_request
)


class TestConsentValidator(unittest.TestCase):
    """Test cases for ConsentValidator class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.validator = ConsentValidator()
        # Use a temporary ledger file for testing
        self.temp_dir = tempfile.mkdtemp()
        self.original_ledger_path = None
        
        # Temporarily override the ledger path
        import cerl_preemptive.consent_ledger as ledger_module
        self.original_ledger_path = ledger_module.LEDGER_PATH
        ledger_module.LEDGER_PATH = os.path.join(self.temp_dir, "test_ledger.jsonl")
    
    def tearDown(self):
        """Clean up test fixtures"""
        # Restore original ledger path
        if self.original_ledger_path:
            import cerl_preemptive.consent_ledger as ledger_module
            ledger_module.LEDGER_PATH = self.original_ledger_path
        
        # Clean up temp directory
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_private_data_access_without_consent_blocked(self):
        """Test that access to private data without consent is blocked"""
        request = {
            "action": "access_user_data",
            "target": "private_data",
            "purpose": "marketing",
            "consent_status": "not_granted",
            "urgency": "none",
            "potential_harm": "privacy_violation",
            "actor": "marketing_system"
        }
        
        with self.assertRaises(ConsentViolationError) as context:
            self.validator.validate_request(request)
        
        self.assertIn("Consent violation", str(context.exception))
        self.assertIn("marketing", str(context.exception))
        self.assertEqual(self.validator.get_violation_count(), 1)
    
    def test_private_data_access_with_consent_allowed(self):
        """Test that access to private data with consent is allowed"""
        request = {
            "action": "access_user_data",
            "target": "private_data",
            "purpose": "service_provision",
            "consent_status": "granted",
            "urgency": "normal",
            "potential_harm": "none",
            "actor": "service_system"
        }
        
        result = self.validator.validate_request(request)
        self.assertTrue(result)
        self.assertEqual(self.validator.get_violation_count(), 0)
    
    def test_personal_data_access_without_consent_blocked(self):
        """Test that access to personal data without consent is blocked"""
        request = {
            "action": "read_data",
            "target": "personal_information",
            "purpose": "analytics",
            "consent_status": "not_granted",
            "urgency": "low",
            "potential_harm": "privacy_violation",
            "actor": "analytics_system"
        }
        
        with self.assertRaises(ConsentViolationError) as context:
            self.validator.validate_request(request)
        
        self.assertIn("Consent violation", str(context.exception))
        self.assertEqual(self.validator.get_violation_count(), 1)
    
    def test_public_data_access_without_consent_allowed(self):
        """Test that access to public data without explicit consent is allowed"""
        request = {
            "action": "read_data",
            "target": "public_information",
            "purpose": "display",
            "consent_status": "not_granted",
            "urgency": "normal",
            "potential_harm": "none",
            "actor": "display_system"
        }
        
        result = self.validator.validate_request(request)
        self.assertTrue(result)
        self.assertEqual(self.validator.get_violation_count(), 0)
    
    def test_check_consent_status_granted(self):
        """Test consent status check for granted consent"""
        self.assertTrue(self.validator.check_consent_status("granted"))
    
    def test_check_consent_status_not_granted(self):
        """Test consent status check for not granted consent"""
        self.assertFalse(self.validator.check_consent_status("not_granted"))
    
    def test_multiple_violations_tracked(self):
        """Test that multiple violations are tracked correctly"""
        request1 = {
            "action": "access_user_data",
            "target": "private_data",
            "purpose": "marketing",
            "consent_status": "not_granted",
            "urgency": "none",
            "potential_harm": "privacy_violation",
            "actor": "system1"
        }
        
        request2 = {
            "action": "access_user_data",
            "target": "private_profile",
            "purpose": "profiling",
            "consent_status": "not_granted",
            "urgency": "low",
            "potential_harm": "discrimination",
            "actor": "system2"
        }
        
        with self.assertRaises(ConsentViolationError):
            self.validator.validate_request(request1)
        
        with self.assertRaises(ConsentViolationError):
            self.validator.validate_request(request2)
        
        self.assertEqual(self.validator.get_violation_count(), 2)
    
    def test_convenience_function_with_violation(self):
        """Test the convenience function with a consent violation"""
        with self.assertRaises(ConsentViolationError):
            validate_data_access_request(
                action="access_user_data",
                target="private_data",
                purpose="marketing",
                consent_status="not_granted",
                actor="marketing_system",
                urgency="none",
                potential_harm="privacy_violation"
            )
    
    def test_convenience_function_with_consent(self):
        """Test the convenience function with proper consent"""
        result = validate_data_access_request(
            action="access_user_data",
            target="private_data",
            purpose="service",
            consent_status="granted",
            actor="service_system",
            urgency="normal",
            potential_harm="none"
        )
        self.assertTrue(result)


class TestProblemStatementScenario(unittest.TestCase):
    """Test the specific scenario from the problem statement"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.validator = ConsentValidator()
        # Use a temporary ledger file for testing
        self.temp_dir = tempfile.mkdtemp()
        
        # Temporarily override the ledger path
        import cerl_preemptive.consent_ledger as ledger_module
        self.original_ledger_path = ledger_module.LEDGER_PATH
        ledger_module.LEDGER_PATH = os.path.join(self.temp_dir, "test_ledger.jsonl")
    
    def tearDown(self):
        """Clean up test fixtures"""
        # Restore original ledger path
        if self.original_ledger_path:
            import cerl_preemptive.consent_ledger as ledger_module
            ledger_module.LEDGER_PATH = self.original_ledger_path
        
        # Clean up temp directory
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_problem_statement_request_blocked(self):
        """
        Test the exact scenario from the problem statement:
        REQUEST:
          action: "access_user_data"
          target: "private_data"
          purpose: "marketing"
          consent_status: "not_granted"
          urgency: "none"
          potential_harm: "privacy_violation"
        
        This request should be BLOCKED.
        """
        request = {
            "action": "access_user_data",
            "target": "private_data",
            "purpose": "marketing",
            "consent_status": "not_granted",
            "urgency": "none",
            "potential_harm": "privacy_violation"
        }
        
        with self.assertRaises(ConsentViolationError) as context:
            self.validator.validate_request(request)
        
        # Verify the error message contains key information
        error_message = str(context.exception)
        self.assertIn("access_user_data", error_message)
        self.assertIn("private_data", error_message)
        self.assertIn("marketing", error_message)
        self.assertIn("privacy_violation", error_message)
        
        # Verify violation was recorded
        self.assertEqual(self.validator.get_violation_count(), 1)


if __name__ == '__main__':
    unittest.main()
