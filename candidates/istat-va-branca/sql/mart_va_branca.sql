-- Mart lungo: VA per regione × branca NACE × anno × valutazione
-- V = prezzi correnti · L_2020 = prezzi costanti base 2020

SELECT
    territorio_codice,
    territorio_nome,
    livello,
    anno,
    nace_codice,
    tipo_dato_codice,
    tipo_dato,
    valutazione_codice,
    valore_mln_eu
FROM clean_input
WHERE
    anno IS NOT NULL
    AND territorio_codice IS NOT NULL
    AND nace_codice IS NOT NULL
    AND tipo_dato_codice IS NOT NULL
    AND valutazione_codice IS NOT NULL
    AND valore_mln_eu IS NOT NULL
ORDER BY territorio_codice, anno, nace_codice, valutazione_codice
