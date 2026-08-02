-- mart_top_amministrazioni — Amministrazioni con più partecipazioni
--
-- 1 riga = 1 amministrazione per anno: numero partecipazioni dichiarate,
-- partecipate distinte, settore/macrocategoria/categoria, regione sede.
-- Risponde: quali amministrazioni dichiarano più partecipazioni?
--
-- PK: (anno, amministrazione_codice_fiscale)

SELECT
    anno,
    amministrazione_codice_fiscale,
    amministrazione_denominazione,
    amministrazione_settore_istituzionale,
    amministrazione_macrocategoria,
    amministrazione_categoria,
    amministrazione_regione_sede                                  AS amministrazione_regione,
    count(*)                                                      AS numero_partecipazioni,
    count(DISTINCT partecipata_codice_fiscale)                    AS numero_partecipate,
    round(100.0 * count(*) FILTER (WHERE appartenenza_perimetro_tusp = 'SI')
          / NULLIF(count(*), 0), 1)                               AS pct_perimetro_tusp
FROM clean_input
GROUP BY
    anno,
    amministrazione_codice_fiscale,
    amministrazione_denominazione,
    amministrazione_settore_istituzionale,
    amministrazione_macrocategoria,
    amministrazione_categoria,
    amministrazione_regione_sede
ORDER BY anno, numero_partecipazioni DESC
