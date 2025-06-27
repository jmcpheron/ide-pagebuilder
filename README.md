<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="logo-dark.png">
    <img src="logo.png" alt="Git-Friendly Banner Pages" width="400">
  </picture>
  
  <p>
    <a href="https://github.com/jmcpheron/ide-pagebuilder/blob/main/LICENSE">
      <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT">
    </a>
    <a href="https://python.org">
      <img src="https://img.shields.io/badge/Python-3.9+-blue.svg" alt="Python 3.9+">
    </a>
    <a href="https://pytest.org">
      <img src="https://img.shields.io/badge/Testing-pytest-green.svg" alt="Testing: pytest">
    </a>
    <a href="https://docs.astral.sh/ruff/">
      <img src="https://img.shields.io/badge/Code%20Style-ruff-black.svg" alt="Code style: ruff">
    </a>
    <a href="https://mypy-lang.org/">
      <img src="https://img.shields.io/badge/Type%20Checking-mypy-blue.svg" alt="Type checking: mypy">
    </a>
    <img src="https://img.shields.io/badge/Version-0.1.0-brightgreen.svg" alt="Version 0.1.0">
    <img src="https://img.shields.io/badge/Tools-Pages%20%2B%20Virtual%20Domains-orange.svg" alt="Pages + Virtual Domains">
    <img src="https://img.shields.io/badge/Vibe-Community%20Fun-ff69b4.svg" alt="Community Fun">
  </p>
</div>

# Git-Friendly Banner Pages

*Community toolkit for sane Banner page development*

Tired of wrestling with Banner pages where all your HTML/CSS/JS code gets smooshed into escaped JSON strings? Sick of trying to review SQL queries that look like `"SELECT * FROM\r\nstudent WHERE\r\nid = :id"`? 

This toolkit has **two tools** that extract all that embedded code into proper files so you can actually see what you're working with.

## Which Tool Do I Need?

**Working on pages?** → Use `extract_literals.py` for HTML/CSS/JS extraction  
**Working on virtual domains?** → Use `extract_virtual_domains.py` for SQL extraction  
**Building a complete app?** → Use both tools together

## Quick Start

### For Page Development (HTML/CSS/JS)

1. **Put your Banner Extensibility page JSON files in a directory**
   ```bash
   pages/
   ├── pages.my-custom-page.json
   ├── pages.another-page.json
   └── pages.third-page.json
   ```

2. **Extract the embedded HTML/CSS/JS into editable files**
   ```bash
   uv run python extract_literals.py extract
   ```

3. **Edit the extracted files with full IDE support**
   ```
   extracted_literals/
   ├── my-custom-page/
   │   ├── header.html          # Now you can edit this with syntax highlighting
   │   ├── main_literal.js      # JavaScript with proper formatting
   │   └── style.js             # CSS styles
   └── another-page/
       └── ...
   ```

4. **Rebuild the JSON files when ready to deploy**
   ```bash
   uv run python extract_literals.py rebuild
   ```

### For Virtual Domain Development (SQL)

1. **Put your Banner Extensibility virtual domain JSON files in a directory**
   ```bash
   virtualDomains/
   ├── virtualDomains.student-lookup.json
   ├── virtualDomains.grade-entry.json
   └── virtualDomains.meal-plan.json
   ```

2. **Extract the embedded SQL into editable files**
   ```bash
   uv run python extract_virtual_domains.py extract "virtualDomains/*.json"
   ```

3. **Edit the extracted SQL files with full IDE support**
   ```
   extracted_virtual_domains/
   ├── student-lookup/
   │   ├── codeget.sql          # GET request SQL with syntax highlighting
   │   ├── codepost.sql         # POST request SQL
   │   └── _extraction_map.json # Rebuild mapping
   └── grade-entry/
       └── ...
   ```

4. **Rebuild the JSON files when ready to deploy**
   ```bash
   uv run python extract_virtual_domains.py rebuild
   ```

That's it! Your JSON files are updated with the changes from your extracted files.

## What This Solves

Banner page development has some interesting challenges:

### Page Development Pain Points
Banner **pages** stuff all your HTML/CSS/JS into escaped JSON strings, which makes:
- Code reviews feel like decoding hieroglyphics
- Git diffs completely unreadable  
- Your IDE think everything is just a big string
- Merge conflicts nightmarish

