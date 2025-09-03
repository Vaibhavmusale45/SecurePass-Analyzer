# SecurePass Analyzer - Deployment Guide

## Local Development Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Internet connection (for breach checking feature)

### Installation Steps

1. **Navigate to project directory:**
   ```bash
   cd SecurePassAnalyzer
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run app.py
   ```

4. **Access the application:**
   - Open your web browser
   - Navigate to `http://localhost:8501`
   - The application should load automatically

## Testing

### Running Unit Tests

```bash
# Run all tests
python tests/run_tests.py

# Run specific test module
python -m unittest tests.test_password_analyzer
python -m unittest tests.test_breach_checker
python -m unittest tests.test_password_generator
```

### Running Examples

```bash
# Run the example demonstrations
python docs/examples.py
```

## Configuration

### Environment Variables

Create a `.env` file in the project root for configuration:

```
# Have I Been Pwned API Key (optional, for email breach checking)
HIBP_API_KEY=your_api_key_here

# Application settings
STREAMLIT_PORT=8501
STREAMLIT_HOST=localhost

# Rate limiting settings
API_RATE_LIMIT_SECONDS=1.5
```

### Streamlit Configuration

Create `.streamlit/config.toml` for Streamlit-specific settings:

```toml
[server]
port = 8501
headless = false
enableCORS = false

[theme]
primaryColor = "#4CAF50"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"

[client]
showErrorDetails = true
```

## Production Deployment

### Option 1: Streamlit Cloud

1. Push your code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Deploy with one click

### Option 2: Heroku Deployment

1. **Create required files:**

   `Procfile`:
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

   `runtime.txt`:
   ```
   python-3.11.0
   ```

2. **Deploy to Heroku:**
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

### Option 3: Docker Deployment

1. **Create Dockerfile:**
   ```dockerfile
   FROM python:3.11-slim
   
   WORKDIR /app
   
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   
   COPY . .
   
   EXPOSE 8501
   
   CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]
   ```

2. **Build and run:**
   ```bash
   docker build -t securepass-analyzer .
   docker run -p 8501:8501 securepass-analyzer
   ```

### Option 4: AWS EC2/DigitalOcean

1. **Set up server environment:**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip git
   git clone your-repository
   cd SecurePassAnalyzer
   pip3 install -r requirements.txt
   ```

2. **Run with process manager:**
   ```bash
   # Install PM2
   npm install -g pm2
   
   # Create ecosystem file
   # ecosystem.config.js
   module.exports = {
     apps: [{
       name: 'securepass-analyzer',
       script: 'streamlit',
       args: 'run app.py --server.port 8501 --server.address 0.0.0.0',
       cwd: '/path/to/SecurePassAnalyzer'
     }]
   }
   
   # Start application
   pm2 start ecosystem.config.js
   ```

## Security Considerations

### Production Security

1. **HTTPS Only:**
   - Always use HTTPS in production
   - Configure SSL certificates properly

2. **API Key Management:**
   - Store API keys securely (environment variables)
   - Never commit API keys to version control
   - Use secret management services in production

3. **Rate Limiting:**
   - Implement proper rate limiting
   - Monitor API usage
   - Set up alerting for unusual activity

4. **Input Validation:**
   - All user inputs are validated
   - No sensitive data is logged
   - Passwords are never stored

### Network Security

1. **Firewall Configuration:**
   - Only allow necessary ports (80, 443)
   - Block direct access to internal services

2. **Monitoring:**
   - Set up logging and monitoring
   - Monitor for suspicious activity
   - Regular security updates

## Performance Optimization

### Caching

```python
# Use Streamlit caching for expensive operations
import streamlit as st

@st.cache_data
def analyze_password_cached(password):
    analyzer = PasswordAnalyzer()
    return analyzer.analyze(password)
```

### Database Integration (Optional)

For storing analysis history:

```python
import sqlite3

def create_analysis_db():
    conn = sqlite3.connect('data/analysis_history.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            score INTEGER,
            strength TEXT,
            entropy_bits REAL
        )
    ''')
    conn.commit()
    conn.close()
```

## Troubleshooting

### Common Issues

1. **Module Import Errors:**
   ```bash
   # Ensure you're in the project directory
   cd SecurePassAnalyzer
   
   # Check Python path
   python -c "import sys; print(sys.path)"
   ```

2. **Streamlit Port Issues:**
   ```bash
   # Use different port
   streamlit run app.py --server.port 8502
   ```

3. **API Connection Issues:**
   - Check internet connectivity
   - Verify API endpoints are accessible
   - Check for firewall blocking

4. **Dependency Issues:**
   ```bash
   # Reinstall dependencies
   pip install --upgrade -r requirements.txt
   
   # Check installed packages
   pip list
   ```

### Performance Issues

1. **Slow Analysis:**
   - Implement caching for repeated analyses
   - Consider async processing for batch operations

2. **Memory Usage:**
   - Monitor memory usage for large batch operations
   - Implement pagination for large datasets

## Monitoring and Maintenance

### Health Checks

```python
def health_check():
    """Basic health check for the application"""
    try:
        # Test core functionality
        analyzer = PasswordAnalyzer()
        generator = PasswordGenerator()
        checker = BreachChecker()
        
        # Test password analysis
        analysis = analyzer.analyze("test123")
        
        # Test password generation
        password = generator.generate_random(12)
        
        return {"status": "healthy", "timestamp": datetime.now()}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
```

### Backup Strategy

1. **Configuration Backup:**
   - Backup `.env` files
   - Document custom configurations

2. **Data Backup:**
   - Regular backup of analysis history
   - Export user preferences

### Updates and Maintenance

1. **Regular Updates:**
   ```bash
   # Update dependencies
   pip install --upgrade -r requirements.txt
   
   # Update zxcvbn database
   pip install --upgrade zxcvbn
   ```

2. **Security Updates:**
   - Monitor security advisories
   - Update dependencies regularly
   - Review API security practices

## Support

For deployment issues:
1. Check the troubleshooting section above
2. Review Streamlit documentation
3. Check project GitHub issues
4. Contact the development team

## License and Compliance

- Ensure compliance with HIBP API terms of service
- Review privacy implications of breach checking
- Follow data protection regulations (GDPR, etc.)
- Document security measures for compliance audits
