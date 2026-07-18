-- Mart dettaglio: preserva righe e chiavi per join con anac_bandi_gara
SELECT
    cig,
    id_aggiudicazione,
    data_aggiudicazione_definitiva,
    data_comunicazione_esito,
    esito,
    criterio_aggiudicazione,
    importo_aggiudicazione,
    ribasso_aggiudicazione,
    numero_offerte_ammesse,
    numero_offerte_escluse,
    num_imprese_offerenti,
    num_imprese_invitate,
    flag_subappalto,
    asta_elettronica,
    cod_esito
FROM clean_input
WHERE cig IS NOT NULL
