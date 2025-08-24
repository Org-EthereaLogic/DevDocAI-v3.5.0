#!/bin/bash

# DevDocAI v3.6.0 Filing System Implementation Script
# Version: 1.0.0
# Date: August 23, 2025
# Purpose: Reorganize documentation according to new filing system

set -e  # Exit on error

echo "========================================="
echo "DevDocAI v3.6.0 Filing System Setup"
echo "========================================="
echo ""

# Define base directory
BASE_DIR="/workspaces/DevDocAI-v3.5.0/docs"
cd "$BASE_DIR"

# Function to create directory structure
create_directories() {
    echo "📁 Creating directory structure..."
    
    # Create main directories
    mkdir -p 00-system
    mkdir -p 01-design-specs
    mkdir -p 02-tracking/module-progress
    mkdir -p 02-tracking/daily-progress
    mkdir -p 02-tracking/decision-log
    mkdir -p 03-working/current-sprint
    mkdir -p 03-working/integration-notes
    mkdir -p 03-working/validation-reports
    mkdir -p 04-reference
    
    echo "✅ Directory structure created"
}

# Function to move system control documents
setup_system_docs() {
    echo "📋 Setting up system control documents..."
    
    # Move newly created system documents
    if [ -f "AI-AGENT-FILING-SYSTEM.md" ]; then
        mv AI-AGENT-FILING-SYSTEM.md 00-system/
    fi
    
    if [ -f "AI-AGENT-INSTRUCTIONS.md" ]; then
        mv AI-AGENT-INSTRUCTIONS.md 00-system/
    fi
    
    if [ -f "DATA-INTEGRITY-RULES.md" ]; then
        mv DATA-INTEGRITY-RULES.md 00-system/
    fi
    
    if [ -f "REFERENCE-INDEX.md" ]; then
        mv REFERENCE-INDEX.md 00-system/
    fi
    
    echo "✅ System control documents in place"
}

# Function to move design specifications
move_design_specs() {
    echo "📚 Moving design specifications to immutable location..."
    
    # Move all DESIGN- prefixed files
    for file in DESIGN-*.md; do
        if [ -f "$file" ]; then
            echo "  Moving: $file"
            mv "$file" 01-design-specs/
        fi
    done
    
    echo "✅ Design specifications secured in immutable directory"
}

# Function to move tracking documents
setup_tracking() {
    echo "📊 Setting up tracking documents..."
    
    # Move implementation status tracker
    if [ -f "implementation-status-tracker.md" ]; then
        mv implementation-status-tracker.md 02-tracking/
    fi
    
    # Create module tracking files
    echo "  Creating module tracking templates..."
    
    modules=(
        "M001-config-manager"
        "M002-storage-system"
        "M003-miair-engine"
        "M004-document-generator"
        "M005-tracking-matrix"
        "M006-suite-manager"
        "M007-review-engine"
        "M008-llm-adapter"
        "M009-enhancement-pipeline"
        "M010-sbom-generator"
        "M011-batch-operations"
        "M012-version-control"
        "M013-template-marketplace"
    )
    
    for module in "${modules[@]}"; do
        touch "02-tracking/module-progress/${module}.tracking.md"
    done
    
    # Create initial daily progress file
    TODAY=$(date +%Y-%m-%d)
    touch "02-tracking/daily-progress/${TODAY}-progress.md"
    
    echo "✅ Tracking system initialized"
}

# Function to create working documents
setup_working_docs() {
    echo "📝 Creating working document templates..."
    
    # Create sprint plan template
    cat > 03-working/current-sprint/sprint-plan.md << 'EOF'
# Current Sprint Plan

**Sprint**: [NUMBER]
**Start Date**: [DATE]
**End Date**: [DATE]
**Goal**: [SPRINT GOAL]

## Sprint Backlog

| Task ID | Module | Description | Assignee | Status | Points |
|---------|--------|-------------|----------|--------|--------|
| | | | | | |

## Sprint Burndown

- Total Points: 
- Completed: 
- Remaining: 

## Daily Standup Notes

### [DATE]
- Completed:
- In Progress:
- Blockers:
EOF
    
    # Create blockers template
    cat > 03-working/current-sprint/blockers.md << 'EOF'
# Current Blockers

**Last Updated**: [DATE]

## Active Blockers

| Blocker ID | Module | Description | Severity | Owner | ETA |
|------------|--------|-------------|----------|-------|-----|
| | | | | | |

## Resolved Blockers

| Blocker ID | Resolution | Date Resolved |
|------------|------------|---------------|
| | | |
EOF
    
    # Create dependencies template
    cat > 03-working/current-sprint/dependencies.md << 'EOF'
# Module Dependencies

**Last Updated**: [DATE]

## Dependency Map

| Module | Depends On | Status | Notes |
|--------|------------|--------|-------|
| M001 | None | Ready | |
| M002 | M001 | Waiting | |
| M003 | M002, M008 | Waiting | |
| M004 | M002, M008 | Waiting | |
| M005 | M002 | Waiting | |
| M006 | M004, M005 | Waiting | |
| M007 | M003, M008 | Waiting | |
| M008 | M001 | Waiting | |
| M009 | M003, M008 | Waiting | |
| M010 | M002 | Waiting | |
| M011 | M004, M006 | Waiting | |
| M012 | M002 | Waiting | |
| M013 | M004 | Waiting | |
EOF
    
    echo "✅ Working documents created"
}

