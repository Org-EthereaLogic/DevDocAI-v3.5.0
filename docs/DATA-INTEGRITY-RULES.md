# Data Integrity Rules for DevDocAI v3.6.0 Filing System

**Version:** 1.0.0  
**Date:** August 23, 2025  
**Purpose:** Enforce consistency and integrity across all project documentation  
**Status:** ACTIVE ENFORCEMENT

---

## 1. Immutability Enforcement

### Protected Documents

```yaml
IMMUTABLE_PATHS:
  - /docs/01-design-specs/DESIGN-*.md
  - /docs/00-system/*.md
  
PROTECTION_LEVEL: ABSOLUTE
MODIFICATION_ALLOWED: NEVER
EXCEPTION_PROCESS: NONE
```

### Checksum Verification

```python
# Verification algorithm for immutable documents
import hashlib

def verify_immutable_document(filepath, expected_checksum):
    """
    Verify document has not been modified.
    
    Args:
        filepath: Path to document
        expected_checksum: SHA-256 hash of original
        
    Returns:
        bool: True if unchanged, False if modified
        
    Raises:
        IntegrityError: If document has been modified
    """
    with open(filepath, 'rb') as f:
        actual_checksum = hashlib.sha256(f.read()).hexdigest()
    
    if actual_checksum != expected_checksum:
        raise IntegrityError(f"Document {filepath} has been modified!")
    
    return True
```

---

## 2. Reference Validation Rules

### Valid Reference Patterns

```regex
# Reference pattern validation
REFERENCE_PATTERN = r'\[(SRC|IMPL|TEST|DEP|BLOCKS|REL):([A-Z0-9-]+)(#[\w-]+)?\]'

# Examples of VALID references:
[SRC:DESIGN-srs#FR-001]     ✓
[IMPL:M001#parser]           ✓
[TEST:TC-001]                ✓
[DEP:M002]                   ✓

# Examples of INVALID references:
[SRC:design-srs#FR-001]      ✗ (lowercase)
[IMPL:Module1#parser]        ✗ (invalid module ID)
[TEST:test-001]              ✗ (incorrect format)
```

### Reference Target Validation

```python
def validate_reference(reference_string):
    """
    Validate that a reference points to an existing target.
    
    Rules:
    1. Target document must exist
    2. Section anchor must exist in target (if specified)
    3. No circular references allowed
    4. No orphaned references allowed
    """
    ref_type, target, anchor = parse_reference(reference_string)
    
    # Rule 1: Document exists
    if not document_exists(target):
        raise ValidationError(f"Target document {target} does not exist")
    
    # Rule 2: Anchor exists
    if anchor and not anchor_exists(target, anchor):
        raise ValidationError(f"Anchor {anchor} not found in {target}")
    
    # Rule 3: No circular references
    if creates_circular_reference(reference_string):
        raise ValidationError("Circular reference detected")
    
    return True
```

---

## 3. Progress Consistency Rules

### Logical Progress Constraints

```python
class ProgressValidator:
    """
    Enforce logical consistency in progress tracking.
    """
    
    @staticmethod
    def validate_module_progress(module_data):
        """
        Rules:
        1. Design % >= Code %
        2. Code % >= Test %
        3. No component > 100%
        4. No component < 0%
        5. If Code = 0%, Tests must = 0%
        6. If Design < 100%, Code must = 0%
        """
        design = module_data['design_percent']
        code = module_data['code_percent']
        test = module_data['test_percent']
        docs = module_data['docs_percent']
        
        # Rule 1: Design must lead
        assert design >= code, "Code cannot exceed design completion"
        
        # Rule 2: Tests follow code
        assert code >= test, "Tests cannot exceed code completion"
        
        # Rule 3 & 4: Valid percentages
        for value in [design, code, test, docs]:
            assert 0 <= value <= 100, f"Invalid percentage: {value}"
        
        # Rule 5: No tests without code
        if code == 0:
            assert test == 0, "Cannot have tests without code"
        
        # Rule 6: No code without complete design
        if design < 100:
            assert code == 0, "Cannot implement incomplete design"
        
        return True
```

### Status Transition Rules

```yaml
VALID_TRANSITIONS:
  PENDING:
    - IN_PROGRESS
    - BLOCKED
  IN_PROGRESS:
    - COMPLETE
    - BLOCKED
    - NEEDS_REVISION
  COMPLETE:
    - NEEDS_REVISION
  BLOCKED:
    - IN_PROGRESS
    - PENDING
  NEEDS_REVISION:
    - IN_PROGRESS

INVALID_TRANSITIONS:
  PENDING:
    - COMPLETE  # Must go through IN_PROGRESS
  COMPLETE:
    - PENDING   # Cannot uncomplete
    - BLOCKED   # Completed items cannot be blocked
```

---

## 4. Dependency Validation

### Dependency Graph Rules

