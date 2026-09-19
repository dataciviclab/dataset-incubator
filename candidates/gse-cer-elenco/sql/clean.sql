-- Clean: GSE Elenco CER — normalizzazione colonne, dedup, tipi
-- Il file sorgente è XLSX; toolkit legge con read_xlsx automaticamente.
-- Dedup: solo righe interamente identiche (stessa denominatione, stesso comune,
-- stessa potenza). Duplicati con coordinate o utenze diverse sono CER separate.
SELECT
    trim("Denominazione Comunità") AS denominazione,
    TRY_CAST(replace("Potenza totale (kW)", ',', '.') AS DOUBLE) AS potenza_kw,
    TRY_CAST("Numero impianti" AS INTEGER) AS n_impianti,
    TRY_CAST("Numero utenze" AS INTEGER) AS n_utenze,
    trim("Comune") AS comune,
    upper(trim("Provincia")) AS provincia,
    trim("Regione") AS regione,
    TRY_CAST(replace("Latitudine", ',', '.') AS DOUBLE) AS latitudine,
    TRY_CAST(replace("Longitudine", ',', '.') AS DOUBLE) AS longitudine,
    trim("Area_Convenzionale") AS area_convenzionale,
    trim("Ragione_Sociale_GdR") AS distributore,
    strptime("Data di aggiornamento", '%d/%m/%Y') AS data_aggiornamento
FROM raw_input
QUALIFY row_number() OVER (
    PARTITION BY "Denominazione Comunità", "Comune", "Potenza totale (kW)",
                 "Numero impianti", "Numero utenze", "Latitudine", "Longitudine"
    ORDER BY "Area_Convenzionale"
) = 1
