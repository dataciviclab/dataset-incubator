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
    COUNT(*) AS n_bandi,
    COUNT(DISTINCT cf_amministrazione_appaltante) AS n_stazioni_appaltanti,
    SUM(importo_complessivo_gara) AS importo_complessivo_totale,
    SUM(importo_lotto) AS importo_lotto_totale,
    AVG(importo_complessivo_gara) AS importo_medio_gara
FROM clean_input
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
