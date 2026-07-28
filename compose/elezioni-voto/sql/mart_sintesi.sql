-- Mart: sintesi affluenza per territorio × tipo elezione
-- Ogni riga: comune/tornata → affluenza + benchmark
--
-- Colonne:
--   data_elezione, tipo_elezione,
--   regione, provincia, comune,
--   elettori, votanti, affluenza_pct,
--   media_provincia_pct, media_regione_pct, media_nazionale_pct,
--   gap_provincia (affluenza_pct - media_provincia_pct),
--   gap_regione, gap_nazionale

WITH affluenza_comune AS (
    SELECT
        data_elezione,
        tipo_elezione,
        regione,
        provincia,
        comune,
        ANY_VALUE(elettori) AS elettori,
        ANY_VALUE(votanti) AS votanti,
        ANY_VALUE(affluenza_pct) AS affluenza_pct
    FROM clean_input
    GROUP BY data_elezione, tipo_elezione, regione, provincia, comune
),

medie AS (
    SELECT
        data_elezione,
        tipo_elezione,
        regione,
        provincia,
        AVG(affluenza_pct) AS media_provincia_pct
    FROM affluenza_comune
    GROUP BY data_elezione, tipo_elezione, regione, provincia
),

medie_regione AS (
    SELECT
        data_elezione,
        tipo_elezione,
        regione,
        AVG(affluenza_pct) AS media_regione_pct
    FROM affluenza_comune
    GROUP BY data_elezione, tipo_elezione, regione
),

medie_nazionali AS (
    SELECT
        data_elezione,
        tipo_elezione,
        AVG(affluenza_pct) AS media_nazionale_pct
    FROM affluenza_comune
    GROUP BY data_elezione, tipo_elezione
)

SELECT
    a.data_elezione,
    a.tipo_elezione,
    EXTRACT(YEAR FROM a.data_elezione) AS anno,
    a.regione,
    a.provincia,
    a.comune,
    a.elettori,
    a.votanti,
    a.affluenza_pct,
    m.media_provincia_pct,
    mr.media_regione_pct,
    mn.media_nazionale_pct,
    ROUND(a.affluenza_pct - m.media_provincia_pct, 2) AS gap_provincia,
    ROUND(a.affluenza_pct - mr.media_regione_pct, 2) AS gap_regione,
    ROUND(a.affluenza_pct - mn.media_nazionale_pct, 2) AS gap_nazionale,
    -- Fascia affluenza (5 fasce)
    CASE
        WHEN a.affluenza_pct >= 80 THEN 'molto_alta'
        WHEN a.affluenza_pct >= 65 THEN 'alta'
        WHEN a.affluenza_pct >= 50 THEN 'media'
        WHEN a.affluenza_pct >= 35 THEN 'bassa'
        ELSE 'molto_bassa'
    END AS fascia_affluenza
FROM affluenza_comune a
LEFT JOIN medie m ON a.data_elezione = m.data_elezione
    AND a.tipo_elezione = m.tipo_elezione
    AND a.regione = m.regione
    AND a.provincia = m.provincia
LEFT JOIN medie_regione mr ON a.data_elezione = mr.data_elezione
    AND a.tipo_elezione = mr.tipo_elezione
    AND a.regione = mr.regione
LEFT JOIN medie_nazionali mn ON a.data_elezione = mn.data_elezione
    AND a.tipo_elezione = mn.tipo_elezione
ORDER BY a.data_elezione DESC, a.regione, a.provincia, a.comune
