-- Clean: GSE Elenco CER — normalizzazione colonne, dedup, tipi
-- Macro toolkit: normalize_string, cast_int, normalize_italian_number
-- Il file sorgente è XLSX; toolkit legge con read_xlsx automaticamente.
-- Dedup: solo righe interamente identiche (stessa denominatione, stesso comune,
-- stessa potenza). Duplicati con coordinate o utenze diverse sono CER separate.
SELECT
    normalize_string("Denominazione Comunità") AS denominazione,
    normalize_italian_number("Potenza totale (kW)") AS potenza_kw,
    cast_int("Numero impianti") AS n_impianti,
    cast_int("Numero utenze") AS n_utenze,
    normalize_string("Comune") AS comune,
    upper(normalize_string("Provincia")) AS provincia,
    normalize_string("Regione") AS regione,
    normalize_italian_number("Latitudine") AS latitudine,
    normalize_italian_number("Longitudine") AS longitudine,
    normalize_string("Area_Convenzionale") AS area_convenzionale,
    normalize_string("Ragione_Sociale_GdR") AS distributore,
    strptime("Data di aggiornamento", '%d/%m/%Y') AS data_aggiornamento
FROM raw_input
QUALIFY row_number() OVER (
    PARTITION BY "Denominazione Comunità", "Comune", "Potenza totale (kW)",
                 "Numero impianti", "Numero utenze", "Latitudine", "Longitudine"
    ORDER BY "Area_Convenzionale"
) = 1
