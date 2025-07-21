# Scripts Directory

This directory contains utility scripts for the Python boilerplate system.

## Structure

```
scripts/
├── setup/          # Initial setup and configuration scripts
├── prp/            # PRP (Project Research Plan) automation tools
├── maintenance/    # System verification and maintenance
└── archive/        # Deprecated scripts (for reference only)
```

## Key Scripts

### Setup Scripts
- `setup/setup.sh` - Main setup script for new projects
- `setup/quick-setup.sh` - Fast setup for experienced users
- `setup/setup-hooks.sh` - Install Claude Code hooks
- `setup/setup-all-dependencies.sh` - Install Python dependencies

### PRP Scripts
- `prp/prp_runner.py` - Execute PRP plans automatically
- `prp/prp_validator.py` - Validate PRP implementation

### Maintenance Scripts
- `maintenance/verify-system.sh` - Verify system health
- `maintenance/verify-all-systems.py` - Comprehensive system check

## Usage

Most scripts should be run from the project root:

```bash
# Setup new project
./scripts/setup/setup.sh

# Run PRP
python scripts/prp/prp_runner.py path/to/prp.md

# Verify system
./scripts/maintenance/verify-system.sh
```
