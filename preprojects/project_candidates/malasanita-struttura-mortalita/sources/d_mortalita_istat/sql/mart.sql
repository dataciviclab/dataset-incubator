-- mart.sql - malasanita_d_mortalita_istat - mart_regioni
-- Output: una riga per territorio regionale (21 righe attese)
--
-- Scelta metodologica v2 (Euro-2013 proxy):
-- - filtro totale su sesso, classe eta (30+), titolo di studio
-- - 12 cause amenable/preventable mappate da Euro-2013 framework
--   (2=Sepsi, 5=Colon-retto, 6=Polmone, 7=Seno, 9=Diabete,
--    15=Ischemiche cuore, 16=Cerebrovascolari, 17=Ipertensive,
--    19=Influenza/Polmonite, 20=BPCO, 22=Cirrosi, 24=Cause esterne)
-- - aggregazione: SUM(decessi), MAX(pop_media) per territorio
-- - tasso_grezzo: non e` tasso age-standardized, e` grezzo 30+
--   denominatore = pop_media 30+ (uguale per tutte le cause dello stesso territorio)
-- - tasso_std_10000 della fonte NON e` sommabile tra cause diverse: conservato nel clean
--
-- Nota: perimetro 30+ dichiarato esplicitamente (cod_classe_eta=9 non ovvio dal codice).

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
