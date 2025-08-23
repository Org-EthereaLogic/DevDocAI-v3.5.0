# 02-Architecture Documentation

## Overview

This directory contains technical design and system architecture documentation for DevDocAI v3.5.0, defining how the system is built and structured.

## Documents

### [System Architecture](devdocai-v3.5-architecture.md)
**Purpose**: High-level technical architecture and system design overview.
**Audience**: Architects, senior developers, technical leads
**Key Sections**: Component architecture, data flow, integration points, technology stack

### [Software Design Document (SDD)](devdocai-v3.5-sdd.md)
**Purpose**: Detailed software design specifications and implementation patterns.
**Audience**: Developers, technical leads, architects
**Key Sections**: Module designs, class diagrams, sequence diagrams, design patterns

### [UI Mockups & Design](devdocai-v3.5-mockups.md)
**Purpose**: Visual design specifications and user interface mockups.
**Audience**: Frontend developers, UX designers, stakeholders
**Key Sections**: Screen layouts, UI components, interaction flows, design system

## Architecture Highlights

- **Modular Component System**: 13 core modules (M001-M013)
- **Memory Mode Architecture**: Adaptive performance based on hardware
- **MIAIR Engine**: Meta-Iterative AI Refinement for quality improvement
- **Multi-LLM Integration**: Support for Claude, ChatGPT, Gemini
- **Quality Gate System**: 85% quality threshold enforcement

## Reading Order

1. Start with **System Architecture** for overall design
2. Review **SDD** for implementation details
3. Check **Mockups** for UI/UX specifications

## Related Documentation

- [Requirements](../01-requirements/) - Business and functional requirements
- [API Documentation](../03-specifications/devdocai-v3.5-api-documentation.md) - Technical interfaces
- [Deployment Guide](../04-deployment/devdocai-v3.5-deployment-installation-guide.md) - System deployment

## Key Architectural Decisions

- **Dual License Model**: Apache-2.0 (Core) + MIT (Plugin SDK)
- **Plugin Architecture**: Ed25519 signed plugins with sandboxed execution
- **Security**: Argon2id encryption for local storage
- **Performance Targets**: <5s document generation, <30s AI enhancement

## Document Status

All architecture documents are currently **Active** and reflect the latest v3.5.0 design.