-- Assenze scomposte per causale e comparto
WITH assenze_per_comparto AS (
    SELECT
        anno, codi_comparto, desc_comparto,
        causale_assenza, tipo_causale, descrizione_causale,
        ROUND(SUM(COALESCE(assenze_uomini, 0) + COALESCE(assenze_donne, 0)), 0) AS tot_assenze
    FROM read_parquet('https://storage.googleapis.com/dataciviclab-clean/conto-annuale/assenze/{year}/assenze_{year}_clean.parquet')
    GROUP BY 1, 2, 3, 4, 5, 6
),
dipendenti_per_comparto AS (
    SELECT
        anno, codi_comparto,
        SUM(COALESCE(tp_u, 0) + COALESCE(tp_d, 0)
          + COALESCE(pti_u, 0) + COALESCE(pti_d, 0)
          + COALESCE(pts_u, 0) + COALESCE(pts_d, 0)) AS dipendenti
    FROM read_parquet('https://storage.googleapis.com/dataciviclab-clean/conto-annuale/occupazione/{year}/occupazione_{year}_clean.parquet')
    GROUP BY 1, 2
)
SELECT
    a.anno,
    a.codi_comparto,
    a.desc_comparto,
    a.causale_assenza,
    a.tipo_causale,
    a.descrizione_causale,
    a.tot_assenze,
    ROUND(o.dipendenti, 0) AS tot_dipendenti,
    ROUND(a.tot_assenze / NULLIF(o.dipendenti, 0), 1) AS giorni_procapite
FROM assenze_per_comparto a
LEFT JOIN dipendenti_per_comparto o ON a.codi_comparto = o.codi_comparto AND a.anno = o.anno
WHERE a.tot_assenze > 0
ORDER BY a.anno DESC, giorni_procapite DESC