# Function to create reference documents
setup_reference_docs() {
    echo "📖 Creating reference documents..."
    
    # Create module dependency graph
    cat > 04-reference/module-dependency-graph.md << 'EOF'
# Module Dependency Graph

**Last Updated**: 2025-08-23

## Visual Dependency Map

```mermaid
graph TD
    M001[M001: Config Manager] --> M002[M002: Storage System]
    M001 --> M008[M008: LLM Adapter]
    
    M002 --> M003[M003: MIAIR Engine]
    M002 --> M004[M004: Doc Generator]
    M002 --> M005[M005: Tracking Matrix]
    M002 --> M010[M010: SBOM Generator]
    M002 --> M012[M012: Version Control]
    
    M003 --> M007[M007: Review Engine]
    M003 --> M009[M009: Enhancement Pipeline]
    
    M004 --> M006[M006: Suite Manager]
    M004 --> M011[M011: Batch Operations]
    M004 --> M013[M013: Template Marketplace]
    
    M005 --> M006
    
    M006 --> M011
    
    M008 --> M003
    M008 --> M004
    M008 --> M007
    M008 --> M009
```

## Implementation Order

### Phase 1: Foundation (P0 Core)
1. M001 - Configuration Manager
2. M002 - Local Storage System

### Phase 2: Core Features (P0)
3. M004 - Document Generator
4. M005 - Tracking Matrix
5. M006 - Suite Manager
6. M007 - Review Engine

### Phase 3: AI Enhancement (P1)
7. M008 - LLM Adapter
8. M003 - MIAIR Engine
9. M009 - Enhancement Pipeline
10. M011 - Batch Operations
11. M012 - Version Control

### Phase 4: Extended Features (P2)
12. M010 - SBOM Generator
13. M013 - Template Marketplace
EOF
    
    # Create API endpoint registry
    cat > 04-reference/api-endpoint-registry.md << 'EOF'
# API Endpoint Registry

**Version**: 1.0.0
**Base URL**: `/api/v1`

## Endpoints by Module

### M001: Configuration Manager
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/config` | Get current configuration |
| PUT | `/config` | Update configuration |
| GET | `/config/validate` | Validate configuration |

### M004: Document Generator
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/documents/generate` | Generate new document |
| GET | `/documents/templates` | List available templates |
| GET | `/documents/{id}` | Get document by ID |

### M007: Review Engine
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/review` | Submit document for review |
| GET | `/review/{id}` | Get review results |
| GET | `/review/metrics` | Get quality metrics |

[Additional endpoints to be added as modules are implemented]
EOF
    
    # Create error code registry
    cat > 04-reference/error-code-registry.md << 'EOF'
# Error Code Registry

**Version**: 1.0.0

## Error Code Format
`[MODULE]-[SEVERITY]-[NUMBER]`

- MODULE: M001-M013
- SEVERITY: E (Error), W (Warning), I (Info)
- NUMBER: 001-999

## Error Codes by Module

### M001: Configuration Manager
| Code | Description | Resolution |
|------|-------------|------------|
| M001-E-001 | Invalid configuration file | Check YAML/JSON syntax |
| M001-E-002 | Missing required field | Add required configuration field |
| M001-W-001 | Deprecated configuration key | Update to new configuration format |

### M002: Storage System
| Code | Description | Resolution |
|------|-------------|------------|
| M002-E-001 | Storage initialization failed | Check disk permissions |
| M002-E-002 | Corrupted data file | Restore from backup |
| M002-W-001 | Storage near capacity | Clean up old data |

[Additional error codes to be added as modules are implemented]
EOF
    
    # Create glossary
    cat > 04-reference/glossary.md << 'EOF'
# DevDocAI Glossary

**Version**: 1.0.0

## Terms and Definitions

| Term | Definition |
|------|------------|
| **ADR** | Architecture Decision Record - Document capturing important architectural decisions |
| **DevDocAI** | AI-powered documentation automation system for software projects |
| **FR** | Functional Requirement - What the system should do |
| **MIAIR** | Multi-Iteration AI Refinement - Enhancement methodology |
| **NFR** | Non-Functional Requirement - How the system should perform |
| **PRD** | Product Requirements Document - High-level product specifications |
| **SBOM** | Software Bill of Materials - Inventory of software components |
| **SDD** | Software Design Document - Detailed technical design |
| **SCMP** | Software Configuration Management Plan - Version control strategy |
| **SRS** | Software Requirements Specification - Detailed requirements |
| **TC** | Test Case - Specific test scenario |
| **US** | User Story - Feature from user perspective |

## Module Abbreviations

| Code | Full Name |
|------|-----------|
| M001 | Configuration Manager |
| M002 | Local Storage System |
| M003 | MIAIR Engine |
| M004 | Document Generator |
| M005 | Tracking Matrix |
| M006 | Suite Manager |
| M007 | Review Engine |
| M008 | LLM Adapter |
| M009 | Enhancement Pipeline |
| M010 | SBOM Generator |
| M011 | Batch Operations Manager |
| M012 | Version Control Integration |
| M013 | Template Marketplace |
EOF
    
    echo "✅ Reference documents created"
}

# Function to create checksums for immutable files
generate_checksums() {
    echo "🔐 Generating checksums for immutable documents..."
    
    CHECKSUM_FILE="00-system/document-checksums.txt"
    > "$CHECKSUM_FILE"
    
    for file in 01-design-specs/*.md; do
        if [ -f "$file" ]; then
            checksum=$(sha256sum "$file" | cut -d' ' -f1)
            filename=$(basename "$file")
            echo "$checksum  $filename" >> "$CHECKSUM_FILE"
            echo "  ✓ $filename"
        fi
    done
    
    echo "✅ Checksums generated and stored"
}

# Function to create implementation summary
create_summary() {
    echo ""
    echo "📋 Creating implementation summary..."
    
    cat > filing-system-implementation.log << 'EOF'
# Filing System Implementation Log

**Date**: 2025-08-23
**Status**: COMPLETE

## Actions Performed

1. ✅ Created directory structure
2. ✅ Moved system control documents to /00-system/
3. ✅ Secured design specifications in /01-design-specs/
4. ✅ Set up tracking system in /02-tracking/
5. ✅ Created working document templates in /03-working/
6. ✅ Established reference documents in /04-reference/
7. ✅ Generated checksums for immutable documents

## Directory Structure

```
docs/
├── 00-system/          [System Control]
├── 01-design-specs/    [Immutable Specs]
├── 02-tracking/        [Progress Tracking]
├── 03-working/         [Active Development]
└── 04-reference/       [Quick References]
```

## Next Steps

1. AI Agents should start with /00-system/REFERENCE-INDEX.md
2. Review /00-system/AI-AGENT-INSTRUCTIONS.md before development
3. Validate integrity using /00-system/DATA-INTEGRITY-RULES.md
4. Begin implementation following module dependency graph

## Validation

Run the following to verify setup:
```bash
ls -la docs/00-system/
ls -la docs/01-design-specs/
ls -la docs/02-tracking/
```
EOF
    
    echo "✅ Implementation summary created"
}

# Main execution
main() {
    echo "Starting filing system implementation..."
    echo ""
    
    create_directories
    setup_system_docs
    move_design_specs
    setup_tracking
    setup_working_docs
    setup_reference_docs
    generate_checksums
    create_summary
    
    echo ""
    echo "========================================="
    echo "✅ Filing System Implementation Complete!"
    echo "========================================="
    echo ""
    echo "📍 Start Point for AI Agents:"
    echo "   /docs/00-system/REFERENCE-INDEX.md"
    echo ""
    echo "📊 Current Status:"
    echo "   - System documents: Ready"
    echo "   - Design specs: Secured (immutable)"
    echo "   - Tracking system: Initialized"
    echo "   - Working documents: Templates created"
    echo "   - Reference guides: Available"
    echo ""
    echo "🚀 Ready for DevDocAI v3.6.0 development!"
}

# Run main function
main