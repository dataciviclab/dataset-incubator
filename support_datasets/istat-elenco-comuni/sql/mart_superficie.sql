SELECT
    codice_istat,
    denominazione,
    superficie_km2,
    sigla_provincia,
    regione
FROM clean_input
ORDER BY codice_istat