### Virtual Domain Headaches
Banner **virtual domains** squish SQL queries into JSON strings too, which means:
- Debugging SQL feels like solving puzzles blindfolded
- Query optimization becomes guesswork
- No syntax highlighting for your SQL
- Collaborating on complex queries is rough

### How We Fix It

Both tools extract embedded content into proper files so you can:

✅ **See actual code changes** in Git diffs  
✅ **Use your IDE properly** - syntax highlighting, autocomplete, formatting  
✅ **Use standard dev tools** - ESLint, Prettier, SQL formatters  
✅ **Collaborate effectively** - your teammates don't need to be JSON experts  
✅ **Debug efficiently** - test SQL directly in your database client  
✅ **Optimize performance** - use proper analysis tools  

## Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd ide-pagebuilder

# Install dependencies with uv (modern Python package manager)
# If you don't have uv installed: pip install uv
uv sync
```

## Usage

### Page Literals (HTML/CSS/JS)

#### Extract Literals
```bash
# Extract from all page JSON files in current directory
uv run python extract_literals.py extract

# Extract from specific files
uv run python extract_literals.py extract "pages/*.json"

# Extract from specific directory
uv run python extract_literals.py extract "my-pages/**/*.json"
```

#### Rebuild JSON Files
```bash
# Rebuild all extracted pages
uv run python extract_literals.py rebuild
```

#### Check Sync Status
```bash
# Verify extracted files match JSON content
uv run python extract_literals.py check
```

### Virtual Domains (SQL)

#### Extract SQL
```bash
# Extract from all virtual domain JSON files
uv run python extract_virtual_domains.py extract "virtualDomains/*.json"

# Extract from specific virtual domain files
uv run python extract_virtual_domains.py extract "virtualDomains/virtualDomains.student-*.json"
```

#### Rebuild JSON Files
```bash
# Rebuild all extracted virtual domains
uv run python extract_virtual_domains.py rebuild
```

#### Check Sync Status
```bash
# Verify extracted SQL files match JSON content
uv run python extract_virtual_domains.py check
```

## Project Structure

```
ide-pagebuilder/
├── extract_literals.py          # Page extraction tool (HTML/CSS/JS)
├── extract_virtual_domains.py   # Virtual domain extraction tool (SQL)
├── extracted_literals/          # Extracted HTML/CSS/JS files from pages
│   ├── my-custom-page/
│   │   ├── header.html          # Extracted HTML
│   │   ├── main_literal.js      # Extracted JavaScript
│   │   ├── style.js             # Extracted CSS
│   │   └── _extraction_map.json # Rebuild mapping
│   └── ...
├── extracted_virtual_domains/   # Extracted SQL files from virtual domains
│   ├── student-lookup/
│   │   ├── codeget.sql          # GET request SQL
│   │   ├── codepost.sql         # POST request SQL
│   │   └── _extraction_map.json # Rebuild mapping
│   └── ...
├── pages/                       # Your Banner Extensibility page JSON files
│   ├── pages.my-custom-page.json
│   └── pages.another-page.json
├── virtualDomains/              # Your Banner Extensibility virtual domain JSON files
│   ├── README.md                # Virtual domains documentation
│   ├── virtualDomains.student-lookup.json
│   └── virtualDomains.grade-entry.json
├── tests/                       # Comprehensive test suite
│   ├── test_basics.py          # Basic functionality tests
│   ├── test_extract_literals.py # Page extraction/rebuild tests
│   ├── test_virtual_domains.py # Virtual domain extraction/rebuild tests
│   ├── test_json_structure.py  # JSON schema validation tests
│   ├── test_page_validation.py # Banner Extensibility validation tests
│   └── test_security.py        # Security-focused tests
├── CLAUDE.md                   # Developer instructions for Claude Code
├── logo.svg                    # Project logo
├── pyproject.toml              # uv configuration and dependencies
├── uv.lock                     # Locked dependency versions
└── README.md
```

## How It Works

### Page Literals Extraction
1. **Scans page JSON files** for `literal` components with embedded HTML/CSS/JS
2. **Extracts content** into separate files with appropriate extensions (`.html`, `.js`, `.css`)
3. **Creates mapping** files to track relationships between extracted files and JSON
4. **Rebuilds JSON** by reading extracted files and updating the original JSON structure

### Virtual Domain SQL Extraction
1. **Scans virtual domain JSON files** for SQL code in fields like `codeGet`, `codePost`, `codePut`, `codeDelete`
2. **Extracts SQL content** into separate `.sql` files with descriptive names
3. **Creates mapping** files to track relationships between extracted SQL files and JSON fields
4. **Rebuilds JSON** by reading extracted SQL files and updating the original virtual domain structure

### Why Extract Both?
- **Pages + Virtual Domains** = Complete Banner Extensibility applications
- **Review frontend and backend code** separately with proper syntax highlighting
- **Test SQL queries** directly in your database client
- **Collaborate on complex applications** where different team members handle UI vs database logic

## Virtual Domains Deep Dive

### What Are Virtual Domains?
Virtual domains are basically Banner's way of letting you create custom API endpoints. They're JSON files that:
- **Define SQL queries** for GET, POST, PUT, DELETE operations  
- **Handle security** and role-based access control
- **Translate HTTP requests** into database operations
- **Return data in JSON format** for your pages to consume

### Virtual Domain Structure
Each virtual domain JSON file contains:
- `serviceName`: Unique identifier for the API endpoint
- `codeGet`: SQL query for GET requests (most common)
- `codePost`: SQL for creating new records
- `codePut`: SQL for updating existing records  
- `codeDelete`: SQL for deleting records
- `virtualDomainRoles`: Array of role-based permissions
- `typeOfCode`: Usually "S" for SQL

### Virtual Domain Development Workflow
```bash
# 1. Create your virtual domain JSON file
virtualDomains/virtualDomains.student-lookup.json

