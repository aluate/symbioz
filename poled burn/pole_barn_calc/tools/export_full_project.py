"""Export entire project structure to a single markdown file for review."""

import sys
from pathlib import Path
import os

def get_directory_tree(root_path, max_depth=3, prefix="", ignore_dirs=None):
    """Generate directory tree structure."""
    if ignore_dirs is None:
        ignore_dirs = {".git", "__pycache__", ".pytest_cache", "dist", "build", ".venv", "venv"}
    
    lines = []
    items = sorted([item for item in root_path.iterdir() if item.name not in ignore_dirs])
    
    for i, item in enumerate(items):
        is_last = i == len(items) - 1
        current_prefix = "└── " if is_last else "├── "
        lines.append(f"{prefix}{current_prefix}{item.name}")
        
        if item.is_dir() and max_depth > 0:
            extension = "    " if is_last else "│   "
            lines.extend(get_directory_tree(item, max_depth - 1, prefix + extension, ignore_dirs))
    
    return lines

def read_file_safe(file_path):
    """Read file with error handling."""
    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except Exception as e:
        return f"# Error reading file: {e}\n"

def export_full_project():
    """Export entire project to markdown."""
    project_root = Path(__file__).parent.parent
    output_file = project_root / "PROJECT_EXPORT_FULL.md"
    
    # Files to include
    code_files = [
        "systems/pole_barn/model.py",
        "systems/pole_barn/geometry.py",
        "systems/pole_barn/assemblies.py",
        "systems/pole_barn/pricing.py",
        "systems/pole_barn/calculator.py",
        "apps/gui.py",
        "apps/cli.py",
    ]
    
    config_files = [
        "config/parts.example.csv",
        "config/pricing.example.csv",
        "config/assemblies.example.csv",
    ]
    
    doc_files = [
        "README.md",
        "NEXT_STEPS.md",
        "GUI_CHANGELOG.md",
        "PRICING_CALIBRATION.md",
        "ASSEMBLIES_DESIGN.md",
        "ASSEMBLIES_STATUS.md",
        "control/pole_barn_calculator.md",
    ]
    
    test_files = [
        "tests/test_geometry.py",
        "tests/test_assemblies.py",
        "tests/test_pricing.py",
        "tests/test_end_to_end.py",
    ]
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# Pole Barn Calculator - Full Project Export\n\n")
        f.write("This document contains the complete project structure and code for review.\n\n")
        f.write("**Generated:** " + str(Path(__file__).stat().st_mtime) + "\n\n")
        f.write("---\n\n")
        
        # Directory Tree
        f.write("## Project Directory Tree\n\n")
        f.write("```\n")
        f.write(project_root.name + "/\n")
        for line in get_directory_tree(project_root, max_depth=3):
            f.write(line + "\n")
        f.write("```\n\n")
        f.write("---\n\n")
        
        # Code Files
        f.write("## Core Code Files\n\n")
        for file_path in code_files:
            full_path = project_root / file_path
            if full_path.exists():
                f.write(f"### File: {file_path}\n\n")
                f.write("```python\n")
                f.write(read_file_safe(full_path))
                f.write("```\n\n")
                f.write("---\n\n")
        
        # Config Files
        f.write("## Configuration Files\n\n")
        for file_path in config_files:
            full_path = project_root / file_path
            if full_path.exists():
                f.write(f"### File: {file_path}\n\n")
                f.write("```csv\n")
                f.write(read_file_safe(full_path))
                f.write("```\n\n")
                f.write("---\n\n")
        
        # Documentation
        f.write("## Documentation Files\n\n")
        for file_path in doc_files:
            full_path = project_root / file_path
            if full_path.exists():
                f.write(f"### File: {file_path}\n\n")
                content = read_file_safe(full_path)
                # For markdown files, include as-is (not in code block)
                if file_path.endswith(".md"):
                    f.write(content)
                else:
                    f.write("```\n")
                    f.write(content)
                    f.write("```\n")
                f.write("\n---\n\n")
        
        # Test Files
        f.write("## Test Files\n\n")
        for file_path in test_files:
            full_path = project_root / file_path
            if full_path.exists():
                f.write(f"### File: {file_path}\n\n")
                f.write("```python\n")
                f.write(read_file_safe(full_path))
                f.write("```\n\n")
                f.write("---\n\n")
        
        f.write("\n## End of Export\n")
    
    print(f"Full project exported to: {output_file}")
    print(f"File size: {output_file.stat().st_size / 1024:.1f} KB")

if __name__ == "__main__":
    export_full_project()

