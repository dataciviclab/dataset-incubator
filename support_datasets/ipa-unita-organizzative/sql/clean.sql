-- Clean: ipa_unita_organizzative
-- Anagrafica unità organizzative (UO) degli enti PA da IndicePA (AgID).
-- Ogni riga rappresenta una UO, con codice univoco e riferimento gerarchico
-- al padre (codice_uni_uo_padre) per ricostruzione dell'albero organizzativo.
-- Fonte: https://indicepa.gov.it/ipa-dati
-- Formato originale: XLSX → letto via pandas.read_excel (openpyxl).
-- Le colonne sono CAST a VARCHAR per robustezza contro tipi misti.

SELECT DISTINCT
    trim(CAST(Codice_IPA AS VARCHAR)) AS codice_ipa,
    trim(CAST(Denominazione_ente AS VARCHAR)) AS denominazione_ente,
    trim(CAST(Codice_fiscale_ente AS VARCHAR)) AS codice_fiscale_ente,
    trim(CAST(Codice_uni_uo AS VARCHAR)) AS codice_uni_uo,
    trim(CAST(Codice_uni_aoo AS VARCHAR)) AS codice_uni_aoo,
    trim(CAST(Codice_uni_uo_padre AS VARCHAR)) AS codice_uni_uo_padre,
    trim(CAST(Descrizione_uo AS VARCHAR)) AS descrizione_uo,
    trim(CAST(Data_istituzione AS VARCHAR)) AS data_istituzione,
    trim(CAST(Nome_responsabile AS VARCHAR)) AS nome_responsabile,
    trim(CAST(Cognome_responsabile AS VARCHAR)) AS cognome_responsabile,
    trim(CAST(Mail_responsabile AS VARCHAR)) AS mail_responsabile,
    trim(CAST(Telefono_responsabile AS VARCHAR)) AS telefono_responsabile,
    trim(CAST(Codice_comune_ISTAT AS VARCHAR)) AS codice_comune_istat,
    trim(CAST(Codice_catastale_comune AS VARCHAR)) AS codice_catastale_comune,
    trim(CAST(CAP AS VARCHAR)) AS cap,
    trim(CAST(Indirizzo AS VARCHAR)) AS indirizzo,
    trim(CAST(Telefono AS VARCHAR)) AS telefono,
    trim(CAST(Fax AS VARCHAR)) AS fax,
    trim(CAST(Mail1 AS VARCHAR)) AS mail1,
    trim(CAST(Tipo_Mail1 AS VARCHAR)) AS tipo_mail1,
    trim(CAST(Mail2 AS VARCHAR)) AS mail2,
    trim(CAST(Tipo_Mail2 AS VARCHAR)) AS tipo_mail2,
    trim(CAST(Mail3 AS VARCHAR)) AS mail3,
    trim(CAST(Tipo_Mail3 AS VARCHAR)) AS tipo_mail3,
    trim(CAST(Data_aggiornamento AS VARCHAR)) AS data_aggiornamento,
    trim(CAST(Url AS VARCHAR)) AS url
FROM raw_input
WHERE trim(CAST(Codice_uni_uo AS VARCHAR)) IS NOT NULL
  AND trim(CAST(Codice_uni_uo AS VARCHAR)) != ''
ORDER BY denominazione_ente, descrizione_uo
