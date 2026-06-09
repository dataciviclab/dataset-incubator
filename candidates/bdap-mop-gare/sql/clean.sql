-- Clean: unifica 21 fonti regionali Gare Opere Pubbliche MOP
-- UNION ALL via * (stesso schema), rinomina colonne nell'outer query

with unified as (
    select 'IT' as cod_regione, 'Territorio Nazionale' as desc_regione, * from raw.bdap_mop_gare_IT
    union all select '01', 'Piemonte', * from raw.bdap_mop_gare_01
    union all select '02', 'Valle d''Aosta', * from raw.bdap_mop_gare_02
    union all select '03', 'Lombardia', * from raw.bdap_mop_gare_03
    union all select '04', 'Trentino-Alto Adige', * from raw.bdap_mop_gare_04
    union all select '05', 'Veneto', * from raw.bdap_mop_gare_05
    union all select '06', 'Friuli-Venezia Giulia', * from raw.bdap_mop_gare_06
    union all select '07', 'Liguria', * from raw.bdap_mop_gare_07
    union all select '08', 'Emilia-Romagna', * from raw.bdap_mop_gare_08
    union all select '09', 'Toscana', * from raw.bdap_mop_gare_09
    union all select '10', 'Umbria', * from raw.bdap_mop_gare_10
    union all select '11', 'Marche', * from raw.bdap_mop_gare_11
    union all select '12', 'Lazio', * from raw.bdap_mop_gare_12
    union all select '13', 'Abruzzo', * from raw.bdap_mop_gare_13
    union all select '14', 'Molise', * from raw.bdap_mop_gare_14
    union all select '15', 'Campania', * from raw.bdap_mop_gare_15
    union all select '16', 'Puglia', * from raw.bdap_mop_gare_16
    union all select '17', 'Basilicata', * from raw.bdap_mop_gare_17
    union all select '18', 'Calabria', * from raw.bdap_mop_gare_18
    union all select '19', 'Sicilia', * from raw.bdap_mop_gare_19
    union all select '20', 'Sardegna', * from raw.bdap_mop_gare_20
)
select
    cod_regione,
    desc_regione,
    case when cod_regione = 'IT' then true else false end as flag_nazionale,
    trim("Codice CUP") as codice_cup,
    trim("Codice CIG") as codice_cig,
    trim("Numero Gara") as numero_gara,
    trim("Oggetto Gara") as oggetto_gara,
    trim("Oggetto Lotto") as oggetto_lotto,
    trim("Data Pubblicazione Gara") as data_pubblicazione_gara,
    trim("Data Gara") as data_gara,
    trim("Codice Tipo Scelta Contraente") as codice_tipo_scelta_contraente,
    trim("Tipo Scelta Contraente") as tipo_scelta_contraente,
    trim("Codice Fiscale Soggetto") as codice_fiscale_soggetto,
    trim("Descrizione Soggetto") as descrizione_soggetto,
    trim("Codice Ente") as codice_ente,
    trim("Descrizione Ente") as descrizione_ente,
    try_cast(trim("Numero Partecipanti Gara") as integer) as numero_partecipanti_gara,
    try_cast(replace(trim("Importo Base d'Asta"), ',', '.') as double) as importo_base_asta,
    try_cast(replace(trim("Importo Aggiudicazione"), ',', '.') as double) as importo_aggiudicazione
from unified
