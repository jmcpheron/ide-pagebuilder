# Banner Extensibility Page Builder - Git-Friendly Code Review Tool

Hey, do you have trouble keeping track of your Banner Extensibility page changes? Trying to review HTML/CSS/JS code that's embedded as escaped strings in JSON files? Here's a tool to help translate the format to work better with Git repositories and make your development workflow much smoother.

## 🚀 Features

- **Literal Content Extraction**: Extract embedded HTML/CSS/JS from JSON files into separate, syntax-highlighted files
- **Code Review Friendly**: See actual code changes in GitHub diffs instead of escaped JSON strings
- **Bi-directional Sync**: Extract for editing, rebuild for deployment
- **Development Workflow**: Makefile commands and git hooks for seamless development
- **Security First**: Environment variable configuration prevents credential leaks

## 📋 Prerequisites

- Python 3.7+
- Banner ERP Extensibility access

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
│   ├── example-page/
│   │   ├── main_literal.js      # JavaScript with syntax highlighting
│   │   ├── style.js             # CSS styles  
│   │   └── _extraction_map.json # Rebuild mapping
│   └── ...
├── example-pages/               # Example page implementations
│   ├── pages.example1.json
│   └── pages.example2.json
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

The project includes example pages to demonstrate the extraction system:
- **Example pages**: Various implementations showing different use cases
- **Custom integrations**: Templates for building your own Banner Extensibility pages

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

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Support

- **Issues**: Report bugs and request features via GitHub Issues
- **Documentation**: Check `README_LITERALS.md` for detailed workflows
- **Community**: Share experiences and get help from other Banner developers

## 👨‍💻 About

Hey there! I'm Jason, and I work at West Valley Mission Community College District. I built this toolkit to solve a real pain point I was having with Banner Extensibility development - trying to review HTML/CSS/JS code that was embedded as escaped strings in JSON files was driving me nuts!

This is my personal project that I'm sharing with my programming colleagues across California. If you're working with Banner Extensibility and dealing with the same frustrations, hopefully this toolkit will make your life easier too.

### Why I'm Sharing This
- 🎓 **California Community Colleges**: I know we're all dealing with similar challenges
- 🏛️ **Banner Schools**: Let's help each other out with better development workflows
- 🤝 **Open Source**: Feel free to use, modify, and contribute back

---

**Note**: This toolkit is designed for Banner ERP Extensibility custom pages. Make sure you have proper Banner system access and permissions before deployment.