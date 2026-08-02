-- mart_trend_anno — Evoluzione partecipazioni pubbliche per anno (multi-year)
--
-- 1 riga = 1 anno: totale partecipazioni dichiarate, amministrazioni distinte,
-- partecipate distinte, quota perimetro TUSP, delta vs anno precedente.
-- Risponde: il fenomeno cresce o cala nel tempo?
--
-- PK: (anno)

WITH per_anno AS (
    SELECT
        anno,
        count(*)                                          AS numero_partecipazioni,
        count(DISTINCT amministrazione_codice_fiscale)    AS numero_amministrazioni,
        count(DISTINCT partecipata_codice_fiscale)        AS numero_partecipate,
        round(100.0 * count(*) FILTER (WHERE appartenenza_perimetro_tusp = 'SI')
              / NULLIF(count(*), 0), 1)                   AS pct_perimetro_tusp
    FROM clean_input
    GROUP BY anno
)
SELECT
    anno,
    numero_partecipazioni,
    numero_amministrazioni,
    numero_partecipate,
    pct_perimetro_tusp,
    numero_partecipazioni - lag(numero_partecipazioni) OVER (ORDER BY anno)
        AS delta_partecipazioni,
    round(100.0 * (numero_partecipazioni - lag(numero_partecipazioni) OVER (ORDER BY anno))
          / NULLIF(lag(numero_partecipazioni) OVER (ORDER BY anno), 0), 2)
        AS variazione_pct
FROM per_anno
ORDER BY anno
