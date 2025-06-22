# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Banner Extensibility pagebuilder project for West Valley Mission College (WVM), specifically focused on a Thomas Meal Plan portal. The project contains custom page definitions and virtual domain configurations that integrate with the Banner ERP system.

## Architecture

The project follows Banner Extensibility's JSON-based page definition structure:

- **Page definitions** (`pages.*.json`): Define the UI components, layout, and interactions for custom pages
- **Virtual domains** (`virtualDomains.*.json`): Define SQL queries and API endpoints that pages can consume
- **Database schema** (`.sql` files): Define custom database tables used by the virtual domains

### Key Components

- `pages.thomas_meal_plan.json`: Main page definition for the meal plan portal
- `virtualDomains.meal_plan_single.json`: API endpoint that queries student meal plan data
- `szbmpln.sql`: Database table definition for meal plan records

## Page Structure

Pages in this system use a component-based architecture with:

- **Literal components**: Raw HTML/CSS/JS content
- **Block components**: Containers for other components with styling
- **Form components**: Interactive elements like select dropdowns
- **Model bindings**: Connect components to virtual domain data sources

## Database Integration

The system uses Oracle SQL with Banner's security model:
- Queries use `:parm_user_pidm` parameter for user context
- Virtual domains handle parameterized queries securely
- Role-based access control through `pageRoles` and `virtualDomainRoles`

## File Naming Conventions

- `pages.{identifier}.json`: Page definitions
- `virtualDomains.{service_name}.json`: API endpoint definitions
- `{table_name}.sql`: Database schema definitions

## Development Setup

This project uses uv for modern Python dependency management and development workflows:

### Setup
```bash
uv sync
```

### Common Commands
```bash
# Run tests
uv run pytest

# Format code
uv run ruff format

# Check code quality
uv run ruff check

# Run extract_literals script
uv run python extract_literals.py extract
uv run python extract_literals.py rebuild
uv run python extract_literals.py check
```

### Testing
The project includes comprehensive test suites:
- **Page validation tests**: Validate JSON structure and Banner Extensibility compliance
- **JSON structure tests**: Schema validation and syntax checking
- **Security tests**: Check for hardcoded secrets and dangerous patterns
- **Extract literals tests**: Test the literal extraction/rebuild functionality

Run all tests: `uv run pytest tests/ -v`