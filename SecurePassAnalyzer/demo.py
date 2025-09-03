"""
Quick Demo Script for SecurePass Analyzer
Tests core functionality without Streamlit interface
"""

import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from password_analyzer import PasswordAnalyzer
from breach_checker import BreachChecker
from password_generator import PasswordGenerator


def main():
    print("🔐 SecurePass Analyzer - Quick Demo")
    print("="*50)
    
    # Initialize components
    analyzer = PasswordAnalyzer()
    generator = PasswordGenerator()
    checker = BreachChecker()
    
    # 1. Generate a password
    print("\n1. 🎲 Generating a secure password...")
    password = generator.generate_random(16, use_symbols=True)
    print(f"   Generated: {password}")
    
    # 2. Analyze the password
    print("\n2. 🔍 Analyzing password strength...")
    analysis = analyzer.analyze(password)
    print(f"   Score: {analysis['score']}/100")
    print(f"   Strength: {analysis['strength']}")
    print(f"   Entropy: {analysis['entropy_bits']} bits")
    
    # Show character diversity
    diversity = analysis['character_diversity']
    types_present = sum(diversity.values())
    print(f"   Character types used: {types_present}/5")
    
    # 3. Check for breaches
    print("\n3. ⚠️ Checking for data breaches...")
    try:
        is_breached, count = checker.check_password_breach(password)
        if is_breached:
            print(f"   ❌ Found in {count:,} breaches!")
        else:
            print("   ✅ Not found in any known breaches")
    except Exception as e:
        print(f"   ⚠️ Could not check breaches: {e}")
    
    # 4. Show recommendations
    print("\n4. 💡 Recommendations:")
    for i, rec in enumerate(analysis['recommendations'][:3], 1):
        print(f"   {i}. {rec}")
    
    # 5. Generate different types of passwords
    print("\n5. 🎯 Different password types:")
    
    examples = [
        ("Memorable", lambda: generator.generate_memorable(4)),
        ("Pronounceable", lambda: generator.generate_pronounceable(12)),
        ("Passphrase", lambda: generator.generate_passphrase(5)),
        ("Custom Pattern", lambda: generator.generate_custom_pattern("LLLLdddd!@"))
    ]
    
    for name, func in examples:
        try:
            pwd = func()
            strength = generator.estimate_strength(pwd)['strength']
            print(f"   {name}: {pwd} ({strength})")
        except Exception as e:
            print(f"   {name}: Error - {e}")
    
    print("\n" + "="*50)
    print("Demo completed! 🎉")
    print("\nTo run the full interactive application:")
    print("   streamlit run app.py")
    print("\nTo run unit tests:")
    print("   python tests/run_tests.py")
    print("\nTo see detailed examples:")
    print("   python docs/examples.py")


if __name__ == "__main__":
    main()
