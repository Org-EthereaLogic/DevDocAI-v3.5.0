<refined_build_instructions>

# DevDocAI v3.5.0 Build Instructions

---
⚠️ **STATUS: DESIGN SPECIFICATION - NOT IMPLEMENTED** ⚠️

**Document Type**: Design Specification  
**Implementation Status**: 0% - No code written  
**Purpose**: Blueprint for future development  

> **This document describes planned functionality and architecture that has not been built yet.**
> All code examples, commands, and installation instructions are design specifications for future implementation.

---

📚 **IMPORTANT FOR READERS**

This document describes how DevDocAI will work once implemented. Currently:

- ❌ No working software exists
- ❌ Installation commands will not work
- ❌ No packages are available for download
- ✅ This is a comprehensive design specification

---

**Version:** 3.5.0  
**Date:** August 21, 2025  
**Status:** FINAL - Suite Aligned v3.5.0  
**License:** Apache-2.0 (Core), MIT (Plugin SDK)

## Prerequisites

### Core Requirements

1. **Node.js** (v18.0.0 or higher, v20.0.0 recommended)
   - Download from: <https://nodejs.org/>
   - Verify installation: `node --version`

2. **npm** (v9.0.0 or higher) or **yarn** (v1.22.0 or higher)
   - npm comes with Node.js
   - Verify installation: `npm --version` or `yarn --version`

3. **Python** (v3.8.0 or higher, v3.11.0 recommended)
   - Required for local AI models and PII detection
   - Download from: <https://python.org/>
   - Verify installation: `python --version`

4. **Git** (v2.30.0 or higher)
   - Download from: <https://git-scm.com/>
   - Verify installation: `git --version`

5. **Visual Studio Code** (v1.85.0 or higher)
   - Download from: <https://code.visualstudio.com/>
   - Required for extension development and testing

### Development Tools

All development tools are managed as project-level dependencies to ensure version consistency and build repeatability:

```bash
# Clone repository first (see Environment Configuration section)
# Then install all development dependencies locally
npm install

# This installs the following tools as devDependencies:
# - yo@4.3.1
# - generator-code@1.7.8
# - vsce@2.15.0
# - typescript@5.3.3
# - @devdocai/cli@3.5.0

# Install Python dependencies for AI features
pip install -r requirements.txt
```

> **Note**: All development tools are installed locally within the project to ensure consistent versions across all development environments. The specific versions are locked in `package-lock.json` for reproducibility.

### Using Local Development Tools

After installation, use the locally installed tools via npm scripts:

```bash
# Instead of global commands, use:
npm run vsce -- package           # Package VS Code extension
npm run yo -- code                # Generate extension scaffolding
npm run tsc -- --version          # TypeScript compiler
npx devdocai --version            # DevDocAI CLI
```

### Memory Mode Requirements

Select your memory mode based on available RAM:

| Mode | RAM Required | Features Available |
|------|--------------|-------------------|
| **Baseline** | <2GB | Templates only, no AI |
| **Standard** | 2-4GB | Full features, cloud AI |
| **Enhanced** | 4-8GB | Local AI models, caching |
| **Performance** | >8GB | All features, max optimization |

## Environment Configuration

### 1. Future Build Process (Not Yet Available)

Once development begins, the build process will follow these steps:

#### Phase 1: Setting Up Development Environment

*Estimated Timeline: Month 1-2 of development*

1. Repository will be created at: <https://github.com/devdocai/devdocai-v3.5>
2. Initial project structure will include:
   - `/src` (source code - TO BE DEVELOPED)
   - `/docs` (design documentation - CURRENTLY AVAILABLE)
   - `/tests` (test suites - TO BE DEVELOPED)
   - `/plugins` (plugin system - TO BE DEVELOPED)
   - `/templates` (document templates - TO BE DEVELOPED)

```bash
# [PLANNED] Commands for future implementation:
# git clone https://github.com/devdocai/devdocai-v3.5.git
# cd devdocai-v3.5
```

**Current Status**: [DESIGN PHASE] Repository structure and build processes are fully designed and ready for implementation.

### 2. [PLANNED] Dependency Installation Process

#### Phase 2: Development Environment Setup

*Estimated Timeline: Month 2 of development*

