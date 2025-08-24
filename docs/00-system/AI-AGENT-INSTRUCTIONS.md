# AI Agent Operating Instructions for DevDocAI v3.6.0

**Version:** 1.0.0  
**Date:** August 23, 2025  
**Purpose:** Operational guidelines for AI Agents working on DevDocAI development  
**Classification:** System Control Document

---

## 1. Primary Directives

### Core Principles

1. **Source of Truth**: Design specifications in `/docs/01-design-specs/` are IMMUTABLE and represent absolute truth
2. **Progress Tracking**: Update tracking documents after EVERY task completion
3. **Validation First**: Validate all references and dependencies before implementation
4. **Documentation Driven**: Read specifications before writing any code
5. **Consistency**: Maintain consistency across all documents and code

---

## 2. Document Access Hierarchy

### Read Priority (Top to Bottom)

```
1. /docs/00-system/REFERENCE-INDEX.md     # Start here for navigation
2. /docs/01-design-specs/DESIGN-*.md      # Source of truth
3. /docs/02-tracking/*.tracking.md        # Current progress
4. /docs/04-reference/*.md                # Quick lookups
5. /docs/03-working/*.md                  # Active work items
```

### Write Permissions

| Directory | Permission | When to Write |
|-----------|------------|---------------|
| `/00-system/` | READ ONLY | Never |
| `/01-design-specs/` | READ ONLY | Never |
| `/02-tracking/` | READ/WRITE | After task completion |
| `/03-working/` | READ/WRITE | During active development |
| `/04-reference/` | READ/APPEND | When adding new references |

---

## 3. Task Execution Protocol

### Before Starting Any Task

```markdown
CHECKLIST:
□ Read relevant design specification
□ Check current implementation status
□ Verify dependencies are complete
□ Check for blockers
□ Create/update sprint plan entry
```

### During Task Execution

```markdown
REQUIREMENTS:
- Follow design specifications exactly
- Maintain code comments referencing spec sections
- Update progress every 2 hours or at logical breakpoints
- Log any deviations or blockers immediately
```

### After Task Completion

```markdown
UPDATE SEQUENCE:
1. Update module tracking file (% complete)
2. Add entry to daily progress log
3. Update master implementation tracker
4. Add test references if applicable
5. Update any dependent module trackers
```

---

## 4. Reference Notation Guide

### How to Create References

```markdown
# In code comments:
// [SRC:DESIGN-srs#FR-001] Implements user authentication requirement

# In tracking documents:
Status: 50% complete [IMPL:M001#auth-module]

# In test files:
// [TEST:TC-001] Validates login functionality per [SRC:DESIGN-srs#FR-001]
```

### Reference Types to Use

| Scenario | Reference Type | Example |
|----------|---------------|---------|
| Implementing a requirement | `[SRC:]` | `[SRC:DESIGN-srs#FR-001]` |
| Linking to implementation | `[IMPL:]` | `[IMPL:M001#parser]` |
| Referencing a test | `[TEST:]` | `[TEST:TC-001]` |
| Showing dependency | `[DEP:]` | `[DEP:M002]` |
| Indicating blocker | `[BLOCKS:]` | `[BLOCKS:M003]` |

---

## 5. Module Implementation Guide

### Module Start Checklist

```markdown
For Module M###:
1. □ Read DESIGN-devdocsai-sdd.md section for module
2. □ Read DESIGN-devdocsai-architecture.md for interfaces
3. □ Check module dependency graph
4. □ Review test plan for module
5. □ Create module tracking file
6. □ Initialize progress metrics
```

### Component Implementation Order

```markdown
For each component:
1. Core data structures
2. Internal utilities
3. Public interfaces
4. Integration points
5. Error handling
6. Tests
7. Documentation
```

---

## 6. Progress Tracking Rules

### Percentage Calculation

```python
# Use this formula for progress calculation:
design_complete = 100  # Always 100% for existing specs
code_complete = (implemented_functions / total_functions) * 100
test_complete = (passing_tests / total_tests) * 100
docs_complete = (documented_functions / total_functions) * 100

overall = (design_complete * 0.2 + 
          code_complete * 0.4 + 
          test_complete * 0.3 + 
          docs_complete * 0.1)
```

### Status Indicators

```markdown
⏳ PENDING: Not started (0%)
🚧 IN PROGRESS: Active development (1-99%)
✅ COMPLETE: Fully implemented and tested (100%)
🔄 NEEDS REVISION: Requires changes
🚫 BLOCKED: Cannot proceed
```

---

## 7. Decision Logging

### When to Create an ADR (Architecture Decision Record)

- Choosing between multiple valid implementation approaches
- Deviating from original design (with justification)
- Selecting third-party libraries or tools
- Defining new interfaces or protocols
- Resolving design ambiguities

### ADR Template

