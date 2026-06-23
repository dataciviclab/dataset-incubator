-- Mart: ipa_enti
-- Tutte le colonne, senza filtri.
-- Serve come anagrafica completa per join con altri dataset.
-- I campi mail consentono di ricavare PEC e altri contatti per ente.

SELECT * FROM clean_input
ORDER BY denominazione_ente
