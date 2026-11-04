-- Sbarchi giornalieri via mare in Italia — clean
-- Fonte: onData / liberiamoli-tutti (Cruscotto statistico del Ministero dell'Interno)
--
-- Il file e' una concatenazione di report (colonna `Data_Report`): ogni report
-- riporta i giorni del suo mese fino alla data del report, quindi lo stesso
-- giorno compare piu' volte (report di meta' mese + report di fine mese) e il
-- valore puo' essere rivisto nei consolidamenti successivi.
--
-- Si tiene UNA riga per giorno: quella del report piu' recente CHE HA UN VALORE.
-- Il filtro sul valore precede il row_number, cosi' un eventuale report futuro
-- con valore vuoto non fa sparire un giorno gia' consolidato (senza dedup le
-- somme gonfiano di ~1,5x: il giorno conta una volta per ogni report che lo riporta).

SELECT
    data_sbarchi,
    valore,
    note,
    fonte
FROM (
    SELECT
        TRY_CAST(Data AS DATE) AS data_sbarchi,
        TRY_CAST(Valore AS BIGINT) AS valore,
        CAST(Note AS VARCHAR) AS note,
        CAST(Fonte AS VARCHAR) AS fonte,
        row_number() OVER (
            PARTITION BY TRY_CAST(Data AS DATE)
            ORDER BY TRY_CAST(Data_Report AS DATE) DESC
        ) AS _rn
    FROM raw_input
    WHERE TRY_CAST(Valore AS BIGINT) IS NOT NULL
) t
WHERE _rn = 1
