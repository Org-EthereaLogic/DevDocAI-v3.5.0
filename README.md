# DevDocAI v3.5.0

**AI-Powered Documentation for Solo Developers**

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Plugin SDK: MIT](https://img.shields.io/badge/Plugin%20SDK-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-3.5.0-brightgreen.svg)](https://github.com/devdocai/devdocai/releases)
[![WCAG 2.1 AA](https://img.shields.io/badge/WCAG%202.1-AA-success.svg)](https://www.w3.org/WAI/WCAG21/quickref/)
[![Documentation](https://img.shields.io/badge/docs-available-brightgreen.svg)](https://docs.devdocai.org)

DevDocAI empowers solo developers, independent contractors, and small teams to create professional-grade technical documentation without dedicated writing resources. Using AI-powered analysis, multi-LLM synthesis, and the innovative MIAIR (Meta-Iterative AI Refinement) methodology, DevDocAI transforms documentation from a burden into an efficient, quality-driven workflow.

## Key Features

### Core Capabilities

- **📝 Comprehensive Document Generation**: Create 40+ document types from intelligent templates
- **🔍 Multi-Dimensional Analysis**: Quality reviews across requirements, design, security, and performance
- **📊 Suite Management**: Visual tracking matrix maintains consistency across all documents
- **🤖 AI Enhancement**: Multi-LLM synthesis using Claude, ChatGPT, and Gemini with 60-75% quality improvement
- **💰 Cost Management**: Smart API routing and budget controls with real-time tracking
- **⚡ Memory Adaptive**: Automatically adjusts to your hardware (1GB to 8GB+ RAM)

### Enterprise Compliance Features (v3.5.0)

- **🔐 SBOM Generation**: Software Bill of Materials in SPDX 2.3 and CycloneDX 1.4 formats
- **🛡️ PII Detection**: Automatic detection with 95%+ accuracy for GDPR/CCPA compliance
- **📋 DSR Support**: Automated Data Subject Rights workflows with 30-day compliance
- **🔒 Privacy-First**: Complete offline capability with optional cloud features
- **✅ Quality Gates**: Enforces exactly 85% documentation quality threshold

## Technology Stack

- **Core**: TypeScript, Node.js 16+, Python 3.8+
- **AI Models**: Claude (Anthropic), ChatGPT (OpenAI), Gemini (Google)
- **Interfaces**: VS Code Extension, Command Line Interface
- **Frameworks**: MIAIR methodology for entropy optimization
- **Security**: Ed25519 signatures, Argon2id encryption, sandboxed plugins
- **Standards**: WCAG 2.1 AA accessibility, SPDX/CycloneDX SBOM formats

## Quick Start

### System Requirements

DevDocAI adapts to your available hardware:

| Memory Mode | RAM | Features |
|-------------|-----|----------|
| **Baseline** | <2GB | Templates only, no AI |
| **Standard** | 2-4GB | Full features with cloud AI |
| **Enhanced** | 4-8GB | Local AI models, heavy caching |
| **Performance** | >8GB | Maximum optimization |

### Installation

#### Method 1: VS Code Extension (Recommended)

1. Open VS Code (version 1.70.0+)
2. Go to Extensions (Ctrl+Shift+X / Cmd+Shift+X)
3. Search for "DevDocAI"
4. Click Install on DevDocAI v3.5.0
5. Reload VS Code when prompted

#### Method 2: Command Line Interface

```bash
# Install globally via npm
npm install -g @devdocai/cli

# Or use with npx (no installation required)
npx @devdocai/cli generate --help

# Verify installation
devdocai --version
```

#### Method 3: From Source

```bash
# Clone the repository
git clone https://github.com/devdocai/devdocai.git
cd devdocai

# Install dependencies
npm install

# Build the project
npm run build

# Run setup wizard
npm run setup
```

### Configuration

Create a `.devdocai.yml` file in your project root:

```yaml
# DevDocAI Configuration v3.5.0
version: 3.5.0
project_name: "Your Project"

# Memory mode (auto-detected if not specified)
memory_mode: standard  # baseline | standard | enhanced | performance

# Quality settings
quality:
  gate_threshold: 85  # Exactly 85% required
  enable_reviews: true
  review_types:
    - requirements
    - design
    - security
    - performance

# AI Configuration (optional)
ai:
  providers:
    - claude    # Primary provider
    - chatgpt   # Secondary provider
    - gemini    # Tertiary provider
  local_models: false  # Enable for Enhanced/Performance modes

# Cost Management
cost_management:
  daily_limit: 10.00    # USD
  monthly_limit: 200.00 # USD
  warning_threshold: 80 # Percentage

# Compliance Features
compliance:
  sbom:
    enabled: true
    format: spdx  # spdx | cyclonedx
    sign: true
  pii_detection:
    enabled: true
    sensitivity: medium  # low | medium | high
  dsr:
    enabled: true
    response_time: 24  # hours

# Privacy Settings
privacy:
  offline_mode: false
  local_storage_only: false
  telemetry: disabled
```

## Usage Guide

### Generate Documentation

```bash
# Generate a Product Requirements Document
devdocai generate prd --project "My App"

# Generate complete documentation suite
devdocai generate suite --all

# Generate with specific template
devdocai generate srs --template agile
```

### Analyze Existing Documentation

```bash
# Analyze a single document
devdocai analyze README.md

# Analyze entire documentation suite
devdocai analyze ./docs --recursive

# Analyze with specific review type
devdocai analyze design-doc.md --review security
```

### Enhance Documentation with AI

```bash
# Enhance document quality using MIAIR methodology
devdocai enhance requirements.md

# Enhance with specific target quality
devdocai enhance api-docs.md --target-quality 90

# Batch enhancement
devdocai enhance ./docs/*.md --parallel
```

### Generate Compliance Documents

```bash
# Generate Software Bill of Materials
devdocai sbom generate --format spdx --sign

# Scan for PII in documentation
devdocai pii scan ./docs --sensitivity high

# Generate GDPR compliance report
devdocai compliance gdpr --export report.pdf
```

### Manage Documentation Suite

```bash
# View documentation tracking matrix
devdocai matrix show

# Check suite consistency
devdocai suite validate

# Update document relationships
devdocai matrix update --auto-detect
```

## API Documentation

### Core Modules

```typescript
import { DevDocAI } from '@devdocai/core';

// Initialize with configuration
const devdocai = new DevDocAI({
  memoryMode: 'standard',
  qualityGate: 0.85,
  enableCompliance: true
});

// Generate document
const document = await devdocai.generate('prd', {
  project: 'My Project',
  context: projectContext
});

// Analyze quality
const analysis = await devdocai.analyze(document);
console.log(`Quality Score: ${analysis.qualityScore}%`);

// Enhance with AI
const enhanced = await devdocai.enhance(document, {
  targetQuality: 0.90,
  useProviders: ['claude', 'chatgpt']
});
```

### Plugin Development

```typescript
import { Plugin, DocumentType } from '@devdocai/plugin-sdk';

export class CustomPlugin extends Plugin {
  constructor() {
    super({
      name: 'my-custom-plugin',
      version: '1.0.0',
      devdocaiVersion: '>=3.5.0'
    });
  }

  async activate(context) {
    // Register custom document types
    this.registerDocumentType({
      id: 'custom-doc',
      name: 'Custom Document',
      template: customTemplate
    });
  }
}
```

## Configuration Details

### Environment Variables

```bash
# API Keys (optional for cloud features)
CLAUDE_API_KEY=your_claude_key
OPENAI_API_KEY=your_openai_key
GEMINI_API_KEY=your_gemini_key

# Cost Limits
DAILY_COST_LIMIT=10.00
MONTHLY_COST_LIMIT=200.00

# Performance
MEMORY_MODE=standard
CACHE_SIZE=500MB
PARALLEL_WORKERS=4

# Security
ENABLE_TELEMETRY=false
OFFLINE_MODE=false
PLUGIN_SANDBOX=true
```

### VS Code Settings

```json
{
  "devdocai.memoryMode": "standard",
  "devdocai.qualityGate": 85,
  "devdocai.enableAI": true,
  "devdocai.costTracking": true,
  "devdocai.compliance.sbom": true,
  "devdocai.compliance.pii": true,
  "devdocai.theme": "dark"
}
```

## Advanced Features

### Multi-LLM Synthesis

DevDocAI intelligently combines outputs from multiple AI models:

- **Claude**: Best for requirements and technical writing
- **ChatGPT**: Excellent for code documentation
- **Gemini**: Optimal for creative content

The system automatically selects providers based on:
- Document type and complexity
- Cost optimization
- Quality requirements
- API availability

### MIAIR Methodology

The Meta-Iterative AI Refinement methodology achieves 60-75% quality improvement through:

1. **Initial Analysis**: Baseline quality assessment
2. **Entropy Reduction**: Systematic organization improvement
3. **Iterative Enhancement**: Multiple refinement passes
4. **Quality Validation**: Ensures 85% threshold

### Plugin Architecture

Extend DevDocAI with custom functionality:

- **Custom Document Types**: Industry-specific templates
- **Specialized Analyzers**: Domain-specific quality checks
- **Integration Connectors**: External tool connections
- **Custom Metrics**: Tailored quality measurements

All plugins are:
- Digitally signed with Ed25519
- Sandboxed for security
- Version-compatible
- Hot-reloadable

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Quick Contribution Guide

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/devdocai.git
cd devdocai

# Install dependencies
npm install

# Run tests
npm test

# Run with hot reload
npm run dev
```

## Documentation

- **[User Manual](docs/devdocai-user-manual.md)**: Complete usage guide
- **[API Documentation](docs/devdocai-api-documentation.md)**: Developer reference
- **[Architecture Blueprint](docs/devdocsai-architecture.md)**: System design
- **[Plugin Development](docs/plugin-guide.md)**: Extension guide
- **[Deployment Guide](docs/devdocai-deployment-installation-guide.md)**: Installation details

## License

DevDocAI uses a dual-license model:

- **Core System**: [Apache License 2.0](LICENSE) - Commercial use allowed
- **Plugin SDK**: MIT License - Maximum flexibility for extensions

See the [LICENSE](LICENSE) file for details.

## Support

### Getting Help

- **Documentation**: [docs.devdocai.org](https://docs.devdocai.org)
- **Discord Community**: [discord.gg/devdocai](https://discord.gg/devdocai)
- **GitHub Issues**: [Report bugs or request features](https://github.com/devdocai/devdocai/issues)
- **Forum**: [forum.devdocai.org](https://forum.devdocai.org)
- **Email Support**: support@devdocai.org

### Professional Support

For enterprise support, custom development, or training:
- **Email**: enterprise@devdocai.org
- **Website**: [devdocai.org/enterprise](https://devdocai.org/enterprise)

## Roadmap

### Phase 1: Foundation (Complete)
- ✅ Core document generation
- ✅ Basic quality analysis
- ✅ VS Code extension
- ✅ CLI interface

### Phase 2: Intelligence (Complete)
- ✅ MIAIR methodology implementation
- ✅ Multi-LLM synthesis
- ✅ Cost management system
- ✅ Batch operations

### Phase 3: Enhancement (Current)
- ✅ SBOM generation
- ✅ PII detection
- ✅ DSR support
- 🚧 Plugin marketplace
- 🚧 Advanced analytics

### Phase 4: Ecosystem (Planned)
- 📅 Cloud collaboration
- 📅 Team features
- 📅 Mobile applications
- 📅 AI model fine-tuning

## Acknowledgments

DevDocAI is built with these excellent open-source projects:

- [TypeScript](https://www.typescriptlang.org/) - Type-safe JavaScript
- [Node.js](https://nodejs.org/) - JavaScript runtime
- [VS Code API](https://code.visualstudio.com/api) - Editor integration
- [Commander.js](https://github.com/tj/commander.js/) - CLI framework
- [Anthropic Claude](https://www.anthropic.com/) - AI language model
- [OpenAI](https://openai.com/) - AI language model
- [Google Gemini](https://deepmind.google/technologies/gemini/) - AI language model

## Community

Join our growing community of developers improving documentation:

- **Contributors**: 50+ active contributors
- **Users**: 1,000+ installations
- **Discord Members**: 500+ members
- **Documentation Generated**: 10,000+ documents

## Citation

If you use DevDocAI in your research or project, please cite:

```bibtex
@software{devdocai2025,
  title = {DevDocAI: AI-Powered Documentation for Solo Developers},
  author = {DevDocAI Team},
  year = {2025},
  version = {3.5.0},
  url = {https://github.com/devdocai/devdocai},
  license = {Apache-2.0}
}
```

---

**Built with ❤️ by developers, for developers**

*Empowering solo developers to create professional documentation with the power of AI*