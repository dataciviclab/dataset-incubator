-- Conto Annuale — Profilo Ente (CLEAN)
-- Una riga per ente con tutte le metriche: demografia, costo, assenze

WITH occupazione AS (
    SELECT
        anno, istituzione, desc_istituzione, codi_comparto, desc_comparto, codi_tipo_istituzione,
        SUM(COALESCE(tp_u, 0) + COALESCE(tp_d, 0)
          + COALESCE(pti_u, 0) + COALESCE(pti_d, 0)
          + COALESCE(pts_u, 0) + COALESCE(pts_d, 0)) AS dipendenti,
        SUM(COALESCE(tp_d, 0) + COALESCE(pti_d, 0) + COALESCE(pts_d, 0)) AS donne
    FROM read_parquet('https://storage.googleapis.com/dataciviclab-clean/conto-annuale/occupazione/{year}/occupazione_{year}_clean.parquet')
    GROUP BY 1, 2, 3, 4, 5, 6
),

eta AS (
    SELECT
        anno, istituzione, codi_comparto,
        SUM(COALESCE(uomini, 0) + COALESCE(donne, 0)) AS tot_persone,
        SUM((COALESCE(uomini, 0) + COALESCE(donne, 0)) *
            CASE fascia
                WHEN 'E0'  THEN 15 WHEN 'E20' THEN 22 WHEN 'E25' THEN 27
                WHEN 'E30' THEN 32 WHEN 'E35' THEN 37 WHEN 'E40' THEN 42
                WHEN 'E45' THEN 47 WHEN 'E50' THEN 52 WHEN 'E55' THEN 57
                WHEN 'E60' THEN 62 WHEN 'E65' THEN 67 WHEN 'E68' THEN 71
                ELSE 45
            END) AS somma_eta
    FROM read_parquet('https://storage.googleapis.com/dataciviclab-clean/conto-annuale/personale/{year}/personale_{year}_clean.parquet')
    GROUP BY 1, 2, 3
),

anzianita AS (
    SELECT
        anno, istituzione, codi_comparto,
        SUM(COALESCE(uomini, 0) + COALESCE(donne, 0)) AS tot_persone_anzianita,
        SUM((COALESCE(uomini, 0) + COALESCE(donne, 0)) *
            CASE fascia
                WHEN 'A0'  THEN 2.5 WHEN 'A6'  THEN 8  WHEN 'A11' THEN 13
                WHEN 'A16' THEN 18  WHEN 'A21' THEN 23 WHEN 'A26' THEN 28
                WHEN 'A31' THEN 33  WHEN 'A36' THEN 38 WHEN 'A41' THEN 42
                WHEN 'A44' THEN 47
                ELSE 15
            END) AS somma_anzianita
    FROM read_parquet('https://storage.googleapis.com/dataciviclab-clean/conto-annuale/anzianita/{year}/anzianita_{year}_clean.parquet')
    GROUP BY 1, 2, 3
),

titoli AS (
    SELECT
        anno, istituzione, codi_comparto,
        SUM(COALESCE(uomini, 0) + COALESCE(donne, 0)) AS tot_con_titolo,
        SUM(CASE WHEN titolo_studio IN ('LAUREA', 'LAUREA BREVE', 'SPECIALIZZAZIONE POST LAUREA / DOTTORATO DI RICERCA', 'ALTRI TITOLI POST LAUREA')
            THEN COALESCE(uomini, 0) + COALESCE(donne, 0) ELSE 0 END) AS laureati
    FROM read_parquet('https://storage.googleapis.com/dataciviclab-clean/conto-annuale/titoli_studio/{year}/titoli_studio_{year}_clean.parquet')
    GROUP BY 1, 2, 3
),

retribuzione AS (
    SELECT
        anno, istituzione, codi_comparto,
        MAX(codi_fiscale) AS codi_fiscale,
        ROUND(SUM(importo), 0) AS retribuzione_totale
    FROM read_parquet('https://storage.googleapis.com/dataciviclab-clean/conto-annuale/composizione_retribuzione/{year}/composizione_retribuzione_{year}_clean.parquet')
    GROUP BY 1, 2, 3
),

costo AS (
    SELECT
        anno, istituzione, codi_comparto,
        MAX(codi_fiscale) AS codi_fiscale,
        ROUND(SUM(totale_spesa), 0) AS costo_totale
    FROM read_parquet('https://storage.googleapis.com/dataciviclab-clean/conto-annuale/costo_lavoro/{year}/costo_lavoro_{year}_clean.parquet')
    GROUP BY 1, 2, 3
),

assenze AS (
    SELECT
        anno, istituzione, codi_comparto,
        MAX(codi_fiscale) AS codi_fiscale,
        ROUND(SUM(COALESCE(assenze_uomini, 0) + COALESCE(assenze_donne, 0)), 0) AS assenze_totali
    FROM read_parquet('https://storage.googleapis.com/dataciviclab-clean/conto-annuale/assenze/{year}/assenze_{year}_clean.parquet')
    GROUP BY 1, 2, 3
)

SELECT
    o.anno, o.istituzione, o.desc_istituzione,
    COALESCE(r.codi_fiscale, c.codi_fiscale, az.codi_fiscale) AS codi_fiscale,
    o.codi_comparto, o.desc_comparto, o.codi_tipo_istituzione,
    o.dipendenti, o.donne,
    -- NULL = dato non disponibile (nessun match nel dataset personale)
    ROUND(e.somma_eta / NULLIF(e.tot_persone, 0), 1) AS eta_media,
    ROUND(a.somma_anzianita / NULLIF(a.tot_persone_anzianita, 0), 1) AS anzianita_media,
    ROUND(t.laureati * 100.0 / NULLIF(t.tot_con_titolo, 0), 1) AS pct_laureati,
    r.retribuzione_totale,
    c.costo_totale,
    az.assenze_totali
FROM occupazione o
LEFT JOIN eta e ON o.istituzione = e.istituzione AND o.anno = e.anno AND o.codi_comparto = e.codi_comparto
LEFT JOIN anzianita a ON o.istituzione = a.istituzione AND o.anno = a.anno AND o.codi_comparto = a.codi_comparto
LEFT JOIN titoli t ON o.istituzione = t.istituzione AND o.anno = t.anno AND o.codi_comparto = t.codi_comparto
LEFT JOIN retribuzione r ON o.istituzione = r.istituzione AND o.anno = r.anno AND o.codi_comparto = r.codi_comparto
LEFT JOIN costo c ON o.istituzione = c.istituzione AND o.anno = c.anno AND o.codi_comparto = c.codi_comparto
LEFT JOIN assenze az ON o.istituzione = az.istituzione AND o.anno = az.anno AND o.codi_comparto = az.codi_comparto
