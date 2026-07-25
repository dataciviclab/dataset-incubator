-- ANAC: Trend annuale per settore (LAVORI/FORNITURE/SERVIZI)
-- Variazione % annua degli importi per settore e regione.
-- Individua settori in crescita o contrazione.
WITH settori_anno AS (
    SELECT
        anno_pubblicazione AS anno,
        sezione_regionale AS regione,
        oggetto_principale_contratto AS settore,
        COUNT(*) AS n_lotti,
        ROUND(SUM(importo_lotto), 0) AS importo_totale
    FROM clean_input
    WHERE stato = 'ATTIVO'
      AND sezione_regionale IS NOT NULL
    GROUP BY anno_pubblicazione, sezione_regionale, oggetto_principale_contratto
)
SELECT
    anno,
    regione,
    settore,
    n_lotti,
    importo_totale,
    -- variazione % rispetto all'anno precedente (per regione-settore)
    ROUND((importo_totale - LAG(importo_totale) OVER (PARTITION BY regione, settore ORDER BY anno))
        * 100.0 / NULLIF(LAG(importo_totale) OVER (PARTITION BY regione, settore ORDER BY anno), 0), 2)
        AS var_pct_anno_prec,
    -- quota del settore sul totale regionale
    ROUND(importo_totale * 100.0 / NULLIF(SUM(importo_totale) OVER (PARTITION BY anno, regione), 0), 2)
        AS quota_pct_su_regione
FROM settori_anno
ORDER BY anno DESC, regione, importo_totale DESC
