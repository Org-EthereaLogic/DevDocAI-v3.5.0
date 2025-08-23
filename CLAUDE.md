# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## DevDocAI Project Overview

DevDocAI v3.5.0 is an AI-powered documentation system for solo developers that transforms documentation from a burden into an efficient, quality-driven workflow. The system uses the MIAIR (Meta-Iterative AI Refinement) methodology to achieve 60-75% quality improvement through multi-LLM synthesis (Claude, ChatGPT, Gemini).

## Core Architecture

### Modular Component System (M001-M013)

The system consists of 13 core modules organized in 4 implementation phases:

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

### Memory Mode Architecture

The system automatically adapts to available hardware:
- **Baseline (<2GB)**: Templates only, no AI
- **Standard (2-4GB)**: Full features with cloud AI
- **Enhanced (4-8GB)**: Local AI models, heavy caching
- **Performance (>8GB)**: Maximum optimization

### Quality Gate System

All documentation must achieve exactly 85% quality score across four dimensions:
1. Requirements Analysis (25%)
2. Design Review (25%)
3. Security Assessment (25%)
4. Performance Optimization (25%)

## Build and Development Commands

### Initial Setup
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

### Build Commands
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

### Testing Commands
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

## AI-Accessible Database System (New)

### Overview
DevDocAI now includes a comprehensive AI-Accessible Database System that serves as the North Star (primary source of truth) for AI agents throughout the development lifecycle. This hybrid architecture enables intelligent querying, semantic search, and real-time synchronization of all documentation.

### Architecture Components
The system uses a hybrid database architecture for optimal performance:
- **Qdrant Vector Database**: Semantic search with OpenAI embeddings (1536-dim)
- **Neo4j Graph Database**: Document relationships and requirement traceability
- **PostgreSQL with pgvector**: Hybrid search combining vector and full-text
- **Redis Cache Layer**: Sub-second response times for frequent queries
- **Elasticsearch**: Advanced full-text search capabilities

### AI Agent Capabilities
The database system provides 7 specialized query types:
1. **Semantic Search**: Natural language queries across all documents
2. **Requirement Tracing**: Follow requirements from US-001 through implementation
3. **Module Dependencies**: Navigate M001-M013 component relationships
4. **Test Coverage Analysis**: Real-time testing gap identification
5. **Implementation Guides**: Step-by-step development guidance
6. **Consistency Checking**: Detect conflicts between documents
7. **Architecture Queries**: Access design patterns and system structure

### Database Setup Commands
```bash
# Navigate to database implementation
cd database-design/implementation

# Set up environment
cp .env.example .env
# Add your OPENAI_API_KEY to .env

# Start all database services
make setup

# Ingest DevDocAI documentation
make ingest

# Run interactive queries
make query

# Start API server
make server
```

### Docker Deployment
```bash
# Deploy complete system with Docker Compose
docker-compose up -d

# Check system health
curl http://localhost:8000/health

# View logs
docker-compose logs -f
```

### API Endpoints
- `GET /` - System information and status
- `GET /health` - Health check for all components
- `POST /api/query` - Execute AI agent queries
- `POST /api/chat` - Interactive chat with documentation
- `POST /api/ingest` - Ingest new documents
- `GET /metrics` - Prometheus metrics for monitoring

### Performance Specifications
- **Query Response Time**: <1 second (p95 latency)
- **Document Ingestion**: 10-15 documents/second
- **Consistency Guarantee**: 99.9% with real-time sync
- **Cache Hit Rate**: 60-70% typical
- **Concurrent Users**: 100+ supported
- **Storage Requirements**: ~50GB for complete suite

### Integration with AI Agents
```python
# Python integration example
from ai_agent_interface import AIAgentInterface, QueryInput

interface = AIAgentInterface()
result = await interface.query(QueryInput(
    query="How to implement MIAIR engine?",
    query_type="implementation_guides"
))
```

### LangChain Integration
The system uses LangChain for seamless AI agent integration:
- Custom tools for each query type
- Conversational retrieval chains
- Memory management for context retention
- Automatic prompt optimization
- Result ranking and fusion

### Database File Structure
```
database-design/
├── implementation/
│   ├── setup_databases.py       # Database initialization
│   ├── document_ingestion.py    # Document processing pipeline
│   ├── ai_agent_interface.py    # AI agent query interface
│   ├── main.py                  # FastAPI server
│   ├── config.yaml              # Configuration
│   ├── docker-compose.yml       # Docker orchestration
│   ├── requirements.txt         # Python dependencies
│   ├── Makefile                 # Automation commands
│   └── README.md                # Detailed documentation
```

### Monitoring and Observability
- **Prometheus Metrics**: Complete system metrics exposed
- **Grafana Dashboards**: Pre-configured visualization
- **Query Logging**: All queries logged for analysis
- **Performance Tracking**: Latency and throughput monitoring
- **Error Tracking**: Comprehensive error handling and alerting

### Security Features
- API key management for authentication
- Role-based access control ready
- Docker network isolation
- Encrypted data at rest
- Audit logging for compliance

### Maintenance Commands
```bash
# Check database status
make status

# View logs
make logs

# Run system tests
make test

# Benchmark performance
make benchmark

# Clean up resources
make clean
```

This AI-Accessible Database System transforms the DevDocAI documentation suite into an intelligent knowledge base that AI agents can reliably query and use as their authoritative reference throughout the entire development process.