# SecurePass Analyzer - API Documentation

## Overview

The SecurePass Analyzer consists of three main modules that work together to provide comprehensive password security analysis:

1. **PasswordAnalyzer** - Analyzes password strength and provides recommendations
2. **BreachChecker** - Checks passwords and emails against known data breaches
3. **PasswordGenerator** - Generates secure passwords with various methods

## PasswordAnalyzer

### Class: `PasswordAnalyzer`

Main class for analyzing password strength using multiple security metrics.

#### Methods

##### `analyze(password: str) -> Dict`

Performs complete password analysis and returns comprehensive results.

**Parameters:**
- `password` (str): The password to analyze

**Returns:**
- Dictionary containing:
  - `password_length` (int): Length of the password
  - `score` (int): Overall security score (0-100)
  - `strength` (str): Strength level (Very Weak, Weak, Moderate, Strong, Very Strong)
  - `entropy_bits` (float): Calculated entropy in bits
  - `patterns_found` (dict): Dictionary of detected patterns
  - `character_diversity` (dict): Character type analysis
  - `crack_time_estimates` (dict): Time estimates for cracking
  - `recommendations` (list): List of improvement suggestions
  - `zxcvbn_score` (int): zxcvbn library score (0-4)
  - `warning` (str): zxcvbn warning message
  - `suggestions` (list): zxcvbn suggestions

**Example:**
```python
analyzer = PasswordAnalyzer()
result = analyzer.analyze("MyS3cur3P@ssw0rd!")
print(f"Score: {result['score']}/100")
print(f"Strength: {result['strength']}")
```

##### `calculate_entropy(password: str) -> float`

Calculates password entropy in bits.

**Parameters:**
- `password` (str): The password to analyze

**Returns:**
- `float`: Entropy value in bits

##### `check_patterns(password: str) -> Dict[str, bool]`

Checks for common weakness patterns in the password.

**Returns:**
- Dictionary with pattern detection results:
  - `sequential_numbers`: Sequential number patterns
  - `sequential_letters`: Sequential letter patterns  
  - `repeated_characters`: Character repetition
  - `keyboard_pattern`: Keyboard layout patterns
  - `common_word`: Common password dictionary
  - `date_pattern`: Date-like patterns

##### `get_character_diversity(password: str) -> Dict[str, bool]`

Analyzes character type diversity in the password.

**Returns:**
- Dictionary with character type presence:
  - `has_lowercase`: Contains lowercase letters
  - `has_uppercase`: Contains uppercase letters
  - `has_numbers`: Contains digits
  - `has_symbols`: Contains special symbols
  - `has_spaces`: Contains spaces

## BreachChecker

### Class: `BreachChecker`

Checks passwords and emails against known data breaches using the Have I Been Pwned API.

#### Methods

##### `check_password_breach(password: str) -> Tuple[bool, int]`

Checks if a password has been found in data breaches using k-anonymity.

**Parameters:**
- `password` (str): The password to check

**Returns:**
- `Tuple[bool, int]`: (is_breached, exposure_count)

**Example:**
```python
checker = BreachChecker()
is_breached, count = checker.check_password_breach("password123")
if is_breached:
    print(f"Password found in {count} breaches!")
```

##### `check_email_breaches(email: str, api_key: Optional[str]) -> Dict`

Checks if an email has been found in data breaches.

**Parameters:**
- `email` (str): Email address to check
- `api_key` (str): Have I Been Pwned API key (required)

**Returns:**
- Dictionary containing breach information

##### `generate_breach_report(password: str, email: Optional[str], api_key: Optional[str]) -> Dict`

Generates a comprehensive breach report for password and email.

**Parameters:**
- `password` (str): Password to check
- `email` (str, optional): Email to check
- `api_key` (str, optional): HIBP API key

**Returns:**
- Dictionary with complete breach analysis and recommendations

## PasswordGenerator

### Class: `PasswordGenerator`

Generates secure passwords using various methods and complexity rules.

#### Methods

##### `generate_random(length: int, **options) -> str`

Generates a random password with specified criteria.

