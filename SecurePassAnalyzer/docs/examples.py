"""
SecurePass Analyzer - Usage Examples
Demonstrates how to use all the features programmatically
"""

import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from password_analyzer import PasswordAnalyzer
from breach_checker import BreachChecker
from password_generator import PasswordGenerator


def demo_password_analysis():
    """Demonstrate password analysis features"""
    print("="*60)
    print("PASSWORD ANALYSIS DEMO")
    print("="*60)
    
    analyzer = PasswordAnalyzer()
    
    test_passwords = [
        ("password123", "Common weak password"),
        ("MyS3cur3P@ssw0rd!", "Mixed case with symbols"),
        ("correcthorsebatterystaple", "Long passphrase"),
        ("Tr0ub4dor&3", "XKCD famous password"),
        ("qwerty", "Keyboard pattern")
    ]
    
    for password, description in test_passwords:
        print(f"\nAnalyzing: {description}")
        print(f"Password: {'*' * len(password)}")  # Masked for security
        
        analysis = analyzer.analyze(password)
        
        print(f"Score: {analysis['score']}/100 ({analysis['strength']})")
        print(f"Entropy: {analysis['entropy_bits']} bits")
        print(f"Length: {analysis['password_length']} characters")
        
        # Show character diversity
        diversity = analysis['character_diversity']
        char_types = []
        if diversity['has_lowercase']: char_types.append("lowercase")
        if diversity['has_uppercase']: char_types.append("uppercase")
        if diversity['has_numbers']: char_types.append("numbers")
        if diversity['has_symbols']: char_types.append("symbols")
        print(f"Character types: {', '.join(char_types)}")
        
        # Show patterns found
        patterns_found = [k for k, v in analysis['patterns_found'].items() if v]
        if patterns_found:
            print(f"⚠️ Patterns found: {', '.join(patterns_found)}")
        
        # Show top recommendation
        if analysis['recommendations']:
            print(f"💡 Top recommendation: {analysis['recommendations'][0]}")
        
        print("-" * 40)


def demo_breach_checking():
    """Demonstrate breach checking features"""
    print("\n" + "="*60)
    print("BREACH CHECKING DEMO")
    print("="*60)
    
    checker = BreachChecker()
    
    # Note: These are known breached passwords for demonstration
    test_passwords = [
        ("password", "Very common password"),
        ("123456", "Sequential numbers"),
        ("admin", "Default admin password"),
        ("ThisIsAVerySecurePassword123!", "Custom strong password")
    ]
    
    for password, description in test_passwords:
        print(f"\nChecking: {description}")
        print(f"Password: {'*' * len(password)}")
        
        try:
            is_breached, count = checker.check_password_breach(password)
            
            if is_breached:
                risk_level = checker._calculate_risk_level(is_breached, count)
                print(f"⚠️ BREACHED: Found {count:,} times in data breaches")
                print(f"Risk level: {risk_level}")
            else:
                print("✅ SAFE: Not found in known breaches")
                
        except Exception as e:
            print(f"❌ Error checking password: {e}")
        
        print("-" * 40)
    
    print("\n🔒 Note: All password checking uses k-anonymity - your actual password")
    print("   is never sent to any server, only a partial hash is transmitted.")


