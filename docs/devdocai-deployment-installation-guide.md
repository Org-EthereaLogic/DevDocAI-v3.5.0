<updated_instructions>

# DevDocAI v3.5.0 Deployment/Installation Guide

## Summary of Major Changes

This guide has been completely updated from v3.0.0 to v3.5.0 to align with the current documentation suite. Major changes include:

- **Standardized Memory Modes**: Replaced fixed RAM requirements with adaptive memory modes (Baseline/Standard/Enhanced/Performance)
- **Updated Configuration**: Migrated from JSON to YAML format with comprehensive cost management and compliance settings
- **New Compliance Features**: Added installation and verification steps for SBOM generation, PII detection, and DSR support
- **Enhanced Security**: Included plugin signature verification using Ed25519 and certificate chain validation
- **Cost Management**: Added configuration for API usage limits and budget controls
- **Expanded CLI Commands**: Documented new commands for batch operations, compliance features, and cost tracking
- **Improved Verification**: Added specific tests for v3.5.0 features including compliance and security components
- **Rollback Procedures**: Added comprehensive upgrade, rollback, and uninstallation instructions

---

## Introduction

DevDocAI v3.5.0 is an open-source documentation enhancement and generation system designed for solo developers, independent software engineers, technical writers, indie game developers, and open source maintainers. Built on the MIAIR (Meta-Iterative AI Refinement) methodology, it provides intelligent document analysis, generation, multi-LLM synthesis with cost management, compliance features (SBOM, PII detection, DSR support), and suite-level consistency checking through both a VS Code extension and a powerful CLI.

This guide covers the complete installation and deployment process for DevDocAI v3.5.0, including all new compliance and security features.

## Prerequisites

### System Requirements by Memory Mode

DevDocAI v3.5.0 adapts to your available hardware with four standardized memory modes:

| Memory Mode | RAM Required | Features Available | Use Case |
|-------------|--------------|-------------------|----------|
| **Baseline** | <2GB | Templates only, no AI | Legacy hardware, basic operations |
| **Standard** | 2-4GB | Full features, cloud AI | Typical development laptop |
| **Enhanced** | 4-8GB | Local AI models, heavy caching | Privacy-focused, power users |
| **Performance** | >8GB | All features, maximum optimization | Large projects, workstations |

### Required Software

#### Core Requirements

1. **Node.js**: Version requirements by memory mode
   - Baseline Mode: 14.x minimum
   - Standard Mode: 16.x minimum
   - Enhanced Mode: 18.x recommended
   - Performance Mode: 20.x recommended
   - Download from: <https://nodejs.org/>
   - Verify installation: `node --version`

2. **npm or yarn**: Package manager (npm comes with Node.js)
   - Verify npm: `npm --version`
   - Or install yarn: `npm install -g yarn`

3. **Git**: Version 2.25.0 or higher
   - Download from: <https://git-scm.com/>
   - Verify installation: `git --version`

4. **VS Code** (for extension): Version 1.70.0 or higher
   - Download from: <https://code.visualstudio.com/>
   - Verify installation: `code --version`

#### Memory Mode Specific Requirements

- **Standard Mode and above**: Python 3.8+ for advanced features
- **Enhanced Mode**: 2-5GB free disk space for local AI models
- **Performance Mode**: SSD storage recommended for optimal caching

### Operating System Support

- **Windows**: Windows 10+ (all memory modes)
- **macOS**: macOS 10.15+ (Standard mode and above)
- **Linux**: Ubuntu 20.04+, Debian 10+, RHEL 8+ (all memory modes)

### Optional Prerequisites

- **Docker**: For containerized deployment
- **Python 3.10+**: For plugin development and local AI models
- **CUDA**: For GPU acceleration in Performance mode

## Installation Steps

### Method 1: VS Code Extension Installation

#### Step 1: Install from VS Code Marketplace

