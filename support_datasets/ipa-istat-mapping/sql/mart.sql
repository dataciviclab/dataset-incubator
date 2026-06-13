-- Mart: ipa_istat_mapping
-- Pass-through: tutto il clean, nessuna aggregazione

SELECT
    codice_istat,
    denominazione,
    regione,
    sigla_provincia,
    codice_regione,
    codice_catastale_istat,
    codice_ipa,
    codice_fiscale,
    denominazione_ipa,
    codice_categoria,
    codice_catastale_comune,
    codice_istat_ipa,
    acronimo,
    indirizzo,
    cap,
    sito_istituzionale
FROM clean_input
WHERE codice_istat IS NOT NULL
ORDER BY codice_istat
