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
