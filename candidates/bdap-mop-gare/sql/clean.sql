-- Clean: Gare Opere Pubbliche MOP — Territorio Nazionale
-- Fonte: BDAP / RGS, osservazione al 29/05/2026

select
    trim("Codice CUP") as codice_cup,
    trim("Codice CIG") as codice_cig,
    trim("Numero Gara") as numero_gara,
    trim("Oggetto Gara") as oggetto_gara,
    trim("Oggetto Lotto") as oggetto_lotto,
    "Data Pubblicazione Gara"::DATE as data_pubblicazione_gara,
    "Data Gara"::DATE as data_gara,
    trim("Codice Tipo Scelta Contraente"::VARCHAR) as codice_tipo_scelta_contraente,
    trim("Tipo Scelta Contraente") as tipo_scelta_contraente,
    trim("Codice Fiscale Soggetto") as codice_fiscale_soggetto,
    trim("Descrizione Soggetto") as descrizione_soggetto,
    trim("Codice Ente"::VARCHAR) as codice_ente,
    trim("Descrizione Ente") as descrizione_ente,
    try_cast("Numero Partecipanti Gara" as integer) as numero_partecipanti_gara,
    try_cast("Importo Base d'Asta" as double) as importo_base_asta,
    try_cast("Importo Aggiudicazione" as double) as importo_aggiudicazione
from raw_input