# 2. Extract SQL for editing
uv run python extract_virtual_domains.py extract "virtualDomains/*.json"

# 3. Edit the extracted SQL files
code extracted_virtual_domains/student-lookup/codeget.sql

# 4. Test your SQL directly in your database client
# (No more escaping strings!)

# 5. Rebuild JSON when ready
uv run python extract_virtual_domains.py rebuild

# 6. Deploy to Banner
```

### SQL Security Best Practices
- ✅ **Use parameterized queries** (`:parameter_name`) to prevent SQL injection
- ✅ **Leverage Banner's security context** (`:parm_user_pidm`) for user-specific data
- ✅ **Define proper roles** in `virtualDomainRoles` for access control
- ❌ **Never hardcode sensitive data** in SQL queries

### Example: Student Name Lookup
```sql
-- Instead of this embedded in JSON:
-- "codeGet": "select s.spriden_id GID, s.spriden_first_name..."

-- You get this clean, editable SQL file:
SELECT 
    s.spriden_id AS gid,
    s.spriden_pidm AS p_pidm,
    CASE 
        WHEN p.spbpers_pref_first_name IS NOT NULL 
        THEN p.spbpers_pref_first_name || '[' || s.spriden_first_name || ']'
        ELSE s.spriden_first_name 
    END AS first_name,
    s.spriden_mi AS middle_name,
    s.spriden_last_name AS last_name 
FROM spriden s, spbpers p
WHERE s.spriden_change_ind IS NULL
    AND s.spriden_id = :gid
    AND s.spriden_pidm = p.spbpers_pidm
```

## Testing & Quality

This project includes a comprehensive test suite to ensure code quality and reliability:

### Running Tests
```bash
# Run all tests
uv run pytest

# Run tests with verbose output
uv run pytest -v

# Run specific test files
uv run pytest tests/test_page_validation.py
uv run pytest tests/test_security.py

# Run tests and show coverage
uv run pytest --cov=.
```

### Test Categories

- **`test_basics.py`** - Basic functionality tests
- **`test_extract_literals.py`** - Tests for page extraction/rebuild functionality
  - File extension detection (HTML, CSS, JS)
  - JSON extraction and reconstruction
  - Sync status validation
  - Multiple content type handling
- **`test_virtual_domains.py`** - Tests for virtual domain extraction/rebuild functionality
  - SQL extraction from virtual domain JSON files
  - Virtual domain structure validation
  - Role-based security validation
  - SQL extraction and reconstruction
- **`test_json_structure.py`** - JSON schema and structure validation
  - Valid JSON formatting
  - Schema compliance
  - Component structure validation
  - Consistent indentation
- **`test_page_validation.py`** - Banner Extensibility page-specific validation
  - Required fields (`constantName`, `modelView`)
  - Component type validation
  - Resource references
  - Naming conventions
- **`test_security.py`** - Security-focused validation
  - Hardcoded secrets detection
  - Dangerous JavaScript patterns
  - SQL injection protection
  - External resource validation

### Code Quality Tools
```bash
# Format code with ruff
uv run ruff format .