**Parameters:**
- `length` (int): Desired password length
- `use_lowercase` (bool): Include lowercase letters (default: True)
- `use_uppercase` (bool): Include uppercase letters (default: True)
- `use_digits` (bool): Include digits (default: True)
- `use_symbols` (bool): Include symbols (default: True)
- `exclude_ambiguous` (bool): Exclude ambiguous characters (default: False)
- `exclude_chars` (str): Specific characters to exclude (default: "")

**Returns:**
- `str`: Generated password

**Example:**
```python
generator = PasswordGenerator()
password = generator.generate_random(16, use_symbols=True)
```

##### `generate_memorable(word_count: int, **options) -> str`

Generates a memorable password using word combinations.

**Parameters:**
- `word_count` (int): Number of words to combine (default: 4)
- `add_numbers` (bool): Add random numbers (default: True)
- `add_symbols` (bool): Add random symbols (default: True)
- `capitalize` (bool): Capitalize some words (default: True)

**Returns:**
- `str`: Generated memorable password

##### `generate_pronounceable(length: int, **options) -> str`

Generates a pronounceable password using syllable patterns.

**Parameters:**
- `length` (int): Approximate desired length (default: 12)
- `add_numbers` (bool): Add numbers at the end (default: True)
- `add_symbols` (bool): Add symbols at the end (default: False)

**Returns:**
- `str`: Generated pronounceable password

##### `generate_passphrase(word_count: int, **options) -> str`

Generates a passphrase using random words.

**Parameters:**
- `word_count` (int): Number of words (default: 6)
- `separator` (str): Word separator (default: "-")
- `capitalize_words` (bool): Capitalize words (default: False)

**Returns:**
- `str`: Generated passphrase

##### `generate_custom_pattern(pattern: str) -> str`

Generates a password based on a custom pattern.

**Pattern Characters:**
- `l`: lowercase letter
- `L`: uppercase letter  
- `d`: digit
- `s`: symbol
- `a`: any alphanumeric
- `*`: any character
- Other characters are used literally

**Example:**
```python
password = generator.generate_custom_pattern("LLLLdddd@@")
# Generates like: ABCD1234@@
```

##### `batch_generate(count: int, **kwargs) -> List[str]`

Generates multiple passwords with the same criteria.

**Parameters:**
- `count` (int): Number of passwords to generate
- `**kwargs`: Same parameters as `generate_random()`

**Returns:**
- `List[str]`: List of generated passwords

## Security Features

### K-Anonymity Protection

The breach checker uses k-anonymity to protect password privacy:
1. Password is hashed using SHA-1
2. Only the first 5 characters of the hash are sent to the API
3. The API returns all hashes starting with those 5 characters
4. Local comparison determines if the password was breached

### Secure Random Generation

All password generation uses the `secrets` module for cryptographically secure randomness.

### No Data Storage

- Passwords are never stored or logged
- All analysis happens locally
- Only hash prefixes are sent to external APIs

## Error Handling

All modules include comprehensive error handling:
- Network timeouts and connection errors
- Invalid API responses
- Input validation
- Graceful degradation when external services are unavailable

## Rate Limiting

The breach checker includes rate limiting to respect API limits:
- 1 request per 1.5 seconds for password checking
- Built-in delays for batch operations

## Integration Example

```python
from src.password_analyzer import PasswordAnalyzer
from src.breach_checker import BreachChecker
from src.password_generator import PasswordGenerator

# Initialize components
analyzer = PasswordAnalyzer()
checker = BreachChecker()
generator = PasswordGenerator()

# Generate and analyze a password
password = generator.generate_random(16)
analysis = analyzer.analyze(password)
is_breached, count = checker.check_password_breach(password)

print(f"Generated: {password}")
print(f"Strength: {analysis['strength']} ({analysis['score']}/100)")
print(f"Breached: {is_breached} ({count} times)" if is_breached else "Safe")
```

## Configuration

The application can be customized through:
- Character sets in password generation
- Pattern detection rules
- Scoring algorithms
- API endpoints and timeouts