```bash
# [TO BE DEVELOPED] Future dependency installation commands:
# npm install
# 
# Development tools that will be included:
# - yo@4.3.1 (VS Code extension scaffolding)
# - generator-code@1.7.8 (Extension templates)
# - vsce@2.15.0 (Extension packaging)
# - typescript@5.3.3 (TypeScript compiler)
# - @devdocai/cli@3.5.0 (Main CLI tool)
#
# Verification commands (when implemented):
# npx yo --version                  # Should show 4.3.1
# npx generator-code --version      # Should show 1.7.8
# npx vsce --version                # Should show 2.15.0
# npx tsc --version                 # Should show 5.3.3
# npx devdocai --version            # Should show 3.5.0
```

**Implementation Status**: [TO BE DEVELOPED] Package.json and dependency configuration designed but not yet created.

### 3. [PLANNED] Memory Mode Configuration

#### Phase 3: System Configuration Setup

*Estimated Timeline: Month 2-3 of development*

**Planned Configuration System**: When implemented, users will configure system memory modes through a `.devdocai.yml` file.

```bash
# [TO BE DEVELOPED] Future configuration commands:
# cp .devdocai.example.yml .devdocai.yml
```

**Planned Configuration Format**:

```yaml
# [DESIGN SPECIFICATION] Configuration file structure:
version: 3.5.0
system:
  memory_mode: standard  # baseline | standard | enhanced | performance
  quality_gate: 85       # Exactly 85% for CI/CD
  
performance:
  max_concurrent: 4      # Adjust based on memory mode
  cache_enabled: true
  batch_size: 10
```

**Implementation Status**: [TO BE DEVELOPED] Configuration system designed, awaiting implementation.

### 4. [PLANNED] API Keys and Cloud Configuration

#### Phase 4: Cloud Integration Setup

*Estimated Timeline: Month 3-4 of development*

**Planned Environment Configuration**: When implemented, users will configure API keys and cost management through environment files.

```bash
# [TO BE DEVELOPED] Future environment setup commands:
# cp .env.example .env
```

**Planned Environment Configuration Format**:

```env
# [DESIGN SPECIFICATION] Environment variable structure:
# LLM Provider APIs (Optional)
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GOOGLE_AI_API_KEY=your_google_ai_api_key_here

# Cost Management (REQ-044)
DAILY_COST_LIMIT=10.00    # USD
MONTHLY_COST_LIMIT=200.00 # USD
WARNING_THRESHOLD=0.80     # 80% warning

# Security Configuration
ENCRYPTION_KEY=generate_with_devdocai_keygen
SIGNING_KEY_PATH=./keys/ed25519_private.pem
CERTIFICATE_PATH=./certs/devdocai.cert
```

**Implementation Status**: [TO BE DEVELOPED] Cost management and API integration systems designed, awaiting implementation.

### 5. [PLANNED] Security Key Generation

#### Phase 5: Security Infrastructure Setup

*Estimated Timeline: Month 4-5 of development*

**Planned Security System**: When implemented, the system will include automated security key generation for encryption, plugin signing, and certificate management.

```bash
# [TO BE DEVELOPED] Future security setup commands:
# npm run security:keygen                    # Generate encryption keys for local storage
# npm run security:generate-signing-keys     # Generate Ed25519 signing keys for plugins
# npm run security:generate-cert             # Generate self-signed certificate for development
```

**Security Features to be Implemented**:

- Plugin signature verification system
- Local data encryption system  
- Certificate-based trust chain
- Key rotation and management tools

**Implementation Status**: [TO BE DEVELOPED] Security architecture designed, awaiting implementation.

## [PLANNED] Build Process - Implementation Roadmap

**Overall Development Timeline**: Estimated 8-12 months for full implementation

### Development Phase 1: Foundation Components [PLANNED]

**Timeline**: Month 1-3 of development  
**Status**: [TO BE DEVELOPED] Architecture designed, ready for implementation

**Planned Foundation Build Process**:

```bash
# [FUTURE IMPLEMENTATION] Build commands for foundation layer:
# npm run build:foundation
#
# Components to be built (M001-M002, M004-M007):
# - Configuration Manager (M001) - System configuration and memory modes
# - Local Storage System (M002) - Encrypted local data storage
# - Document Generator (M004) - Template-based document creation
# - Tracking Matrix (M005) - Requirement traceability system
# - Suite Manager (M006) - Multi-document management
# - Review Engine (M007) - Quality scoring and analysis
```

