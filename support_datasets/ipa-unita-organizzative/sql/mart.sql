-- Mart: ipa_unita_organizzative
-- Pass-through: tutte le colonne clean senza filtri.
-- Serve come tabella dimensionale per join con ipa_enti, dipendenti_pubblici,
-- anac_bandi_gara, siope_* e altri dataset con codice IPA.

SELECT * FROM clean_input
ORDER BY denominazione_ente, descrizione_uo
