# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## DevDocAI Project Overview

DevDocAI v3.5.0 is a **newly designed** AI-powered documentation system for solo developers that transforms documentation from a burden into an efficient, quality-driven workflow. This is a **greenfield project** being built from scratch based on comprehensive design specifications and documentation. The system will use the MIAIR (Meta-Iterative AI Refinement) methodology to achieve 60-75% quality improvement through multi-LLM synthesis (Claude, ChatGPT, Gemini).

### Project Status
- **Version**: 3.5.0
- **Stage**: Initial Implementation Phase (Building from Design Specifications)
- **Development Status**: First-time implementation - No existing codebase
- **Design Status**: Complete - Comprehensive specifications and documentation ready
- **License**: Apache-2.0 (Core), MIT (Plugin SDK)
- **Target Audience**: Solo developers and small development teams
- **Documentation**: Design documentation complete (Dec 2024)

## Core Architecture

### Modular Component System (M001-M013)

The system is designed to consist of 13 core modules organized in 4 implementation phases:

**Phase 1 - Foundation (M001-M007)**:
- M001: Configuration Manager - Memory mode detection and adaptive configuration
- M002: Local Storage System - Encrypted file operations with Argon2id
- M004: Document Generator - 40+ document types from templates
- M005: Tracking Matrix - Visual suite management dashboard
- M006: Suite Manager - Document consistency enforcement
- M007: Review Engine - Multi-dimensional quality analysis

**Phase 2 - Intelligence (M003, M008-M009, M011-M012)**:
- M003: MIAIR Engine - Meta-Iterative AI Refinement with entropy optimization
- M008: LLM Adapter - Multi-provider integration with cost management
- M009: Enhancement Pipeline - Progressive quality improvement workflow
- M011: Batch Operations - Parallel processing with resource optimization
- M012: Version Control - Git integration with auto-commit

**Phase 3 - Advanced (M010, M013)**:
- M010: SBOM Generator - SPDX 2.3 and CycloneDX 1.4 compliance
- M013: Template Marketplace - Community template sharing

**Phase 4 - Future**:
- Real-time collaboration features (planned)

### Memory Mode Architecture (Planned)

The system will automatically adapt to available hardware:
- **Baseline (<2GB)**: Templates only, no AI
- **Standard (2-4GB)**: Full features with cloud AI
- **Enhanced (4-8GB)**: Local AI models, heavy caching
- **Performance (>8GB)**: Maximum optimization

### Quality Gate System (Design Specification)

All documentation will need to achieve exactly 85% quality score across four dimensions:
1. Requirements Analysis (25%)
2. Design Review (25%)
3. Security Assessment (25%)
4. Performance Optimization (25%)

## Build and Development Commands

**Important**: These commands represent the planned implementation structure. As this is a greenfield project being built for the first time, these commands will become available as each module is implemented.

### Initial Setup (For Development)
```bash
# Clone and install dependencies
git clone https://github.com/devdocai/devdocai-v3.5.git
cd devdocai-v3.5
npm install

# Install Python dependencies for AI features
pip install -r requirements.txt

# Generate security keys
npm run security:keygen
npm run security:generate-signing-keys
npm run security:generate-cert

# Configure environment
cp .devdocai.example.yml .devdocai.yml
cp .env.example .env
```

### Build Commands (To Be Implemented)
```bash
# Build specific phases
npm run build:foundation     # M001-M002, M004-M007
npm run build:intelligence   # M003, M008-M009, M011-M012
npm run build:advanced       # M010, M013

# Complete production build
npm run build:prod           # All components + packaging

# Platform-specific builds
npm run build:win           # Windows executable
npm run build:mac           # macOS application
npm run build:linux         # Linux binary
```

### Testing Commands (To Be Implemented)
```bash
# Run test suites
npm test                    # All tests
npm run test:unit          # Unit tests only
npm run test:integration   # Integration tests
npm run test:e2e           # End-to-end tests
npm run test:performance   # Performance benchmarks
npm run test:security      # Security audits
npm run test:compliance    # WCAG 2.1 AA compliance

# Coverage and quality
npm run test:coverage      # Generate coverage report
npm run quality:check      # Verify 85% quality gate
```

### Development Commands
```bash
# Development mode
npm run dev                # Start development server
npm run dev:extension      # VS Code extension dev mode
npm run dev:cli           # CLI development mode

# Code quality
npm run lint              # ESLint checks
npm run format            # Prettier formatting
npm run typecheck         # TypeScript validation

# Plugin development
npm run plugin:scaffold   # Create new plugin template
npm run plugin:verify     # Verify plugin signatures
npm run plugin:package    # Package for marketplace
```

### Deployment Commands
```bash
# VS Code extension
npm run vsce:package      # Package extension
npm run vsce:publish      # Publish to marketplace

# CLI distribution
npm run cli:package       # Create CLI packages
npm run cli:sign         # Sign with Ed25519

# Docker
npm run docker:build      # Build Docker image
npm run docker:push      # Push to registry
```

## Compliance Features

### SBOM Generation (M010)
```bash
# Generate Software Bill of Materials
devdocai sbom --format spdx    # SPDX 2.3 format
devdocai sbom --format cyclonedx # CycloneDX 1.4 format
devdocai sbom --sign           # With Ed25519 signature
```

### PII Detection
```bash
# Scan for personally identifiable information
devdocai pii scan --sensitivity medium
devdocai pii report --format json
```

### Data Subject Rights (DSR)
```bash
# Handle GDPR/CCPA requests
devdocai dsr export --user <id>
devdocai dsr delete --user <id>
devdocai dsr anonymize --user <id>
```

