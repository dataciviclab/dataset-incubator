# Makefile — interfaccia del repo per la CI (ADR-001).
#
# Lo YAML non contiene logica: chiama solo questi target. I workflow condivisi
# usano `run-batch` (PR: batch.txt scritto dal detect) e `run-all`
# (schedule/dispatch: batch completo).

TOOLKIT ?= toolkit
PYTHON ?= python3
BATCH ?= batch.txt
DATASET_DIRS := candidates support_datasets compose

.PHONY: check validate-structure test run run-all run-batch clean registry registry-write help

# Validazione config: preflight su ogni dataset.yml (fonte raggiungibile inclusa).
check:
	@for f in $$(find $(DATASET_DIRS) -name dataset.yml | sort); do \
		echo "→ $$f"; \
		$(TOOLKIT) run preflight --config "$$f" > /dev/null 2>&1 || exit 1; \
	done
	@echo "✅ All configs valid"

# Gate struttura+config strict: docs/candidate-standard.md.
validate-structure:
	$(PYTHON) scripts/validate_candidate_structure.py

test:
	$(PYTHON) -m pytest tests/ -q

run: run-all

# Batch completo: schedule/dispatch.
run-all:
	@find $(DATASET_DIRS) -name dataset.yml | sort > "$(BATCH)"
	@$(MAKE) run-batch

# Batch selettivo: su PR il file batch.txt lo scrive il workflow condiviso.
#
# I candidate dipendono da fonti pubbliche instabili e un dataset rotto non deve
# bloccare il publish degli altri. `toolkit run --batch` esce 1 se qualcuno
# fallisce: qui l'errore viene riportato ma non propagato — il Batch Report
# sopra elenca i fallimenti e il resto viene comunque sincronizzato su GCS.
run-batch:
	@if [ ! -s "$(BATCH)" ]; then echo "batch vuoto — niente da eseguire"; exit 0; fi; \
	 $(TOOLKIT) run --batch "$(BATCH)" || \
	   echo "::warning title=Candidate falliti::alcuni dataset sono falliti (vedi Batch Report) — il publish prosegue"

clean:
	rm -rf out/data/_runs out/data/probe out/data/raw out/data/clean out/data/mart out/data/cross .tmp/

registry:
	$(TOOLKIT) registry build

registry-write:
	$(TOOLKIT) registry build --write

help:
	@grep -E '^[a-zA-Z_-]+:' Makefile | sort