**Implementation Priority**: High - Required for basic functionality

### Development Phase 2: Intelligence Components [PLANNED]

**Timeline**: Month 4-6 of development  
**Status**: [TO BE DEVELOPED] AI integration architecture designed

**Planned Intelligence Build Process**:

```bash
# [FUTURE IMPLEMENTATION] Build commands for intelligence layer:
# npm run build:intelligence
#
# Components to be built (M003, M008-M009, M011-M012):
# - MIAIR Engine (M003) - AI-powered document analysis
# - LLM Adapter with Cost Management (M008) - Multi-provider AI integration
# - Enhancement Pipeline (M009) - Document improvement workflows
# - Batch Operations Manager (M011) - Bulk processing system
# - Version Control Integration (M012) - Git workflow automation
```

**Implementation Priority**: Medium - Builds on foundation components

### Development Phase 3: Advanced Components [PLANNED]

**Timeline**: Month 7-9 of development  
**Status**: [TO BE DEVELOPED] Compliance and marketplace systems designed

**Planned Advanced Build Process**:

```bash
# [FUTURE IMPLEMENTATION] Build commands for advanced features:
# npm run build:advanced
#
# Components to be built (M010, M013):
# - SBOM Generator (M010) - Software Bill of Materials generation
# - Template Marketplace Client (M013) - Community template sharing
# - PII Detection Engine - Privacy compliance automation
# - DSR Handler - Data subject request processing
# - Dashboard - Web-based project overview
```

**Implementation Priority**: Low - Premium/compliance features

### Complete Build System [PLANNED]

**Timeline**: Month 10-12 of development  
**Status**: [TO BE DEVELOPED] Production build system designed

**Planned Production Build Process**:

```bash
# [FUTURE IMPLEMENTATION] Full production build command:
# npm run build:prod
#
# Planned build artifacts:
# - dist/devdocai-extension-3.5.0.vsix (VS Code extension package)
# - dist/devdocai-cli-{platform}-3.5.0 (CLI executables for each platform)
# - dist/plugins/ (Core plugins with signatures)
# - dist/templates/ (Document templates library)
# - dist/models/ (Local AI models for enhanced mode)
# - dist/certificates/ (Security certificates and keys)
```

**Build System Features to be Implemented**:

- Multi-platform compilation (Windows, macOS, Linux)
- Code signing and verification
- Dependency bundling and optimization
- Test execution and coverage reporting

## [PLANNED] Platform-Specific Build System

**Status**: [TO BE DEVELOPED] Cross-platform build system designed but not yet implemented

### Windows Build Process [PLANNED]

**Planned Windows Build Configuration**:

```bash
# [FUTURE IMPLEMENTATION] Windows-specific build commands:
# set DEVDOCAI_MEMORY_MODE=standard
# npm run build:win
#
# Planned output: dist/devdocai-cli-win-3.5.0.exe
```

**Windows-Specific Features to be Implemented**:

- Windows Service integration for background processing
- Windows Certificate Store integration
- PowerShell module for advanced automation
- Windows-specific performance optimizations

### macOS Build Process [PLANNED]

**Planned macOS Build Configuration**:

```bash
# [FUTURE IMPLEMENTATION] macOS-specific build commands:
# export DEVDOCAI_MEMORY_MODE=enhanced
# npm run build:mac
#
# Planned outputs: 
# - dist/devdocai-cli-mac-x64-3.5.0 (Intel Macs)
# - dist/devdocai-cli-mac-arm64-3.5.0 (Apple Silicon Macs)
```

**macOS-Specific Features to be Implemented**:

- macOS Keychain integration for secure key storage
- Universal binary support (Intel + Apple Silicon)
- macOS sandboxing compliance
- Launch Agent integration for background services

### Linux Build Process [PLANNED]

**Planned Linux Build Configuration**:

```bash
# [FUTURE IMPLEMENTATION] Linux-specific build commands:
# export DEVDOCAI_MEMORY_MODE=performance
# npm run build:linux
#
# Planned output: dist/devdocai-cli-linux-3.5.0
```

