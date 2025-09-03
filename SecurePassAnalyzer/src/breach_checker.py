"""
Data Breach Checker Module
Checks passwords and emails against the Have I Been Pwned (HIBP) database
Uses k-anonymity to securely check passwords without sending them in plaintext
"""

import hashlib
import requests
from typing import Dict, List, Optional, Tuple
import time

class BreachChecker:
    """Check passwords and emails against known data breaches"""
    
    def __init__(self):
        self.hibp_password_api = "https://api.pwnedpasswords.com/range/"
        self.hibp_breach_api = "https://haveibeenpwned.com/api/v3/breachedaccount/"
        self.hibp_paste_api = "https://haveibeenpwned.com/api/v3/pasteaccount/"
        self.headers = {
            'User-Agent': 'SecurePass-Analyzer-1.0'
        }
        
    def check_password_breach(self, password: str) -> Tuple[bool, int]:
        """
        Check if password has been found in data breaches using k-anonymity
        Returns: (is_breached, number_of_times_seen)
        """
        try:
            # Create SHA-1 hash of the password
            sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
            
            # Take first 5 characters for k-anonymity
            prefix = sha1_hash[:5]
            suffix = sha1_hash[5:]
            
            # Query the API
            response = requests.get(
                f"{self.hibp_password_api}{prefix}",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code != 200:
                print(f"API Error: Status {response.status_code}")
                return False, 0
            
            # Check if our hash suffix appears in the results
            hashes = response.text.split('\r\n')
            for hash_entry in hashes:
                if ':' in hash_entry:
                    hash_suffix, count = hash_entry.split(':')
                    if hash_suffix == suffix:
                        return True, int(count)
            
            return False, 0
            
        except requests.exceptions.RequestException as e:
            print(f"Network error checking password breach: {e}")
            return False, 0
        except Exception as e:
            print(f"Error checking password breach: {e}")
            return False, 0
    
    def check_email_breaches(self, email: str, api_key: Optional[str] = None) -> Dict:
        """
        Check if email has been found in data breaches
        Note: Requires HIBP API key for authenticated requests
        """
        result = {
            'email': email,
            'breached': False,
            'breach_count': 0,
            'breaches': [],
            'error': None
        }
        
        if not api_key:
            result['error'] = "API key required for email breach checking (get one at haveibeenpwned.com/API/Key)"
            return result
        
        try:
            headers = self.headers.copy()
            headers['hibp-api-key'] = api_key
            
            response = requests.get(
                f"{self.hibp_breach_api}{email}",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 404:
                # No breaches found
                return result
            elif response.status_code == 200:
                breaches = response.json()
                result['breached'] = True
                result['breach_count'] = len(breaches)
                
                # Extract relevant breach information
                for breach in breaches:
                    result['breaches'].append({
                        'name': breach.get('Name', 'Unknown'),
                        'domain': breach.get('Domain', 'Unknown'),
                        'date': breach.get('BreachDate', 'Unknown'),
                        'data_types': breach.get('DataClasses', []),
                        'verified': breach.get('IsVerified', False),
                        'description': breach.get('Description', '')[:200]  # Truncate description
                    })
                    
            else:
                result['error'] = f"API Error: Status {response.status_code}"
                
        except requests.exceptions.RequestException as e:
            result['error'] = f"Network error: {str(e)}"
        except Exception as e:
            result['error'] = f"Error checking email breaches: {str(e)}"
        
        return result
    
    def batch_check_passwords(self, passwords: List[str]) -> List[Dict]:
        """
        Check multiple passwords for breaches
        Includes rate limiting to respect API limits
        """
        results = []
        
        for password in passwords:
            is_breached, count = self.check_password_breach(password)
            results.append({
                'password': '•' * len(password),  # Masked for security
                'is_breached': is_breached,
                'exposure_count': count,
                'risk_level': self._calculate_risk_level(is_breached, count)
            })
            
            # Rate limiting: 1 request per 1.5 seconds
            time.sleep(1.5)
        
        return results
    
    def _calculate_risk_level(self, is_breached: bool, exposure_count: int) -> str:
        """Calculate risk level based on breach exposure"""
        if not is_breached:
            return "Safe"
        elif exposure_count < 10:
            return "Low Risk"
        elif exposure_count < 100:
            return "Medium Risk"
        elif exposure_count < 1000:
            return "High Risk"
        else:
            return "Critical Risk"
    
    def get_breach_statistics(self, passwords: List[str]) -> Dict:
        """Generate statistics for a set of passwords"""
        total = len(passwords)
        breached_count = 0
        total_exposures = 0
        risk_distribution = {
            'Safe': 0,
            'Low Risk': 0,
            'Medium Risk': 0,
            'High Risk': 0,
            'Critical Risk': 0
        }
        
        for password in passwords:
            is_breached, count = self.check_password_breach(password)
            if is_breached:
                breached_count += 1
                total_exposures += count
            
            risk_level = self._calculate_risk_level(is_breached, count)
            risk_distribution[risk_level] += 1
            
            time.sleep(1.5)  # Rate limiting
        
        return {
            'total_checked': total,
            'breached_count': breached_count,
            'safe_count': total - breached_count,
            'breach_percentage': (breached_count / total * 100) if total > 0 else 0,
            'total_exposures': total_exposures,
            'average_exposures': total_exposures / breached_count if breached_count > 0 else 0,
            'risk_distribution': risk_distribution
        }
    
    def generate_breach_report(self, password: str, email: Optional[str] = None, 
                              api_key: Optional[str] = None) -> Dict:
        """Generate a comprehensive breach report for a password and optionally an email"""
        report = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'password_check': {},
            'email_check': None,
            'recommendations': []
        }
        
        # Check password
        is_breached, count = self.check_password_breach(password)
        report['password_check'] = {
            'checked': True,
            'is_breached': is_breached,
            'exposure_count': count,
            'risk_level': self._calculate_risk_level(is_breached, count)
        }
        
        # Check email if provided
        if email:
            report['email_check'] = self.check_email_breaches(email, api_key)
        
        # Generate recommendations
        if is_breached:
            report['recommendations'].append(f"⚠️ This password has been exposed {count:,} times in data breaches!")
            report['recommendations'].append("🔄 Change this password immediately")
            report['recommendations'].append("🔑 Use a unique password for each account")
            report['recommendations'].append("🛡️ Enable two-factor authentication where possible")
            
            if count > 1000:
                report['recommendations'].append("⛔ This is an extremely common password - never use it again")
        else:
            report['recommendations'].append("✅ Password not found in known breaches")
            report['recommendations'].append("💡 Still, consider using a password manager")
            report['recommendations'].append("🔐 Regularly update your passwords")
        
        if email and report['email_check'] and report['email_check']['breached']:
            breach_count = report['email_check']['breach_count']
            report['recommendations'].append(f"📧 Your email was found in {breach_count} breach(es)")
            report['recommendations'].append("🔍 Review the affected services and update passwords")
            report['recommendations'].append("📬 Watch for phishing attempts targeting this email")
        
        return report


if __name__ == "__main__":
    # Test the breach checker
    checker = BreachChecker()
    
    # Test password breach checking
    test_passwords = ["password123", "MyS3cur3P@ssw0rd2024!", "qwerty"]
    
    print("Testing Password Breach Checker:\n")
    for pwd in test_passwords:
        is_breached, count = checker.check_password_breach(pwd)
        masked_pwd = pwd[:2] + '*' * (len(pwd) - 4) + pwd[-2:] if len(pwd) > 4 else '*' * len(pwd)
        if is_breached:
            print(f"❌ Password '{masked_pwd}' found {count:,} times in breaches")
        else:
            print(f"✅ Password '{masked_pwd}' not found in breaches")
    
    print("\n" + "="*50)
    print("Note: For email checking, you'll need an API key from haveibeenpwned.com")
