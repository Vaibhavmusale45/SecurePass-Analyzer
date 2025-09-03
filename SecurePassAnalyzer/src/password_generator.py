"""
Secure Password Generator Module
Generates strong, customizable passwords with various complexity rules
Includes memorable password options and pronounceable passwords
"""

import random
import string
import secrets
from typing import List, Dict, Optional
import json

class PasswordGenerator:
    """Generate secure passwords with customizable rules"""
    
    def __init__(self):
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        # Word lists for memorable passwords
        self.adjectives = [
            "happy", "brave", "quick", "smart", "bright", "strong", "swift", "bold",
            "fierce", "gentle", "mighty", "noble", "proud", "royal", "sharp", "wise"
        ]
        
        self.nouns = [
            "eagle", "tiger", "mountain", "ocean", "thunder", "lightning", "dragon",
            "phoenix", "warrior", "hunter", "guardian", "champion", "legend", "hero"
        ]
        
        self.verbs = [
            "runs", "flies", "jumps", "fights", "guards", "protects", "strikes",
            "soars", "climbs", "dives", "hunts", "explores", "conquers", "defends"
        ]
        
    def generate_random(self, length: int = 16, 
                       use_lowercase: bool = True,
                       use_uppercase: bool = True,
                       use_digits: bool = True,
                       use_symbols: bool = True,
                       exclude_ambiguous: bool = False,
                       exclude_chars: str = "") -> str:
        """Generate a random password with specified criteria"""
        
        if length < 4:
            raise ValueError("Password length must be at least 4 characters")
        
        # Build character pool
        char_pool = ""
        required_chars = []
        
        if use_lowercase:
            chars = self.lowercase
            if exclude_ambiguous:
                chars = chars.replace('l', '').replace('o', '')
            char_pool += chars
            required_chars.append(secrets.choice(chars))
            
        if use_uppercase:
            chars = self.uppercase
            if exclude_ambiguous:
                chars = chars.replace('O', '').replace('I', '')
            char_pool += chars
            required_chars.append(secrets.choice(chars))
            
        if use_digits:
            chars = self.digits
            if exclude_ambiguous:
                chars = chars.replace('0', '').replace('1', '')
            char_pool += chars
            required_chars.append(secrets.choice(chars))
            
        if use_symbols:
            char_pool += self.symbols
            required_chars.append(secrets.choice(self.symbols))
        
        # Remove excluded characters
        for char in exclude_chars:
            char_pool = char_pool.replace(char, '')
        
        if not char_pool:
            raise ValueError("No characters available with the specified criteria")
        
        # Generate password
        # Ensure at least one character from each selected category
        password = required_chars.copy()
        
        # Fill the rest randomly
        remaining_length = length - len(password)
        for _ in range(remaining_length):
            password.append(secrets.choice(char_pool))
        
        # Shuffle to avoid predictable patterns
        random.shuffle(password)
        
        return ''.join(password)
    
    def generate_memorable(self, word_count: int = 4, 
                          add_numbers: bool = True,
                          add_symbols: bool = True,
                          capitalize: bool = True) -> str:
        """Generate a memorable password using word combinations"""
        
        if word_count < 2:
            word_count = 2
        
        words = []
        
        # Create a pattern of words
        for i in range(word_count):
            if i % 3 == 0:
                word = secrets.choice(self.adjectives)
            elif i % 3 == 1:
                word = secrets.choice(self.nouns)
            else:
                word = secrets.choice(self.verbs)
            
            if capitalize and i % 2 == 0:
                word = word.capitalize()
                
            words.append(word)
        
        password = ''.join(words)
        
        if add_numbers:
            # Add random 2-4 digit number
            num_digits = secrets.choice([2, 3, 4])
            number = ''.join([str(secrets.randbelow(10)) for _ in range(num_digits)])
            password += number
        
        if add_symbols:
            # Add 1-2 random symbols
            num_symbols = secrets.choice([1, 2])
            symbols = ''.join([secrets.choice(self.symbols) for _ in range(num_symbols)])
            password += symbols
        
        return password
    
    def generate_pronounceable(self, length: int = 12, 
                              add_numbers: bool = True,
                              add_symbols: bool = False) -> str:
        """Generate a pronounceable password using syllable patterns"""
        
        consonants = 'bcdfghjklmnpqrstvwxyz'
        vowels = 'aeiou'
        
        password = ""
        
        # Create syllables (consonant-vowel or consonant-vowel-consonant patterns)
        while len(password) < length - (4 if add_numbers else 0) - (2 if add_symbols else 0):
            pattern = secrets.choice(['cv', 'cvc', 'vc'])
            syllable = ""
            
            for char in pattern:
                if char == 'c':
                    syllable += secrets.choice(consonants)
                else:  # vowel
                    syllable += secrets.choice(vowels)
            
            # Occasionally capitalize
            if len(password) == 0 or secrets.randbelow(3) == 0:
                syllable = syllable.capitalize()
                
            password += syllable
        
        # Trim to exact length
        password = password[:length - (4 if add_numbers else 0) - (2 if add_symbols else 0)]
        
        if add_numbers:
            password += ''.join([str(secrets.randbelow(10)) for _ in range(4)])
        
        if add_symbols:
            password += ''.join([secrets.choice(self.symbols) for _ in range(2)])
        
        return password
    
    def generate_passphrase(self, word_count: int = 6, 
                           separator: str = "-",
                           capitalize_words: bool = False) -> str:
        """Generate a passphrase using random words"""
        
        # Extended word list for passphrases
        word_list = (self.adjectives + self.nouns + 
                    ["book", "tree", "river", "cloud", "star", "moon", "sun",
                     "fire", "water", "earth", "wind", "stone", "crystal",
                     "shadow", "light", "dream", "spirit", "heart", "soul"])
        
        words = []
        for _ in range(word_count):
            word = secrets.choice(word_list)
            if capitalize_words:
                word = word.capitalize()
            words.append(word)
        
        return separator.join(words)
    
    def generate_custom_pattern(self, pattern: str) -> str:
        """
        Generate password based on a pattern string
        Pattern characters:
        - l: lowercase letter
        - L: uppercase letter
        - d: digit
        - s: symbol
        - a: any alphanumeric
        - *: any character
        Example: "LLLLdddd!!" generates like "ABCD1234!!"
        """
        
        password = ""
        
        for char in pattern:
            if char == 'l':
                password += secrets.choice(self.lowercase)
            elif char == 'L':
                password += secrets.choice(self.uppercase)
            elif char == 'd':
                password += secrets.choice(self.digits)
            elif char == 's':
                password += secrets.choice(self.symbols)
            elif char == 'a':
                password += secrets.choice(self.lowercase + self.uppercase + self.digits)
            elif char == '*':
                password += secrets.choice(self.lowercase + self.uppercase + 
                                          self.digits + self.symbols)
            else:
                # Literal character
                password += char
        
        return password
    
    def batch_generate(self, count: int = 5, **kwargs) -> List[str]:
        """Generate multiple passwords with the same criteria"""
        
        passwords = []
        for _ in range(count):
            passwords.append(self.generate_random(**kwargs))
        
        return passwords
    
    def get_password_suggestions(self, purpose: str = "general") -> Dict:
        """Get password suggestions based on purpose"""
        
        suggestions = {
            "general": {
                "length": 16,
                "pattern": "Random with all character types",
                "example": self.generate_random(16),
                "strength": "Strong"
            },
            "high_security": {
                "length": 24,
                "pattern": "Random with all character types",
                "example": self.generate_random(24),
                "strength": "Very Strong"
            },
            "memorable": {
                "length": 20,
                "pattern": "Word combination with numbers and symbols",
                "example": self.generate_memorable(),
                "strength": "Strong"
            },
            "passphrase": {
                "length": 30,
                "pattern": "Multiple words separated by hyphens",
                "example": self.generate_passphrase(),
                "strength": "Very Strong"
            },
            "pin": {
                "length": 6,
                "pattern": "Digits only",
                "example": self.generate_random(6, use_lowercase=False, 
                                               use_uppercase=False, 
                                               use_symbols=False),
                "strength": "Weak (for PINs only)"
            }
        }
        
        return suggestions.get(purpose, suggestions["general"])
    
    def estimate_strength(self, password: str) -> Dict:
        """Quick strength estimation for generated passwords"""
        
        length = len(password)
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_symbol = any(c in self.symbols for c in password)
        
        # Calculate charset size
        charset_size = 0
        if has_lower:
            charset_size += 26
        if has_upper:
            charset_size += 26
        if has_digit:
            charset_size += 10
        if has_symbol:
            charset_size += len(self.symbols)
        
        # Calculate entropy
        import math
        entropy = length * math.log2(charset_size) if charset_size > 0 else 0
        
        # Determine strength
        if entropy >= 60:
            strength = "Very Strong"
        elif entropy >= 40:
            strength = "Strong"
        elif entropy >= 30:
            strength = "Moderate"
        else:
            strength = "Weak"
        
        return {
            "entropy": round(entropy, 2),
            "strength": strength,
            "charset_size": charset_size,
            "length": length
        }


