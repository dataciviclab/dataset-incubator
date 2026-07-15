-- Clean: ipa_aree_organizzative_omogenee
-- Anagrafica Aree Organizzative Omogenee (AOO) degli enti PA da IndicePA (AgID).
-- Ogni AOO corrisponde a un registro di protocollo dell'ente e raggruppa
-- le Unità Organizzative (UO) per area (es. Area Amministrativa, Area Tecnica).
-- Fonte: https://indicepa.gov.it/ipa-dati
-- Formato originale: XLSX → letto via pandas.read_excel (openpyxl).

SELECT DISTINCT
    trim(CAST(Codice_IPA AS VARCHAR)) AS codice_ipa,
    trim(CAST(Denominazione_ente AS VARCHAR)) AS denominazione_ente,
    trim(CAST(Codice_fiscale_ente AS VARCHAR)) AS codice_fiscale_ente,
    trim(CAST(Codice_uni_aoo AS VARCHAR)) AS codice_uni_aoo,
    trim(CAST(Denominazione_aoo AS VARCHAR)) AS denominazione_aoo,
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
    trim(CAST(Protocollo_informatico AS VARCHAR)) AS protocollo_informatico,
    trim(CAST(URI_Protocollo_informatico AS VARCHAR)) AS uri_protocollo_informatico,
    trim(CAST(Data_aggiornamento AS VARCHAR)) AS data_aggiornamento,
    trim(CAST(cod_AOO AS VARCHAR)) AS cod_aoo
FROM raw_input
WHERE trim(CAST(Codice_uni_aoo AS VARCHAR)) IS NOT NULL
  AND trim(CAST(Codice_uni_aoo AS VARCHAR)) != ''
ORDER BY denominazione_ente, denominazione_aoo
