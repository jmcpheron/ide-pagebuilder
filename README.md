# Banner Extensibility PageBuilder

A development toolkit for Banner ERP Extensibility custom pages with an innovative literal content extraction system that makes HTML/CSS/JS code reviewable and maintainable.

## 🚀 Features

- **Literal Content Extraction**: Extract embedded HTML/CSS/JS from JSON files into separate, syntax-highlighted files
- **Code Review Friendly**: See actual code changes in GitHub diffs instead of escaped JSON strings
- **Bi-directional Sync**: Extract for editing, rebuild for deployment
- **Development Workflow**: Makefile commands and git hooks for seamless development
- **Security First**: Environment variable configuration prevents credential leaks

## 📋 Prerequisites

- Python 3.7+
- Banner ERP Extensibility access
- Name Coach account (for name pronunciation features)

## ⚙️ Quick Start

### 1. Configuration

Copy the environment template and configure your settings:

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

### 2. Extract Literals for Development

```bash
# Extract all literal content for editing
make extract

# Or use Python directly
python extract_literals.py extract
```

### 3. Development Workflow

```bash
# 1. Extract literals before editing
make extract

# 2. Edit files in extracted_literals/ directory with full IDE support

# 3. Rebuild JSON files before deployment
make rebuild

# 4. Deploy to Banner
# Upload the updated JSON files to Banner Extensibility
```

## 📁 Project Structure

```
banner-extensibility-pagebuilder/
├── extract_literals.py          # Main extraction tool
├── extracted_literals/          # Extracted HTML/CSS/JS files
│   ├── name-coach-v3/
│   │   ├── main_literal.js      # JavaScript with syntax highlighting
│   │   ├── style.js             # CSS styles  
│   │   └── _extraction_map.json # Rebuild mapping
│   └── ...
├── name-coach/                  # Name Coach integration pages
│   ├── pages.name-coach-v3.json
│   └── pages.name-coach.json
├── free-tuition/               # Free tuition status pages
│   ├── pages.ftReview.json
│   └── pages.efgByStu.json
├── sample-git-hooks/           # Optional automation
│   ├── pre-commit
│   └── post-merge
├── .env.example               # Configuration template
├── Makefile                   # Development commands
└── README_LITERALS.md         # Detailed extraction documentation
```

## 🔧 Available Commands

```bash
# Development workflow
make extract      # Extract literals for editing
make rebuild      # Rebuild JSON from extracted files
make check-sync   # Verify files are in sync
make clean        # Remove extracted files

# Git integration
make install-hooks # Install automated git hooks

# Quick shortcuts
make dev-start    # Extract and start development
make dev-commit   # Rebuild and prepare for commit
```

## 📄 Sample Pages

### Name Coach Integration
- **name-coach-v3**: Modern name pronunciation recording interface
- **name-coach**: Legacy name coach implementation

### Free Tuition Status
- **ftReview**: AB 3158 free tuition eligibility checker
- **efgByStu**: Student-specific tuition status display

## 🛠️ How It Works

### The Problem
Banner Extensibility pages store HTML/CSS/JS as escaped strings in JSON files, making:
- Code reviews nearly impossible
- Diffs unreadable
- Syntax highlighting unavailable
- Merge conflicts difficult to resolve

### The Solution
Our extraction system:
1. **Extracts** literal content into separate `.html`, `.css`, `.js` files
2. **Preserves** the relationship via extraction maps
3. **Rebuilds** JSON files from the edited content
4. **Maintains** Banner compatibility

### Benefits
✅ **Readable code reviews** - See actual HTML/CSS/JS changes in GitHub  
✅ **Full IDE support** - Syntax highlighting, IntelliSense, formatting  
✅ **Standard tooling** - Use ESLint, Prettier, etc.  
✅ **Better collaboration** - Junior developers can edit without JSON expertise  
✅ **Easier merging** - Resolve conflicts in readable files  

## 🔒 Security

- **Environment Variables**: Sensitive credentials stored in `.env` (git-ignored)
- **Token Templating**: API keys replaced with `${VARIABLE}` placeholders
- **No Hardcoded Values**: Institution-specific values externalized

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Extract literals: `make extract`
4. Make your changes in `extracted_literals/`
5. Rebuild: `make rebuild`
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## 📚 Documentation

- [Detailed Extraction Guide](README_LITERALS.md) - Complete workflow documentation
- [Banner Extensibility Docs](https://banner.ellucian.com/) - Official Banner documentation
- [Name Coach Integration](https://www.name-coach.com/) - Name pronunciation service

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Support

- **Issues**: Report bugs and request features via GitHub Issues
- **Documentation**: Check `README_LITERALS.md` for detailed workflows
- **Community**: Share experiences and get help from other Banner developers

## 🏫 About

Created by **West Valley Mission Community College District** for educational institutions using Banner ERP Extensibility to build custom student and faculty portals. 

We're excited to share this toolkit with other **California Community Colleges** and **Banner schools** to help improve student services and development workflows across our educational community.

### Community Collaboration
- 🎓 **California Community Colleges**: We welcome collaboration and knowledge sharing
- 🏛️ **Banner Schools**: Open to partnerships with other Banner ERP institutions
- 🤝 **Contributions Welcome**: Help us improve tools for the educational community

---

**Note**: This toolkit is designed for Banner ERP Extensibility custom pages. Ensure you have proper Banner system access and permissions before deployment.