1. Open VS Code (version 1.70.0 or higher)
2. Navigate to Extensions (Ctrl+Shift+X / Cmd+Shift+X)
3. Search for "DevDocAI"
4. Click "Install" on the DevDocAI v3.5.0 extension
5. Reload VS Code when prompted

#### Step 2: Verify Extension Installation

1. Open Command Palette (Ctrl+Shift+P / Cmd+Shift+P)
2. Type "DevDocAI" - you should see v3.5.0 commands including:
   - `DevDocAI: Generate Document`
   - `DevDocAI: Analyze Quality`
   - `DevDocAI: Generate SBOM`
   - `DevDocAI: Scan for PII`
3. Check the DevDocAI icon in the Activity Bar
4. Verify version: `DevDocAI: Show Version` should display v3.5.0

### Method 2: CLI Installation

#### Step 1: Install via npm

```bash
# Global installation (recommended)
npm install -g devdocai@3.5.0

# Or using yarn
yarn global add devdocai@3.5.0

# For specific memory mode optimization
npm install -g devdocai@3.5.0 --memory-mode=standard
```

#### Step 2: Verify CLI Installation

```bash
# Check version (should show 3.5.0)
devdocai --version

# View available commands including new v3.5.0 features
devdocai --help

# Check memory mode detection
devdocai doctor --check-memory
```

### Method 3: Development Installation (From Source)

#### Step 1: Clone the Repository

```bash
git clone https://github.com/devdocai/devdocai.git
cd devdocai
git checkout v3.5.0
```

#### Step 2: Install Dependencies

```bash
# Install all dependencies
npm install

# Or using yarn
yarn install

# Install compliance components
npm run install:compliance
```

#### Step 3: Build the Project

```bash
# Build all components including new v3.5.0 features
npm run build

# Build specific components
npm run build:cli          # CLI only
npm run build:vscode       # VS Code extension only
npm run build:compliance   # SBOM, PII, DSR components
```

#### Step 4: Link for Development

```bash
# Link CLI globally
npm link

# For VS Code extension development
cd packages/vscode-extension
npm run package
# Install the generated .vsix file in VS Code
code --install-extension devdocai-3.5.0.vsix
```

## Configuration

### Initial Setup Wizard

On first run, DevDocAI v3.5.0 launches an enhanced setup wizard:

```bash
# Run setup wizard with memory mode detection
devdocai setup

# Or specify memory mode
devdocai setup --memory-mode=standard

# In VS Code
# Command Palette > DevDocAI: Initial Setup v3.5.0
```

### Configuration File Structure

#### Create Configuration File

Create `.devdocai.yml` in your home directory or project root:

```yaml
# DevDocAI v3.5.0 Configuration
version: 3.5.0

# Memory mode configuration
system:
  memory_mode: standard  # baseline, standard, enhanced, performance
  
# Quality settings with exact threshold
quality:
  quality_gate: 85  # Exactly 85% threshold for pass/fail
  quality_target: 90  # Target for enhancement
  auto_enhance: true
  review_on_save: true
  enforce_gate_in_ci: true

# Cost management (REQ-044)
cost_management:
  enabled: true
  budgets:
    daily_limit: 10.00  # USD
    monthly_limit: 200.00  # USD
    per_project_limit: 50.00  # USD
    warning_threshold: 80  # Percentage
  
  optimization:
    prefer_economical: true
    provider_selection: "cost_quality_ratio"
    cache_responses: true
    batch_requests: true
    max_batch_size: 10
    
  providers:
    claude:
      enabled: true
      api_key: "${CLAUDE_API_KEY}"
      model: "claude-opus-4-1-20250805"
      weight: 0.4
      cost_per_1k_tokens: 0.015
      quality_score: 0.95
    chatgpt:
      enabled: true
      api_key: "${OPENAI_API_KEY}"
      model: "gpt-4"
      weight: 0.35
      cost_per_1k_tokens: 0.020
      quality_score: 0.90
    gemini:
      enabled: true
      api_key: "${GEMINI_API_KEY}"
      model: "gemini-pro"
      weight: 0.25
      cost_per_1k_tokens: 0.010
      quality_score: 0.85
      
  fallback:
    use_local_models: true
    local_model_path: "./models/"
    reduce_quality_gracefully: true

# Privacy settings
privacy:
  offline_mode: false
  telemetry: false  # Opt-in only
  local_encryption: true  # AES-256-GCM
  data_retention:
    logs: 90  # Days
    analytics: 30
    temp_files: 1
  dsr:
    enabled: true  # GDPR/CCPA support
    export_format: json
    automatic_response: true

# Compliance features (US-019, US-020, US-021)
compliance:
  sbom:
    enabled: true
    format: spdx  # spdx or cyclonedx
    auto_generate_on_build: true
    include_vulnerabilities: true
    sign_with_ed25519: true
  
  pii_detection:
    enabled: true
    sensitivity: medium  # low, medium, high
    accuracy_target: 0.95
    scan_on_save: true
    compliance_mode: both  # gdpr, ccpa, or both
    
  dsr:
    enabled: true
    response_time: 24  # Hours for automated requests
    encryption_required: true
    audit_logging: true

# Plugin settings with security
plugins:
  security:
    verify_signatures: true  # Ed25519 verification
    check_revocation: true   # CRL and OCSP
    scan_for_malware: true
    sandbox_execution: true
  trusted_sources:
    - "@devdocai/*"
    - "github:devdocai/*"

# Paths configuration
paths:
  templates: "~/.devdocai/templates"
  plugins: "~/.devdocai/plugins"
  cache: "~/.devdocai/cache"
  models: "~/.devdocai/models"  # For local AI models

# Git integration
git:
  hooks:
    pre_commit: true
    pre_push: false
  auto_commit_docs: false
  branch_protection: true

# Batch operations (US-019)
batch_operations:
  enabled: true
  max_concurrent: 4  # Adjust based on memory mode
  queue_size: 100
  progress_reporting: true

# Learning system (US-015)
learning:
  enabled: true
  pattern_threshold: 5  # Corrections before learning
  project_isolation: true
  export_style_guide: true
```

### Environment Variables

Create a `.env` file in your project root:

```bash
# LLM API Keys (optional - for cloud features)
export CLAUDE_API_KEY="your-claude-api-key"
export OPENAI_API_KEY="your-openai-api-key"
export GEMINI_API_KEY="your-gemini-api-key"

# DevDocAI Settings
export DEVDOCAI_HOME="~/.devdocai"
export DEVDOCAI_VERSION="3.5.0"
export DEVDOCAI_MEMORY_MODE="standard"
export DEVDOCAI_OFFLINE=false
export DEVDOCAI_LOG_LEVEL="info"

# Security Settings
export DEVDOCAI_ENCRYPTION_KEY="auto-generated-on-setup"
export DEVDOCAI_PLUGIN_CA_CERT="~/.devdocai/certs/ca.pem"

# Cost Management
export DEVDOCAI_DAILY_BUDGET="10.00"
export DEVDOCAI_MONTHLY_BUDGET="200.00"
```

### VS Code Workspace Settings

Add to `.vscode/settings.json`:

```json
{
  "devdocai.version": "3.5.0",
  "devdocai.memoryMode": "standard",
  "devdocai.enableRealTimeAnalysis": true,
  "devdocai.showInlineHints": true,
  "devdocai.autoGenerateOnSave": false,
  "devdocai.trackingMatrix.enabled": true,
  "devdocai.defaultDocumentPath": "./docs",
  "devdocai.qualityGate": 85,
  "devdocai.llm.provider": "claude",
  "devdocai.compliance.sbomAutoGenerate": true,
  "devdocai.compliance.piiScanOnSave": true,
  "devdocai.costManagement.showWarnings": true,
  "devdocai.costManagement.dailyLimit": 10.00
}
```

## Plugin Installation with Security

### Installing Plugins with Signature Verification