**Linux-Specific Features to be Implemented**:

- systemd service integration for background processing
- Linux kernel keyring integration for secure storage
- AppImage packaging for portable distribution
- Docker container support for containerized environments
- Multiple distribution support (Ubuntu, RHEL, SUSE, etc.)

## [PLANNED] Testing Framework - Implementation Roadmap

**Overall Testing Strategy**: Comprehensive test coverage across all components when implemented

### Unit Testing Framework [PLANNED]

**Timeline**: Implemented alongside each development phase  
**Status**: [TO BE DEVELOPED] Testing architecture designed

```bash
# Run unit tests with coverage requirements
npm run test:unit

# Expected coverage:
# - Overall: ≥80%
# - Critical paths: ≥90%
# - Security functions: 100%
```

### Integration Testing

```bash
# Test component integration
npm run test:integration

# Tests include:
# - LLM adapter integration
# - Storage encryption
# - Plugin sandboxing
# - Git integration
```

### Compliance Testing

```bash
# Test compliance features (US-019, US-020, US-021)
npm run test:compliance

# Tests include:
# - SBOM generation (<30s)
# - PII detection accuracy (≥95%)
# - DSR workflow completion
# - GDPR/CCPA compliance
```

### Performance Testing

```bash
# Verify performance requirements
npm run test:performance

# Validates:
# - VS Code response time (<500ms)
# - Document analysis (<10s)
# - Suite analysis (<2min for 20 docs)
# - Quality Gate (exactly 85%)
```

### Security Testing

```bash
# Run security tests
npm run test:security

# Tests include:
# - Plugin signature verification
# - Certificate chain validation
# - Encryption/decryption
# - Sandbox isolation
```

## Verification

### VS Code Extension Verification

1. **Launch Development Host**:

   ```bash
   # Open VS Code in project directory
   code .
   
   # Press F5 to launch Extension Development Host
   ```

2. **Test Core Features**:

   ```bash
   # In Extension Host, open Command Palette (Ctrl+Shift+P)
   
   # Test document generation
   DevDocAI: Generate Document
   
   # Test quality analysis
   DevDocAI: Analyze Document
   
   # Test tracking matrix
   DevDocAI: Show Tracking Matrix
   ```

3. **Verify Memory Mode**:

   ```bash
   # Check memory usage in status bar
   DevDocAI: Show System Info
   ```

### CLI Verification

```bash
# Verify installation (using local CLI)
npx devdocai --version
# Expected: DevDocAI v3.5.0

# Test document generation
npx devdocai generate prd --template standard

# Test batch operations (US-019)
npx devdocai batch analyze docs/*.md --memory-mode=standard

# Test SBOM generation (US-019)
npx devdocai sbom generate --format=spdx --sign

# Test PII detection (US-020)
npx devdocai pii scan document.md --sensitivity=high

# Test quality gate
npx devdocai analyze readme.md --quality-gate=85
```

### Dashboard Verification

```bash
# Start dashboard server
npm run dashboard:start

# Open browser to http://localhost:3000
# Verify:
# - Health score display
# - Progressive disclosure
# - Responsive design (mobile/tablet/desktop)
# - Accessibility (WCAG 2.1 AA)
```

## Development Mode

### Hot Reload Development

```bash
# Start development watchers
npm run dev

# In separate terminals:
npm run watch:extension  # VS Code extension
npm run watch:cli       # CLI tool
npm run watch:dashboard # Web dashboard
```

### Memory Mode Testing

```bash
# Test different memory modes
npm run dev:baseline    # <2GB RAM
npm run dev:standard    # 2-4GB RAM
npm run dev:enhanced    # 4-8GB RAM
npm run dev:performance # >8GB RAM
```

### Using Development Tools

All development tools are available through npm scripts or npx:

```bash
# Package VS Code extension (using local vsce)
npm run package:extension
# Or directly: npx vsce package

# Generate new VS Code extension component
npm run generate:component
# Or directly: npx yo code

# Compile TypeScript
npm run compile
# Or directly: npx tsc

# Link CLI for local development
npm run link:cli
# This creates a local link to npx devdocai
```

## Troubleshooting

### Common Issues

