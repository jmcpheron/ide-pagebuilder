# Literal Content Extraction System

This system addresses the code review challenge of having HTML/CSS/JS embedded as strings in Banner Extensibility JSON files by extracting them into separate, reviewable files.

## Configuration

Before using this system, copy `.env.example` to `.env` and configure your institution's settings:

```bash
cp .env.example .env
# Edit .env with your institution's values
```

Required environment variables:
- `COLLEGE_NAME` - Your institution's name
- `COLLEGE_LOGO_URL` - URL to your college logo
- `BANNER_BASE_URL` - Your Banner ERP server URL
- `NAME_COACH_EVENT_CODE` - Your Name Coach event code
- `NAME_COACH_ACCESS_TOKEN` - Your Name Coach API token

**Note**: The `.env` file is git-ignored to prevent accidentally committing sensitive credentials.

## Problem

When HTML, CSS, and JavaScript are embedded as string values in JSON files:
- GitHub diffs are unreadable
- No syntax highlighting for embedded code
- Code formatting tools don't work
- Code review becomes nearly impossible
- Merge conflicts are difficult to resolve

## Solution

The `extract_literals.py` script provides a bidirectional workflow:

1. **Extract**: Pull literal content from JSON into separate `.html`, `.css`, `.js` files
2. **Edit**: Work with proper syntax highlighting and formatting
3. **Rebuild**: Update JSON files with changes from extracted files

## Usage

### Basic Commands

```bash
# Extract all literal content from page JSON files
python extract_literals.py extract

# Extract from specific files/pattern  
python extract_literals.py extract "free-tuition/*.json"

# Rebuild JSON files from extracted content
python extract_literals.py rebuild

# Check if extracted files are in sync with JSON
python extract_literals.py check
```

### Workflow Example

```bash
# 1. Extract literals before making changes
python extract_literals.py extract

# 2. Edit the extracted files in extracted_literals/ directory
# - Use your favorite editor with syntax highlighting
# - Make changes to .html, .css, .js files

# 3. Rebuild JSON files before committing
python extract_literals.py rebuild

# 4. Commit both the JSON and extracted files
git add .
git commit -m "Update page content"
```

## Directory Structure

After extraction, you'll see:

```
extracted_literals/
├── ftReview/
│   ├── style.css
│   ├── header.html  
│   ├── main_literal.html
│   ├── functions.js
│   ├── js.js
│   └── _extraction_map.json
├── efgByStu/
│   ├── style.css
│   ├── header.html
│   ├── main_literal.html
│   ├── functions.js
│   ├── js.js
│   └── _extraction_map.json
└── ...
```

## File Type Detection

The script automatically determines file extensions based on content:

- **`.js`**: Content with `<script>` tags or component names containing 'js', 'script', 'function'
- **`.css`**: Content with `<style>` tags or names containing 'css', 'style' 
- **`.html`**: Default for most literal content

## Git Integration

### Option 1: Manual Workflow
```bash
# Before editing
python extract_literals.py extract

# After editing  
python extract_literals.py rebuild
git add .
git commit -m "Your changes"
```

### Option 2: Git Hooks (Automated)

Create `.git/hooks/pre-commit`:
```bash
#!/bin/bash
# Auto-extract literals before commit
python extract_literals.py extract
git add extracted_literals/
```

Create `.git/hooks/post-merge`:
```bash
#!/bin/bash  
# Auto-rebuild after merging
python extract_literals.py rebuild
```

### Option 3: Make Commands

Add to your `Makefile`:
```makefile
.PHONY: extract rebuild check-sync

extract:
	python extract_literals.py extract

rebuild:  
	python extract_literals.py rebuild

check-sync:
	python extract_literals.py check

# Before committing
pre-commit: extract rebuild
	git add .
```

## Git Ignore Considerations

You have two options for `.gitignore`:

### Option A: Commit extracted files (Recommended)
```gitignore
# Don't ignore extracted_literals/ - commit them for better diffs
```

**Pros**: 
- Reviewers can see HTML/CSS/JS changes clearly
- Diffs are meaningful and reviewable
- No build step required for reviewers

**Cons**: 
- Slightly larger repository

### Option B: Generate on demand
```gitignore
extracted_literals/
```

**Pros**: 
- Smaller repository
- No duplicate content

**Cons**: 
- Reviewers must extract to see changes
- Loses the main benefit of readable diffs

## Troubleshooting

### Check sync status
```bash
python extract_literals.py check
```

### Files out of sync
If extracted files don't match JSON:
```bash
# Re-extract from JSON (loses extracted file changes)
python extract_literals.py extract

# OR rebuild JSON (keeps extracted file changes) 
python extract_literals.py rebuild
```

### Merge conflicts
1. Resolve conflicts in extracted files (easier to read)
2. Run `python extract_literals.py rebuild`
3. Commit the resolved state

## Benefits

✅ **Readable code reviews**: See actual HTML/CSS/JS changes in GitHub
✅ **Syntax highlighting**: Edit with proper language support  
✅ **Code formatting**: Use standard tools like Prettier, ESLint
✅ **Better merging**: Resolve conflicts in readable files
✅ **IDE support**: Full IntelliSense and error checking
✅ **Team friendly**: Junior developers can edit without JSON expertise

## Migration

For existing repositories:
1. Run `python extract_literals.py extract` once
2. Commit the extracted files
3. Team members can now edit extracted files instead of JSON
4. Use `rebuild` before deployment/commits

The original JSON files remain the source of truth for the Banner system, but development happens in the extracted files.