## Plugin Development

Plugins use the MIT-licensed SDK and require:
1. Ed25519 digital signature
2. Certificate validation
3. Malware scanning
4. Sandboxed execution
5. Quality gate compliance (85%)

```javascript
// Plugin structure
class CustomPlugin extends Plugin {
  constructor() {
    super({
      name: 'plugin-name',
      version: '1.0.0',
      devdocaiVersion: '>=3.5.0',
      permissions: ['documents.read', 'documents.write'],
      memoryMode: 'standard'
    });
  }
}
```

## Important Conventions

### File Organization
- Core modules: `src/modules/M###-name/`
- Plugins: `plugins/plugin-name/`
- Templates: `templates/category/template.md`
- Tests: Mirror source structure in `tests/`

### Licensing
- Core system: Apache-2.0
- Plugin SDK: MIT
- All contributions must comply with dual-license model

### Security Requirements
- All plugins must be signed with Ed25519
- Local storage uses Argon2id encryption
- API keys stored in `.env` (never commit)
- Certificate validation for marketplace

### Performance Targets
- Document generation: <5 seconds
- AI enhancement: <30 seconds
- Quality analysis: <10 seconds
- Memory usage: Adaptive to mode

## Key Integration Points

### VS Code Extension
- Entry point: `src/extension/extension.ts`
- Activation events in `package.json`
- WebView for tracking matrix: `src/extension/webview/`

### CLI Interface
- Entry point: `src/cli/index.ts`
- Commands defined in `src/cli/commands/`
- Configuration: `.devdocai.yml`

### LLM Integration
- Providers: `src/modules/M008-llm-adapter/providers/`
- Cost tracking: `src/modules/M008-llm-adapter/cost-manager.ts`
- Rate limiting per provider API limits

### Template System
- Base templates: `templates/base/`
- Custom templates: User's `.devdocai/templates/`
- Marketplace templates: Downloaded to `templates/marketplace/`

## Project Roadmap

### Completed (Design Phase)
- Core modular architecture design (M001-M013)
- MIAIR Engine specification
- Multi-LLM integration design
- Quality gate system architecture (85% threshold)
- Plugin SDK design with digital signatures
- Comprehensive documentation and specifications

### Current Phase (Initial Implementation)
- Setting up project foundation
- Implementing Phase 1 modules (M001-M007)
- Creating base infrastructure

### Upcoming Phases
- Phase 2: Intelligence modules (M003, M008-M009, M011-M012)
- Phase 3: Advanced features (M010, M013)
- VS Code extension development
- Template marketplace infrastructure

### Future Enhancements
- Real-time collaboration features
- Cloud sync capabilities
- Advanced analytics dashboard
- Mobile companion app

## Contributing Guidelines

### Code Style
- Follow TypeScript best practices
- Use ESLint and Prettier configurations
- Maintain 80% test coverage minimum
- Document all public APIs

### Pull Request Process
1. Create feature branch from `main`
2. Implement changes with tests
3. Ensure quality gate passes (85%)
4. Submit PR with detailed description
5. Address review feedback

### Issue Reporting
- Use GitHub issue templates
- Include reproduction steps
- Attach relevant logs
- Specify environment details

## Documentation Structure

The design documentation has been organized into a hierarchical, module-based structure:

```
docs/
├── 01-requirements/      # PRDs, user stories, requirements
├── 02-architecture/      # System design, architecture docs
├── 03-specifications/    # API docs, data models, schemas
├── 04-deployment/        # Installation, configuration, CI/CD
├── 05-testing/          # Test plans, QA strategies
├── 06-user-guides/      # User manuals, tutorials, FAQs
├── meta/                # Documentation standards, templates
├── modules/             # Module definitions (M001-M013)
├── DOCUMENT_INDEX.md    # Master catalog of all documentation
├── TAXONOMY.md          # Document classification system
├── NAVIGATION.md        # Navigation guide and quick paths
└── AI_AGENT_GUIDE.md    # Optimized guide for AI assistants
```

### Key Documentation Files

- **Requirements**: `/docs/01-requirements/devdocai-v3.5-prd.md`
- **Architecture**: `/docs/02-architecture/devdocai-v3.5-architecture.md`
- **Build Instructions**: `/docs/04-deployment/devdocai-v3.5-build-instructions.md`
- **Module Definitions**: `/docs/modules/MODULE_DEFINITIONS.md`

## Support and Resources

- **Documentation Index**: `/docs/DOCUMENT_INDEX.md`
- **Navigation Guide**: `/docs/NAVIGATION.md`
- **API Reference**: Generated from TypeScript definitions (when implemented)
- **Examples**: See `/examples` for usage patterns (when available)
- **Community**: GitHub Discussions for Q&A

## Quick Start (Once Implemented)

```bash
# Install DevDocAI globally (when published)
npm install -g devdocai

# Initialize in your project
devdocai init

# Generate your first document
devdocai generate readme

# Run quality analysis
devdocai quality check
```

## Development Information

This is a **greenfield project** being built from scratch. The creator has designed the complete system architecture and documentation, and we are now in the initial implementation phase. 

### For Developers
- All design specifications are complete in the `/docs` directory
- Implementation follows the phased approach outlined in the module definitions
- Each module (M001-M013) has detailed specifications ready for implementation
- The project uses TypeScript with a modular architecture

## Contact

- **Repository**: https://github.com/devdocai/devdocai-v3.5
- **Issues**: https://github.com/devdocai/devdocai-v3.5/issues
- **Discussions**: https://github.com/devdocai/devdocai-v3.5/discussions