```markdown
# ADR-####: [Title]

## Status
[PROPOSED | ACCEPTED | DEPRECATED | SUPERSEDED]

## Context
[What is the issue that we're seeing that is motivating this decision?]

## Decision
[What is the change that we're proposing/doing?]

## Consequences
[What becomes easier or more difficult because of this change?]

## References
- [SRC:DESIGN-spec#section]
- [REL:ADR-previous]
```

---

## 8. Quality Gates

### Before Marking Component Complete

```markdown
MUST SATISFY ALL:
□ Code matches design specification
□ All tests pass (100% of defined tests)
□ Code coverage ≥ 80% for non-UI code
□ Documentation complete
□ No unresolved TODOs
□ Cross-references added
□ Integration tests pass
```

### Module Completion Criteria

```markdown
REQUIREMENTS:
□ All components complete
□ Integration tests pass
□ Performance benchmarks met
□ Security review passed
□ Documentation reviewed
□ Demo prepared
```

---

## 9. Communication Patterns

### Blocker Reporting

```markdown
## Blocker Report Template

**Blocker ID**: BLK-####
**Module**: M###
**Severity**: [LOW|MEDIUM|HIGH|CRITICAL]
**Description**: [Clear description of the issue]
**Impact**: [What is blocked]
**Proposed Solution**: [If any]
**Dependencies**: [DEP:M###]
**Estimated Resolution**: [Date/Time]
```

### Progress Updates

```markdown
## Daily Progress Template

**Date**: YYYY-MM-DD
**Agent**: [AI-AGENT-ID]

### Completed Today
- [x] Task description [IMPL:M###] (##%)

### In Progress
- [ ] Task description [IMPL:M###] (##%)

### Planned Tomorrow
- [ ] Task description [Target: ##%]

### Blockers
- [If any, reference BLK-####]
```

---

## 10. Code Standards Alignment

### File Headers

```python
"""
Module: M### - [Module Name]
Component: [Component Name]
Reference: [SRC:DESIGN-sdd#section]
Dependencies: [DEP:M###, DEP:M###]

Description: [Brief description]
"""
```

### Function Documentation

```python
def function_name(params):
    """
    Brief description.
    
    Reference: [SRC:DESIGN-spec#requirement]
    Test: [TEST:TC-###]
    
    Args:
        params: Description
        
    Returns:
        Description
        
    Raises:
        Exception: When...
    """
```

---

## 11. Testing Protocol

### Test File Organization

```
tests/
├── unit/
│   └── M###_module_name/
│       ├── test_component.py
│       └── test_integration.py
├── integration/
│   └── test_M###_M###_integration.py
└── e2e/
    └── test_feature_flow.py
```

### Test Documentation

```python
def test_feature():
    """
    Test: TC-### - [Test Name]
    Requirement: [SRC:DESIGN-srs#FR-###]
    Module: [IMPL:M###]
    
    Validates: [What is being validated]
    """
```

---

## 12. Emergency Procedures

### On Specification Ambiguity

1. Check traceability matrix for clarification
2. Review related specifications
3. Check ADRs for previous decisions
4. Create ADR for interpretation
5. Proceed with most conservative interpretation

### On Integration Failure

1. Document failure in module tracking
2. Create blocker report
3. Check dependency status
4. Review interface specifications
5. Update integration notes

### On Test Failure

1. Verify test matches specification
2. Check if specification has changed
3. Review implementation against design
4. Document discrepancy
5. Create ADR if design change needed

---

## Quick Command Reference

```bash
# Find requirement
grep -r "FR-001" docs/01-design-specs/

# Update progress
echo "Progress: 45%" >> docs/02-tracking/module-progress/M001-*.tracking.md

# Check dependencies
grep "DEP:" docs/02-tracking/module-progress/*.md

# Find TODOs
grep -r "TODO" src/

# Run module tests
pytest tests/unit/M001*/

# Validate references
python scripts/validate_references.py
```

---

## Appendix: Module Quick Reference

| Module | Primary Spec | Key Dependencies | Priority |
|--------|-------------|------------------|----------|
| M001 | Config Manager | None | P0 |
| M002 | Storage System | M001 | P0 |
| M003 | MIAIR Engine | M002, M008 | P1 |
| M004 | Doc Generator | M002, M008 | P0 |
| M005 | Tracking Matrix | M002 | P0 |
| M006 | Suite Manager | M004, M005 | P0 |
| M007 | Review Engine | M003, M008 | P0 |
| M008 | LLM Adapter | M001 | P1 |
| M009 | Enhancement | M003, M008 | P1 |
| M010 | SBOM Generator | M002 | P2 |
| M011 | Batch Ops | M004, M006 | P1 |
| M012 | Version Control | M002 | P1 |
| M013 | Template Market | M004 | P2 |

---

*End of AI Agent Instructions*