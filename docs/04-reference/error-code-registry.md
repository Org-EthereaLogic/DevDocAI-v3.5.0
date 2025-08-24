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
