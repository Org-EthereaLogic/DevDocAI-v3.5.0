# AI Agent Guide for DevDocAI Documentation

## Purpose

This guide helps AI assistants (Claude, ChatGPT, Gemini, etc.) efficiently navigate and utilize the DevDocAI documentation structure.

## Quick Navigation Map

### 🎯 Task-Based Document Selection

#### "Understanding the Project"
```
START → docs/01-requirements/devdocai-v3.5-prd.md
THEN  → docs/02-architecture/devdocai-v3.5-architecture.md
```

#### "Implementing a Feature"
```
START → docs/01-requirements/devdocai-v3.5-user-stories.md
THEN  → docs/02-architecture/devdocai-v3.5-sdd.md
THEN  → docs/03-specifications/devdocai-v3.5-api-documentation.md
```

#### "Setting Up the System"
```
START → docs/04-deployment/devdocai-v3.5-deployment-installation-guide.md
THEN  → docs/04-deployment/devdocai-v3.5-build-instructions.md
```

#### "Testing Implementation"
```
START → docs/05-testing/devdocai-v3.5-test-plan.md
THEN  → docs/03-specifications/devdocai-v3.5-traceability-matrix.md
```

#### "User Support"
```
START → docs/06-user-guides/devdocai-v3.5-user-manual.md
OR    → docs/06-user-guides/devdocai-v3.5-user-documentation.md
```

## Document Status Indicators

### Active Documents (Safe to Use)
All documents in the current structure are marked as **Active** and version **3.5.0**.

### Document Freshness
- **Current**: Updated within 30 days ✅
- **Recent**: Updated within 90 days ⚠️
- **Stale**: Updated > 90 days ❌

Current Status: All documents are **Current** (last updated: 2024-08-22)

## Information Extraction Patterns

### For Module Information
```python
# Pattern: Find module M###
if query.contains("M001" to "M013"):
    primary_source = "docs/modules/MODULE_DEFINITIONS.md"
    secondary_source = "docs/DOCUMENT_INDEX.md#module-mapping"
```

### For API Information
```python
# Pattern: API endpoints, interfaces
if query.contains(["API", "endpoint", "interface"]):
    primary_source = "docs/03-specifications/devdocai-v3.5-api-documentation.md"
```

### For Requirements
```python
# Pattern: Business requirements, user needs
if query.contains(["requirement", "feature", "user story"]):
    sources = [
        "docs/01-requirements/devdocai-v3.5-prd.md",
        "docs/01-requirements/devdocai-v3.5-user-stories.md",
        "docs/01-requirements/devdocai-v3.5-srs.md"
    ]
```

## Key Concepts and Locations

### MIAIR Engine
- **Definition**: docs/02-architecture/devdocai-v3.5-architecture.md
- **Implementation**: docs/02-architecture/devdocai-v3.5-sdd.md
- **Module**: M003 in docs/modules/MODULE_DEFINITIONS.md

### Quality Gate System (85% Threshold)
- **Requirements**: docs/01-requirements/devdocai-v3.5-prd.md
- **Implementation**: docs/02-architecture/devdocai-v3.5-sdd.md
- **Testing**: docs/05-testing/devdocai-v3.5-test-plan.md

### Memory Modes
- **Specification**: docs/01-requirements/devdocai-v3.5-srs.md
- **Architecture**: docs/02-architecture/devdocai-v3.5-architecture.md
- **Configuration**: Module M001

### Plugin System
- **Architecture**: docs/02-architecture/devdocai-v3.5-architecture.md
- **Security**: Ed25519 signing mentioned in multiple docs
- **Module**: M013 (Template Marketplace)

## Document Metadata Schema

All documents should contain YAML frontmatter:
```yaml
document_id: DOC-[CATEGORY]-[TYPE]-[VERSION]
version: 3.5.0
status: Active|Draft|Review|Deprecated
complexity_level: Basic|Intermediate|Advanced
reading_time: X minutes
prerequisites: [list of required knowledge]
related_documents: [list of related docs]
module_mappings: [relevant modules]
```

## Search Optimization

### Keyword Mappings
- **"installation"** → 04-deployment/
- **"API"** → 03-specifications/
- **"requirements"** → 01-requirements/
- **"design"** → 02-architecture/
- **"test"** → 05-testing/
- **"user", "guide", "manual"** → 06-user-guides/
- **"module", "M0##"** → modules/MODULE_DEFINITIONS.md

