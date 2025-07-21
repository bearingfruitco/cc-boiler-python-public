# CHANGELOG

## [2.4.1] - 2025-01-20

### Added
- **Automatic Test-Driven Development (TDD)**
  - Tests now generate automatically when starting work
  - New hook: `13-auto-test-generation.py` monitors workflow triggers
  - Enhanced commands: `/fw start`, `/pt`, `/cti --tests`
  - Test status visibility throughout development
  - Configurable TDD enforcement in settings.json

- **New Commands**
  - `/generate-tests` - Manual test generation from PRD/PRP/Issues
  - `/tdd-config` - Configure TDD settings and enforcement
  - `/fw test-status` - Check TDD progress for features

- **New Hooks**
  - `18-cloud-config-validator.py` - Validates cloud deployments
  - `19-test-generation-enforcer.py` - Blocks code without tests
  - `12-code-test-validator.py` - Auto-runs tests after changes

- **Enhanced Documentation**
  - Daily Workflow Guide - Complete command flows
  - Day 1 Quick Start - 30-minute onboarding
  - Getting Started Guide - Comprehensive introduction
  - Command Reference Card - Printable quick reference
  - System Overview - Architecture and features

### Changed
- `/fw start` now auto-generates tests from GitHub issues
- `/pt` enforces TDD by checking for tests before implementation
- `/cti --tests` creates issue AND generates tests in one command
- Updated all workflow chains to include TDD steps
- Enhanced PRP progress tracking to suggest test generation

### Fixed
- Hook permissions now properly set as executable
- Import validation handles circular dependencies better
- Context preservation improved for long sessions

## [2.4.0] - 2025-01-19

### Added
- Smart Issue Creation & Dependency Tracking
- Python Dependency Management with `/pydeps`
- Creation Guard to prevent duplicate modules
- Response Capture for AI analyses
- PRP (Product Requirement Prompt) system
- Multi-agent orchestration with parallel execution

### Changed
- Enhanced Python-specific workflows
- Improved context management
- Better error handling in hooks

## [2.3.6] - 2025-01-15

### Added
- Async Event-Driven Architecture
- Event Queue System with fire-and-forget pattern
- Parallel processing detection
- Required loading states for async operations
- Smart form events with tracking hooks
- Timeout protection for external calls

## [2.3.4] - 2025-01-10

### Added
- CodeRabbit Integration for real-time code review
- Dual-AI workflow (Claude generates, CodeRabbit reviews)
- PR feedback monitoring

## [2.3.0] - 2025-01-05

### Added
- Grove-Inspired Enhancements
- PRD Clarity Linter
- Specification pattern extraction
- Test generation from PRD acceptance criteria
- Implementation grading (0-100% alignment score)
