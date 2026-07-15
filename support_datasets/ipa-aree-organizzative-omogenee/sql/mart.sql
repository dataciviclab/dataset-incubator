-- Mart: ipa_aree_organizzative_omogenee
-- Pass-through: tutte le colonne clean senza filtri.
-- Serve come tabella dimensionale per raggruppare le UO per area organizzativa.

SELECT * FROM clean_input
ORDER BY denominazione_ente, denominazione_aoo
