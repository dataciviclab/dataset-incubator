-- MinLavoro agevolazioni — CLEAN
-- Esclude righe senza anno (tabelle cross-section senza serie storica:
-- altre_agevolazioni, obiettivi decontribuzione, contratti attivi detassazione).

SELECT
    normalize_string(tabella_id) AS tabella_id,
    normalize_string(tipo_agevolazione) AS tipo_agevolazione,
    normalize_string(regione) AS regione,
    normalize_string(mese) AS mese,
    normalize_string(settore) AS settore,
    normalize_string(tipologia_contratto) AS tipologia_contratto,
    normalize_string(categoria) AS categoria,
    normalize_string(indicatore) AS indicatore,
    cast_int(anno) AS anno,
    cast_double(valore) AS valore
FROM raw_input
WHERE cast_double(valore) IS NOT NULL
  AND cast_int(anno) IS NOT NULL
