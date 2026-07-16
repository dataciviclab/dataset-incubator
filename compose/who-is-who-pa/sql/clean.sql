-- Clean: who-is-who-pa
-- Compose da ipa_enti + ipa_unita_organizzative + ipa_aree_organizzative_omogenee
-- Ogni riga = un'unità organizzativa con contesto ente e responsabile
-- DuckDB 1.5.4+ legge https://storage.googleapis.com/ nativamente
--
-- TODO: join con dait_amministratori_locali via comuni_master (mappatura codice)
-- Policy: aggiornare gli URL se cambia l'anno dei dataset upstream

WITH enti AS (
    SELECT * FROM read_parquet('https://storage.googleapis.com/dataciviclab-clean/ipa_enti/2026/ipa_enti_2026_clean.parquet')
),

uo AS (
    SELECT * FROM read_parquet('https://storage.googleapis.com/dataciviclab-clean/ipa_unita_organizzative/2026/ipa_unita_organizzative_2026_clean.parquet')
),

aoo AS (
    SELECT * FROM read_parquet('https://storage.googleapis.com/dataciviclab-clean/ipa_aree_organizzative_omogenee/2026/ipa_aree_organizzative_omogenee_2026_clean.parquet')
)

SELECT
    -- Ente
    e.codice_ipa,
    e.denominazione_ente,
    e.codice_fiscale_ente,
    e.codice_categoria,
    e.tipologia,
    e.codice_istat,
    e.acronimo,
    e.titolo_responsabile AS vertice_ente_titolo,
    e.nome_responsabile AS vertice_ente_nome,
    e.cognome_responsabile AS vertice_ente_cognome,
    e.sito_istituzionale,

    -- UO
    uo.codice_uni_uo,
    uo.descrizione_uo,
    uo.codice_uni_uo_padre,
    uo.data_istituzione AS uo_data_istituzione,
    uo.nome_responsabile AS uo_resp_nome,
    uo.cognome_responsabile AS uo_resp_cognome,
    uo.mail_responsabile AS uo_resp_email,
    uo.telefono_responsabile AS uo_resp_telefono,
    uo.mail1 AS uo_mail,
    uo.tipo_mail1 AS uo_tipo_mail,
    uo.mail2 AS uo_mail2,
    uo.tipo_mail2 AS uo_tipo_mail2,

    -- AOO
    aoo.codice_uni_aoo,
    aoo.denominazione_aoo,
    aoo.nome_responsabile AS aoo_resp_nome,
    aoo.cognome_responsabile AS aoo_resp_cognome,
    aoo.mail1 AS aoo_mail,
    aoo.tipo_mail1 AS aoo_tipo_mail,
    aoo.protocollo_informatico,
    aoo.uri_protocollo_informatico,

    -- Sede
    uo.codice_comune_istat,
    uo.codice_catastale_comune,
    uo.cap,
    uo.indirizzo,
    e.codice_comune_istat AS ente_codice_comune_istat

FROM uo
LEFT JOIN enti e ON uo.codice_ipa = e.codice_ipa
LEFT JOIN aoo ON uo.codice_uni_aoo = aoo.codice_uni_aoo
ORDER BY e.denominazione_ente, uo.descrizione_uo
