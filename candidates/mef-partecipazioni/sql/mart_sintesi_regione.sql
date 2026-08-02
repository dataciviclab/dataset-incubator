-- mart_sintesi_regione — Profilo partecipazioni per regione e categoria amministrazione
--
-- 1 riga = 1 (anno, regione, categoria): numero partecipazioni dichiarate,
-- amministrazioni distinte, partecipate distinte, % perimetro TUSP.
-- Risponde: il profilo per territorio (regione) e tipo (categoria) conferma
-- l'intuizione attesa? Dove si concentrano le partecipazioni?
--
-- PK: (anno, amministrazione_regione, amministrazione_categoria)

SELECT
    anno,
    amministrazione_regione_sede                                   AS amministrazione_regione,
    amministrazione_categoria,
    count(*)                                                       AS numero_partecipazioni,
    count(DISTINCT amministrazione_codice_fiscale)                 AS numero_amministrazioni,
    count(DISTINCT partecipata_codice_fiscale)                     AS numero_partecipate,
    round(100.0 * count(*) FILTER (WHERE appartenenza_perimetro_tusp = 'SI')
          / NULLIF(count(*), 0), 1)                                AS pct_perimetro_tusp,
    round(100.0 * count(*) FILTER (WHERE appartenenza_perimetro_revisione_periodica = 'SI')
          / NULLIF(count(*), 0), 1)                                AS pct_perimetro_revisione
FROM clean_input
WHERE amministrazione_regione_sede IS NOT NULL
GROUP BY anno, amministrazione_regione_sede, amministrazione_categoria
ORDER BY anno, amministrazione_regione_sede, numero_partecipazioni DESC
