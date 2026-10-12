-- MinLavoro flussi — CLEAN
-- L'extract.py produce già schema long normalizzato; qui solo cast e pulizia.
-- Genere 'Totale' è riga di subtotale fonte: tenuta ma marcata.

SELECT
    normalize_string(fonte) AS fonte,
    normalize_string(tabella_id) AS tabella_id,
    normalize_string(tipo_flusso) AS tipo_flusso,
    cast_int(anno) AS anno,
    normalize_string(trimestre) AS trimestre,
    normalize_string(geo_level) AS geo_level,
    normalize_string(geo) AS geo,
    normalize_string(genere) AS genere,
    CASE
        WHEN normalize_string(genere) = 'Totale' THEN TRUE
        ELSE FALSE
    END AS is_totale_genere,
    normalize_string(tipologia_contratto) AS tipologia_contratto,
    normalize_string(settore) AS settore,
    normalize_string(classe_eta) AS classe_eta,
    normalize_string(motivo_cessazione) AS motivo_cessazione,
    normalize_string(durata_fascia) AS durata_fascia,
    normalize_string(qualifica) AS qualifica,
    normalize_string(indicatore) AS indicatore,
    cast_double(valore) AS valore
FROM raw_input
WHERE cast_double(valore) IS NOT NULL
  AND cast_int(anno) IS NOT NULL
