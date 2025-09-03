"""
SecurePass Analyzer - Main Application
Interactive cybersecurity tool for password analysis, breach checking, and secure generation
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from password_analyzer import PasswordAnalyzer
from breach_checker import BreachChecker
from password_generator import PasswordGenerator

# Page configuration
st.set_page_config(
    page_title="SecurePass Analyzer",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .stButton > button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #45a049;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .danger-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
    }
    .warning-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #fff3cd;
        border: 1px solid #ffeeba;
        color: #856404;
    }
    .big-font {
        font-size: 24px !important;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'analyzer' not in st.session_state:
    st.session_state.analyzer = PasswordAnalyzer()
    st.session_state.checker = BreachChecker()
    st.session_state.generator = PasswordGenerator()
    st.session_state.analysis_history = []

def main():
    # Title and description
    st.title("🔐 SecurePass Analyzer")
    st.markdown("### check your security")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/150x150.png?text=SecurePass", width=150)
        st.markdown("## Navigation")
        page = st.radio(
            "Choose a feature:",
            ["🔍 Password Analyzer", "⚠️ Breach Checker", "🎲 Password Generator", 
             "📊 Security Dashboard", "📚 Security Tips"]
        )
        
        st.markdown("---")
        st.markdown("### About")
        st.info(
            "SecurePass Analyzer helps you:\n"
            "• Analyze password strength\n"
            "• Check for data breaches\n"
            "• Generate secure passwords\n"
            "• Learn security best practices"
        )
        
        # Creator credits
        st.markdown("---")
        st.markdown(
            "<div style='text-align: center; color: #666; font-size: 14px; padding: 10px;'>"
            "💻 <strong>Created by Vaibhav</strong><br>"
            "🔐 Cybersecurity & Python Developer<br>"
            "<a href='mailto:musalevaibhaw@gmail.com' style='color: #4CAF50;'>musalevaibhaw@gmail.com</a>"
            "</div>", 
            unsafe_allow_html=True
        )
    
    # Main content area
    if page == "🔍 Password Analyzer":
        password_analyzer_page()
    elif page == "⚠️ Breach Checker":
        breach_checker_page()
    elif page == "🎲 Password Generator":
        password_generator_page()
    elif page == "📊 Security Dashboard":
        security_dashboard_page()
    elif page == "📚 Security Tips":
        security_tips_page()
    
    # Footer with creator information
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #888; font-size: 16px; padding: 20px; background-color: #f8f9fa; border-radius: 10px; margin-top: 50px;'>"
        "🔐 <strong>SecurePass Analyzer</strong> | "
        "💻 Created with ❤️ by <strong>hav Musale</strong><br>"
        "🎓 Cybersecurity Enthusiast  | 🛡️ Security Analyst<br>"
        "<a href='mailto:musalevaibhaw@gmail.com' style='color: #4CAF50; text-decoration: none;'>📧 musalevaibhaw@gmail.com</a> | "
        "<a href='#' style='color: #4CAF50; text-decoration: none;'>🔗 LinkedIn</a> | "
        "<a href='#' style='color: #4CAF50; text-decoration: none;'>💼 Portfolio</a><br><br>"
        "<em>✨ Passionate about making cybersecurity accessible to everyone ✨</em>"
        "</div>",
        unsafe_allow_html=True
    )

def password_analyzer_page():
    st.header("🔍 Password Strength Analyzer")
    st.markdown("Analyze your password's strength and get personalized recommendations")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        password = st.text_input(
            "Enter password to analyze:",
            type="password",
            help="Your password is not stored and is only analyzed locally"
        )
        
        show_password = st.checkbox("Show password")
        if show_password and password:
            st.text(f"Password: {password}")
    
    with col2:
        st.markdown("### Quick Stats")
        if password:
            length = len(password)
            if length < 8:
                st.error(f"Length: {length} characters")
            elif length < 12:
                st.warning(f"Length: {length} characters")
            else:
                st.success(f"Length: {length} characters")
    
    if st.button("Analyze Password", type="primary"):
        if password:
            with st.spinner("Analyzing password..."):
                analysis = st.session_state.analyzer.analyze(password)
                
                # Store in history
                st.session_state.analysis_history.append({
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'score': analysis['score'],
                    'strength': analysis['strength']
                })
                
                # Display results
                st.markdown("---")
                st.markdown("## Analysis Results")
                
                # Score meter
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=analysis['score'],
                        domain={'x': [0, 1], 'y': [0, 1]},
                        title={'text': "Security Score"},
                        gauge={
                            'axis': {'range': [None, 100]},
                            'bar': {'color': get_score_color(analysis['score'])},
                            'steps': [
                                {'range': [0, 20], 'color': "lightgray"},
                                {'range': [20, 40], 'color': "lightyellow"},
                                {'range': [40, 60], 'color': "lightblue"},
                                {'range': [60, 80], 'color': "lightgreen"},
                                {'range': [80, 100], 'color': "darkgreen"}
                            ],
                            'threshold': {
                                'line': {'color': "red", 'width': 4},
                                'thickness': 0.75,
                                'value': 60
                            }
                        }
                    ))
                    fig.update_layout(height=300)
                    st.plotly_chart(fig, use_container_width=True)
                
                # Strength badge
                strength_color = get_strength_color(analysis['strength'])
                st.markdown(f"<h2 style='text-align: center; color: {strength_color};'>"
                           f"{analysis['strength']}</h2>", unsafe_allow_html=True)
                
                # Detailed metrics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Entropy", f"{analysis['entropy_bits']:.1f} bits")
                
                with col2:
                    diversity_count = sum(analysis['character_diversity'].values())
                    st.metric("Character Types", f"{diversity_count}/5")
                
                with col3:
                    pattern_count = sum(analysis['patterns_found'].values())
                    st.metric("Patterns Found", pattern_count)
                
                with col4:
                    st.metric("Length", analysis['password_length'])
                
                # Crack time estimates
                st.markdown("### ⏱️ Estimated Crack Time")
                crack_times = analysis['crack_time_estimates']
                
                col1, col2 = st.columns(2)
                with col1:
                    st.info(f"**Online (throttled):** {crack_times['online_throttled']}")
                    st.warning(f"**Online (no throttling):** {crack_times['online_unthrottled']}")
                
                with col2:
                    st.error(f"**Offline (fast):** {crack_times['offline_fast']}")
                    st.success(f"**Offline (slow):** {crack_times['offline_slow']}")
                
                # Character diversity
                st.markdown("### 🔤 Character Diversity")
                diversity = analysis['character_diversity']
                diversity_df = pd.DataFrame([
                    {"Type": "Lowercase", "Present": "✅" if diversity['has_lowercase'] else "❌"},
                    {"Type": "Uppercase", "Present": "✅" if diversity['has_uppercase'] else "❌"},
                    {"Type": "Numbers", "Present": "✅" if diversity['has_numbers'] else "❌"},
                    {"Type": "Symbols", "Present": "✅" if diversity['has_symbols'] else "❌"},
                    {"Type": "Spaces", "Present": "✅" if diversity['has_spaces'] else "❌"}
                ])
                st.table(diversity_df)
                
                # Patterns detected
                st.markdown("### 🔍 Pattern Detection")
                patterns = analysis['patterns_found']
                pattern_data = []
                for pattern, found in patterns.items():
                    status = "⚠️ Detected" if found else "✅ Not found"
                    pattern_name = pattern.replace('_', ' ').title()
                    pattern_data.append({"Pattern": pattern_name, "Status": status})
                
                patterns_df = pd.DataFrame(pattern_data)
                st.table(patterns_df)
                
                # Recommendations
                st.markdown("### 💡 Recommendations")
                if analysis['recommendations']:
                    for rec in analysis['recommendations']:
                        st.warning(f"• {rec}")
                
                # ZXCVBN suggestions
                if analysis['suggestions']:
                    st.markdown("### 🎯 Additional Suggestions")
                    for suggestion in analysis['suggestions']:
                        st.info(f"• {suggestion}")
        else:
            st.warning("Please enter a password to analyze")

def breach_checker_page():
    st.header("⚠️ Data Breach Checker")
    st.markdown("Check if your passwords or email have been exposed in data breaches")
    
    tab1, tab2 = st.tabs(["Password Breach Check", "Email Breach Check"])
    
    with tab1:
        st.markdown("### Check Password Against Known Breaches")
        st.info("🔒 Your password is never sent to any server. We use k-anonymity to ensure privacy.")
        
        password_to_check = st.text_input(
            "Enter password to check:",
            type="password",
            key="breach_password"
        )
        
        if st.button("Check Password Breach"):
            if password_to_check:
                with st.spinner("Checking against breach databases..."):
                    is_breached, count = st.session_state.checker.check_password_breach(password_to_check)
                    
                    if is_breached:
                        st.error(f"⚠️ **WARNING**: This password has been found in {count:,} data breaches!")
                        st.markdown("""
                        ### What should you do?
                        1. **Change this password immediately** on all accounts where you use it
                        2. **Never use this password again**
                        3. **Use unique passwords** for each account
                        4. **Enable two-factor authentication** wherever possible
                        5. **Consider using a password manager**
                        """)
                        
                        # Risk level visualization
                        risk_level = st.session_state.checker._calculate_risk_level(is_breached, count)
                        risk_color = {
                            "Low Risk": "yellow",
                            "Medium Risk": "orange",
                            "High Risk": "red",
                            "Critical Risk": "darkred"
                        }.get(risk_level, "red")
                        
                        st.markdown(f"<h3 style='color: {risk_color};'>Risk Level: {risk_level}</h3>",
                                  unsafe_allow_html=True)
                    else:
                        st.success("✅ Good news! This password has not been found in any known data breaches.")
                        st.info("However, still ensure you're using unique passwords for each account.")
            else:
                st.warning("Please enter a password to check")
    
    with tab2:
        st.markdown("### Check Email Against Known Breaches")
        st.warning("⚠️ Note: Email breach checking requires a Have I Been Pwned API key")
        
        email = st.text_input("Enter email address:", key="breach_email")
        api_key = st.text_input(
            "HIBP API Key (optional):",
            type="password",
            help="Get your API key at https://haveibeenpwned.com/API/Key"
        )
        
        if st.button("Check Email Breach"):
            if email:
                if not api_key:
                    st.error("API key is required for email breach checking. Get one at haveibeenpwned.com/API/Key")
                else:
                    with st.spinner("Checking email against breach databases..."):
                        result = st.session_state.checker.check_email_breaches(email, api_key)
                        
                        if result['error']:
                            st.error(f"Error: {result['error']}")
                        elif result['breached']:
                            st.error(f"⚠️ This email was found in {result['breach_count']} breach(es)!")
                            
                            st.markdown("### Breached Services:")
                            for breach in result['breaches'][:10]:  # Show first 10
                                with st.expander(f"{breach['name']} - {breach['date']}"):
                                    st.write(f"**Domain:** {breach['domain']}")
                                    st.write(f"**Verified:** {'Yes' if breach['verified'] else 'No'}")
                                    st.write(f"**Compromised data:** {', '.join(breach['data_types'])}")
                        else:
                            st.success("✅ Good news! This email has not been found in any known data breaches.")
            else:
                st.warning("Please enter an email address to check")

def password_generator_page():
    st.header("🎲 Password Generator")
    st.markdown("Generate strong, secure passwords with customizable options")
    
    # Generator type selection
    gen_type = st.selectbox(
        "Select generation method:",
        ["Random", "Memorable", "Pronounceable", "Passphrase", "Custom Pattern"]
    )
    
    generated_password = None
    
    if gen_type == "Random":
        col1, col2 = st.columns(2)
        
        with col1:
            length = st.slider("Password length:", 8, 32, 16)
            use_lowercase = st.checkbox("Lowercase letters (a-z)", value=True)
            use_uppercase = st.checkbox("Uppercase letters (A-Z)", value=True)
            use_digits = st.checkbox("Numbers (0-9)", value=True)
        
        with col2:
            use_symbols = st.checkbox("Symbols (!@#$...)", value=True)
            exclude_ambiguous = st.checkbox("Exclude ambiguous characters (0, O, l, I)")
            exclude_chars = st.text_input("Exclude specific characters:")
        
        if st.button("Generate Random Password"):
            try:
                generated_password = st.session_state.generator.generate_random(
                    length=length,
                    use_lowercase=use_lowercase,
                    use_uppercase=use_uppercase,
                    use_digits=use_digits,
                    use_symbols=use_symbols,
                    exclude_ambiguous=exclude_ambiguous,
                    exclude_chars=exclude_chars
                )
            except ValueError as e:
                st.error(str(e))
    
    elif gen_type == "Memorable":
        col1, col2 = st.columns(2)
        
        with col1:
            word_count = st.slider("Number of words:", 2, 6, 4)
            add_numbers = st.checkbox("Add numbers", value=True)
        
        with col2:
            add_symbols = st.checkbox("Add symbols", value=True)
            capitalize = st.checkbox("Capitalize words", value=True)
        
        if st.button("Generate Memorable Password"):
            generated_password = st.session_state.generator.generate_memorable(
                word_count=word_count,
                add_numbers=add_numbers,
                add_symbols=add_symbols,
                capitalize=capitalize
            )
    
    elif gen_type == "Pronounceable":
        col1, col2 = st.columns(2)
        
        with col1:
            length = st.slider("Password length:", 8, 20, 12)
            add_numbers = st.checkbox("Add numbers", value=True)
        
        with col2:
            add_symbols = st.checkbox("Add symbols", value=False)
        
        if st.button("Generate Pronounceable Password"):
            generated_password = st.session_state.generator.generate_pronounceable(
                length=length,
                add_numbers=add_numbers,
                add_symbols=add_symbols
            )
    
    elif gen_type == "Passphrase":
        col1, col2 = st.columns(2)
        
        with col1:
            word_count = st.slider("Number of words:", 3, 8, 6)
            separator = st.text_input("Word separator:", value="-")
        
        with col2:
            capitalize_words = st.checkbox("Capitalize words", value=False)
        
        if st.button("Generate Passphrase"):
            generated_password = st.session_state.generator.generate_passphrase(
                word_count=word_count,
                separator=separator,
                capitalize_words=capitalize_words
            )
    
    elif gen_type == "Custom Pattern":
        st.markdown("""
        ### Pattern Guide:
        - `l` - lowercase letter
        - `L` - uppercase letter  
        - `d` - digit
        - `s` - symbol
        - `a` - any alphanumeric
        - `*` - any character
        - Other characters are used literally
        
        **Example:** `LLLLdddd@@` generates like `ABCD1234@@`
        """)
        
        pattern = st.text_input("Enter pattern:", value="LLLLdddd@@")
        
        if st.button("Generate from Pattern"):
            try:
                generated_password = st.session_state.generator.generate_custom_pattern(pattern)
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    # Display generated password
    if generated_password:
        st.markdown("---")
        st.markdown("### Generated Password")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.code(generated_password, language=None)
        
        with col2:
            if st.button("📋 Copy to Clipboard"):
                st.write("Password copied!")
                st.balloons()
        
        # Analyze the generated password
        st.markdown("### Password Analysis")
        analysis = st.session_state.analyzer.analyze(generated_password)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Score", f"{analysis['score']}/100")
        
        with col2:
            st.metric("Strength", analysis['strength'])
        
        with col3:
            st.metric("Entropy", f"{analysis['entropy_bits']:.1f} bits")
        
        # Batch generation
        st.markdown("### Batch Generation")
        batch_count = st.slider("Generate multiple passwords:", 1, 10, 5)
        
        if st.button("Generate Batch"):
            if gen_type == "Random":
                passwords = st.session_state.generator.batch_generate(
                    count=batch_count,
                    length=length if 'length' in locals() else 16,
                    use_lowercase=use_lowercase if 'use_lowercase' in locals() else True,
                    use_uppercase=use_uppercase if 'use_uppercase' in locals() else True,
                    use_digits=use_digits if 'use_digits' in locals() else True,
                    use_symbols=use_symbols if 'use_symbols' in locals() else True
                )
                
                st.markdown("### Generated Passwords:")
                for i, pwd in enumerate(passwords, 1):
                    st.code(f"{i}. {pwd}", language=None)

def security_dashboard_page():
    st.header("📊 Security Dashboard")
    st.markdown("View your password analysis history and security trends")
    
    if not st.session_state.analysis_history:
        st.info("No analysis history yet. Analyze some passwords to see your dashboard!")
        return
    
    # Convert history to DataFrame
    df = pd.DataFrame(st.session_state.analysis_history)
    
    # Summary statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Analyzed", len(df))
    
    with col2:
        avg_score = df['score'].mean()
        st.metric("Average Score", f"{avg_score:.1f}")
    
    with col3:
        strong_count = len(df[df['strength'].isin(['Strong', 'Very Strong'])])
        st.metric("Strong Passwords", strong_count)
    
    with col4:
        weak_count = len(df[df['strength'].isin(['Weak', 'Very Weak'])])
        st.metric("Weak Passwords", weak_count)
    
    # Score trend over time
    st.markdown("### Score Trend")
    fig = px.line(df, x='timestamp', y='score', title='Password Score Over Time',
                  markers=True, line_shape='spline')
    fig.update_layout(yaxis_range=[0, 100])
    st.plotly_chart(fig, use_container_width=True)
    
    # Strength distribution
    st.markdown("### Strength Distribution")
    strength_counts = df['strength'].value_counts()
    fig = px.pie(values=strength_counts.values, names=strength_counts.index,
                 title='Password Strength Distribution',
                 color_discrete_map={
                     'Very Strong': '#00CC00',
                     'Strong': '#66FF66',
                     'Moderate': '#FFFF00',
                     'Weak': '#FF9900',
                     'Very Weak': '#FF0000'
                 })
    st.plotly_chart(fig, use_container_width=True)
    
    # Recent analyses table
    st.markdown("### Recent Analyses")
    recent_df = df.tail(10)[['timestamp', 'score', 'strength']]
    st.table(recent_df)
    
    # Export data
    if st.button("Export Analysis History"):
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"password_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

def security_tips_page():
    st.header("📚 Security Best Practices")
    st.markdown("Learn how to improve your password security")
    
    tips = {
        "🔑 Password Creation": [
            "Use at least 12 characters (16+ is better)",
            "Include uppercase, lowercase, numbers, and symbols",
            "Avoid dictionary words and personal information",
            "Don't use keyboard patterns (qwerty, 123456)",
            "Create unique passwords for each account"
        ],
        "🛡️ Password Management": [
            "Use a reputable password manager",
            "Enable two-factor authentication (2FA) everywhere",
            "Never share passwords via email or text",
            "Change passwords immediately if breached",
            "Review and update passwords regularly"
        ],
        "⚠️ Common Mistakes": [
            "Using the same password everywhere",
            "Including personal info (birthdays, names)",
            "Writing passwords on sticky notes",
            "Sharing passwords with others",
            "Using simple variations (Password1, Password2)"
        ],
        "🎯 Advanced Tips": [
            "Use passphrases for master passwords",
            "Enable login alerts when available",
            "Use hardware security keys for critical accounts",
            "Regularly check haveibeenpwned.com",
            "Keep software and browsers updated"
        ]
    }
    
    for category, items in tips.items():
        st.markdown(f"### {category}")
        for tip in items:
            st.write(f"• {tip}")
        st.markdown("")
    
    # Interactive password tips
    st.markdown("---")
    st.markdown("### 🎮 Interactive Tips")
    
    if st.button("Generate a Strong Password Example"):
        example = st.session_state.generator.generate_random(20)
        st.success(f"Example strong password: `{example}`")
        st.info("This password has high entropy and uses all character types!")
    
    if st.button("Generate a Memorable Passphrase"):
        passphrase = st.session_state.generator.generate_passphrase()
        st.success(f"Example passphrase: `{passphrase}`")
        st.info("Passphrases are long but easier to remember!")
    
    # Resources
    st.markdown("---")
    st.markdown("### 📖 Additional Resources")
    st.markdown("""
    - [Have I Been Pwned](https://haveibeenpwned.com) - Check for data breaches
    - [Two Factor Auth](https://2fa.directory) - Sites supporting 2FA
    - [Password Managers](https://www.privacytools.io/secure-password-manager) - Recommended managers
    - [Security Checklist](https://securitycheckli.st) - Personal security checklist
    """)

def get_score_color(score):
    if score >= 80:
        return "darkgreen"
    elif score >= 60:
        return "green"
    elif score >= 40:
        return "orange"
    elif score >= 20:
        return "darkorange"
    else:
        return "red"

def get_strength_color(strength):
    colors = {
        "Very Strong": "darkgreen",
        "Strong": "green",
        "Moderate": "orange",
        "Weak": "darkorange",
        "Very Weak": "red"
    }
    return colors.get(strength, "gray")

if __name__ == "__main__":
    main()
