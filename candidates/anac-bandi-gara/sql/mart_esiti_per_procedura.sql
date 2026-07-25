-- ANAC: Esiti per tipo procedura e regione
-- Tasso di aggiudicazione per tipo scelta contraente e regione.
-- Quali procedure hanno piu' esiti positivi e quali no.
WITH base AS (
    SELECT
        anno_pubblicazione AS anno,
        sezione_regionale AS regione,
        oggetto_principale_contratto AS settore,
        tipo_scelta_contraente,
        CASE
            WHEN esito IN ('AGGIUDICATA', 'AGGIUDICATA EFFICACE', 'AGGIUDICATA EFFICACE - CONTRATTO STIPULATO',
                           'AGGIUDICATA - CONTRATTO STIPULATO', 'AGGIUDICAZIONE EFFICACE',
                           'AGGIUDICAZIONE EFFICACE - CONTRATTO STIPULATO')
                THEN 'aggiudicata'
            WHEN esito IN ('NON AGGIUDICATA', 'DESERTA', 'PROCEDURA DESERTA',
                           'NON AGGIUDICATA - NESSUNA OFFERTA', 'NON AGGIUDICATA - OFFERTE INAMMISSIBILI')
                THEN 'non_aggiudicata'
            WHEN esito IN ('ANNULLATA', 'CANCELLATA', 'REVOCATA')
                THEN 'annullata'
            ELSE 'altro'
        END AS macro_esito,
        importo_lotto
    FROM clean_input
    WHERE stato = 'ATTIVO'
      AND tipo_scelta_contraente IS NOT NULL
      AND sezione_regionale IS NOT NULL
)
SELECT
    anno,
    regione,
    settore,
    tipo_scelta_contraente,
    macro_esito,
    COUNT(*) AS n_lotti,
    ROUND(SUM(importo_lotto), 0) AS importo_totale,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY anno, regione, tipo_scelta_contraente), 2) AS quota_pct
FROM base
GROUP BY anno, regione, settore, tipo_scelta_contraente, macro_esito
ORDER BY anno DESC, regione, tipo_scelta_contraente, n_lotti DESC
