# App Workflow Guide

This document contains standing rules and procedures that must be followed during development and testing.

---

## 🔐 Standing Rule: CSV Schema Consistency Requirement

**Apply Before Any Code Changes**

Whenever implementing any change request in this project, always perform the following steps *before* modifying code:

1. **Scan all CSV loader functions**, including:
   - `pricing.py` → `load_parts()`, `load_pricing()`, `load_assemblies()`
   - Any additional CSV loaders added in the future

2. Identify the **required column names** for each CSV file.

3. Open all CSV files in `/config/`, including:
   - `parts.example.csv`
   - `pricing.example.csv`
   - `assemblies.example.csv`
   - Any non-example `.csv` files present

4. If any required column is missing or misnamed, perform an automatic fix:
   - Add the missing column(s) with reasonable placeholder values
   - Ensure header names exactly match loader expectations
   - Do not remove or rename existing columns unless explicitly instructed

5. After updating CSVs, ensure:
   - All tests in `tests/` reflect the correct schema
   - No loader produces an error when importing the CSVs
   - Running `python -m apps.gui` does not produce schema-related errors

6. Only after all schema mismatches have been corrected may you proceed with implementing the requested feature.

### ⚠️ Why this rule exists:

This project uses multiple config files with multiple dependent loaders. Schema mismatches can easily break the GUI, CLI, tests, or exe packaging. This standing rule ensures stability during iterative development.

### 📝 When to apply:

- Before implementing any feature change
- Before modifying CSV loaders
- Before adding new CSV files
- Before running tests after code changes
- When encountering CSV-related errors

---

## Development Workflow

### Testing Round Workflow

1. **Collect Changes**: Add entries to `GUI_CHANGELOG.md` during testing
2. **Review Changelog**: Review all collected changes before implementation
3. **Apply Standing Rules**: Check CSV schemas and other standing requirements
4. **Implement Batch**: Implement all changes in the changelog
5. **Test**: Verify all changes work together
6. **Clear Changelog**: Archive or clear changelog for next round

### Before Each Implementation Batch

1. Read `GUI_CHANGELOG.md` for all pending changes
2. Review `APP_WORKFLOW_GUIDE.md` for standing rules
3. Check CSV schema consistency (see standing rule above)
4. Verify tests pass before making changes
5. Implement changes
6. Verify tests pass after changes
7. Test GUI manually if applicable

---

*Last Updated: Testing Round 1*

