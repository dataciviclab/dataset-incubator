-- mart_sintesi.sql - aifa_spesa_consumo - mart_sintesi_regione_anno
-- Sintesi territoriale: 1 riga = 1 regione × anno, solo flusso convenzionata.
-- Serve a rispondere alle domande "quanto spende ogni regione" e "quanto costa
-- una confezione" senza passare dal dettaglio ATC4.

WITH base AS (
    SELECT
        anno,
        codreg,
        regione,
        SUM(spesa_convenzionata)              AS spesa,
        SUM(numero_confezioni_convenzionata)  AS confezioni
    FROM clean_input
    WHERE spesa_convenzionata IS NOT NULL
    GROUP BY anno, codreg, regione
),
nazionale AS (
    SELECT anno, SUM(spesa) AS spesa_nazionale
    FROM base
    GROUP BY anno
)
SELECT
    b.anno,
    b.codreg,
    b.regione,
    ROUND(b.spesa, 2)                                              AS spesa_convenzionata,
    CAST(ROUND(b.confezioni, 0) AS BIGINT)                         AS num_confezioni,
    ROUND(b.spesa / NULLIF(b.confezioni, 0), 2)                    AS costo_medio_confezione,
    ROUND(b.spesa / NULLIF(n.spesa_nazionale, 0) * 100, 2)         AS quota_nazionale_pct,
    RANK() OVER (
        PARTITION BY b.anno
        ORDER BY b.spesa / NULLIF(b.confezioni, 0) DESC
    )                                                              AS rank_costo_medio
FROM base b
JOIN nazionale n USING (anno)
ORDER BY b.anno, b.regione
