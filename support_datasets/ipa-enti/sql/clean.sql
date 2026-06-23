-- Clean: ipa_enti
-- Anagrafica completa enti da IPA (Indice PA), fonte AgID.
-- Dump CSV con encoding UTF-8, delim ',', header.
-- Include tutte le categorie: PA, Stazioni Appaltanti, Gestori, Società, ecc.
-- Fonte: https://indicepa.gov.it/ipa-dati
-- Note: CAST(... AS VARCHAR) prima di trim() perché DuckDB deduce
-- tipi numerici per colonne con pochi testi (es. Codice_natura).
-- DROP implicito: Url_facebook, Url_linkedin, Url_twitter, Url_youtube, _id
-- (social/tecnici, non servono per anagrafica advocacy).

SELECT DISTINCT
    trim(CAST(Codice_IPA AS VARCHAR)) AS codice_ipa,
    trim(CAST(Denominazione_ente AS VARCHAR)) AS denominazione_ente,
    trim(CAST(Codice_fiscale_ente AS VARCHAR)) AS codice_fiscale_ente,
    trim(CAST(Tipologia AS VARCHAR)) AS tipologia,
    trim(CAST(Codice_Categoria AS VARCHAR)) AS codice_categoria,
    trim(CAST(Codice_natura AS VARCHAR)) AS codice_natura,
    trim(CAST(Codice_ateco AS VARCHAR)) AS codice_ateco,
    CASE WHEN trim(CAST(Ente_in_liquidazione AS VARCHAR)) IN ('S','s') THEN TRUE
         WHEN trim(CAST(Ente_in_liquidazione AS VARCHAR)) IN ('N','n') THEN FALSE
         ELSE NULL END AS ente_in_liquidazione,
    trim(CAST(Codice_MIUR AS VARCHAR)) AS codice_miur,
    trim(CAST(Codice_ISTAT AS VARCHAR)) AS codice_istat,
    trim(CAST(Acronimo AS VARCHAR)) AS acronimo,
    trim(CAST(Nome_responsabile AS VARCHAR)) AS nome_responsabile,
    trim(CAST(Cognome_responsabile AS VARCHAR)) AS cognome_responsabile,
    trim(CAST(Titolo_responsabile AS VARCHAR)) AS titolo_responsabile,
    trim(CAST(Codice_comune_ISTAT AS VARCHAR)) AS codice_comune_istat,
    trim(CAST(Codice_catastale_comune AS VARCHAR)) AS codice_catastale_comune,
    trim(CAST(CAP AS VARCHAR)) AS cap,
    trim(CAST(Indirizzo AS VARCHAR)) AS indirizzo,
    trim(CAST(Mail1 AS VARCHAR)) AS mail1,
    trim(CAST(Tipo_Mail1 AS VARCHAR)) AS tipo_mail1,
    trim(CAST(Mail2 AS VARCHAR)) AS mail2,
    trim(CAST(Tipo_Mail2 AS VARCHAR)) AS tipo_mail2,
    trim(CAST(Mail3 AS VARCHAR)) AS mail3,
    trim(CAST(Tipo_Mail3 AS VARCHAR)) AS tipo_mail3,
    trim(CAST(Mail4 AS VARCHAR)) AS mail4,
    trim(CAST(Tipo_Mail4 AS VARCHAR)) AS tipo_mail4,
    trim(CAST(Mail5 AS VARCHAR)) AS mail5,
    trim(CAST(Tipo_Mail5 AS VARCHAR)) AS tipo_mail5,
    trim(CAST(Sito_istituzionale AS VARCHAR)) AS sito_istituzionale,
    trim(CAST(Data_aggiornamento AS VARCHAR)) AS data_aggiornamento
FROM raw_input
WHERE CAST(Codice_IPA AS VARCHAR) IS NOT NULL
  AND trim(CAST(Codice_IPA AS VARCHAR)) != ''
ORDER BY denominazione_ente
