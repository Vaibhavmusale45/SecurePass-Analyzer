"""
Unit tests for password_analyzer module
"""

import unittest
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from password_analyzer import PasswordAnalyzer


class TestPasswordAnalyzer(unittest.TestCase):
    """Test cases for PasswordAnalyzer class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.analyzer = PasswordAnalyzer()
    
    def test_entropy_calculation(self):
        """Test entropy calculation for different passwords"""
        # Test basic entropy calculation
        entropy = self.analyzer.calculate_entropy("abc123")
        self.assertGreater(entropy, 0)
        
        # More complex password should have higher entropy
        simple_entropy = self.analyzer.calculate_entropy("password")
        complex_entropy = self.analyzer.calculate_entropy("P@ssW0rd!123")
        self.assertGreater(complex_entropy, simple_entropy)
    
    def test_pattern_detection(self):
        """Test pattern detection functionality"""
        # Test sequential numbers
        patterns = self.analyzer.check_patterns("password123")
        self.assertTrue(patterns['sequential_numbers'])
        
        # Test keyboard pattern
        patterns = self.analyzer.check_patterns("qwerty123")
        self.assertTrue(patterns['keyboard_pattern'])
        
        # Test repeated characters
        patterns = self.analyzer.check_patterns("aaa123")
        self.assertTrue(patterns['repeated_characters'])
        
        # Test common password
        patterns = self.analyzer.check_patterns("password")
        self.assertTrue(patterns['common_word'])
    
    def test_character_diversity(self):
        """Test character diversity analysis"""
        # Test password with all character types
        diversity = self.analyzer.get_character_diversity("Abc123!@#")
        self.assertTrue(diversity['has_lowercase'])
        self.assertTrue(diversity['has_uppercase'])
        self.assertTrue(diversity['has_numbers'])
        self.assertTrue(diversity['has_symbols'])
        
        # Test password with only lowercase
        diversity = self.analyzer.get_character_diversity("abcdef")
        self.assertTrue(diversity['has_lowercase'])
        self.assertFalse(diversity['has_uppercase'])
        self.assertFalse(diversity['has_numbers'])
        self.assertFalse(diversity['has_symbols'])
    
    def test_score_calculation(self):
        """Test password score calculation"""
        # Very weak password
        score, strength = self.analyzer.calculate_score("123")
        self.assertLess(score, 30)
        self.assertEqual(strength, "Very Weak")
        
        # Strong password
        score, strength = self.analyzer.calculate_score("MyVerySecur3P@ssword!")
        self.assertGreater(score, 60)
        self.assertIn(strength, ["Strong", "Very Strong"])
        
        # Empty password
        score, strength = self.analyzer.calculate_score("")
        self.assertEqual(score, 0)
        self.assertEqual(strength, "Empty")
    
    def test_full_analysis(self):
        """Test complete password analysis"""
        analysis = self.analyzer.analyze("TestP@ssw0rd123!")
        
        # Check required fields are present
        required_fields = [
            'password_length', 'score', 'strength', 'entropy_bits',
            'patterns_found', 'character_diversity', 'crack_time_estimates',
            'recommendations', 'zxcvbn_score'
        ]
        
        for field in required_fields:
            self.assertIn(field, analysis)
        
        # Check score is within valid range
        self.assertGreaterEqual(analysis['score'], 0)
        self.assertLessEqual(analysis['score'], 100)
        
        # Check recommendations are provided
        self.assertIsInstance(analysis['recommendations'], list)
    
    def test_recommendations_generation(self):
        """Test recommendation generation"""
        # Test weak password gets recommendations
        patterns = {
            'sequential_numbers': True, 'sequential_letters': False, 
            'repeated_characters': False, 'keyboard_pattern': False, 
            'common_word': True, 'date_pattern': False
        }
        diversity = {
            'has_lowercase': True, 'has_uppercase': False, 
            'has_numbers': True, 'has_symbols': False, 'has_spaces': False
        }
        recommendations = self.analyzer.generate_recommendations(
            "password123", patterns, diversity
        )
        
        self.assertGreater(len(recommendations), 0)
        self.assertTrue(any("uppercase" in rec.lower() for rec in recommendations))
        self.assertTrue(any("symbols" in rec.lower() for rec in recommendations))


if __name__ == '__main__':
    unittest.main()