if __name__ == "__main__":
    # Test the generator
    generator = PasswordGenerator()
    
    print("Password Generator Examples:\n")
    print("="*50)
    
    # Random password
    pwd = generator.generate_random(16)
    print(f"Random (16 chars): {pwd}")
    print(f"Strength: {generator.estimate_strength(pwd)['strength']}\n")
    
    # Memorable password
    pwd = generator.generate_memorable()
    print(f"Memorable: {pwd}")
    print(f"Strength: {generator.estimate_strength(pwd)['strength']}\n")
    
    # Pronounceable password
    pwd = generator.generate_pronounceable()
    print(f"Pronounceable: {pwd}")
    print(f"Strength: {generator.estimate_strength(pwd)['strength']}\n")
    
    # Passphrase
    pwd = generator.generate_passphrase()
    print(f"Passphrase: {pwd}")
    print(f"Strength: {generator.estimate_strength(pwd)['strength']}\n")
    
    # Custom pattern
    pwd = generator.generate_custom_pattern("LLLLdddd@@")
    print(f"Custom Pattern (LLLLdddd@@): {pwd}")
    print(f"Strength: {generator.estimate_strength(pwd)['strength']}\n")
    
    print("="*50)
    print("\nPassword Suggestions by Purpose:")
    for purpose in ["general", "high_security", "memorable", "passphrase"]:
        suggestion = generator.get_password_suggestions(purpose)
        print(f"\n{purpose.upper()}:")
        print(f"  Example: {suggestion['example']}")
        print(f"  Strength: {suggestion['strength']}")