```python
class DependencyValidator:
    """
    Validate module dependencies.
    """
    
    @staticmethod
    def validate_dependencies(dependency_graph):
        """
        Rules:
        1. No circular dependencies
        2. Dependencies must be declared before use
        3. Cannot depend on lower-priority modules
        4. Core modules (P0) cannot depend on optional (P2)
        """
        # Rule 1: Detect cycles
        if has_cycle(dependency_graph):
            raise ValidationError("Circular dependency detected")
        
        # Rule 2: Forward declaration only
        for module, deps in dependency_graph.items():
            for dep in deps:
                if not is_declared(dep):
                    raise ValidationError(f"{dep} not declared")
        
        # Rule 3 & 4: Priority constraints
        for module, deps in dependency_graph.items():
            module_priority = get_priority(module)
            for dep in deps:
                dep_priority = get_priority(dep)
                if dep_priority > module_priority:
                    raise ValidationError(
                        f"{module} (P{module_priority}) cannot depend on "
                        f"{dep} (P{dep_priority})"
                    )
        
        return True
```

### Module Completion Order

```yaml
COMPLETION_RULES:
  - Dependencies must be ≥50% complete before dependent module starts
  - Core modules (P0) must be complete before P1 modules reach 50%
  - Integration tests require all dependencies at 100%
```

---

## 5. Document Structure Validation

### Metadata Requirements

```yaml
REQUIRED_METADATA:
  ALL_DOCUMENTS:
    - document_id       # Unique identifier
    - document_type     # SPEC|TRACK|WORK|REF|LOG|RPT
    - version          # Semantic version
    - last_updated     # ISO-8601 timestamp
    - status           # Document status
    
  TRACKING_DOCUMENTS:
    - module_id        # M### format
    - implementation_status
      - design_percent
      - code_percent
      - test_percent
      - docs_percent
    - last_progress_update
    
  DESIGN_SPECIFICATIONS:
    - checksum         # SHA-256 hash
    - approval_status  # DRAFT|APPROVED|FINAL
```

### Naming Convention Validation

```python
import re

class NamingValidator:
    """
    Validate file naming conventions.
    """
    
    PATTERNS = {
        'design': r'^DESIGN-[\w-]+\.md$',
        'tracking': r'^M\d{3}-[\w-]+\.tracking\.md$',
        'adr': r'^ADR-\d{4}-[\w-]+\.md$',
        'progress': r'^\d{4}-\d{2}-\d{2}-progress\.md$',
    }
    
    @classmethod
    def validate_filename(cls, filepath, doc_type):
        """
        Validate filename matches expected pattern.
        """
        filename = os.path.basename(filepath)
        pattern = cls.PATTERNS.get(doc_type)
        
        if not pattern:
            raise ValidationError(f"Unknown document type: {doc_type}")
        
        if not re.match(pattern, filename):
            raise ValidationError(
                f"Invalid filename: {filename} "
                f"(expected pattern: {pattern})"
            )
        
        return True
```

---

## 6. Update Validation Rules

### Update Frequency Limits

```yaml
MINIMUM_UPDATE_INTERVALS:
  implementation-status-tracker.md: 1 hour
  module-tracking.md: 30 minutes
  daily-progress.md: 1 entry per day
  sprint-plan.md: 1 day
  
MAXIMUM_UPDATE_FREQUENCY:
  per_file: 10 updates per hour
  per_module: 50 updates per day
```

### Update Authorization

```python
class UpdateAuthorization:
    """
    Validate update permissions.
    """
    
    PERMISSIONS = {
        '/00-system/': 'READ_ONLY',
        '/01-design-specs/': 'READ_ONLY',
        '/02-tracking/': 'READ_WRITE',
        '/03-working/': 'READ_WRITE',
        '/04-reference/': 'READ_APPEND',
    }
    
    @classmethod
    def can_update(cls, filepath, operation='WRITE'):
        """
        Check if update is allowed.
        """
        for path_prefix, permission in cls.PERMISSIONS.items():
            if path_prefix in filepath:
                if permission == 'READ_ONLY':
                    return False
                if permission == 'READ_APPEND' and operation == 'WRITE':
                    return False
                return True
        return False
```

---

## 7. Cross-Document Consistency

### Synchronization Rules

```yaml
SYNCHRONIZATION_REQUIREMENTS:
  # When updating module tracking, also update:
  - implementation-status-tracker.md
  - daily-progress/YYYY-MM-DD-progress.md
  
  # When creating ADR, also update:
  - affected module tracking files
  - reference index
  
  # When completing module, also update:
  - dependent module tracking files
  - test plan status
  - integration notes
```

### Consistency Validation

```python
class ConsistencyValidator:
    """
    Validate cross-document consistency.
    """
    
    @staticmethod
    def validate_cross_references():
        """
        Ensure all cross-references are bidirectional where required.
        """
        all_refs = collect_all_references()
        
        for ref in all_refs:
            if ref.type in ['DEP', 'BLOCKS']:
                # These must be bidirectional
                reverse_ref = find_reverse_reference(ref)
                if not reverse_ref:
                    raise ValidationError(
                        f"Missing reverse reference for {ref}"
                    )
        
        return True
    
    @staticmethod
    def validate_progress_sync():
        """
        Ensure progress is synchronized across all tracking documents.
        """
        master_tracker = read_master_tracker()
        
        for module_id in master_tracker.modules:
            module_tracker = read_module_tracker(module_id)
            
            # Progress must match
            if master_tracker[module_id] != module_tracker.progress:
                raise ValidationError(
                    f"Progress mismatch for {module_id}"
                )
        
        return True
```