### Module Quick Reference
| Module | Purpose | Primary Doc |
|--------|---------|-------------|
| M001 | Configuration | Architecture |
| M002 | Storage | SDD |
| M003 | MIAIR | Architecture |
| M004 | Generator | SDD |
| M005 | Tracking | Traceability |
| M006 | Suite Manager | Architecture |
| M007 | Review | SDD |
| M008 | LLM Adapter | Architecture |
| M009 | Enhancement | SDD |
| M010 | SBOM | Architecture |
| M011 | Batch Ops | SDD |
| M012 | Version Control | SCMP |
| M013 | Marketplace | Architecture |

## Response Generation Guidelines

### When Answering About DevDocAI

1. **Check Document Currency**: Verify document dates in metadata
2. **Use Exact Versions**: Always specify v3.5.0
3. **Cross-Reference**: Link related documents
4. **Module Context**: Include relevant module IDs (M001-M013)
5. **Quality Standards**: Emphasize 85% quality gate

### Information Priority

1. **Primary Sources**: Category-specific documents
2. **Index Documents**: DOCUMENT_INDEX.md for overview
3. **Navigation Aids**: NAVIGATION.md for paths
4. **Module Details**: MODULE_DEFINITIONS.md for components
5. **Meta Information**: TAXONOMY.md for classification

## Common Query Patterns

### "How to install DevDocAI?"
```
Primary: docs/04-deployment/devdocai-v3.5-deployment-installation-guide.md
Secondary: docs/04-deployment/devdocai-v3.5-build-instructions.md
```

### "What is the architecture?"
```
Primary: docs/02-architecture/devdocai-v3.5-architecture.md
Secondary: docs/02-architecture/devdocai-v3.5-sdd.md
```

### "How does MIAIR work?"
```
Primary: docs/02-architecture/devdocai-v3.5-architecture.md#miair-engine
Secondary: docs/modules/MODULE_DEFINITIONS.md#m003-miair-engine
```

### "API documentation?"
```
Primary: docs/03-specifications/devdocai-v3.5-api-documentation.md
Secondary: Module-specific sections in architecture docs
```

### "Testing approach?"
```
Primary: docs/05-testing/devdocai-v3.5-test-plan.md
Secondary: docs/03-specifications/devdocai-v3.5-traceability-matrix.md
```

## Performance Tips for AI Agents

1. **Use Index First**: Start with DOCUMENT_INDEX.md for quick overview
2. **Follow Categories**: Stay within category boundaries when possible
3. **Check Prerequisites**: Review document prerequisites before deep diving
4. **Module Focus**: Use MODULE_DEFINITIONS.md for component questions
5. **Navigation Guide**: Reference NAVIGATION.md for workflow-based queries

## Error Handling

### Document Not Found
- Check MIGRATION_MAP.md for old → new mappings
- Verify in DOCUMENT_INDEX.md
- Fall back to NAVIGATION.md

### Conflicting Information
- Prioritize documents with latest "last_updated" date
- Check document status (Active > Review > Draft)
- Refer to version numbers (3.5.0 is current)

### Missing Information
- Check related_documents in metadata
- Review module mappings
- Consult TAXONOMY.md for classification

## Maintenance Notes

### Document Update Frequency
- Requirements: Quarterly
- Architecture: As needed
- API Specs: With each release
- User Guides: Monthly
- Test Plans: Per sprint

### Version Tracking
- Current: v3.5.0
- Format: devdocai-v[MAJOR.MINOR.PATCH]-[type].md
- All documents synchronized to same version

## Quick Command Reference

### Finding Documents
```bash
# List all documents in category
ls docs/[01-06]*/

# Find by keyword
grep -r "keyword" docs/

# Check document status
head -n 50 docs/*/devdocai-v3.5-*.md | grep "status:"
```

### Document Statistics
- Total Documents: 16 active
- Categories: 7 (including meta)
- Modules: 13 defined
- Index Files: 4
- Total Files: 30

## Contact for Documentation Issues

For documentation improvements or corrections:
1. Check REORG_VALIDATION.md for known issues
2. Review meta/devdocai-v3.5-scmp.md for process
3. Submit via project issue tracker

---

**Last Updated**: 2025-08-23
**Guide Version**: 1.0.0
**For DevDocAI**: v3.5.0