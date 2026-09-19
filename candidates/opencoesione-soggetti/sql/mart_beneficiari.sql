-- mart_beneficiari.sql — OpenCoesione: beneficiari unici per CF
-- Input: clean_input (soggetti puliti)
-- Output: una riga per CF con conteggio progetti e finanziamenti

SELECT
  OC_CODICE_FISCALE_SOGG as codice_fiscale,
  MAX(OC_DENOMINAZIONE_SOGG) as denominazione,
  MAX(DESCR_FORMA_GIURIDICA_SOGG) as forma_giuridica,
  MAX(COD_COMUNE_SEDE_SOGG) as comune_sede,
  MAX(DESCRIZIONE_ATECO_SOGG) as attivita_ateco,
  MAX(DESCR_DIMENSIONE_SOGG) as dimensione,
  COUNT(DISTINCT COD_LOCALE_PROGETTO) as n_progetti,
  COUNT(DISTINCT CASE WHEN SOGG_DESCR_RUOLO LIKE '%Beneficiario%' THEN COD_LOCALE_PROGETTO END) as n_progetti_beneficiario
FROM clean_input
GROUP BY OC_CODICE_FISCALE_SOGG
