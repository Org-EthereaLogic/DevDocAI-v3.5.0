#!/usr/bin/env python3
"""
DevDocAI v3.6.0 Filing System Integrity Validator
Version: 1.0.0
Date: August 23, 2025
Purpose: Validate filing system integrity and consistency
"""

import os
import re
import hashlib
import json
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import sys

class IntegrityValidator:
    """Main validator class for filing system integrity."""
    
    def __init__(self, base_path: str = "/workspaces/DevDocAI-v3.5.0/docs"):
        self.base_path = Path(base_path)
        self.errors = []
        self.warnings = []
        self.info = []
        
        # Define immutable paths
        self.immutable_paths = [
            self.base_path / "00-system",
            self.base_path / "01-design-specs"
        ]
        
        # Define required directories
        self.required_dirs = [
            "00-system",
            "01-design-specs", 
            "02-tracking",
            "02-tracking/module-progress",
            "02-tracking/daily-progress",
            "02-tracking/decision-log",
            "03-working",
            "03-working/current-sprint",
            "03-working/integration-notes",
            "03-working/validation-reports",
            "04-reference"
        ]
        
        # Reference patterns
        self.reference_pattern = re.compile(
            r'\[(SRC|IMPL|TEST|DEP|BLOCKS|REL):([A-Z0-9-]+)(#[\w-]+)?\]'
        )
        
        # Module IDs
        self.module_ids = [f"M{i:03d}" for i in range(1, 14)]
        
    def validate_all(self) -> bool:
        """Run all validation checks."""
        print("=" * 60)
        print("DevDocAI Filing System Integrity Validation")
        print("=" * 60)
        print()
        
        checks = [
            ("Directory Structure", self.check_directory_structure),
            ("Immutable Documents", self.check_immutable_documents),
            ("Document Naming", self.check_naming_conventions),
            ("Cross-References", self.validate_references),
            ("Progress Consistency", self.check_progress_consistency),
            ("Module Dependencies", self.validate_dependencies),
            ("Required Metadata", self.check_metadata),
            ("Orphaned Documents", self.check_orphaned_documents),
        ]
        
        all_passed = True
        for check_name, check_func in checks:
            print(f"🔍 Checking {check_name}...")
            passed = check_func()
            status = "✅ PASSED" if passed else "❌ FAILED"
            print(f"   {status}")
            all_passed = all_passed and passed
            print()
        
        self.generate_report()
        return all_passed
    
    def check_directory_structure(self) -> bool:
        """Validate required directory structure exists."""
        missing_dirs = []
        
        for dir_name in self.required_dirs:
            dir_path = self.base_path / dir_name
            if not dir_path.exists():
                missing_dirs.append(dir_name)
                self.errors.append(f"Missing required directory: {dir_name}")
        
        if missing_dirs:
            print(f"   ❌ Missing directories: {', '.join(missing_dirs)}")
            return False
        
        self.info.append("All required directories present")
        return True
    
    def check_immutable_documents(self) -> bool:
        """Verify immutable documents haven't been modified."""
        checksum_file = self.base_path / "00-system" / "document-checksums.txt"
        
        if not checksum_file.exists():
            self.warnings.append("Checksum file not found - cannot verify immutability")
            return True  # Warning, not error
        
        violations = []
        with open(checksum_file, 'r') as f:
            for line in f:
                if line.strip():
                    expected_hash, filename = line.strip().split('  ')
                    file_path = self.base_path / "01-design-specs" / filename
                    
                    if file_path.exists():
                        actual_hash = self.calculate_checksum(file_path)
                        if actual_hash != expected_hash:
                            violations.append(filename)
                            self.errors.append(
                                f"Immutable document modified: {filename}"
                            )
        
        if violations:
            print(f"   ❌ Modified immutable files: {', '.join(violations)}")
            return False
        
        self.info.append("All immutable documents unchanged")
        return True
    
    def calculate_checksum(self, filepath: Path) -> str:
        """Calculate SHA-256 checksum of a file."""
        sha256_hash = hashlib.sha256()
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    def check_naming_conventions(self) -> bool:
        """Validate file naming conventions."""
        patterns = {
            "01-design-specs": r'^DESIGN-[\w-]+\.md$',
            "02-tracking/module-progress": r'^M\d{3}-[\w-]+\.tracking\.md$',
            "02-tracking/decision-log": r'^ADR-\d{4}-[\w-]+\.md$',
            "02-tracking/daily-progress": r'^\d{4}-\d{2}-\d{2}-progress\.md$',
        }
        
        violations = []
        for path_pattern, regex in patterns.items():
            dir_path = self.base_path / path_pattern
            if dir_path.exists() and dir_path.is_dir():
                pattern = re.compile(regex)
                for file in dir_path.glob("*.md"):
                    if not pattern.match(file.name):
                        violations.append(f"{path_pattern}/{file.name}")
                        self.errors.append(
                            f"Invalid naming convention: {path_pattern}/{file.name}"
                        )
        
        if violations:
            print(f"   ❌ Files with invalid names: {len(violations)}")
            return False
        
        self.info.append("All files follow naming conventions")
        return True
    
    def validate_references(self) -> bool:
        """Validate all cross-references point to valid targets."""
        invalid_refs = []
        
        # Scan all markdown files for references
        for md_file in self.base_path.glob("**/*.md"):
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            matches = self.reference_pattern.findall(content)
            for ref_type, target, anchor in matches:
                if not self.validate_single_reference(ref_type, target, anchor):
                    invalid_refs.append(f"{ref_type}:{target}{anchor or ''}")
                    self.warnings.append(
                        f"Invalid reference in {md_file.name}: "
                        f"[{ref_type}:{target}{anchor or ''}]"
                    )
        
        if invalid_refs:
            print(f"   ⚠️  Invalid references found: {len(invalid_refs)}")
            return True  # Warning, not failure
        
        self.info.append("All references valid")
        return True
    
    def validate_single_reference(self, ref_type: str, target: str, 
                                 anchor: Optional[str]) -> bool:
        """Validate a single reference."""
        # Check if target document/module exists
        if ref_type == "SRC":
            # Check design specs
            design_files = list(self.base_path.glob("01-design-specs/DESIGN-*.md"))
            design_names = [f.stem for f in design_files]
            if not any(target in name for name in design_names):
                return False
                
        elif ref_type in ["IMPL", "DEP", "BLOCKS"]:
            # Check module references
            if not target.startswith("M") or target not in self.module_ids:
                return False
                
        elif ref_type == "TEST":
            # Check test case format
            if not re.match(r'^TC-\d{3}', target):
                return False
        
        return True
    
    def check_progress_consistency(self) -> bool:
        """Validate progress percentages are logically consistent."""
        inconsistencies = []
        
        module_dir = self.base_path / "02-tracking" / "module-progress"
        if not module_dir.exists():
            self.warnings.append("Module progress directory not found")
            return True
        
        for tracking_file in module_dir.glob("*.tracking.md"):
            with open(tracking_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract progress percentages using regex
            design_match = re.search(r'Design:.*?(\d+)%', content)
            code_match = re.search(r'Code:.*?(\d+)%', content)
            test_match = re.search(r'Tests?:.*?(\d+)%', content)
            
            if design_match and code_match and test_match:
                design = int(design_match.group(1))
                code = int(code_match.group(1))
                test = int(test_match.group(1))
                
                # Validate logical constraints
                if design < code:
                    inconsistencies.append(
                        f"{tracking_file.name}: Code ({code}%) > Design ({design}%)"
                    )
                    self.errors.append(
                        f"Progress inconsistency in {tracking_file.name}: "
                        f"Code cannot exceed design"
                    )
                
                if code < test:
                    inconsistencies.append(
                        f"{tracking_file.name}: Tests ({test}%) > Code ({code}%)"
                    )
                    self.errors.append(
                        f"Progress inconsistency in {tracking_file.name}: "
                        f"Tests cannot exceed code"
                    )
                
                if code == 0 and test > 0:
                    inconsistencies.append(
                        f"{tracking_file.name}: Tests without code"
                    )
                    self.errors.append(
                        f"Progress inconsistency in {tracking_file.name}: "
                        f"Cannot have tests without code"
                    )
        
        if inconsistencies:
            print(f"   ❌ Progress inconsistencies: {len(inconsistencies)}")
            return False
        
        self.info.append("Progress tracking is consistent")
        return True
    
    def validate_dependencies(self) -> bool:
        """Check for circular dependencies and validate dependency graph."""
        dependency_graph = {
            "M001": [],
            "M002": ["M001"],
            "M003": ["M002", "M008"],
            "M004": ["M002", "M008"],
            "M005": ["M002"],
            "M006": ["M004", "M005"],
            "M007": ["M003", "M008"],
            "M008": ["M001"],
            "M009": ["M003", "M008"],
            "M010": ["M002"],
            "M011": ["M004", "M006"],
            "M012": ["M002"],
            "M013": ["M004"],
        }
        
        # Check for circular dependencies
        def has_cycle(graph):
            visited = set()
            rec_stack = set()
            
            def visit(node):
                if node in rec_stack:
                    return True
                if node in visited:
                    return False
                
                visited.add(node)
                rec_stack.add(node)
                
                for neighbor in graph.get(node, []):
                    if visit(neighbor):
                        return True
                
                rec_stack.remove(node)
                return False
            
            for node in graph:
                if node not in visited:
                    if visit(node):
                        return True
            return False
        
        if has_cycle(dependency_graph):
            self.errors.append("Circular dependency detected in module graph")
            print("   ❌ Circular dependencies found")
            return False
        
        self.info.append("No circular dependencies detected")
        return True
    
    def check_metadata(self) -> bool:
        """Verify required metadata in tracking documents."""
        missing_metadata = []
        
        tracking_dir = self.base_path / "02-tracking"
        if not tracking_dir.exists():
            return True
        
        required_fields = [
            "document_id", "document_type", "version", 
            "last_updated", "status"
        ]
        
        for md_file in tracking_dir.glob("**/*.tracking.md"):
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for metadata section
            if "---" in content:
                # Extract metadata section
                parts = content.split("---")
                if len(parts) >= 3:
                    metadata_text = parts[1]
                    for field in required_fields:
                        if field not in metadata_text:
                            missing_metadata.append(
                                f"{md_file.name}: missing {field}"
                            )
                            self.warnings.append(
                                f"Missing metadata field '{field}' in {md_file.name}"
                            )
        
        if missing_metadata:
            print(f"   ⚠️  Documents with missing metadata: {len(missing_metadata)}")
            return True  # Warning, not failure
        
        self.info.append("All required metadata present")
        return True
    
    def check_orphaned_documents(self) -> bool:
        """Check for orphaned documents not referenced anywhere."""
        orphaned = []
        
        # Get all markdown files
        all_files = set()
        for md_file in self.base_path.glob("**/*.md"):
            rel_path = md_file.relative_to(self.base_path)
            all_files.add(str(rel_path))
        
        # Check which files are referenced
        referenced_files = set()
        for md_file in self.base_path.glob("**/*.md"):
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Look for file references
            for other_file in all_files:
                if other_file in content:
                    referenced_files.add(other_file)
        
        # Find orphaned files (excluding system files)
        system_files = {"00-system", "01-design-specs"}
        for file_path in all_files:
            if file_path not in referenced_files:
                # Check if it's a system file
                if not any(sys_dir in file_path for sys_dir in system_files):
                    orphaned.append(file_path)
                    self.warnings.append(f"Potentially orphaned document: {file_path}")
        
        if orphaned:
            print(f"   ⚠️  Potentially orphaned documents: {len(orphaned)}")
            return True  # Warning, not failure
        
        self.info.append("No orphaned documents found")
        return True
    
    def generate_report(self):
        """Generate validation report."""
        report_path = self.base_path / "validation-report.md"
        
        with open(report_path, 'w') as f:
            f.write("# Filing System Integrity Validation Report\n\n")
            f.write(f"**Date**: {datetime.now().isoformat()}\n")
            f.write(f"**Status**: {'PASS' if not self.errors else 'FAIL'}\n\n")
            
            f.write("## Summary\n\n")
            f.write(f"- Errors: {len(self.errors)}\n")
            f.write(f"- Warnings: {len(self.warnings)}\n")
            f.write(f"- Info: {len(self.info)}\n\n")
            
            if self.errors:
                f.write("## Errors (Must Fix)\n\n")
                for error in self.errors:
                    f.write(f"- ❌ {error}\n")
                f.write("\n")
            
            if self.warnings:
                f.write("## Warnings (Should Review)\n\n")
                for warning in self.warnings:
                    f.write(f"- ⚠️  {warning}\n")
                f.write("\n")
            
            if self.info:
                f.write("## Information\n\n")
                for info in self.info:
                    f.write(f"- ℹ️  {info}\n")
                f.write("\n")
            
            f.write("## Recommendations\n\n")
            if self.errors:
                f.write("1. Fix all errors before proceeding with development\n")
                f.write("2. Run validation again after fixes\n")
            else:
                f.write("1. Filing system is ready for use\n")
                f.write("2. Run validation regularly to maintain integrity\n")
        
        print(f"📄 Report saved to: {report_path}")


def main():
    """Main entry point."""
    validator = IntegrityValidator()
    
    print("🚀 Starting integrity validation...\n")
    
    if validator.validate_all():
        print("✅ All validation checks passed!")
        print("   Filing system is ready for DevDocAI v3.6.0 development")
        sys.exit(0)
    else:
        print("❌ Validation failed!")
        print("   Please review the report and fix issues before proceeding")
        sys.exit(1)


if __name__ == "__main__":
    main()