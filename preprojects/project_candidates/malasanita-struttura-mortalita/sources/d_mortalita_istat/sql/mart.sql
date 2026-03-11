-- mart.sql - malasanita_d_mortalita_istat - mart_regioni
-- Output: una riga per territorio regionale (21 righe attese)
--
-- Metodologia v2: Euro-2013 proxy (Eurostat Avoidable Mortality framework)
-- Riferimento: Eurostat 2019 — lista cause amenable e preventable per eta 30-74.
-- Il perimetro qui e` esteso a 30+ (non 30-74) per coerenza con le fonti Ministero.
--
-- Mapping codici ISTAT -> Euro-2013:
--
--   AMENABLE (mortalita evitabile con cure adeguate):
--     2  = Sepsi                          -> amenable
--     5  = Colon, retto, ano              -> amenable
--     7  = Tumore maligno del seno        -> amenable
--     9  = Diabete mellito                -> amenable
--    15  = Malattie ischemiche del cuore  -> amenable
--    16  = Malattie cerebrovascolari      -> amenable
--    17  = Malattie ipertensive           -> amenable (parziale)
--    19  = Influenza e polmonite          -> amenable
--
--   PREVENTABLE (mortalita riducibile con prevenzione primaria):
--     6  = Tumore trachea/bronchi/polmone -> preventable
--    20  = Malattie croniche basse vie resp (BPCO) -> preventable
--    22  = Cirrosi, fibrosi, epatite cronica       -> preventable
--    24  = Cause esterne di traumatismo             -> preventable (parziale)
--
--   ESCLUSI (aggregati, non mappabili, distorsivi):
--    25  = Totale                  -> proxy v1, non usare in v2
--    26  = Covid-19                -> distorce confronti 2022, escluso
--     3  = Tumori (aggregato)      -> sovraconta, cause specifiche gia incluse
--    23  = Cause mal definite      -> escluso sempre
--
-- Cause Euro-2013 non mappabili dalla fonte (peso epidemiologico marginale):
--   tumore cervice (C53), testicolo, tiroide, appendicite
--
-- Aggregazione:
-- - SUM(decessi): somma delle 12 cause per territorio — non sovrasconta perche
--   le cause sono mutualmente esclusive a livello di riga nel clean
-- - MAX(pop_media): la pop_media 30+ e` identica per tutte le righe dello stesso
--   territorio/anno (e` la popolazione di riferimento della fascia 30+, non della
--   singola causa). MAX() equivale a prendere il valore unico — verificato sul clean.
-- - tasso_grezzo_evitabile_10000_30plus: tasso grezzo, NON age-standardized.
--   Denominatore = pop_media 30+ (non popolazione totale del compose).
--   La colonna nel compose finale usa denominatore pop_totale: denominatore ibrido,
--   documentato esplicitamente nel notebook e nel compose.
-- - tasso_std_10000 della fonte e` pre-calcolato per singola causa: NON sommabile
--   tra cause diverse, conservato solo nel clean per analisi future.
--
-- Perimetro 30+: cod_classe_eta=9 corrisponde alla fascia "30 anni e oltre".
-- Il valore 9 non e` intuitivo dal codice — dichiarato esplicitamente qui.

WITH base AS (
    SELECT
        anno,
        cod_territorio,
        territorio,
        decessi,
        pop_media
    FROM clean_input
    WHERE cod_sesso = 3
      AND cod_classe_eta = 9
      AND cod_titolo_studio = 9
      AND cod_causa IN (2, 5, 6, 7, 9, 15, 16, 17, 19, 20, 22, 24)
)
SELECT
    anno,
    cod_territorio,
    territorio,
    SUM(decessi) AS decessi_evitabili_30plus,
    MAX(pop_media) AS pop_media_30plus,
    ROUND(SUM(decessi) / NULLIF(MAX(pop_media), 0) * 10000, 2) AS tasso_grezzo_evitabile_10000_30plus
FROM base
GROUP BY anno, cod_territorio, territorio
ORDER BY cod_territorio