```bash
# Install official plugins (automatically verified)
devdocai plugin install @devdocai/game-dev --verify
devdocai plugin install @devdocai/api-docs --verify
devdocai plugin install @devdocai/security-scanner --verify

# List installed plugins with security status
devdocai plugin list --show-signatures

# Install from GitHub with signature check
devdocai plugin install github:username/plugin-name --verify-signature

# Check plugin security before installation
devdocai plugin verify github:username/plugin-name

# View plugin permissions
devdocai plugin inspect @devdocai/game-dev --permissions
```

### Handling Plugin Security Warnings

If a plugin fails signature verification:

```bash
# Check revocation status
devdocai plugin check-revocation <plugin-name>

# View certificate details
devdocai plugin cert-info <plugin-name>

# Install with explicit risk acceptance (not recommended)
devdocai plugin install <plugin-name> --accept-unsigned
```

## Compliance and Security Setup

### SBOM Generation Setup

```bash
# Initialize SBOM configuration
devdocai sbom init

# Generate SBOM for your project
devdocai sbom generate --format=spdx --sign

# Verify SBOM generation
devdocai sbom verify --check-signatures

# Schedule automatic SBOM updates
devdocai sbom schedule --on-build --on-deploy
```

### PII Detection Configuration

```bash
# Configure PII detection patterns
devdocai pii configure --sensitivity=medium

# Test PII detection
devdocai pii test --sample-data

# Scan existing documentation
devdocai pii scan ./docs --recursive

# View PII detection patterns
devdocai pii patterns --list
```

### DSR (Data Subject Rights) Setup

```bash
# Enable DSR support
devdocai dsr enable

# Configure DSR workflows
devdocai dsr configure --gdpr --ccpa

# Test DSR export
devdocai dsr test-export --format=json

# Verify DSR deletion
devdocai dsr test-delete --dry-run
```

## Verification

### Step 1: Run Comprehensive System Check

```bash
# Full system check for v3.5.0
devdocai doctor --full

# Expected output:
# ✓ DevDocAI Version: 3.5.0
# ✓ Memory Mode: Standard (2-4GB detected)
# ✓ Node.js version: 16.20.0 (meets Standard mode requirement)
# ✓ Configuration file: .devdocai.yml found and valid
# ✓ Template directory exists: 40+ templates available
# ✓ Plugin system: Initialized with Ed25519 verification
# ✓ Compliance features:
#   ✓ SBOM Generator: Ready (SPDX 2.3, CycloneDX 1.4)
#   ✓ PII Detection: Configured (95% accuracy target)
#   ✓ DSR Handler: Enabled (GDPR/CCPA compliant)
# ✓ Cost Management: Active (Daily: $10.00, Monthly: $200.00)
# ⚠ LLM APIs: 2/3 configured (offline mode available)
# ✓ Git integration: Ready with hooks
# ✓ Security: Encryption enabled (AES-256-GCM)
# ✓ Quality Gate: Set to exactly 85%
# ✓ All systems operational for v3.5.0
```

### Step 2: Test Core Document Generation

```bash
# Generate a test document with quality check
devdocai generate readme --test --check-quality

# Verify generation and quality gate
cat README.md
devdocai analyze README.md --quality-gate=85
```

### Step 3: Test VS Code Integration

1. Open a project in VS Code
2. Open Command Palette (Ctrl+Shift+P)
3. Run: `DevDocAI: Generate Document`
4. Select "README" from templates
5. Verify quality score appears in status bar
6. Check tracking matrix visualization

### Step 4: Verify New v3.5.0 Features

```bash
# Test SBOM generation
devdocai sbom generate --format=spdx --output=sbom.json
cat sbom.json | head -20

# Test PII detection
echo "John Doe's SSN is 123-45-6789" > test.txt
devdocai pii scan test.txt
# Should detect and flag PII with 95%+ accuracy

# Test DSR export
devdocai dsr export --user-id=test --format=json

# Test cost tracking
devdocai cost report --today
devdocai cost estimate "generate prd"

# Test batch operations
devdocai batch analyze ./docs/*.md --memory-mode=standard
```

