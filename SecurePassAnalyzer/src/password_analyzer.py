"""
Password Strength Analyzer Module
Analyzes password strength using multiple metrics including entropy, patterns, and common weaknesses
"""

import re
import math
from typing import Dict, List, Tuple
import zxcvbn

class PasswordAnalyzer:
    """Advanced password strength analyzer with multiple security metrics"""
    
    def __init__(self):
        self.common_passwords = self._load_common_passwords()
        self.keyboard_patterns = [
            'qwerty', 'asdf', 'zxcv', '1234', '0987',
            'qwertyuiop', 'asdfghjkl', 'zxcvbnm'
        ]
        
    def _load_common_passwords(self) -> set:
        """Load a set of common passwords to check against"""
        # In production, this would load from a file
        return {
            'password', '123456', 'password123', 'admin', 'letmein',
            'welcome', 'monkey', '1234567890', 'qwerty', 'abc123',
            'Password1', 'password1', '123456789', 'welcome123'
        }
    
    def calculate_entropy(self, password: str) -> float:
        """Calculate password entropy in bits"""
        charset_size = 0
        
        if re.search(r'[a-z]', password):
            charset_size += 26
        if re.search(r'[A-Z]', password):
            charset_size += 26
        if re.search(r'[0-9]', password):
            charset_size += 10
        if re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', password):
            charset_size += 32
            
        if charset_size == 0:
            return 0
            
        entropy = len(password) * math.log2(charset_size)
        return round(entropy, 2)
    
    def check_patterns(self, password: str) -> Dict[str, bool]:
        """Check for common patterns in password"""
        patterns = {
            'sequential_numbers': bool(re.search(r'(012|123|234|345|456|567|678|789|890)', password.lower())),
            'sequential_letters': bool(re.search(r'(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)', password.lower())),
            'repeated_characters': bool(re.search(r'(.)\1{2,}', password)),
            'keyboard_pattern': any(pattern in password.lower() for pattern in self.keyboard_patterns),
            'common_word': password.lower() in self.common_passwords,
            'date_pattern': bool(re.search(r'\d{2,4}[-/]\d{2}[-/]\d{2,4}|\d{6,8}', password))
        }
        return patterns
    
    def get_character_diversity(self, password: str) -> Dict[str, bool]:
        """Analyze character type diversity"""
        return {
            'has_lowercase': bool(re.search(r'[a-z]', password)),
            'has_uppercase': bool(re.search(r'[A-Z]', password)),
            'has_numbers': bool(re.search(r'[0-9]', password)),
            'has_symbols': bool(re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', password)),
            'has_spaces': ' ' in password
        }
    
    def calculate_score(self, password: str) -> Tuple[int, str]:
        """Calculate overall password score (0-100) and strength level"""
        if not password:
            return 0, "Empty"
            
        score = 0
        
        # Length scoring (max 30 points)
        length = len(password)
        if length >= 16:
            score += 30
        elif length >= 12:
            score += 25
        elif length >= 8:
            score += 15
        else:
            score += max(0, length * 2)
        
        # Entropy scoring (max 30 points)
        entropy = self.calculate_entropy(password)
        if entropy >= 60:
            score += 30
        elif entropy >= 40:
            score += 20
        elif entropy >= 25:
            score += 10
        else:
            score += max(0, int(entropy / 2))
        
        # Character diversity (max 20 points)
        diversity = self.get_character_diversity(password)
        score += sum([5 for value in diversity.values() if value])
        
        # Pattern penalties (max -30 points)
        patterns = self.check_patterns(password)
        penalties = {
            'sequential_numbers': -5,
            'sequential_letters': -5,
            'repeated_characters': -10,
            'keyboard_pattern': -10,
            'common_word': -20,
            'date_pattern': -5
        }
        
        for pattern, has_pattern in patterns.items():
            if has_pattern:
                score += penalties.get(pattern, 0)
        
        # Use zxcvbn for additional analysis (max 20 points)
        zxcvbn_result = zxcvbn.zxcvbn(password)
        score += zxcvbn_result['score'] * 4
        
        # Ensure score is between 0 and 100
        score = max(0, min(100, score))
        
        # Determine strength level
        if score >= 80:
            strength = "Very Strong"
        elif score >= 60:
            strength = "Strong"
        elif score >= 40:
            strength = "Moderate"
        elif score >= 20:
            strength = "Weak"
        else:
            strength = "Very Weak"
            
        return score, strength
    
    def analyze(self, password: str) -> Dict:
        """Perform complete password analysis"""
        score, strength = self.calculate_score(password)
        patterns = self.check_patterns(password)
        diversity = self.get_character_diversity(password)
        entropy = self.calculate_entropy(password)
        
        # Get zxcvbn analysis
        zxcvbn_result = zxcvbn.zxcvbn(password)
        
        # Time to crack estimates
        crack_times = {
            'offline_slow': zxcvbn_result['crack_times_display']['offline_slow_hashing_1e4_per_second'],
            'offline_fast': zxcvbn_result['crack_times_display']['offline_fast_hashing_1e10_per_second'],
            'online_throttled': zxcvbn_result['crack_times_display']['online_throttling_100_per_hour'],
            'online_unthrottled': zxcvbn_result['crack_times_display']['online_no_throttling_10_per_second']
        }
        
        # Generate recommendations
        recommendations = self.generate_recommendations(password, patterns, diversity)
        
        return {
            'password_length': len(password),
            'score': score,
            'strength': strength,
            'entropy_bits': entropy,
            'patterns_found': patterns,
            'character_diversity': diversity,
            'crack_time_estimates': crack_times,
            'recommendations': recommendations,
            'zxcvbn_score': zxcvbn_result['score'],
            'warning': zxcvbn_result.get('feedback', {}).get('warning', ''),
            'suggestions': zxcvbn_result.get('feedback', {}).get('suggestions', [])
        }
    
    def generate_recommendations(self, password: str, patterns: Dict, diversity: Dict) -> List[str]:
        """Generate specific recommendations for password improvement"""
        recommendations = []
        
        if len(password) < 12:
            recommendations.append("Increase password length to at least 12 characters")
        
        if not diversity['has_uppercase']:
            recommendations.append("Add uppercase letters")
        if not diversity['has_lowercase']:
            recommendations.append("Add lowercase letters")
        if not diversity['has_numbers']:
            recommendations.append("Include numbers")
        if not diversity['has_symbols']:
            recommendations.append("Add special symbols (!@#$%^&*)")
        
        if patterns['sequential_numbers']:
            recommendations.append("Avoid sequential numbers (123, 456)")
        if patterns['sequential_letters']:
            recommendations.append("Avoid sequential letters (abc, xyz)")
        if patterns['repeated_characters']:
            recommendations.append("Avoid repeating the same character multiple times")
        if patterns['keyboard_pattern']:
            recommendations.append("Avoid keyboard patterns (qwerty, asdf)")
        if patterns['common_word']:
            recommendations.append("This password is too common - choose something unique")
        if patterns['date_pattern']:
            recommendations.append("Avoid using dates as they're easy to guess")
        
        if not recommendations:
            recommendations.append("Great password! Consider using a password manager to store it securely.")
        
        return recommendations


if __name__ == "__main__":
    # Test the analyzer
    analyzer = PasswordAnalyzer()
    
    test_passwords = [
        "password123",
        "MyS3cur3P@ssw0rd!",
        "qwerty",
        "Tr0ub4dor&3",
        "CorrectHorseBatteryStaple"
    ]
    
    for pwd in test_passwords:
        print(f"\nAnalyzing: {pwd}")
        result = analyzer.analyze(pwd)
        print(f"Score: {result['score']}/100 - {result['strength']}")
        print(f"Entropy: {result['entropy_bits']} bits")
        print(f"Recommendations: {', '.join(result['recommendations'][:2])}")
