# Virtual Domains

This directory contains Banner Extensibility virtual domain definitions for the West Valley Mission College pagebuilder project.

## What are Virtual Domains?

Virtual domains in Banner Extensibility are JSON-based API endpoint definitions that:
- Define SQL queries for GET, POST, PUT, DELETE operations  
- Handle security/role-based access control
- Translate HTTP requests into database operations
- Return data in JSON format for consumption by pages

## Directory Structure

```
project-root/
├── virtualDomains/
│   ├── README.md                               # This file
│   └── virtualDomains.{serviceName}.json      # Virtual domain definitions
└── extracted_virtual_domains/                 # Extracted SQL files (when using extraction tool)
    └── {serviceName}/
        ├── codeget.sql                         # GET operation SQL
        ├── codepost.sql                        # POST operation SQL (if exists)
        ├── codeput.sql                         # PUT operation SQL (if exists)
        ├── codedelete.sql                      # DELETE operation SQL (if exists)
        └── _extraction_map.json                # Mapping for rebuilding JSON
```

## Virtual Domain Structure

Each virtual domain JSON file contains:

- `serviceName`: Unique identifier for the API endpoint
- `codeGet`: SQL query for GET requests (most common)
- `codePost`: SQL for creating new records
- `codePut`: SQL for updating existing records  
- `codeDelete`: SQL for deleting records
- `virtualDomainRoles`: Array of role-based permissions
- `typeOfCode`: Usually "S" for SQL
- Other metadata fields

## G0 Number Convention

This project uses West Valley Mission College's local Banner ID format where student IDs are called "G0 numbers". In virtual domain SQL:
- Use `:gid` parameter for G0 number inputs
- Reference `spriden_id` field for G0 numbers in Banner tables

## Working with Virtual Domains

### Extract SQL for Editing
```bash
# Extract SQL code from JSON files into editable .sql files
uv run python extract_virtual_domains.py extract "virtualDomains/*.json"
```

### Edit SQL Files
After extraction, edit the `.sql` files in `extracted_virtual_domains/{serviceName}/` using your preferred SQL editor with syntax highlighting and validation.

### Rebuild JSON Files
```bash  
# Rebuild JSON files from edited SQL files
uv run python extract_virtual_domains.py rebuild
```

### Check Sync Status
```bash
# Check if extracted files are in sync with JSON
uv run python extract_virtual_domains.py check
```

## Security Considerations

- All SQL queries use parameterized inputs (`:parameter_name`) to prevent SQL injection
- Virtual domain roles control access permissions per HTTP method
- Use Banner's built-in security context (`:parm_user_pidm`) where appropriate
- Never hardcode sensitive data in SQL queries

## Testing

Run virtual domain tests:
```bash
uv run pytest tests/test_virtual_domains.py -v
```

## Example Virtual Domain

See `virtualDomains.spridenName.json` for a working example that:
- Accepts a G0 number (`:gid` parameter)
- Queries student name information from Banner tables
- Handles preferred name display logic
- Includes appropriate role-based security