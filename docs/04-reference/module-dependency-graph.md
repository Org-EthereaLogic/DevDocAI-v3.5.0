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
