-- ISTAT SDMX DCCN_PILT — PIL lato offerta
-- Fonte: CSV SDMX
-- Colonne CSV: DATAFLOW, FREQ, REF_AREA, DATA_TYPE_AGGR, VALUATION, ADJUSTMENT, EDITION, TIME_PERIOD, OBS_VALUE

-- Mapping codici REF_AREA → nome territorio + livello
-- Fonte: ISTAT codelist CL_ITTER107
with
territori (codice, nome, livello) as (
    values
    -- Nazionale
    ('IT', 'Italia', 'nazionale'),
    -- Macro-aree (solo lettere dopo IT, o 3 char)
    ('ITC', 'Nord-ovest', 'macro_area'),
    ('ITD', 'Nord-est', 'macro_area'),
    ('ITE', 'Centro', 'macro_area'),
    ('ITF', 'Sud', 'macro_area'),
    ('ITG', 'Isole', 'macro_area'),
    ('ITCD', 'Centro-nord', 'macro_area'),
    ('ITDA', 'Trentino-Alto Adige', 'macro_area'),
    ('ITFG', 'Mezzogiorno', 'macro_area'),
    ('ITZ', 'Extra-Regio', 'macro_area'),
    -- Regioni (IT + lettera + 1 cifra)
    ('ITC1', 'Piemonte', 'regione'),
    ('ITC2', 'Valle d''Aosta / Vallée d''Aoste', 'regione'),
    ('ITC3', 'Liguria', 'regione'),
    ('ITC4', 'Lombardia', 'regione'),
    ('ITD1', 'Provincia Autonoma Bolzano', 'regione'),
    ('ITD2', 'Provincia Autonoma Trento', 'regione'),
    ('ITD3', 'Veneto', 'regione'),
    ('ITD4', 'Friuli-Venezia Giulia', 'regione'),
    ('ITD5', 'Emilia-Romagna', 'regione'),
    ('ITE1', 'Toscana', 'regione'),
    ('ITE2', 'Umbria', 'regione'),
    ('ITE3', 'Marche', 'regione'),
    ('ITE4', 'Lazio', 'regione'),
    ('ITF1', 'Abruzzo', 'regione'),
    ('ITF2', 'Molise', 'regione'),
    ('ITF3', 'Campania', 'regione'),
    ('ITF4', 'Puglia', 'regione'),
    ('ITF5', 'Basilicata', 'regione'),
    ('ITF6', 'Calabria', 'regione'),
    ('ITG1', 'Sicilia', 'regione'),
    ('ITG2', 'Sardegna', 'regione'),
    -- Province Piemonte
    ('ITC11', 'Torino', 'provincia'),
    ('ITC12', 'Vercelli', 'provincia'),
    ('ITC13', 'Biella', 'provincia'),
    ('ITC14', 'Verbano-Cusio-Ossola', 'provincia'),
    ('ITC15', 'Novara', 'provincia'),
    ('ITC16', 'Cuneo', 'provincia'),
    ('ITC17', 'Asti', 'provincia'),
    ('ITC18', 'Alessandria', 'provincia'),
    ('ITC20', 'Valle d''Aosta', 'provincia'),
    -- Province Liguria
    ('ITC31', 'Imperia', 'provincia'),
    ('ITC32', 'Savona', 'provincia'),
    ('ITC33', 'Genova', 'provincia'),
    ('ITC34', 'La Spezia', 'provincia'),
    -- Province Lombardia
    ('ITC41', 'Varese', 'provincia'),
    ('ITC42', 'Como', 'provincia'),
    ('ITC43', 'Lecco', 'provincia'),
    ('ITC44', 'Sondrio', 'provincia'),
    ('ITC45', 'Milano', 'provincia'),
    ('ITC46', 'Bergamo', 'provincia'),
    ('ITC47', 'Brescia', 'provincia'),
    ('ITC48', 'Pavia', 'provincia'),
    ('ITC49', 'Lodi', 'provincia'),
    ('ITC4A', 'Cremona', 'provincia'),
    ('ITC4B', 'Mantova', 'provincia'),
    ('IT108', 'Monza e della Brianza', 'provincia'),
    -- Province Trentino A.A.
    ('ITD10', 'Bolzano', 'provincia'),
    ('ITD20', 'Trento', 'provincia'),
    -- Province Veneto
    ('ITD31', 'Verona', 'provincia'),
    ('ITD32', 'Vicenza', 'provincia'),
    ('ITD33', 'Belluno', 'provincia'),
    ('ITD34', 'Treviso', 'provincia'),
    ('ITD35', 'Venezia', 'provincia'),
    ('ITD36', 'Padova', 'provincia'),
    ('ITD37', 'Rovigo', 'provincia'),
    -- Province Friuli-V.G.
    ('ITD41', 'Pordenone', 'provincia'),
    ('ITD42', 'Udine', 'provincia'),
    ('ITD43', 'Gorizia', 'provincia'),
    ('ITD44', 'Trieste', 'provincia'),
    -- Province Emilia-Romagna
    ('ITD51', 'Piacenza', 'provincia'),
    ('ITD52', 'Parma', 'provincia'),
    ('ITD53', 'Reggio nell''Emilia', 'provincia'),
    ('ITD54', 'Modena', 'provincia'),
    ('ITD55', 'Bologna', 'provincia'),
    ('ITD56', 'Ferrara', 'provincia'),
    ('ITD57', 'Ravenna', 'provincia'),
    ('ITD58', 'Forlì-Cesena', 'provincia'),
    ('ITD59', 'Rimini', 'provincia'),
    -- Province Toscana
    ('ITE11', 'Massa-Carrara', 'provincia'),
    ('ITE12', 'Lucca', 'provincia'),
    ('ITE13', 'Pistoia', 'provincia'),
    ('ITE14', 'Firenze', 'provincia'),
    ('ITE15', 'Prato', 'provincia'),
    ('ITE16', 'Livorno', 'provincia'),
    ('ITE17', 'Pisa', 'provincia'),
    ('ITE18', 'Arezzo', 'provincia'),
    ('ITE19', 'Siena', 'provincia'),
    ('ITE1A', 'Grosseto', 'provincia'),
    -- Province Umbria
    ('ITE21', 'Perugia', 'provincia'),
    ('ITE22', 'Terni', 'provincia'),
    -- Province Marche
    ('ITE31', 'Pesaro e Urbino', 'provincia'),
    ('ITE32', 'Ancona', 'provincia'),
    ('ITE33', 'Macerata', 'provincia'),
    ('ITE34', 'Ascoli Piceno', 'provincia'),
    ('IT109', 'Fermo', 'provincia'),
    -- Province Lazio
    ('ITE41', 'Viterbo', 'provincia'),
    ('ITE42', 'Rieti', 'provincia'),
    ('ITE43', 'Roma', 'provincia'),
    ('ITE44', 'Latina', 'provincia'),
    ('ITE45', 'Frosinone', 'provincia'),
    -- Province Abruzzo
    ('ITF11', 'L''Aquila', 'provincia'),
    ('ITF12', 'Teramo', 'provincia'),
    ('ITF13', 'Pescara', 'provincia'),
    ('ITF14', 'Chieti', 'provincia'),
    -- Province Molise
    ('ITF21', 'Isernia', 'provincia'),
    ('ITF22', 'Campobasso', 'provincia'),
    -- Province Campania
    ('ITF31', 'Caserta', 'provincia'),
    ('ITF32', 'Benevento', 'provincia'),
    ('ITF33', 'Napoli', 'provincia'),
    ('ITF34', 'Avellino', 'provincia'),
    ('ITF35', 'Salerno', 'provincia'),
    -- Province Puglia
    ('ITF41', 'Foggia', 'provincia'),
    ('ITF42', 'Bari', 'provincia'),
    ('ITF43', 'Taranto', 'provincia'),
    ('ITF44', 'Brindisi', 'provincia'),
    ('ITF45', 'Lecce', 'provincia'),
    ('IT110', 'Barletta-Andria-Trani', 'provincia'),
    -- Province Basilicata
    ('ITF51', 'Potenza', 'provincia'),
    ('ITF52', 'Matera', 'provincia'),
    -- Province Calabria
    ('ITF61', 'Cosenza', 'provincia'),
    ('ITF62', 'Crotone', 'provincia'),
    ('ITF63', 'Catanzaro', 'provincia'),
    ('ITF64', 'Vibo Valentia', 'provincia'),
    ('ITF65', 'Reggio di Calabria', 'provincia'),
    -- Province Sicilia
    ('ITG11', 'Trapani', 'provincia'),
    ('ITG12', 'Palermo', 'provincia'),
    ('ITG13', 'Messina', 'provincia'),
    ('ITG14', 'Agrigento', 'provincia'),
    ('ITG15', 'Caltanissetta', 'provincia'),
    ('ITG16', 'Enna', 'provincia'),
    ('ITG17', 'Catania', 'provincia'),
    ('ITG18', 'Ragusa', 'provincia'),
    ('ITG19', 'Siracusa', 'provincia'),
    -- Province Sardegna
    ('ITG25', 'Sassari', 'provincia'),
    ('ITG26', 'Nuoro', 'provincia'),
    ('ITG27', 'Cagliari', 'provincia'),
    ('ITG28', 'Oristano', 'provincia'),
    ('IT111', 'Sud Sardegna', 'provincia')
),
edizione_max as (
    select max(EDITION) as max_ed from raw_input
)
select
    raw.REF_AREA as territorio_codice,
    coalesce(t.nome, raw.REF_AREA) as territorio_nome,
    coalesce(t.livello,
        case
            when raw.REF_AREA = 'IT' then 'nazionale'
            when length(raw.REF_AREA) = 3 then 'macro_area'
            when length(raw.REF_AREA) = 4 and raw.REF_AREA not similar to 'IT[A-Z]{2,}' then 'regione'
            when length(raw.REF_AREA) = 5 and not (raw.REF_AREA similar to 'IT[A-Z]{2,}') then 'provincia'
            else 'altro'
        end
    ) as livello,
    raw.DATA_TYPE_AGGR as tipo_dato_codice,
    raw.VALUATION as valutazione_codice,
    cast(raw.TIME_PERIOD as integer) as anno,
    cast(raw.OBS_VALUE as double) as valore_mln_eu
from raw_input raw
left join territori t on raw.REF_AREA = t.codice
cross join edizione_max e
where raw.EDITION = e.max_ed
  and raw.VALUATION = 'V'
  and raw.ADJUSTMENT = 'N'
  and raw.OBS_VALUE is not null
