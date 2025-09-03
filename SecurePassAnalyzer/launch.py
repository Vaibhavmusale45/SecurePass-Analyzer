"""
Launch script for SecurePass Analyzer
Checks dependencies and starts the Streamlit application
"""

import sys
import os
import subprocess
import importlib.util


def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = [
        'streamlit', 'pandas', 'plotly', 'requests', 
        'cryptography', 'zxcvbn', 'python-dotenv'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        if package == 'python-dotenv':
            package_import = 'dotenv'
        else:
            package_import = package
            
        spec = importlib.util.find_spec(package_import)
        if spec is None:
            missing_packages.append(package)
    
    return missing_packages


def check_project_structure():
    """Verify project structure is complete"""
    required_files = [
        'app.py',
        'requirements.txt',
        'src/password_analyzer.py',
        'src/breach_checker.py', 
        'src/password_generator.py'
    ]
    
    required_dirs = ['src', 'tests', 'docs', 'data', 'reports']
    
    missing_items = []
    
    # Check files
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_items.append(f"File: {file_path}")
    
    # Check directories
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            missing_items.append(f"Directory: {dir_path}")
    
    return missing_items


def main():
    """Main launch function"""
    print("🔐 SecurePass Analyzer - Launcher")
    print("="*50)
    
    # Check if we're in the right directory
    if not os.path.exists('app.py'):
        print("❌ Error: app.py not found!")
        print("   Please run this script from the SecurePassAnalyzer directory")
        return False
    
    print("✅ Found app.py")
    
    # Check project structure
    print("\n📁 Checking project structure...")
    missing_items = check_project_structure()
    if missing_items:
        print("⚠️ Warning: Missing project items:")
        for item in missing_items:
            print(f"   • {item}")
    else:
        print("✅ Project structure complete")
    
    # Check dependencies
    print("\n📦 Checking dependencies...")
    missing_packages = check_dependencies()
    
    if missing_packages:
        print("❌ Missing packages:")
        for package in missing_packages:
            print(f"   • {package}")
        print("\nTo install missing packages:")
        print("   pip install -r requirements.txt")
        return False
    else:
        print("✅ All dependencies installed")
    
    # Test core functionality
    print("\n🧪 Testing core functionality...")
    try:
        from src.password_analyzer import PasswordAnalyzer
        from src.breach_checker import BreachChecker
        from src.password_generator import PasswordGenerator
        
        # Quick functionality test
        analyzer = PasswordAnalyzer()
        generator = PasswordGenerator()
        checker = BreachChecker()
        
        # Test basic operations
        test_password = generator.generate_random(12)
        analysis = analyzer.analyze("TestPassword123!")
        
        print("✅ Core functionality working")
        
    except Exception as e:
        print(f"❌ Error testing functionality: {e}")
        return False
    
    # Launch Streamlit
    print("\n🚀 Launching Streamlit application...")
    print("   Opening in your default web browser...")
    print("   URL: http://localhost:8501")
    print("   Press Ctrl+C to stop the application")
    print("\n" + "="*50)
    
    try:
        # Launch Streamlit
        subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'app.py'], check=True)
        
    except KeyboardInterrupt:
        print("\n\n🛑 Application stopped by user")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error launching Streamlit: {e}")
        print("\nTry running manually:")
        print("   streamlit run app.py")
        return False
        
    except FileNotFoundError:
        print("\n❌ Streamlit not found!")
        print("Install it with: pip install streamlit")
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ Launch completed successfully!")
    else:
        print("\n❌ Launch failed. Please check the error messages above.")
        sys.exit(1)
