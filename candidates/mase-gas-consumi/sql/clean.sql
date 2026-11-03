-- MASE SISEN — "Gas naturale totale distribuito per provincia".
-- File: Gas_Distribuito_Province_YYYY.xlsx, foglio "Foglio1".
-- Layout non tabellare (verificato 2024):
--   riga 5 = header (REGIONE, PROVINCIA, INDUSTRIALE, [spacer], TERMOELETTRICO,
--                    RETI DI DISTRIBUZIONE, TOTALE GENERALE)
--   righe 6+ = province, poi una riga "TOTALE " per regione con la regione in colonna A
--   -> il nome regione sta in FONDO al blocco, non in testa: le province di una
--      regione sono quelle che precedono la sua riga "TOTALE".
--   -> la colonna "spacer" (D) è sempre 0: scartata.
--   read.skip=4 + header=true -> header = riga 5.
-- Unità: M Sm3 (milioni di Sm3), PCS 10,57275 kWh/Sm3.
-- Le righe "TOTALE " di regione sono escluse: il totale si ricalcola dai comuni nel mart.

WITH base AS (
    SELECT
        row_number() OVER () AS rn,
        CAST(regione_raw AS VARCHAR) AS regione_raw,
        CAST(provincia_raw AS VARCHAR) AS provincia_raw,
        CAST(industriale AS VARCHAR) AS industriale,
        CAST(termoelettrico AS VARCHAR) AS termoelettrico,
        CAST(reti AS VARCHAR) AS reti
    FROM raw_input
),
-- Regione di ogni riga = prossimo (o corrente) nome regione non vuoto andando in avanti.
lab AS (
    SELECT
        *,
        MIN(CASE WHEN trim(COALESCE(regione_raw, '')) <> '' THEN rn END)
            OVER (ORDER BY rn ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING) AS region_rn
    FROM base
),
joined AS (
    SELECT
        l.rn,
        r.regione_raw AS regione,
        l.provincia_raw,
        l.industriale,
        l.termoelettrico,
        l.reti
    FROM lab l
    LEFT JOIN base r ON r.rn = l.region_rn
),
prov AS (
    SELECT *
    FROM joined
    WHERE provincia_raw IS NOT NULL
      AND trim(provincia_raw) <> ''
      AND upper(trim(provincia_raw)) NOT LIKE 'TOTALE%'
),
long AS (
    UNPIVOT prov
    ON industriale, termoelettrico, reti
    INTO NAME settore VALUE consumo_msmc
)
SELECT
    {year} AS anno,
    regione,
    provincia_raw AS provincia,
    settore,
    TRY_CAST(consumo_msmc AS DOUBLE) AS consumo_msmc
FROM long