### Step 5: Verify Offline Mode

```bash
# Enable offline mode
devdocai config set privacy.offline_mode true

# Test offline capabilities
devdocai analyze ./docs/sample.md --offline
devdocai generate test-plan --offline --use-local-models

# Should complete without network requests
```

### Step 6: Run Test Suite

```bash
# Run complete v3.5.0 test suite
devdocai test --version=3.5.0

# Run specific test categories
devdocai test --suite generation
devdocai test --suite analysis
devdocai test --suite compliance  # New in v3.5.0
devdocai test --suite security    # Enhanced in v3.5.0
devdocai test --suite cost        # New in v3.5.0
```

## Troubleshooting

### Common Issues and Solutions

#### Issue: Command 'devdocai' not found after installation

**Solution:**

```bash
# Check npm global path
npm config get prefix

# Add to PATH (Linux/Mac)
export PATH=$PATH:$(npm config get prefix)/bin
echo 'export PATH=$PATH:$(npm config get prefix)/bin' >> ~/.bashrc

# Windows: Add npm prefix\bin to System PATH via Environment Variables
```

#### Issue: Memory mode incorrectly detected

**Solution:**

```bash
# Manually set memory mode
devdocai config set system.memory_mode standard

# Verify detection
devdocai doctor --check-memory --verbose

# Override in environment
export DEVDOCAI_MEMORY_MODE=enhanced
```

#### Issue: VS Code extension not loading or showing old version

**Solution:**

1. Check VS Code version (requires 1.70.0+)
2. Uninstall old version completely:
   - Extensions → DevDocAI → Uninstall
   - Delete `~/.vscode/extensions/devdocai*`
3. Reload window: Ctrl+Shift+P → "Developer: Reload Window"
4. Reinstall v3.5.0 from marketplace
5. Check logs: View → Output → Select "DevDocAI"

#### Issue: LLM API connection failures or cost limit exceeded

**Solution:**

```bash
# Verify API keys and limits
devdocai config validate --check-apis

# Check cost status
devdocai cost status
devdocai cost reset --daily  # Reset daily limit

# Test individual providers
devdocai test provider claude --verbose
devdocai test provider openai --verbose

# Enable fallback to local models
devdocai config set cost_management.fallback.use_local_models true

# Adjust budget limits
devdocai config set cost_management.budgets.daily_limit 20.00
```

#### Issue: SBOM generation fails

**Solution:**

```bash
# Check dependencies are detected
devdocai sbom scan --verbose

# Verify format support
devdocai sbom formats --list

# Test without signing
devdocai sbom generate --format=spdx --no-sign

# Clear cache and retry
rm -rf ~/.devdocai/cache/sbom
devdocai sbom generate --fresh
```

#### Issue: PII detection not reaching 95% accuracy

**Solution:**

```bash
# Adjust sensitivity level
devdocai pii configure --sensitivity=high

# Update pattern database
devdocai pii update-patterns

# Test with known dataset
devdocai pii test --benchmark

# View detection logs
devdocai pii logs --verbose
```

#### Issue: Plugin signature verification fails

**Solution:**

```bash
# Update certificate store
devdocai plugin update-certs

# Check certificate chain
devdocai plugin verify-chain <plugin-name>

# Clear revocation cache
devdocai plugin clear-crl-cache

# Install from trusted source only
devdocai plugin install @devdocai/<plugin-name>
```

#### Issue: Git hooks not triggering with quality gate

**Solution:**

```bash
# Reinstall hooks with v3.5.0 quality gate
devdocai hooks uninstall
devdocai hooks install --quality-gate=85

# Verify hook configuration
cat .git/hooks/pre-commit | grep "quality-gate"

# Test hook manually
devdocai check --staged --quality-gate=85 --fail-on-error
```

### Debug Mode

Enable comprehensive debugging:

