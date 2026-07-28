-- Mart: voti per lista aggregati per territorio
-- Ogni riga: tipo_elezione × provincia/regione × lista × anno
--
-- Colonne:
--   data_elezione, tipo_elezione, anno,
--   regione, provincia (NULL per aggregati regionali),
--   lista, voti_lista, totale_voti_validi,
--   pct_voti (quota % della lista),
--   rank_lista (posizione in provincia),
--   voti_primo, voti_secondo (per concentrazione)

WITH voti_per_lista AS (
    SELECT
        data_elezione,
        tipo_elezione,
        EXTRACT(YEAR FROM data_elezione) AS anno,
        regione,
        provincia,
        lista,
        SUM(voti_lista) AS voti_lista
    FROM clean_input
    WHERE voti_lista IS NOT NULL AND lista IS NOT NULL
    GROUP BY data_elezione, tipo_elezione, regione, provincia, lista
),

-- Totali per provincia×tornata
totali_provincia AS (
    SELECT
        data_elezione,
        tipo_elezione,
        regione,
        provincia,
        SUM(voti_lista) AS totale_voti_validi
    FROM voti_per_lista
    GROUP BY data_elezione, tipo_elezione, regione, provincia
),

-- Rank e quota per lista in ogni provincia×tornata
rank_liste AS (
    SELECT
        v.data_elezione,
        v.tipo_elezione,
        v.anno,
        v.regione,
        v.provincia,
        v.lista,
        v.voti_lista,
        t.totale_voti_validi,
        ROUND(CAST(v.voti_lista AS DOUBLE) / NULLIF(CAST(t.totale_voti_validi AS DOUBLE), 0) * 100, 2) AS pct_voti,
        ROW_NUMBER() OVER (
            PARTITION BY v.data_elezione, v.tipo_elezione, v.regione, v.provincia
            ORDER BY v.voti_lista DESC
        ) AS rank_lista
    FROM voti_per_lista v
    INNER JOIN totali_provincia t
        ON v.data_elezione = t.data_elezione
        AND v.tipo_elezione = t.tipo_elezione
        AND v.regione = t.regione
        AND v.provincia = t.provincia
),

-- Concentrazione: indice Herfindahl-Hirschman (HHI) per provincia×tornata
concentrazione AS (
    SELECT
        data_elezione,
        tipo_elezione,
        regione,
        provincia,
        -- HHI = sum(pct^2) normalizzato 0-10000
        ROUND(SUM(POW(CAST(voti_lista AS DOUBLE) / NULLIF(CAST(totale_voti_validi AS DOUBLE), 0) * 100, 2)), 0) AS hhi,
        -- Quota del primo partito
        MAX(CASE WHEN rank_lista = 1 THEN pct_voti END) AS primo_pct,
        MAX(CASE WHEN rank_lista = 2 THEN pct_voti END) AS secondo_pct,
        -- Numero di liste con >1%
        COUNT(DISTINCT CASE WHEN pct_voti >= 1 THEN lista END) AS n_liste_significative
    FROM rank_liste
    GROUP BY data_elezione, tipo_elezione, regione, provincia
)

SELECT
    r.*,
    c.hhi,
    c.primo_pct,
    c.secondo_pct,
    c.n_liste_significative,
    -- Differenziale primo-secondo (quanto la prima lista stacca la seconda)
    ROUND(c.primo_pct - c.secondo_pct, 2) AS gap_primo_secondo,
    -- Fascia concentrazione
    CASE
        WHEN c.hhi >= 2500 THEN 'alta'
        WHEN c.hhi >= 1500 THEN 'medio-alta'
        WHEN c.hhi >= 1000 THEN 'media'
        ELSE 'bassa'
    END AS fascia_concentrazione
FROM rank_liste r
LEFT JOIN concentrazione c
    ON r.data_elezione = c.data_elezione
    AND r.tipo_elezione = c.tipo_elezione
    AND r.regione = c.regione
    AND r.provincia = c.provincia
ORDER BY r.data_elezione DESC, r.regione, r.provincia, r.rank_lista
