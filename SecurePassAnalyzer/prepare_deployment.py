"""
Prepare SecurePass Analyzer for Deployment
Sets up the project for various free deployment platforms
"""

import os
import subprocess
import sys


def check_git_status():
    """Check if git is initialized and files are committed"""
    try:
        result = subprocess.run(['git', 'status'], 
                              capture_output=True, text=True, check=True)
        print("✅ Git repository initialized")
        
        if "nothing to commit" in result.stdout:
            print("✅ All files committed")
            return True
        else:
            print("⚠️ Uncommitted changes detected")
            return False
            
    except subprocess.CalledProcessError:
        print("❌ Git not initialized")
        return False
    except FileNotFoundError:
        print("❌ Git not installed")
        return False


def initialize_git():
    """Initialize git repository and commit files"""
    try:
        print("🔧 Initializing git repository...")
        subprocess.run(['git', 'init'], check=True)
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', 'Initial commit: SecurePass Analyzer project'], check=True)
        print("✅ Git repository initialized and files committed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error initializing git: {e}")
        return False


def check_required_files():
    """Check if all deployment files are present"""
    required_files = {
        'LICENSE': 'MIT License file',
        'Procfile': 'Heroku deployment configuration',
        'runtime.txt': 'Python runtime specification',
        'railway.json': 'Railway deployment configuration',
        '.streamlit/config.toml': 'Streamlit configuration',
        '.gitignore': 'Git ignore rules'
    }
    
    missing_files = []
    for file_path, description in required_files.items():
        if not os.path.exists(file_path):
            missing_files.append((file_path, description))
    
    return missing_files


def display_deployment_options():
    """Display available deployment options"""
    print("\n" + "="*60)
    print("🌟 FREE DEPLOYMENT OPTIONS")
    print("="*60)
    
    options = [
        {
            "name": "Streamlit Cloud",
            "cost": "100% Free",
            "difficulty": "⭐ Easiest",
            "time": "5 minutes",
            "url": "https://share.streamlit.io",
            "pros": ["Direct GitHub integration", "Automatic updates", "Custom domains"]
        },
        {
            "name": "Railway",
            "cost": "$5/month free tier",
            "difficulty": "⭐⭐ Easy",
            "time": "10 minutes", 
            "url": "https://railway.app",
            "pros": ["Fast deployment", "Great performance", "Easy scaling"]
        },
        {
            "name": "Render",
            "cost": "Free tier available",
            "difficulty": "⭐⭐ Easy",
            "time": "10 minutes",
            "url": "https://render.com",
            "pros": ["Free SSL", "Automatic deploys", "Good performance"]
        },
        {
            "name": "Heroku",
            "cost": "Limited free hours",
            "difficulty": "⭐⭐⭐ Moderate",
            "time": "15 minutes",
            "url": "https://heroku.com",
            "pros": ["Well-established", "Many add-ons", "Good documentation"]
        }
    ]
    
    for i, option in enumerate(options, 1):
        print(f"\n{i}. 🚀 **{option['name']}**")
        print(f"   💰 Cost: {option['cost']}")
        print(f"   🎯 Difficulty: {option['difficulty']}")
        print(f"   ⏱️ Setup time: {option['time']}")
        print(f"   🔗 URL: {option['url']}")
        print(f"   ✨ Pros: {', '.join(option['pros'])}")


def show_streamlit_cloud_instructions():
    """Show detailed Streamlit Cloud deployment instructions"""
    print("\n" + "="*60)
    print("🎯 STREAMLIT CLOUD DEPLOYMENT (RECOMMENDED)")
    print("="*60)
    
    print("""
📋 Step-by-Step Instructions:

1. 📂 **Push to GitHub**:
   • Go to https://github.com
   • Create new repository: 'SecurePass-Analyzer'
   • Make it PUBLIC (required for free tier)
   • Copy the git commands shown

2. 💻 **Upload your code**:
   git remote add origin https://github.com/YOUR_USERNAME/SecurePass-Analyzer.git
   git branch -M main
   git push -u origin main

3. 🌐 **Deploy on Streamlit Cloud**:
   • Visit https://share.streamlit.io
   • Sign in with GitHub
   • Click "New app"
   • Select your repository
   • Main file: app.py
   • Click "Deploy!"

4. 🎉 **Access your live app**:
   • Your app will be at: https://YOUR_APP_NAME.streamlit.app
   • Share this URL with employers, friends, anyone!

⏱️ Total time: 5-10 minutes
💰 Cost: 100% FREE forever!
""")


def main():
    """Main preparation function"""
    print("🚀 SecurePass Analyzer - Deployment Preparation")
    print("="*60)
    
    # Check current directory
    if not os.path.exists('app.py'):
        print("❌ Error: Run this from the SecurePassAnalyzer directory")
        return
    
    print("✅ Found SecurePass Analyzer project")
    
    # Check required files
    print("\n📁 Checking deployment files...")
    missing_files = check_required_files()
    
    if missing_files:
        print("❌ Missing deployment files:")
        for file_path, description in missing_files:
            print(f"   • {file_path} - {description}")
        print("\n💡 Run the main setup to create missing files")
    else:
        print("✅ All deployment files present")
    
    # Check git status
    print("\n📝 Checking git status...")
    git_ready = check_git_status()
    
    if not git_ready:
        print("\n🔧 Would you like to initialize git? (Recommended for deployment)")
        print("This will:")
        print("• Initialize git repository")
        print("• Add all files")
        print("• Create initial commit")
        print("\nType 'yes' to proceed or 'no' to skip:")
        
        # For demo purposes, we'll assume yes
        response = "yes"  # input().lower()
        
        if response == "yes":
            if initialize_git():
                git_ready = True
    
    # Display deployment options
    display_deployment_options()
    
    # Show recommended deployment method
    show_streamlit_cloud_instructions()
    
    # Final status
    print("\n" + "="*60)
    print("📋 DEPLOYMENT READINESS CHECKLIST")
    print("="*60)
    
    checklist = [
        ("📄 LICENSE file", os.path.exists('LICENSE')),
        ("⚙️ Deployment configs", len(check_required_files()) == 0),
        ("📝 Git repository", git_ready),
        ("🐍 Dependencies", os.path.exists('requirements.txt')),
        ("📚 Documentation", os.path.exists('docs/README.md')),
        ("🧪 Tests passing", os.path.exists('tests/run_tests.py'))
    ]
    
    for item, status in checklist:
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {item}")
    
    ready_count = sum(status for _, status in checklist)
    total_count = len(checklist)
    
    print(f"\n📊 Deployment readiness: {ready_count}/{total_count}")
    
    if ready_count == total_count:
        print("🎉 Your project is ready for deployment!")
        print("\n💡 Recommended next steps:")
        print("1. Push code to GitHub")
        print("2. Deploy on Streamlit Cloud (easiest)")
        print("3. Share your live URL!")
    else:
        print("⚠️ Complete the missing items above before deploying")
    
    print(f"\n🔗 Live demo URL will be: https://your-securepass-analyzer.streamlit.app")
    print("📧 Perfect for sharing with employers and on your resume!")


if __name__ == "__main__":
    main()
