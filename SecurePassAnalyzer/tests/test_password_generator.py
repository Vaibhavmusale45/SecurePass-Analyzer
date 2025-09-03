"""
Unit tests for password_generator module
"""

import unittest
import sys
import os
import string

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from password_generator import PasswordGenerator


class TestPasswordGenerator(unittest.TestCase):
    """Test cases for PasswordGenerator class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.generator = PasswordGenerator()
    
    def test_random_password_generation(self):
        """Test random password generation with various options"""
        # Test basic generation
        password = self.generator.generate_random(12)
        self.assertEqual(len(password), 12)
        
        # Test with specific character types
        password = self.generator.generate_random(
            16, use_lowercase=True, use_uppercase=True,
            use_digits=True, use_symbols=True
        )
        self.assertEqual(len(password), 16)
        self.assertTrue(any(c.islower() for c in password))
        self.assertTrue(any(c.isupper() for c in password))
        self.assertTrue(any(c.isdigit() for c in password))
        self.assertTrue(any(c in self.generator.symbols for c in password))
        
        # Test with only lowercase
        password = self.generator.generate_random(
            10, use_lowercase=True, use_uppercase=False,
            use_digits=False, use_symbols=False
        )
        self.assertEqual(len(password), 10)
        self.assertTrue(all(c.islower() for c in password))
    
    def test_memorable_password_generation(self):
        """Test memorable password generation"""
        password = self.generator.generate_memorable(word_count=3)
        self.assertGreater(len(password), 0)
        
        # Test with specific options
        password = self.generator.generate_memorable(
            word_count=4, add_numbers=True, add_symbols=True, capitalize=True
        )
        self.assertGreater(len(password), 10)
        self.assertTrue(any(c.isdigit() for c in password))
        self.assertTrue(any(c in self.generator.symbols for c in password))
    
    def test_pronounceable_password_generation(self):
        """Test pronounceable password generation"""
        password = self.generator.generate_pronounceable(12)
        self.assertGreaterEqual(len(password), 8)  # Might be slightly shorter due to syllable patterns
        
        # Test with numbers and symbols
        password = self.generator.generate_pronounceable(
            16, add_numbers=True, add_symbols=True
        )
        self.assertTrue(any(c.isdigit() for c in password))
        self.assertTrue(any(c in self.generator.symbols for c in password))
    
    def test_passphrase_generation(self):
        """Test passphrase generation"""
        passphrase = self.generator.generate_passphrase(word_count=4)
        self.assertGreater(len(passphrase), 0)
        self.assertIn("-", passphrase)  # Default separator
        
        # Test with custom separator
        passphrase = self.generator.generate_passphrase(
            word_count=3, separator="_", capitalize_words=True
        )
        self.assertIn("_", passphrase)
        # Should have at least one capitalized word
        words = passphrase.split("_")
        self.assertTrue(any(word[0].isupper() for word in words if word))
    
    def test_custom_pattern_generation(self):
        """Test custom pattern generation"""
        # Test basic pattern
        password = self.generator.generate_custom_pattern("LLLLdddd")
        self.assertEqual(len(password), 8)
        self.assertTrue(password[:4].isupper())
        self.assertTrue(password[4:].isdigit())
        
        # Test pattern with literals
        password = self.generator.generate_custom_pattern("LLdd@@")
        self.assertEqual(len(password), 6)
        self.assertEqual(password[-2:], "@@")
        
        # Test mixed pattern
        password = self.generator.generate_custom_pattern("Lldls*")
        self.assertEqual(len(password), 6)
        self.assertTrue(password[0].isupper())
        self.assertTrue(password[1].islower())
        self.assertTrue(password[2].isdigit())
    
    def test_batch_generation(self):
        """Test batch password generation"""
        passwords = self.generator.batch_generate(count=5, length=12)
        self.assertEqual(len(passwords), 5)
        
        # All passwords should be unique
        self.assertEqual(len(set(passwords)), 5)
        
        # All passwords should be the correct length
        for password in passwords:
            self.assertEqual(len(password), 12)
    
    def test_password_suggestions(self):
        """Test password suggestions for different purposes"""
        # Test general purpose
        suggestion = self.generator.get_password_suggestions("general")
        self.assertIn("length", suggestion)
        self.assertIn("example", suggestion)
        self.assertIn("strength", suggestion)
        
        # Test high security
        suggestion = self.generator.get_password_suggestions("high_security")
        self.assertGreater(suggestion["length"], 20)
        
        # Test memorable
        suggestion = self.generator.get_password_suggestions("memorable")
        self.assertIn("example", suggestion)
    
    def test_strength_estimation(self):
        """Test quick strength estimation"""
        # Test weak password
        estimation = self.generator.estimate_strength("123456")
        self.assertEqual(estimation["strength"], "Weak")
        
        # Test strong password
        estimation = self.generator.estimate_strength("MyVerySecur3P@ssword!")
        self.assertIn(estimation["strength"], ["Strong", "Very Strong"])
        
        # Check estimation includes required fields
        required_fields = ["entropy", "strength", "charset_size", "length"]
        for field in required_fields:
            self.assertIn(field, estimation)
    
    def test_error_handling(self):
        """Test error handling for invalid inputs"""
        # Test minimum length requirement
        with self.assertRaises(ValueError):
            self.generator.generate_random(3)  # Too short
        
        # Test no character types selected
        with self.assertRaises(ValueError):
            self.generator.generate_random(
                10, use_lowercase=False, use_uppercase=False,
                use_digits=False, use_symbols=False
            )


if __name__ == '__main__':
    unittest.main()
