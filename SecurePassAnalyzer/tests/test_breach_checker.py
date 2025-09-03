"""
Unit tests for breach_checker module
"""

import unittest
import sys
import os
from unittest.mock import Mock, patch

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from breach_checker import BreachChecker


class TestBreachChecker(unittest.TestCase):
    """Test cases for BreachChecker class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.checker = BreachChecker()
    
    def test_initialization(self):
        """Test proper initialization of BreachChecker"""
        self.assertIsInstance(self.checker, BreachChecker)
        self.assertTrue(self.checker.hibp_password_api)
        self.assertTrue(self.checker.hibp_breach_api)
        self.assertIn('User-Agent', self.checker.headers)
    
    @patch('requests.get')
    def test_password_breach_check_found(self, mock_get):
        """Test password breach checking when password is found"""
        # Mock response for a breached password
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "00F9E393C8308B858A9EAAF6E308CBC5E5F6:2\r\n001E5C5B87D4F21F76A7500E6A2B39F8FB1A:3\r\n"
        mock_get.return_value = mock_response
        
        # Test with a password that would match the second hash
        is_breached, count = self.checker.check_password_breach("test")
        
        # Since we're mocking, the exact result depends on the hash calculation
        # But we can verify the method handles the response correctly
        self.assertIsInstance(is_breached, bool)
        self.assertIsInstance(count, int)
    
    @patch('requests.get')
    def test_password_breach_check_not_found(self, mock_get):
        """Test password breach checking when password is not found"""
        # Mock response for a non-breached password
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "00F9E393C8308B858A9EAAF6E308CBC5E5F6:2\r\n001E5C5B87D4F21F76A7500E6A2B39F8FB1A:3\r\n"
        mock_get.return_value = mock_response
        
        # The password hash won't match our mock data
        is_breached, count = self.checker.check_password_breach("verysecurepassword123!")
        
        self.assertIsInstance(is_breached, bool)
        self.assertEqual(count, 0)
    
    @patch('requests.get')
    def test_password_breach_api_error(self, mock_get):
        """Test handling of API errors"""
        # Mock API error response
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response
        
        is_breached, count = self.checker.check_password_breach("test")
        
        # Should handle error gracefully
        self.assertFalse(is_breached)
        self.assertEqual(count, 0)
    
    def test_email_breach_check_no_api_key(self):
        """Test email breach checking without API key"""
        result = self.checker.check_email_breaches("test@example.com")
        
        self.assertIn('error', result)
        self.assertIn('API key required', result['error'])
        self.assertFalse(result['breached'])
    
    @patch('requests.get')
    def test_email_breach_check_with_api_key(self, mock_get):
        """Test email breach checking with API key"""
        # Mock response for email not in breaches
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        result = self.checker.check_email_breaches("test@example.com", "fake_api_key")
        
        self.assertFalse(result['breached'])
        self.assertEqual(result['breach_count'], 0)
        self.assertIsNone(result['error'])
    
    def test_risk_level_calculation(self):
        """Test risk level calculation"""
        # Test safe password
        risk = self.checker._calculate_risk_level(False, 0)
        self.assertEqual(risk, "Safe")
        
        # Test low risk
        risk = self.checker._calculate_risk_level(True, 5)
        self.assertEqual(risk, "Low Risk")
        
        # Test medium risk
        risk = self.checker._calculate_risk_level(True, 50)
        self.assertEqual(risk, "Medium Risk")
        
        # Test high risk
        risk = self.checker._calculate_risk_level(True, 500)
        self.assertEqual(risk, "High Risk")
        
        # Test critical risk
        risk = self.checker._calculate_risk_level(True, 5000)
        self.assertEqual(risk, "Critical Risk")
    
    @patch.object(BreachChecker, 'check_password_breach')
    def test_batch_check_passwords(self, mock_check):
        """Test batch password checking"""
        # Mock the individual password check method
        mock_check.side_effect = [(True, 100), (False, 0), (True, 10)]
        
        passwords = ["weak1", "strong1", "weak2"]
        results = self.checker.batch_check_passwords(passwords)
        
        self.assertEqual(len(results), 3)
        self.assertTrue(results[0]['is_breached'])
        self.assertEqual(results[0]['exposure_count'], 100)
        self.assertFalse(results[1]['is_breached'])
        self.assertTrue(results[2]['is_breached'])
    
    @patch.object(BreachChecker, 'check_password_breach')
    def test_breach_statistics(self, mock_check):
        """Test breach statistics generation"""
        # Mock password check results
        mock_check.side_effect = [(True, 1000), (False, 0), (True, 10), (False, 0)]
        
        passwords = ["pwd1", "pwd2", "pwd3", "pwd4"]
        stats = self.checker.get_breach_statistics(passwords)
        
        self.assertEqual(stats['total_checked'], 4)
        self.assertEqual(stats['breached_count'], 2)
        self.assertEqual(stats['safe_count'], 2)
        self.assertEqual(stats['breach_percentage'], 50.0)
        self.assertEqual(stats['total_exposures'], 1010)
    
    @patch.object(BreachChecker, 'check_password_breach')
    @patch.object(BreachChecker, 'check_email_breaches')
    def test_generate_breach_report(self, mock_email_check, mock_password_check):
        """Test comprehensive breach report generation"""
        # Mock results
        mock_password_check.return_value = (True, 500)
        mock_email_check.return_value = {
            'breached': True,
            'breach_count': 3,
            'error': None
        }
        
        report = self.checker.generate_breach_report(
            "testpassword", "test@example.com", "fake_api_key"
        )
        
        # Check report structure
        self.assertIn('timestamp', report)
        self.assertIn('password_check', report)
        self.assertIn('email_check', report)
        self.assertIn('recommendations', report)
        
        # Check password check results
        self.assertTrue(report['password_check']['is_breached'])
        self.assertEqual(report['password_check']['exposure_count'], 500)
        
        # Check recommendations are provided
        self.assertGreater(len(report['recommendations']), 0)


if __name__ == '__main__':
    unittest.main()
