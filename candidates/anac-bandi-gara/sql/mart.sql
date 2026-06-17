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
    MEDIAN(importo_lotto) AS importo_lotto_mediano,
    -- massimo per singola provincia/mese/CPV — cattura mega-contratti
    -- (es. servizio idrico Puglia €17Mld validi su 20 anni)
    MAX(importo_lotto) AS importo_lotto_massimo
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
