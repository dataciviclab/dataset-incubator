-- mart.sql — mef_rappresentanti_partecipate
SELECT
    anno, amministrazione, amm_settore, amm_macrocategoria, amm_categoria,
    amm_cf, amm_regione, amm_provincia, amm_comune,
    societa, societa_cf, societa_anno_costituzione,
    societa_forma_giuridica, societa_stato, societa_settore, societa_ateco,
    societa_regione, societa_provincia, societa_comune,
    rapp_id, rapp_cognome, rapp_nome, rapp_genere,
    incarico_tipo, incarico_data_inizio, incarico_data_fine,
    incarico_gratuito, incarico_importo_eur, incarico_riversato_eur
FROM clean_input
