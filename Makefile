# Banner Extensibility Development Makefile
#
# Common tasks for working with literal content extraction

.PHONY: help extract rebuild check-sync clean install-hooks

help:
	@echo "Banner Extensibility Development Commands:"
	@echo ""
	@echo "  extract      - Extract literal content from JSON files for editing"
	@echo "  rebuild      - Rebuild JSON files from extracted content"
	@echo "  check-sync   - Check if extracted files are in sync with JSON"
	@echo "  clean        - Remove all extracted files"
	@echo "  install-hooks - Install git hooks for automatic extraction"
	@echo ""
	@echo "Typical workflow:"
	@echo "  1. make extract     # Before editing"
	@echo "  2. Edit files in extracted_literals/"
	@echo "  3. make rebuild     # Before committing"
	@echo "  4. git commit"

extract:
	@echo "🔄 Extracting literal content..."
	python3 extract_literals.py extract
	@echo "✅ Extraction complete!"

rebuild:
	@echo "🔄 Rebuilding JSON files..."
	python3 extract_literals.py rebuild
	@echo "✅ Rebuild complete!"

check-sync:
	@echo "🔍 Checking sync status..."
	python3 extract_literals.py check

clean:
	@echo "🧹 Cleaning extracted files..."
	rm -rf extracted_literals/
	@echo "✅ Cleaned!"

install-hooks:
	@echo "🔧 Installing git hooks..."
	@if [ ! -d .git ]; then echo "❌ Not in a git repository"; exit 1; fi
	cp sample-git-hooks/pre-commit .git/hooks/pre-commit
	cp sample-git-hooks/post-merge .git/hooks/post-merge
	chmod +x .git/hooks/pre-commit
	chmod +x .git/hooks/post-merge
	@echo "✅ Git hooks installed!"

# Development workflow shortcuts
dev-start: extract
	@echo "🚀 Ready for development! Edit files in extracted_literals/"

dev-commit: rebuild
	@echo "📝 Files rebuilt, ready to commit!"
	@echo "Run: git add . && git commit -m 'Your message'"

# Quality checks
lint-check: check-sync
	@echo "🔍 Running quality checks..."
	# Add other linting commands here if needed