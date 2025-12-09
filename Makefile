# Makefile for PPak-INNERGY migration tasks
# Otto-friendly targets for running migration scripts

.PHONY: help ppak-migrate-latest innergy-sync-materials innergy-import-projects migration-health-check

# Default target
help:
	@echo "PPak-INNERGY Migration Makefile"
	@echo ""
	@echo "Available targets:"
	@echo "  ppak-migrate-latest      - Run ETL on latest PPak exports"
	@echo "  innergy-sync-materials   - Sync material library to INNERGY"
	@echo "  innergy-import-projects  - Import latest canonical projects to INNERGY"
	@echo "  migration-health-check   - Run health checks on migration"
	@echo ""
	@echo "Environment variables:"
	@echo "  PPAK_EXPORT_DIR          - Directory with PPak CSV exports"
	@echo "  MIGRATION_OUTPUT_DIR     - Directory for canonical output files"
	@echo "  MATERIAL_LIBRARY_MASTER   - Path to canonical material library"
	@echo "  INNERGY_API_KEY          - INNERGY API key"
	@echo "  INNERGY_API_BASE_URL     - INNERGY API base URL"

# Run PPak ETL migration
ppak-migrate-latest:
	@echo "Running PPak ETL migration..."
	@python -m integrations.ppak.etl.run_migration \
		--ppak-export-dir "$(PPAK_EXPORT_DIR)" \
		--output-dir "$(MIGRATION_OUTPUT_DIR)"

# Sync material library to INNERGY (dry-run by default)
innergy-sync-materials:
	@echo "Syncing material library to INNERGY (dry-run)..."
	@python -m integrations.innergy.sync_materials \
		--material-library "$(MATERIAL_LIBRARY_MASTER)" \
		--api-key "$(INNERGY_API_KEY)" \
		--api-url "$(INNERGY_API_BASE_URL)" \
		--dry-run

# Sync material library to INNERGY (live mode)
innergy-sync-materials-live:
	@echo "Syncing material library to INNERGY (LIVE MODE)..."
	@python -m integrations.innergy.sync_materials \
		--material-library "$(MATERIAL_LIBRARY_MASTER)" \
		--api-key "$(INNERGY_API_KEY)" \
		--api-url "$(INNERGY_API_BASE_URL)" \
		--no-dry-run

# Import projects to INNERGY (placeholder - implement when import script is ready)
innergy-import-projects:
	@echo "Importing projects to INNERGY..."
	@echo "TODO: Implement integrations.innergy.import_projects module"
	@echo "For now, use: python -m integrations.innergy.import_projects --canonical-file <file>"

# Run health checks (placeholder - implement when health check script is ready)
migration-health-check:
	@echo "Running migration health checks..."
	@echo "TODO: Implement integrations.canonical.health_check module"
	@echo "For now, use: python -m integrations.canonical.health_check --canonical-file <file>"

