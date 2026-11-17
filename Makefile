# Makefile — interfaccia del repo per la CI (ADR-001).
#
# Lo YAML non contiene logica: chiama solo questi target, che delegano al
# toolkit. Il batch arriva dal workflow condiviso, che scrive `batch.txt` con
# i dataset.yml da eseguire (solo i cambiati su PR, tutti su schedule/dispatch).

TOOLKIT ?= toolkit
BATCH ?= batch.txt

.PHONY: run-all run-batch

# `run-all` e `run-batch` fanno la stessa cosa: il batch lo decide il workflow
# che scrive batch.txt. `run-all` serve al ramo schedule/dispatch, `run-batch`
# a quello PR (il reusable risolve `run-batch-command` prima di `run-command`).
run-all: run-batch

# I candidate dipendono da fonti pubbliche instabili e un dataset rotto non deve
# bloccare il publish degli altri. `toolkit run --batch` esce 1 se qualcuno
# fallisce: qui l'errore viene riportato ma non propagato — il Batch Report
# sopra elenca i fallimenti e il resto viene comunque sincronizzato su GCS.
run-batch:
	@if [ ! -s "$(BATCH)" ]; then echo "batch vuoto — niente da eseguire"; exit 0; fi; \
	 $(TOOLKIT) run --batch "$(BATCH)" || \
	   echo "::warning title=Candidate falliti::alcuni dataset sono falliti (vedi Batch Report) — il publish prosegue"
