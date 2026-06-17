SELECT
    anno_pubblicazione,
    mese_pubblicazione,
    provincia,
    oggetto_principale_contratto,
    cod_cpv,
    descrizione_cpv,
    stato,
    esito,
    flag_pnrr,
    COUNT(*) AS n_lotti,
    COUNT(DISTINCT cig) AS n_bandi,
    COUNT(DISTINCT cf_amministrazione_appaltante) AS n_stazioni_appaltanti,
    SUM(importo_lotto) AS importo_lotti_totale,
    MEDIAN(importo_lotto) AS importo_lotto_mediano
FROM clean_input
-- Esclude outlier: alcuni importi nel dataset ANAC sono palesemente errati
-- (es. 12 miliardi per formazione camerale, 7.9 miliardi per materiale
--  consumo di un liceo). Probabilmente centesimi interpretati come euro.
-- I 44 lotti > 1 miliardo su 1.47M rappresentano lo 0.003% delle righe.
WHERE importo_lotto < 1000000000
GROUP BY
    anno_pubblicazione,
    mese_pubblicazione,
    provincia,
    oggetto_principale_contratto,
    cod_cpv,
    descrizione_cpv,
    stato,
    esito,
    flag_pnrr
