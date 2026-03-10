-- mart.sql - malasanita_d_mortalita_istat - mart_regioni
-- Output: una riga per territorio regionale (21 righe attese)
--
-- Scelta metodologica v2 — Euro-2013 proxy (Eurostat, Avoidable mortality):
-- - filtro su sesso totale (cod_sesso=3), classe eta 30+ (cod_classe_eta=9), titolo studio totale (cod_titolo_studio=9)
-- - cod_classe_eta=9 = fascia 30 anni e oltre (perimetro dichiarato, non ovvio dal codice)
-- - 12 cause mappate al framework Euro-2013 (amenable + preventable):
--     2  Sepsi                                          amenable
--     5  Tumori maligni colon/retto/ano                amenable
--     6  Tumori maligni trachea/bronchi/polmoni        preventable
--     7  Tumore maligno del seno                       amenable
--     9  Diabete mellito                               amenable
--    15  Malattie ischemiche del cuore                 amenable
--    16  Malattie cerebrovascolari                     amenable
--    17  Malattie ipertensive                          amenable (parziale)
--    19  Influenza e Polmonite                         amenable
--    20  Malattie croniche basse vie respiratorie      preventable
--    22  Cirrosi, fibrosi ed epatite cronica           preventable
--    24  Cause esterne di traumatismo e avvelenamento  preventable (parziale)
-- - cause non mappabili dalla fonte (cervice, testicolo, tiroide, appendicite): peso marginale, escluse
-- - cod_causa=26 (Covid-19) escluso — distorce confronti 2022
-- - tasso_std_10000 originale conservato nel clean ma NON sommato tra cause diverse (tasso pre-calcolato)
-- - aggregazione: SUM(decessi) / MAX(pop_media) * 10000 = tasso_grezzo_evitabile_10000_30plus
--   pop_media e identica per tutte le righe dello stesso territorio/anno → MAX equivale al valore unico
-- - naming deliberato: tasso_grezzo_evitabile, non tasso_evitabile o tasso_std_evitabile

WITH base AS (
    SELECT
        anno,
        cod_territorio,
        territorio,
        SUM(decessi) AS decessi_evitabili_30plus,
        MAX(pop_media) AS pop_media_30plus
    FROM clean_input
    WHERE cod_sesso = 3
      AND cod_classe_eta = 9
      AND cod_titolo_studio = 9
      AND cod_causa IN (2, 5, 6, 7, 9, 15, 16, 17, 19, 20, 22, 24)
    GROUP BY anno, cod_territorio, territorio
)
SELECT
    anno,
    cod_territorio,
    territorio,
    decessi_evitabili_30plus,
    pop_media_30plus,
    ROUND(decessi_evitabili_30plus / pop_media_30plus * 10000, 2) AS tasso_grezzo_evitabile_10000_30plus,
    ROUND(decessi_evitabili_30plus / pop_media_30plus * 100000, 2) AS tasso_grezzo_evitabile_100k_30plus
FROM base
ORDER BY cod_territorio