# Lint code with ruff
uv run ruff check .

# Type checking with mypy
uv run mypy extract_literals.py
uv run mypy extract_virtual_domains.py
```

## Troubleshooting

### Common Issues

**❌ "No JSON files found matching pattern"**
- Check your file paths and patterns
- Ensure JSON files are valid Banner Extensibility format
- For pages: Look for `literal` components
- For virtual domains: Look for `serviceName` and SQL code fields

**❌ "Out of sync" warnings**
```bash
# Check what's different
uv run python extract_literals.py check
uv run python extract_virtual_domains.py check

# Re-extract if JSON was modified externally
uv run python extract_literals.py extract

# Re-rebuild if extracted files were modified
uv run python extract_literals.py rebuild
```

**❌ SQL Syntax Errors in Virtual Domains**
- Test your SQL directly in your database client first
- Use proper parameter syntax (`:parameter_name`)
- Check for unescaped quotes or special characters

**❌ Page Literal Components Not Extracting**
- Ensure your page JSON has `literal` components
- Check that the `literal` field contains actual HTML/CSS/JS content
- Verify JSON structure is valid

### Getting Help
- Check the `CLAUDE.md` file for detailed developer instructions
- Check the `virtualDomains/README.md` for virtual domain specifics
- Run the test suite: `uv run pytest -v`
- Open an issue on GitHub if you're stuck

## Common Workflows

### Building a Complete App
```bash
# 1. Set up your project structure
mkdir my-banner-app
cd my-banner-app
git clone <this-repo> .

# 2. Add your JSON files
# - Put page definitions in pages/
# - Put virtual domain definitions in virtualDomains/

# 3. Extract everything for development
uv run python extract_literals.py extract
uv run python extract_virtual_domains.py extract "virtualDomains/*.json"

# 4. Develop with full IDE support
# - Edit HTML/CSS/JS in extracted_literals/
# - Edit SQL in extracted_virtual_domains/
# - Test SQL directly in your database client
# - Use ESLint, Prettier, SQL formatters, etc.

# 5. Before committing changes
uv run python extract_literals.py rebuild
uv run python extract_virtual_domains.py rebuild
uv run pytest  # Run all tests

# 6. Deploy to Banner Extensibility
# Your JSON files are ready!
```

### Code Review Workflow
```bash
# Reviewer can easily see actual code changes
git diff  # Shows real HTML/CSS/JS/SQL changes, not escaped JSON

# Comments can reference specific lines in extracted files
# "In extracted_literals/student-portal/main.js line 45..."
# "The SQL in extracted_virtual_domains/grades/codeget.sql could be optimized..."
```

## Configuration (Optional)

For environment-specific values, create a `.env` file:
```bash
# .env
COLLEGE_NAME=Your College Name
COLLEGE_LOGO_URL=https://your-college.edu/logo.png
BANNER_BASE_URL=https://your-banner-server.edu
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Extract files for development:
   ```bash
   # For page development:
   uv run python extract_literals.py extract
   
   # For virtual domain development:
   uv run python extract_virtual_domains.py extract "virtualDomains/*.json"
   ```
4. Make your changes:
   - Page changes: Edit files in `extracted_literals/`
   - Virtual domain changes: Edit SQL files in `extracted_virtual_domains/`
5. Test your changes:
   ```bash
   uv run pytest  # Run all tests
   uv run ruff check .  # Check code style
   ```
6. Rebuild JSON files:
   ```bash
   uv run python extract_literals.py rebuild
   uv run python extract_virtual_domains.py rebuild
   ```
7. Commit your changes (`git commit -m 'Add amazing feature'`)
8. Push to the branch (`git push origin feature/amazing-feature`)
9. Open a Pull Request

## About This Project

Hey there! I'm Jason, and I work at West Valley Mission Community College District. I built this toolkit because Banner page development was getting frustrating – all that code trapped in escaped JSON strings, there had to be a better way.

This is my side project that I'm sharing with fellow Banner developers. If you're dealing with the same frustrations, hopefully this makes your workflow smoother.

### Why I'm Sharing This
- **Community colleges**: We're all dealing with similar challenges
- **Banner developers**: Let's make this easier for everyone
- **Open source**: Use it, improve it, share it

---

**Note**: This toolkit is designed for Banner custom pages. Make sure you have proper Banner system access and permissions before deployment.