```bash
# Set debug logging
export DEVDOCAI_LOG_LEVEL=debug

# Run with full debug output
devdocai --debug --verbose <command>

# Enable compliance debugging
export DEVDOCAI_DEBUG_COMPLIANCE=true

# View detailed logs
tail -f ~/.devdocai/logs/devdocai.log
tail -f ~/.devdocai/logs/compliance.log
tail -f ~/.devdocai/logs/cost.log
```

### Getting Help

- **Documentation**: <https://docs.devdocai.org/v3.5.0>
- **GitHub Issues**: <https://github.com/devdocai/devdocai/issues>
- **Community Discord**: <https://discord.gg/devdocai>
- **Security Issues**: <security@devdocai.org>
- **Commercial Support**: <support@devdocai.org>

## Upgrade and Rollback Procedures

### Upgrading from Previous Versions

```bash
# Backup current installation
devdocai backup create --include-config --include-data

# Check upgrade compatibility
devdocai upgrade check --from=3.0.0 --to=3.5.0

# Perform upgrade
npm update -g devdocai@3.5.0

# Migrate configuration
devdocai migrate config --from=3.0.0 --to=3.5.0

# Verify upgrade
devdocai doctor --post-upgrade
```

### Rolling Back to Previous Version

```bash
# List available backups
devdocai backup list

# Rollback to specific version
npm install -g devdocai@3.0.0

# Restore configuration
devdocai backup restore --version=3.0.0

# Verify rollback
devdocai --version
```

## Uninstallation

### Complete Uninstallation

```bash
# Uninstall CLI
npm uninstall -g devdocai

# Remove VS Code extension
code --uninstall-extension devdocai.devdocai

# Backup user data (optional)
cp -r ~/.devdocai ~/.devdocai.backup

# Remove all DevDocAI data
rm -rf ~/.devdocai
rm -rf ~/.config/devdocai
rm -rf ~/.cache/devdocai

# Remove environment variables
unset DEVDOCAI_HOME
unset DEVDOCAI_API_KEY
# Remove from .bashrc/.zshrc as needed

# Remove git hooks
devdocai hooks uninstall  # Run before uninstalling CLI
```

## Next Steps

1. **Configure memory mode**: `devdocai config set system.memory_mode <mode>`
2. **Set up cost limits**: `devdocai cost configure --interactive`
3. **Generate your first document**: `devdocai generate prd --analyze`
4. **Analyze existing documentation**: `devdocai analyze ./docs --recursive`
5. **Set up tracking matrix**: `devdocai track init --visualize`
6. **Configure compliance**: `devdocai compliance setup --gdpr --ccpa`
7. **Install domain plugins**: `devdocai plugin search --category=<domain>`
8. **Generate SBOM**: `devdocai sbom generate --sign`
9. **Scan for PII**: `devdocai pii scan ./docs --fix`
10. **Set up CI/CD integration**: `devdocai ci setup --github-actions`

## Security Notes

### Data Protection

- All API keys encrypted with AES-256-GCM
- Local storage uses Argon2id key derivation
- Sensitive data never transmitted without explicit consent
- Offline mode ensures complete data privacy

### Plugin Security

- All plugins verified with Ed25519 signatures
- Certificate chain validation to DevDocAI Plugin CA
- Automatic revocation checking via CRL and OCSP
- Sandboxed execution environment

### Compliance

- GDPR Article 15-22 compliant for DSR
- CCPA Title 1.81.5 compliant
- SBOM generation meets regulatory requirements
- PII detection achieves 95%+ accuracy target

### Audit and Monitoring

- All operations logged with tamper-evident records
- Security events tracked separately
- Cost tracking with budget enforcement
- Quality gate enforcement at exactly 85%

---

**Version**: 3.5.0  
**Last Updated**: August 21, 2025  
**License**: Apache-2.0 (Core), MIT (Plugin SDK)  
**Status**: FINAL - Suite Aligned v3.5.0
</updated_instructions>
