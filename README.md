# Banner Extensibility Page Builder - Git-Friendly Code Review Tool

Hey, do you have trouble keeping track of your Banner Extensibility page changes? Trying to review HTML/CSS/JS code that's embedded as escaped strings in JSON files? Here's a tool to help translate the format to work better with Git repositories and make your development workflow much smoother.

## Quick Start

1. **Put your Banner Extensibility JSON files in a directory**
   ```bash
   my-banner-pages/
   ├── pages.my-custom-page.json
   ├── pages.another-page.json
   └── pages.third-page.json
   ```

2. **Extract the embedded HTML/CSS/JS into editable files**
   ```bash
   python extract_literals.py extract
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
   python extract_literals.py rebuild
   ```

That's it! Your JSON files are updated with the changes from your extracted files.

## What This Solves

Banner Extensibility pages store HTML/CSS/JS as escaped strings in JSON files, making:
- Code reviews nearly impossible
- Diffs unreadable  
- Syntax highlighting unavailable
- Merge conflicts difficult to resolve

This tool extracts that content into separate files so you can:
✅ **See actual code changes** in GitHub diffs  
✅ **Use full IDE features** - syntax highlighting, IntelliSense, formatting  
✅ **Use standard tools** - ESLint, Prettier, etc.  
✅ **Collaborate better** - Junior developers can edit without JSON expertise  

## Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd ide-pagebuilder

# Install dependencies with uv (modern Python package manager)
# If you don't have uv installed: pip install uv
uv install
```

## Usage

### Extract Literals
```bash
# Extract from all JSON files in current directory
uv run python extract_literals.py extract

# Extract from specific files
uv run python extract_literals.py extract "pages/*.json"

# Extract from specific directory
uv run python extract_literals.py extract "my-pages/**/*.json"
```

### Rebuild JSON Files
```bash
# Rebuild all extracted pages
uv run python extract_literals.py rebuild
```

### Check Sync Status
```bash
# Verify extracted files match JSON content
uv run python extract_literals.py check
```

## Project Structure

```
ide-pagebuilder/
├── extract_literals.py          # Main extraction tool
├── extracted_literals/          # Extracted HTML/CSS/JS files
│   ├── my-custom-page/
│   │   ├── header.html          # Extracted HTML
│   │   ├── main_literal.js      # Extracted JavaScript
│   │   ├── style.js             # Extracted CSS
│   │   └── _extraction_map.json # Rebuild mapping
│   └── ...
├── pages/                       # Your Banner Extensibility JSON files
│   ├── pages.my-custom-page.json
│   └── pages.another-page.json
├── tests/                       # Comprehensive test suite
│   ├── test_basics.py          # Basic functionality tests
│   ├── test_extract_literals.py # Extract/rebuild functionality tests
│   ├── test_json_structure.py  # JSON schema validation tests
│   ├── test_page_validation.py # Banner Extensibility validation tests
│   └── test_security.py        # Security-focused tests
├── pyproject.toml              # uv configuration and dependencies
├── uv.lock                     # Locked dependency versions
└── README.md
```

## How It Works

1. **Scans JSON files** for `literal` components with embedded HTML/CSS/JS
2. **Extracts content** into separate files with appropriate extensions (`.html`, `.js`, `.css`)
3. **Creates mapping** files to track relationships between extracted files and JSON
4. **Rebuilds JSON** by reading extracted files and updating the original JSON structure

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
- **`test_extract_literals.py`** - Tests for the core extract/rebuild functionality
  - File extension detection (HTML, CSS, JS)
  - JSON extraction and reconstruction
  - Sync status validation
  - Multiple content type handling
- **`test_json_structure.py`** - JSON schema and structure validation
  - Valid JSON formatting
  - Schema compliance
  - Component structure validation
  - Consistent indentation
- **`test_page_validation.py`** - Banner Extensibility specific validation
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
3. Extract literals: `uv run python extract_literals.py extract`
4. Make your changes in `extracted_literals/`
5. Rebuild: `uv run python extract_literals.py rebuild`
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## About

Hey there! I'm Jason, and I work at West Valley Mission Community College District. I built this toolkit to solve a real pain point I was having with Banner Extensibility development - trying to review HTML/CSS/JS code that was embedded as escaped strings in JSON files was driving me nuts!

This is my personal project that I'm sharing with my programming colleagues across California. If you're working with Banner Extensibility and dealing with the same frustrations, hopefully this toolkit will make your life easier too.

### Why I'm Sharing This
- 🎓 **California Community Colleges**: I know we're all dealing with similar challenges
- 🏛️ **Banner Schools**: Let's help each other out with better development workflows
- 🤝 **Open Source**: Feel free to use, modify, and contribute back

---

**Note**: This toolkit is designed for Banner ERP Extensibility custom pages. Make sure you have proper Banner system access and permissions before deployment.