def demo_password_generation():
    """Demonstrate password generation features"""
    print("\n" + "="*60)
    print("PASSWORD GENERATION DEMO")
    print("="*60)
    
    generator = PasswordGenerator()
    analyzer = PasswordAnalyzer()
    
    generation_methods = [
        ("Random 16-char", lambda: generator.generate_random(16)),
        ("Random 20-char high security", lambda: generator.generate_random(20, use_symbols=True)),
        ("Memorable", lambda: generator.generate_memorable(word_count=4)),
        ("Pronounceable", lambda: generator.generate_pronounceable(14)),
        ("Passphrase", lambda: generator.generate_passphrase(word_count=5)),
        ("Custom Pattern", lambda: generator.generate_custom_pattern("LLLLdddd!@"))
    ]
    
    for method_name, generation_func in generation_methods:
        print(f"\n{method_name}:")
        
        try:
            password = generation_func()
            print(f"Generated: {password}")
            
            # Quick analysis
            quick_analysis = generator.estimate_strength(password)
            print(f"Estimated strength: {quick_analysis['strength']}")
            print(f"Entropy: {quick_analysis['entropy']:.1f} bits")
            print(f"Character set size: {quick_analysis['charset_size']}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 40)
    
    # Batch generation example
    print("\nBatch Generation Example:")
    batch_passwords = generator.batch_generate(count=3, length=12)
    for i, pwd in enumerate(batch_passwords, 1):
        strength = generator.estimate_strength(pwd)['strength']
        print(f"{i}. {pwd} ({strength})")


def demo_complete_workflow():
    """Demonstrate a complete security analysis workflow"""
    print("\n" + "="*60)
    print("COMPLETE SECURITY WORKFLOW DEMO")
    print("="*60)
    
    # Initialize all components
    analyzer = PasswordAnalyzer()
    checker = BreachChecker()
    generator = PasswordGenerator()
    
    print("\n1. Generate a secure password:")
    password = generator.generate_random(16, use_symbols=True)
    print(f"Generated: {password}")
    
    print("\n2. Analyze its strength:")
    analysis = analyzer.analyze(password)
    print(f"Score: {analysis['score']}/100 ({analysis['strength']})")
    print(f"Entropy: {analysis['entropy_bits']} bits")
    
    print("\n3. Check for breaches:")
    try:
        is_breached, count = checker.check_password_breach(password)
        if is_breached:
            print(f"⚠️ Found in {count:,} breaches")
        else:
            print("✅ Not found in any known breaches")
    except Exception as e:
        print(f"Could not check breaches: {e}")
    
    print("\n4. Recommendations:")
    for rec in analysis['recommendations'][:3]:
        print(f"• {rec}")
    
    print("\n" + "="*60)
    print("WORKFLOW COMPLETE")
    print("="*60)


def show_password_strength_comparison():
    """Show comparison of different password strengths"""
    print("\n" + "="*60)
    print("PASSWORD STRENGTH COMPARISON")
    print("="*60)
    
    analyzer = PasswordAnalyzer()
    
    comparison_passwords = [
        ("123456", "Very weak - common pattern"),
        ("password", "Very weak - dictionary word"),
        ("Password1", "Weak - slight variation"),
        ("MyPassword123!", "Moderate - mixed case with number and symbol"),
        ("Th1s1sMyV3ryS3cur3P@ssw0rd!", "Strong - long with complexity"),
        ("correct-horse-battery-staple-2024", "Strong - passphrase style")
    ]
    
    print(f"{'Password Type':<35} {'Score':<8} {'Strength':<12} {'Entropy'}")
    print("-" * 75)
    
    for pwd, description in comparison_passwords:
        analysis = analyzer.analyze(pwd)
        print(f"{description:<35} {analysis['score']:<8} {analysis['strength']:<12} {analysis['entropy_bits']:.1f} bits")
    
    print("\n💡 Key Takeaways:")
    print("• Length matters significantly for security")
    print("• Character diversity improves strength")
    print("• Avoid common patterns and dictionary words")
    print("• Entropy above 50 bits is generally considered secure")


if __name__ == "__main__":
    print("SecurePass Analyzer - Usage Examples")
    print("This script demonstrates all the major features")
    
    try:
        demo_password_analysis()
        demo_password_generation()
        demo_breach_checking()
        show_password_strength_comparison()
        demo_complete_workflow()
        
        print("\n🎉 All demos completed successfully!")
        print("\nTo run the full interactive application:")
        print("streamlit run app.py")
        
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
    except Exception as e:
        print(f"\nError running demos: {e}")
        print("Make sure all dependencies are installed: pip install -r requirements.txt")
