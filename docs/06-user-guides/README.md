# 06-User Guides Documentation

## Overview

This directory contains end-user documentation, tutorials, and guides for DevDocAI v3.5.0.

## Documents

### [User Manual](devdocai-v3.5-user-manual.md)
**Purpose**: Comprehensive guide for end users to effectively use DevDocAI.
**Audience**: End users, support teams, training teams
**Key Sections**: Getting started, features, workflows, troubleshooting

### [User Documentation](devdocai-v3.5-user-documentation.md)
**Purpose**: Quick reference and task-oriented documentation.
**Audience**: End users, developers using DevDocAI
**Key Sections**: Command reference, configuration, examples, FAQs

## Quick Start Guide

### Installation
```bash
# Install globally via npm
npm install -g devdocai

# Initialize in your project
devdocai init

# Generate your first document
devdocai generate readme

# Run quality analysis
devdocai quality check
```

### Key Features

#### Document Generation
- 40+ document types
- Template-based generation
- AI enhancement with MIAIR
- Quality gate enforcement (85%)

#### Multi-LLM Support
- Claude integration
- ChatGPT integration
- Gemini integration
- Cost optimization

#### Memory Modes
- **Baseline (<2GB)**: Templates only
- **Standard (2-4GB)**: Full features
- **Enhanced (4-8GB)**: Local AI
- **Performance (>8GB)**: Maximum optimization

## Common Use Cases

### For Solo Developers
1. Automated documentation generation
2. Quality improvement through AI
3. Consistency across projects
4. Time savings (60-75%)

### For Small Teams
1. Standardized documentation
2. Template sharing
3. Quality enforcement
4. Knowledge preservation

## User Workflows

### Basic Workflow
1. Initialize DevDocAI
2. Configure settings
3. Generate documents
4. AI enhancement
5. Quality review
6. Export/publish

### Advanced Features
- Custom templates
- Plugin development
- Batch operations
- CI/CD integration
- SBOM generation

## Reading Order

1. Start with **User Manual** for comprehensive understanding
2. Use **User Documentation** as quick reference
3. Check project README for latest updates

## Related Documentation

- [Installation Guide](../04-deployment/devdocai-v3.5-deployment-installation-guide.md) - Setup details
- [API Documentation](../03-specifications/devdocai-v3.5-api-documentation.md) - Programmatic usage
- [Build Instructions](../04-deployment/devdocai-v3.5-build-instructions.md) - Building from source

## Support Resources

### Getting Help
- **Documentation**: This user guide
- **Examples**: `/examples` directory
- **Issues**: GitHub issue tracker
- **Discussions**: GitHub Discussions

### Common Issues
- Memory mode detection
- LLM API configuration
- Template customization
- Quality gate failures

## Tips and Best Practices

1. **Start Simple**: Use default templates initially
2. **Configure Properly**: Set up .env for API keys
3. **Use Quality Gates**: Don't skip quality checks
4. **Leverage AI**: Enable MIAIR for better docs
5. **Customize Gradually**: Build custom templates over time

## Document Status

User documentation is currently **Active** and regularly updated based on user feedback.