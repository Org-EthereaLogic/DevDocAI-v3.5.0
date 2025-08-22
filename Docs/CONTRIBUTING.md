# Contributing to DevDocAI v3.5.0

Welcome to DevDocAI! We're thrilled that you're interested in contributing to our open-source documentation enhancement and generation system. DevDocAI empowers solo developers, independent contractors, and small teams to create professional-grade technical documentation with AI-powered analysis, multi-LLM synthesis, and enterprise-level compliance features.

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [📜 Licensing](#-licensing)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Process](#development-process)
- [Coding Standards](#coding-standards)
- [Testing Requirements](#testing-requirements)
- [Documentation Guidelines](#documentation-guidelines)
- [Quality Standards](#quality-standards)
- [Reporting Issues](#reporting-issues)
- [Feature Requests](#feature-requests)
- [Plugin Development](#plugin-development)
- [Community & Communication](#community--communication)
- [Code of Conduct](#code-of-conduct)
- [Recognition](#recognition)

## Project Overview

DevDocAI v3.5.0 is built on the MIAIR (Meta-Iterative AI Refinement) methodology and provides comprehensive documentation capabilities:

### Core Features

- **Document Generation**: Create 40+ document types from intelligent templates
- **Multi-Dimensional Analysis**: Comprehensive quality reviews across requirements, design, security, and performance
- **Suite Management**: Maintain consistency across entire documentation suites with visual tracking matrix
- **AI Enhancement**: Multi-LLM synthesis using Claude, ChatGPT, and Gemini with cost optimization
- **Workflow Integration**: Seamless VS Code extension and powerful CLI automation

### Compliance & Security Features (v3.5.0)

- **SBOM Generation** (M010): Generate Software Bill of Materials in SPDX 2.3 and CycloneDX 1.4 formats
- **PII Detection**: Automatic detection of personally identifiable information with 95%+ accuracy
- **DSR Support**: Data Subject Rights implementation for GDPR/CCPA compliance
- **Privacy-First**: Complete offline capability with optional cloud features
- **Code Signing**: Ed25519 digital signatures for plugin verification

### Architecture Components

The project is organized into modular components (M001-M013) across four implementation phases. See our [Architecture Blueprint](docs/architecture.md) for detailed component descriptions.

## 📜 Licensing

DevDocAI uses a dual-license model to balance openness with flexibility:

- **Core System**: Licensed under **Apache License 2.0**
- **Plugin SDK**: Licensed under **MIT License**

### Contributor License Agreement

By submitting a pull request to this repository, you agree that:

1. Your contributions to the core DevDocAI repository are submitted under the **Apache License 2.0**
2. Your contributions to the Plugin SDK are submitted under the **MIT License**
3. You have the right to submit the work under these licenses
4. You understand that your contributions are public and may be redistributed

No formal CLA signature is required, but all contributions must comply with these licensing terms.

## Getting Started

### Prerequisites

DevDocAI adapts to your available hardware with four memory modes:

| Memory Mode | RAM Required | Node.js Version | Python Version | Features |
|-------------|--------------|-----------------|----------------|----------|
| **Baseline** | <2GB | 14.x+ | Not required | Templates only |
| **Standard** | 2-4GB | 16.x+ | 3.8+ | Full features |
| **Enhanced** | 4-8GB | 18.x+ | 3.10+ | Local AI models |
| **Performance** | >8GB | 20.x+ | 3.11+ | Maximum optimization |

Additional requirements:

- Git 2.25+
- VS Code 1.70.0+ (for extension development)
- Docker (optional, for containerized testing)

### Development Setup

```bash
# Clone the repository
git clone https://github.com/devdocai/devdocai.git
cd devdocai

# Install dependencies based on your memory mode
npm install

# Run setup script which detects your system capabilities
npm run setup:dev

# Verify installation and run initial tests
npm test

# For VS Code extension development
cd packages/vscode-extension
npm install
code .

# For CLI development
cd packages/cli
pip install -r requirements-dev.txt

# For compliance features development
cd packages/compliance
npm install
```

### Environment Configuration

Create a `.env.local` file in the root directory:

```env
# Memory mode configuration (auto-detected if not set)
MEMORY_MODE=standard  # baseline | standard | enhanced | performance

# Optional: LLM API keys for cloud features
CLAUDE_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here

# Cost management settings
DAILY_COST_LIMIT=10.00
MONTHLY_COST_LIMIT=200.00

# Development settings
DEBUG_MODE=true
LOG_LEVEL=verbose
QUALITY_GATE_THRESHOLD=85  # Exactly 85% required

# Compliance features
ENABLE_PII_DETECTION=true
ENABLE_SBOM_GENERATION=true
ENABLE_DSR_SUPPORT=true
```

## How to Contribute

We welcome contributions of all types! Here's how you can help:

### Areas for Contribution

#### Core Features (Phase 1-2)

- **Document Generators** (M004): Add new document types or improve templates
- **Analysis Engine** (M007): Enhance review algorithms and quality metrics
- **Tracking Matrix** (M005): Improve visualization and relationship management
- **Suite Manager** (M006): Enhance cross-document consistency checks

#### Enhancement Features (Phase 2)

- **MIAIR Engine** (M003): Optimize entropy reduction algorithms
- **LLM Adapter** (M008): Add new AI models or improve synthesis
- **Cost Management**: Optimize API usage and cost tracking
- **Batch Operations** (M011): Improve parallel processing efficiency

#### Compliance Features (Phase 3)

- **SBOM Generator** (M010): Enhance dependency scanning and vulnerability detection
- **PII Detection**: Improve pattern recognition and accuracy
- **DSR Handler**: Streamline data subject request workflows
- **Security Analysis**: Add new security review patterns

#### Developer Tools

- **VS Code Extension**: Enhance IDE integration and real-time assistance
- **CLI Tools**: Add new commands and improve automation capabilities
- **Dashboard**: Improve metrics visualization and reporting

#### Community Contributions

- **Plugins**: Create domain-specific extensions
- **Templates**: Contribute industry-specific document templates
- **Documentation**: Improve guides, tutorials, and API documentation
- **Testing**: Increase test coverage and add edge cases
- **Accessibility**: Ensure WCAG 2.1 Level AA compliance

## Development Process

### 1. Fork and Clone

```bash
# Fork the repository on GitHub first, then:
git clone https://github.com/YOUR_USERNAME/devdocai.git
cd devdocai
git remote add upstream https://github.com/devdocai/devdocai.git
```

### 2. Create a Feature Branch

```bash
# Sync with upstream
git checkout main
git pull upstream main

# Create a feature branch following our naming convention
git checkout -b feature/component-name/description
# Examples:
# git checkout -b feature/m004-generator/add-swagger-template
# git checkout -b fix/m007-analyzer/pii-false-positives
# git checkout -b docs/m010-sbom/update-api-reference
```

### 3. Make Your Changes

- Write clean, documented code following our standards
- Ensure changes align with the relevant architectural component
- Add comprehensive tests for new functionality
- Update documentation to reflect your changes
- Verify compliance with quality gates

### 4. Commit Your Changes

We use [Conventional Commits](https://www.conventionalcommits.org/) for clear history:

```bash
# Stage your changes
git add .

# Commit with a descriptive message
git commit -m "feat(m004): add OpenAPI 3.0 document generator"

# Commit types:
# feat: New feature
# fix: Bug fix
# docs: Documentation changes
# style: Code style changes (formatting, etc.)
# refactor: Code refactoring
# perf: Performance improvements
# test: Test additions or corrections
# build: Build system changes
# ci: CI/CD changes
# chore: Maintenance tasks
```

### 5. Push and Create Pull Request

```bash
# Push to your fork
git push origin feature/component-name/description

# Create a pull request on GitHub
# Use our PR template and ensure:
# - All tests pass
# - Quality gate (85%) is met
# - Documentation is updated
# - No licensing conflicts
```

## Coding Standards

### TypeScript/JavaScript

Follow our ESLint and Prettier configurations (`.eslintrc.json` and `.prettierrc`):

```typescript
// Use clear, descriptive names and comprehensive JSDoc
export class DocumentAnalyzer implements IAnalyzer {
  private readonly config: AnalyzerConfig;
  private readonly qualityGate: number = 0.85; // Exactly 85%
  
  /**
   * Analyzes a document for quality metrics per M007 requirements
   * @param document - The document to analyze
   * @param options - Optional analysis configuration
   * @returns Analysis results with quality score and recommendations
   * @throws {ValidationError} If document format is invalid
   * @example
   * const result = await analyzer.analyze(document, { 
   *   includePII: true 
   * });
   */
  public async analyze(
    document: Document, 
    options?: AnalysisOptions
  ): Promise<AnalysisResult> {
    // Validate input
    this.validateDocument(document);
    
    // Perform analysis with error handling
    try {
      const metrics = await this.calculateMetrics(document);
      return this.formatResults(metrics, options);
    } catch (error) {
      this.logger.error('Analysis failed', { error, documentId: document.id });
      throw new AnalysisError('Document analysis failed', error);
    }
  }
}
```

### Python (CLI)

Follow PEP 8 and our project conventions (`pyproject.toml`):

```python
"""Document generator module implementing M004 architecture component."""

from typing import Dict, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class GeneratorConfig:
    """Configuration for document generation."""
    template_path: str
    quality_gate: float = 0.85  # Exactly 85% threshold
    enable_ai: bool = True
    memory_mode: str = "standard"


class DocumentGenerator:
    """
    Generates documents from templates using AI synthesis.
    
    Implements M004 component of DevDocAI architecture.
    """
    
    def __init__(self, config: GeneratorConfig) -> None:
        """
        Initialize generator with configuration.
        
        Args:
            config: Generator configuration including quality thresholds
        """
        self.config = config
        self._validate_config()
    
    def generate(
        self, 
        doc_type: str, 
        context: Dict[str, any],
        validate_quality: bool = True
    ) -> Document:
        """
        Generate a new document of specified type.
        
        Args:
            doc_type: Type of document to generate (e.g., 'prd', 'srs')
            context: Context data for document generation
            validate_quality: Whether to enforce quality gate
            
        Returns:
            Generated document meeting quality standards
            
        Raises:
            QualityGateError: If document doesn't meet 85% quality threshold
            GenerationError: If generation fails
            
        Example:
            >>> generator = DocumentGenerator(config)
            >>> doc = generator.generate('prd', {'project': 'DevDocAI'})
        """
        try:
            document = self._create_from_template(doc_type, context)
            
            if validate_quality:
                self._enforce_quality_gate(document)
                
            return document
        except Exception as e:
            logger.error(f"Generation failed for {doc_type}: {e}")
            raise GenerationError(f"Failed to generate {doc_type}") from e
```

### General Guidelines

- **DRY Principle**: Don't repeat yourself - extract common functionality
- **Single Responsibility**: Each function/class should have one clear purpose
- **Error Handling**: Always handle errors gracefully with proper logging
- **Magic Numbers**: Use named constants (e.g., `QUALITY_GATE_THRESHOLD = 0.85`)
- **Async Operations**: Use async/await for I/O operations
- **Type Safety**: Use TypeScript types and Python type hints
- **Component Alignment**: Reference architecture components (M001-M013) in code

## Testing Requirements

### Coverage Requirements (v3.5.0 Aligned)

Per SRS Section 3.2.5 (NFR-010) and Section 4.3.5:

| Test Category | Required Coverage | Verification |
|---------------|------------------|--------------|
| **Overall** | ≥80% | `npm run test:coverage` |
| **Critical Paths** | ≥90% | Includes core workflows |
| **Security Functions** | 100% | All auth, crypto, and validation |
| **New Features** | ≥80% | Before PR merge |
| **Bug Fixes** | Include regression tests | Prevent reoccurrence |
| **Compliance Features** | ≥85% | SBOM, PII, DSR functions |

### Running Tests

```bash
# Run all tests with coverage
npm test

# Run specific component tests
npm test -- --grep "M007.*Review Engine"

# Run security tests (must have 100% coverage)
npm run test:security

# Run compliance tests
npm run test:compliance

# Run integration tests
npm run test:integration

# Run performance tests
npm run test:performance

# VS Code extension tests
cd packages/vscode-extension && npm test

# CLI tests
cd packages/cli && pytest --cov=devdocai --cov-report=html

# Run quality gate validation
npm run quality:check -- --threshold=85
```

### Writing Effective Tests

```typescript
import { describe, it, expect, beforeEach, afterEach } from '@jest/globals';
import { DocumentAnalyzer } from '../src/m007-analyzer';
import { createMockDocument, cleanupTestData } from './helpers';

describe('M007 - Document Review Engine', () => {
  let analyzer: DocumentAnalyzer;
  
  beforeEach(() => {
    analyzer = new DocumentAnalyzer({
      qualityGate: 0.85, // Exactly 85% threshold
      enablePII: true
    });
  });
  
  afterEach(async () => {
    await cleanupTestData();
  });
  
  describe('Requirements Validation (US-005)', () => {
    it('should detect ambiguous requirements with high severity', async () => {
      // Arrange
      const document = createMockDocument('requirements', {
        content: 'The system should be fast and user-friendly.'
      });
      
      // Act
      const result = await analyzer.analyze(document);
      
      // Assert
      expect(result.qualityScore).toBeLessThan(0.85);
      expect(result.issues).toContainEqual(
        expect.objectContaining({
          type: 'ambiguous-requirement',
          severity: 'high',
          line: 1,
          suggestion: expect.stringContaining('measurable')
        })
      );
    });
    
    it('should achieve exactly 85% quality gate for valid documents', async () => {
      const document = createMockDocument('requirements', {
        content: getValidRequirementsContent()
      });
      
      const result = await analyzer.analyze(document);
      
      expect(result.qualityScore).toBeGreaterThanOrEqual(0.85);
      expect(result.passesQualityGate).toBe(true);
    });
  });
  
  describe('PII Detection (US-020)', () => {
    it('should detect PII with ≥95% accuracy', async () => {
      const document = createMockDocument('user-manual', {
        content: 'Contact John Doe at john.doe@example.com or 555-1234.'
      });
      
      const result = await analyzer.detectPII(document);
      
      expect(result.accuracy).toBeGreaterThanOrEqual(0.95);
      expect(result.findings).toHaveLength(3); // name, email, phone
      expect(result.findings[0].type).toBe('name');
      expect(result.findings[0].confidence).toBeGreaterThan(0.9);
    });
  });
});
```

## Documentation Guidelines

### Code Documentation Standards

All code must be thoroughly documented:

```typescript
/**
 * Component: M010 - SBOM Generator
 * Purpose: Generate Software Bill of Materials for compliance
 * 
 * @module SBOMGenerator
 * @implements {ISBOMGenerator}
 * @since v3.5.0
 */

/**
 * Generates SBOM in specified format with digital signature
 * 
 * @param {string} projectPath - Path to project root
 * @param {SBOMOptions} options - Generation options
 * @param {('spdx'|'cyclonedx')} options.format - Output format (default: 'spdx')
 * @param {boolean} options.sign - Whether to sign with Ed25519 (default: true)
 * @param {boolean} options.includeVulnerabilities - Include CVE scanning (default: true)
 * 
 * @returns {Promise<SBOM>} Generated and signed SBOM
 * 
 * @throws {ValidationError} If project structure is invalid
 * @throws {ScanError} If dependency scanning fails
 * 
 * @example
 * const sbom = await generator.generate('/path/to/project', {
 *   format: 'spdx',
 *   sign: true,
 *   includeVulnerabilities: true
 * });
 * 
 * @see {@link https://spdx.dev/specifications/} SPDX Specification
 * @see {@link https://cyclonedx.org/specification/} CycloneDX Specification
 */
```

### User Documentation Updates

When contributing features, update:

1. **API Documentation** (`/docs/api/`)
   - Add new endpoints with OpenAPI specs
   - Include request/response examples
   - Document error codes

2. **User Guides** (`/docs/guides/`)
   - Step-by-step tutorials
   - Best practices
   - Common use cases

3. **Architecture Docs** (`/docs/architecture/`)
   - Component diagrams
   - Sequence diagrams
   - Integration patterns

4. **CLI Help** (`/packages/cli/help/`)
   - Command descriptions
   - Option explanations
   - Usage examples

5. **VS Code Commands** (`/packages/vscode-extension/package.json`)
   - Command palette entries
   - Keybinding suggestions
   - Context menu items

## Quality Standards

### Quality Gate Enforcement

All contributions must meet DevDocAI's quality standards:

- **Documentation Quality**: Exactly **85%** threshold (per PRD Section 4.2)
- **Code Quality**: Passes all linting rules
- **Test Coverage**: Meets requirements per test category
- **Performance**: No regression in benchmarks
- **Accessibility**: WCAG 2.1 Level AA compliant
- **Security**: No vulnerabilities in dependencies

### Quality Validation

```bash
# Run complete quality check before submitting PR
npm run quality:validate

# This runs:
# - Linting (ESLint, Prettier)
# - Type checking (TypeScript)
# - Test coverage validation
# - Documentation quality analysis (85% gate)
# - Security audit
# - Performance benchmarks
# - Accessibility checks
```

## Reporting Issues

### Bug Report Template

Use our issue template and provide:

```markdown
### Bug Description
Clear, concise description of the issue

### Steps to Reproduce
1. Environment setup
2. Actions taken
3. Observed result

### Expected Behavior
What should happen

### Actual Behavior
What actually happens

### Environment
- **OS**: Ubuntu 22.04 / Windows 11 / macOS 13
- **Node.js**: 18.17.0
- **Python**: 3.10.0
- **DevDocAI**: v3.5.0
- **Memory Mode**: standard (4GB RAM)
- **Component**: M007 (Analysis Engine)

### Error Output
```

Error stack trace or logs

```

### Additional Context
- Screenshots if applicable
- Related issues
- Potential solutions considered
```

### Security Issues

For security vulnerabilities:

- **DO NOT** create public issues
- Email <security@devdocai.org> with details
- Use PGP encryption if possible (key ID: `0x1234567890ABCDEF`)
- Include steps to reproduce and potential impact
- Allow 90 days for fix before public disclosure

## Feature Requests

### Feature Request Template

```markdown
### Problem Statement
As a [type of user], I need [capability] so that [benefit]

### Proposed Solution
DevDocAI could implement [specific solution]

### Architecture Alignment
- **Component**: M### (component that would be modified)
- **User Story**: US-### (related user story if applicable)
- **Phase**: 1-4 (implementation phase)

### Alternative Solutions
1. Alternative approach A
2. Alternative approach B

### Success Criteria
- [ ] Measurable outcome 1
- [ ] Measurable outcome 2

### Additional Context
- Use cases
- Similar features in other tools
- Mockups or diagrams
```

## Plugin Development

### Creating a Plugin

Plugins extend DevDocAI's capabilities using the MIT-licensed SDK:

```typescript
import { Plugin, PluginManifest, DocumentType, Analyzer } from '@devdocai/plugin-sdk';
import { createHash } from 'crypto';

/**
 * Example plugin for game development documentation
 */
export class GameDevPlugin implements Plugin {
  public readonly manifest: PluginManifest = {
    name: 'gamedev-toolkit',
    version: '1.0.0',
    author: 'Your Name',
    description: 'Game development documentation tools',
    license: 'MIT',
    devdocaiVersion: '^3.5.0',
    permissions: [
      'document:read',
      'document:write',
      'analysis:custom'
    ],
    signature: '' // Will be added during publishing
  };
  
  public readonly documentTypes: DocumentType[] = [
    {
      id: 'game-design-doc',
      name: 'Game Design Document',
      template: gameDesignTemplate,
      schema: gameDesignSchema,
      examples: ['rpg-gdd.md', 'puzzle-gdd.md']
    },
    {
      id: 'level-design',
      name: 'Level Design Specification',
      template: levelDesignTemplate,
      schema: levelDesignSchema
    }
  ];
  
  public readonly analyzers: Analyzer[] = [
    new GameplayBalanceAnalyzer(),
    new NarrativeConsistencyChecker(),
    new DifficultyProgressionValidator()
  ];
  
  public async activate(context: PluginContext): Promise<void> {
    // Plugin initialization
    context.subscriptions.push(
      context.onDocumentChange(this.validateGameDesign.bind(this))
    );
  }
  
  public async deactivate(): Promise<void> {
    // Cleanup resources
  }
}
```

### Plugin Security Requirements

All plugins must:

1. **Digital Signature**: Sign with Ed25519 key
2. **Manifest Validation**: Include complete manifest
3. **Permission Declaration**: Request only needed permissions
4. **Sandbox Compliance**: Run within security sandbox
5. **Version Compatibility**: Specify DevDocAI version range
6. **License Declaration**: Clear licensing terms

### Publishing Plugins

```bash
# Build and test your plugin
npm run build
npm test

# Sign your plugin with Ed25519 key
devdocai plugin:sign --key=./private-key.pem

# Validate plugin package
devdocai plugin:validate ./dist/plugin.zip

# Publish to marketplace
devdocai plugin:publish --category=gamedev

# Plugin will undergo security review before marketplace listing
```

## Community & Communication

### Communication Channels

- **GitHub Discussions**: General questions, ideas, and announcements
- **Discord**: [discord.gg/devdocai](https://discord.gg/devdocai) - Real-time chat and support
- **Forum**: [forum.devdocai.org](https://forum.devdocai.org) - In-depth technical discussions
- **Twitter/X**: [@devdocai](https://twitter.com/devdocai) - Updates and news
- **Blog**: [blog.devdocai.org](https://blog.devdocai.org) - Technical articles and tutorials

### Getting Help

1. Check [documentation](https://docs.devdocai.org) and [FAQ](https://docs.devdocai.org/faq)
2. Search existing [GitHub issues](https://github.com/devdocai/devdocai/issues)
3. Ask in Discord `#help` channel for quick questions
4. Create a [GitHub Discussion](https://github.com/devdocai/devdocai/discussions) for design questions
5. Email <support@devdocai.org> for sensitive matters

### Community Meetings

- **Community Call**: Thursdays 3:00 PM UTC (Monthly)
  - Project updates and roadmap discussion
  - Feature demonstrations
  - Q&A session
  
- **Contributor Sync**: Tuesdays 5:00 PM UTC (Bi-weekly)
  - Technical deep-dives
  - PR reviews and design discussions
  - Sprint planning

Meeting notes are posted in `/meetings` and recordings on our [YouTube channel](https://youtube.com/@devdocai).

## Code of Conduct

We are committed to providing a welcoming, inclusive, and harassment-free environment for all contributors.

### Our Standards

- **Be Respectful**: Value diverse perspectives and experiences
- **Be Constructive**: Provide actionable, helpful feedback
- **Be Inclusive**: Welcome contributors of all backgrounds and skill levels
- **Be Professional**: Focus on what's best for the community and project
- **Be Patient**: Remember that everyone was new once

### Unacceptable Behavior

- Harassment, discrimination, or offensive language
- Personal attacks or inflammatory comments
- Publishing others' private information
- Sexual harassment or unwelcome advances
- Trolling or intentionally disruptive behavior
- Any conduct inappropriate for a professional setting

### Enforcement

1. **First Offense**: Private warning from maintainers
2. **Second Offense**: Public warning with specific consequences
3. **Third Offense**: Temporary ban from project interactions
4. **Severe Violations**: Immediate permanent ban

### Reporting

If you experience or witness unacceptable behavior:

- **Email**: <conduct@devdocai.org> (private, confidential)
- **Discord**: DM any moderator
- **Anonymous Form**: [devdocai.org/report](https://devdocai.org/report)

All reports are reviewed within 48 hours. We maintain strict confidentiality and protect reporters from retaliation.

For complete details, see [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## Recognition

### Contributor Recognition Program

We value every contribution and recognize contributors through:

- **Contributors File**: Listed in [CONTRIBUTORS.md](CONTRIBUTORS.md) with contribution details
- **Release Notes**: Highlighted in version releases
- **Contributor Badge**: Special Discord role and GitHub badge
- **Swag Program**: DevDocAI merchandise for significant contributions
- **Conference Tickets**: Sponsorship for major contributors to attend conferences
- **Advisory Board**: Top contributors invited to join technical advisory board

### Contribution Levels

| Level | Contributions | Recognition |
|-------|--------------|-------------|
| **Supporter** | 1-2 merged PRs | Contributors file |
| **Contributor** | 3-9 merged PRs | Badge + swag |
| **Core Contributor** | 10-24 merged PRs | All above + conference ticket |
| **Maintainer** | 25+ merged PRs | All above + advisory board |

## Questions?

If you have questions about contributing:

1. Check our comprehensive [FAQ](https://docs.devdocai.org/faq)
2. Ask in Discord `#contributors` channel
3. Create a [GitHub Discussion](https://github.com/devdocai/devdocai/discussions)
4. Attend our community meetings
5. Email <maintainers@devdocai.org> for specific concerns

---

**Thank you for contributing to DevDocAI v3.5.0!** 🚀

Your contributions help thousands of solo developers and small teams create better documentation with less effort. Whether you're fixing a typo, adding a feature, or creating a plugin, every contribution makes DevDocAI better for our entire community.

Together, we're democratizing professional documentation creation and making enterprise-grade documentation tools accessible to everyone!

*Last Updated: August 2025 | Version: 3.5.0*
