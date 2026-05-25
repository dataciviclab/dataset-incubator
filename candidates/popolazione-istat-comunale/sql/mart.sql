-- Mart SQL placeholder for Popolazione ISTAT Comunale
-- Questo file può contenere query di aggregazione per il data mart.

SELECT
    anno,
    codice_comune,
    nome_comune,
    popolazione_totale,
    maschi,
    femmine
FROM
    clean_input;