1. **Development Tool Version Conflicts**:

   ```bash
   # Ensure using local project versions
   which vsce  # Should NOT show a global path
   
   # If global tools interfere, use npx explicitly
   npx vsce --version
   npx yo --version
   
   # Reset local dependencies if needed
   rm -rf node_modules package-lock.json
   npm install
   ```

2. **Memory Mode Issues**:

   ```bash
   # Check current memory mode
   npx devdocai config get memory_mode
   
   # Adjust if needed
   npx devdocai config set memory_mode standard
   ```

3. **Build Failures**:

   ```bash
   # Clean and rebuild
   npm run clean
   npm cache clean --force
   rm -rf node_modules package-lock.json
   npm install
   npm run build
   ```

4. **Quality Gate Failures**:

   ```bash
   # Check quality score
   npx devdocai analyze --verbose
   
   # Enhance to meet 85% threshold
   npx devdocai enhance --target-quality=85
   ```

5. **API Rate Limits**:

   ```bash
   # Check cost usage
   npx devdocai cost report
   
   # Switch to local models
   npx devdocai config set use_local true
   ```

6. **Plugin Security Errors**:

   ```bash
   # Verify plugin signatures
   npx devdocai plugin verify --all
   
   # Update revoked plugins
   npx devdocai plugin update --security
   ```

7. **PII Detection Issues**:

   ```bash
   # Update PII patterns
   npm run update:pii-patterns
   
   # Test detection accuracy
   npm run test:pii-accuracy
   ```

## Build Artifacts

A successful build produces:

```
dist/
├── devdocai-extension-3.5.0.vsix     # VS Code extension
├── devdocai-cli-{platform}-3.5.0     # CLI executables
├── plugins/                           # Core plugins
│   ├── security-analyzer.js
│   ├── pii-detector.js
│   └── sbom-generator.js
├── templates/                         # Document templates
│   ├── prd/
│   ├── srs/
│   └── user-stories/
├── models/                           # Local AI models (Enhanced mode)
│   ├── miair-v3.5.gguf
│   └── quality-scorer.onnx
└── certificates/                     # Security certificates
    ├── devdocai-ca.crt
    └── plugin-signing.crt
```

## Quality Validation

Ensure build meets quality standards:

```bash
# Run full validation suite
npm run validate

# Checks:
# ✓ Code coverage ≥80% overall, ≥90% critical
# ✓ Quality Gate = 85%
# ✓ Performance targets met
# ✓ Security tests passed
# ✓ Accessibility WCAG 2.1 AA
# ✓ All user stories implemented
# ✓ Documentation complete
```

## Release Preparation

```bash
# Prepare release package
npm run release:prepare

# Generate SBOM for release
npm run release:sbom

# Sign release artifacts
npm run release:sign

# Create release notes
npm run release:notes

# Verify all tools are at correct versions
npm run verify:tool-versions
```

## Continuous Integration

For CI/CD environments, all tools are automatically available:

```yaml
# .github/workflows/build.yml example
name: Build DevDocAI
on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '20'
          cache: 'npm'
      
      - name: Install Dependencies
        run: npm ci  # Uses package-lock.json for exact versions
      
      - name: Build
        run: npm run build:prod
      
      - name: Test
        run: npm test
      
      - name: Package Extension
        run: npm run package:extension  # Uses local vsce
```

## Support

For build issues or questions:

- **Documentation**: <https://docs.devdocai.org>
- **Issues**: <https://github.com/devdocai/devdocai-v3.5/issues>
- **Community**: <https://community.devdocai.org>
- **Email**: <build-support@devdocai.org>

---

**Document Status**: FINAL - v3.5.0 Suite Aligned (Future Development Planning)  
**Alignment**: Complete consistency with Architecture v3.5.0, SRS v3.6.0, PRD v3.6.0, and User Stories v3.5.0  
**Last Updated**: August 23, 2025  
**Next Review**: September 23, 2025

**Revision Notes**:

- v3.5.0-UPDATED: Transformed build instructions from active development to future development planning format
- Added [PLANNED], [TO BE DEVELOPED], and [DESIGN PHASE] status indicators throughout document
- Converted active commands to commented design specifications
- Added development timeline estimates (8-12 months total implementation)
- Clarified that no working software currently exists, only comprehensive design documentation
- All tool installations and commands are now clearly marked as future implementation specifications
</refined_build_instructions>
