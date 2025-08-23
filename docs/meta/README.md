# Meta Documentation

## Overview

This directory contains documentation standards, templates, and governance documents for the DevDocAI v3.5.0 documentation system.

## Documents

### [Software Configuration Management Plan (SCMP)](devdocai-v3.5-scmp.md)
**Purpose**: Defines configuration management processes, version control, and change management procedures.
**Audience**: Development team, project managers, documentation team
**Key Sections**: Version control, change management, release procedures, documentation standards

## Documentation Standards

### Document Structure
- **Consistent Headers**: All documents use standardized headers
- **Version Control**: Semantic versioning (v3.5.0)
- **Metadata**: YAML frontmatter for all documents
- **Status Tracking**: Draft → Review → Active → Deprecated

### Naming Conventions
```
devdocai-[version]-[document-type].md
```

Examples:
- `devdocai-v3.5-prd.md`
- `devdocai-v3.5-api-documentation.md`
- `devdocai-v3.5-user-manual.md`

### Document Categories
1. **01-requirements**: Business and functional requirements
2. **02-architecture**: Technical design and architecture
3. **03-specifications**: APIs and technical specs
4. **04-deployment**: Installation and operations
5. **05-testing**: Quality assurance
6. **06-user-guides**: End-user documentation
7. **meta**: Documentation governance

## Documentation Lifecycle

### Phases
1. **Draft**: Initial creation, work in progress
2. **Review**: Under stakeholder review
3. **Active**: Approved and current
4. **Deprecated**: Outdated but retained
5. **Archived**: No longer relevant

### Review Process
1. Author creates draft
2. Technical review
3. Stakeholder review
4. Approval and activation
5. Regular updates

## Quality Standards

### Documentation Quality Metrics
- **Completeness**: All sections filled
- **Accuracy**: Technically correct
- **Clarity**: Readability score >60
- **Currency**: Updated within 90 days
- **Consistency**: Follows style guide
- **Coverage**: Addresses all requirements

### Quality Levels
- **Green (90-100%)**: Excellent
- **Yellow (70-89%)**: Good
- **Orange (50-69%)**: Fair
- **Red (<50%)**: Poor

## Version Control

### Git Workflow
- **Branches**: feature/*, bugfix/*, release/*
- **Commits**: Descriptive messages
- **Tags**: Version releases (v3.5.0)
- **History**: Preserve with git mv

### Change Management
- Document all changes
- Review before merge
- Update version numbers
- Maintain change log

## Templates

### Document Template Structure
```markdown
# Document Title

## Metadata
```yaml
document_id: DOC-CAT-TYPE-VERSION
version: 3.5.0
status: Active
last_updated: YYYY-MM-DD
```

## Overview
[Brief description]

## Purpose
[Document purpose]

## Audience
[Target readers]

## Content
[Main content sections]

## Related Documents
[Links to related docs]
```

## Reading Order

1. Review **SCMP** for configuration management
2. Check **Documentation Standards** above
3. Follow **Templates** for new documents

## Related Documentation

- [Document Index](../DOCUMENT_INDEX.md) - Master index
- [Taxonomy](../TAXONOMY.md) - Classification system
- [Navigation Guide](../NAVIGATION.md) - How to navigate

## Governance

### Roles and Responsibilities
- **Authors**: Create and update content
- **Reviewers**: Technical accuracy
- **Approvers**: Sign-off on changes
- **Maintainers**: Overall quality

### Update Schedule
- **Critical**: Immediate
- **Major**: Within 7 days
- **Minor**: Within 30 days
- **Review**: Quarterly

## Document Status

Meta documentation is currently **Active** and serves as the authoritative guide for documentation standards.