---

## 8. Data Recovery Rules

### Backup Requirements

```yaml
BACKUP_POLICY:
  frequency: Every 4 hours
  retention: 30 days
  location: .backup/
  
BACKUP_TRIGGERS:
  - Before major updates
  - After completing module
  - Before integration
  - On validation failure
```

### Recovery Procedures

```python
class RecoveryProcedure:
    """
    Data recovery procedures.
    """
    
    @staticmethod
    def recover_from_corruption(filepath):
        """
        Recovery steps:
        1. Detect corruption via checksum
        2. Find last valid backup
        3. Restore from backup
        4. Replay recent updates from log
        5. Validate recovered state
        """
        if is_immutable(filepath):
            # Immutable files: restore from original
            restore_from_original(filepath)
        else:
            # Mutable files: restore from backup
            backup = find_latest_valid_backup(filepath)
            restore_from_backup(filepath, backup)
            replay_updates_since(backup.timestamp)
        
        # Validate recovery
        validate_document(filepath)
        validate_cross_references(filepath)
        
        return True
```

---

## 9. Validation Automation

### Automated Checks

```bash
#!/bin/bash
# Automated validation script

# Run every 30 minutes via cron
*/30 * * * * /scripts/validate_integrity.sh

# Validation sequence
validate_integrity.sh:
  1. Check immutable document checksums
  2. Validate all references
  3. Check progress consistency
  4. Verify dependency graph
  5. Validate naming conventions
  6. Check for orphaned documents
  7. Verify backup freshness
  8. Generate validation report
```

### Validation Report Template

```markdown
# Integrity Validation Report

**Date**: YYYY-MM-DD HH:MM:SS
**Status**: [PASS|FAIL]

## Checksum Validation
- Files checked: ###
- Passed: ###
- Failed: ###

## Reference Validation
- Total references: ###
- Valid: ###
- Invalid: ###
- Orphaned: ###

## Progress Consistency
- Modules checked: 13
- Consistent: ###
- Inconsistent: ###

## Issues Found
1. [Issue description]
   - File: [filepath]
   - Type: [ERROR|WARNING]
   - Action: [Required action]

## Automatic Fixes Applied
- [List of automatic fixes]

## Manual Review Required
- [List of issues requiring manual intervention]
```

---

## 10. Enforcement Mechanisms

### Pre-Commit Hooks

```python
# .git/hooks/pre-commit
#!/usr/bin/env python3
"""
Pre-commit hook to enforce integrity rules.
"""

def pre_commit_check():
    """
    Prevent commits that violate integrity rules.
    """
    # Check 1: No modifications to immutable files
    immutable_modified = check_immutable_modifications()
    if immutable_modified:
        print(f"ERROR: Cannot modify immutable files: {immutable_modified}")
        return False
    
    # Check 2: Validate references
    invalid_refs = validate_all_references()
    if invalid_refs:
        print(f"ERROR: Invalid references found: {invalid_refs}")
        return False
    
    # Check 3: Progress consistency
    if not validate_progress_consistency():
        print("ERROR: Progress tracking inconsistent")
        return False
    
    # Check 4: Required metadata
    missing_metadata = check_required_metadata()
    if missing_metadata:
        print(f"ERROR: Missing metadata: {missing_metadata}")
        return False
    
    return True

if __name__ == "__main__":
    if not pre_commit_check():
        sys.exit(1)
```

### Continuous Validation

```yaml
# .github/workflows/integrity-check.yml
name: Integrity Validation

on:
  push:
    paths:
      - 'docs/**'
  pull_request:
    paths:
      - 'docs/**'
  schedule:
    - cron: '0 */4 * * *'  # Every 4 hours

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run integrity checks
        run: |
          python scripts/validate_integrity.py
          python scripts/validate_references.py
          python scripts/validate_progress.py
      - name: Generate report
        if: always()
        run: python scripts/generate_validation_report.py
      - name: Upload report
        uses: actions/upload-artifact@v2
        with:
          name: integrity-report
          path: validation-report.md
```

---

## Appendix: Quick Validation Commands

```bash
# Check specific document integrity
python -m validate.check_document docs/02-tracking/module-progress/M001-*.md

# Validate all references
grep -r "\[.*:.*\]" docs/ | python -m validate.references

# Check progress consistency
python -m validate.progress_sync

# Verify dependency graph
python -m validate.dependencies

# Full integrity check
make validate-all

# Recovery from backup
python -m recovery.restore --file <filepath> --timestamp <backup-time>
```

---

*End of Data Integrity Rules Document*