-- ISTAT 93_498 — PIL/VA/imposte lato offerta
-- Canale dbnomics · macros toolkit (normalize_string / cast_int / cast_double)
-- territorio_nome: label NUTS da codelist ESTAT GEO (statica; NUTS stabili)
-- Ultima edizione per REF_AREA × DATA_TYPE_AGGR

with
edizione_max as (
    select
        normalize_string(REF_AREA) as REF_AREA,
        normalize_string(DATA_TYPE_AGGR) as DATA_TYPE_AGGR,
        max(normalize_string(EDITION)) as max_ed
    from raw_input
    group by 1, 2
)
select
    normalize_string(r.REF_AREA) as territorio_codice,
    case normalize_string(r.REF_AREA)
        when 'IT' then 'Italia'
        when 'ITC' then 'Nord-Ovest'
        when 'ITC1' then 'Piemonte'
        when 'ITC11' then 'Torino'
        when 'ITC12' then 'Vercelli'
        when 'ITC13' then 'Biella'
        when 'ITC14' then 'Verbano-Cusio-Ossola'
        when 'ITC15' then 'Novara'
        when 'ITC16' then 'Cuneo'
        when 'ITC17' then 'Asti'
        when 'ITC18' then 'Alessandria'
        when 'ITC2' then 'Valle d''Aosta'
        when 'ITC20' then 'Valle d''Aosta'
        when 'ITC3' then 'Liguria'
        when 'ITC31' then 'Imperia'
        when 'ITC32' then 'Savona'
        when 'ITC33' then 'Genova'
        when 'ITC34' then 'La Spezia'
        when 'ITC4' then 'Lombardia'
        when 'ITC41' then 'Varese'
        when 'ITC42' then 'Como'
        when 'ITC43' then 'Lecco'
        when 'ITC44' then 'Sondrio'
        when 'ITC45' then 'Milano'
        when 'ITC46' then 'Bergamo'
        when 'ITC47' then 'Brescia'
        when 'ITC48' then 'Pavia'
        when 'ITC49' then 'Lodi'
        when 'ITC4A' then 'Cremona'
        when 'ITC4B' then 'Mantova'
        when 'ITCD' then 'Centro (aggregato ISTAT)'
        when 'ITCDE' then 'Centro-Est (aggregato ISTAT)'
        when 'ITD' then 'Nord-Est'
        when 'ITD1' then 'Provincia Autonoma Bolzano/Bozen'
        when 'ITD10' then 'Bolzano-Bozen'
        when 'ITD2' then 'Provincia Autonoma Trento'
        when 'ITD20' then 'Trento'
        when 'ITD3' then 'Veneto'
        when 'ITD31' then 'Verona'
        when 'ITD32' then 'Vicenza'
        when 'ITD33' then 'Belluno'
        when 'ITD34' then 'Treviso'
        when 'ITD35' then 'Venezia'
        when 'ITD36' then 'Padova'
        when 'ITD37' then 'Rovigo'
        when 'ITD4' then 'Friuli-Venezia Giulia'
        when 'ITD41' then 'Pordenone'
        when 'ITD42' then 'Udine'
        when 'ITD43' then 'Gorizia'
        when 'ITD44' then 'Trieste'
        when 'ITD5' then 'Emilia-Romagna'
        when 'ITD51' then 'Piacenza'
        when 'ITD52' then 'Parma'
        when 'ITD53' then 'Reggio nell''Emilia'
        when 'ITD54' then 'Modena'
        when 'ITD55' then 'Bologna'
        when 'ITD56' then 'Ferrara'
        when 'ITD57' then 'Ravenna'
        when 'ITD58' then 'Forlì-Cesena'
        when 'ITD59' then 'Rimini'
        when 'ITDA' then 'Sud (aggregato ISTAT)'
        when 'ITE' then 'Centro'
        when 'ITE1' then 'Toscana'
        when 'ITE11' then 'Massa-Carrara'
        when 'ITE12' then 'Lucca'
        when 'ITE13' then 'Pistoia'
        when 'ITE14' then 'Firenze'
        when 'ITE15' then 'Prato'
        when 'ITE16' then 'Livorno'
        when 'ITE17' then 'Pisa'
        when 'ITE18' then 'Arezzo'
        when 'ITE19' then 'Siena'
        when 'ITE1A' then 'Grosseto'
        when 'ITE2' then 'Umbria'
        when 'ITE21' then 'Perugia'
        when 'ITE22' then 'Terni'
        when 'ITE3' then 'Marche'
        when 'ITE31' then 'Pesaro e Urbino'
        when 'ITE32' then 'Ancona'
        when 'ITE33' then 'Macerata'
        when 'ITE34' then 'Ascoli Piceno'
        when 'ITE4' then 'Lazio'
        when 'ITE41' then 'Viterbo'
        when 'ITE42' then 'Rieti'
        when 'ITE43' then 'Roma'
        when 'ITE44' then 'Latina'
        when 'ITE45' then 'Frosinone'
        when 'ITF' then 'Sud'
        when 'ITF1' then 'Abruzzo'
        when 'ITF11' then 'L''Aquila'
        when 'ITF12' then 'Teramo'
        when 'ITF13' then 'Pescara'
        when 'ITF14' then 'Chieti'
        when 'ITF2' then 'Molise'
        when 'ITF21' then 'Isernia'
        when 'ITF22' then 'Campobasso'
        when 'ITF3' then 'Campania'
        when 'ITF31' then 'Caserta'
        when 'ITF32' then 'Benevento'
        when 'ITF33' then 'Napoli'
        when 'ITF34' then 'Avellino'
        when 'ITF35' then 'Salerno'
        when 'ITF4' then 'Puglia'
        when 'ITF41' then 'Foggia'
        when 'ITF42' then 'Bari'
        when 'ITF43' then 'Taranto'
        when 'ITF44' then 'Brindisi'
        when 'ITF45' then 'Lecce'
        when 'ITF5' then 'Basilicata'
        when 'ITF51' then 'Potenza'
        when 'ITF52' then 'Matera'
        when 'ITF6' then 'Calabria'
        when 'ITF61' then 'Cosenza'
        when 'ITF62' then 'Crotone'
        when 'ITF63' then 'Catanzaro'
        when 'ITF64' then 'Vibo Valentia'
        when 'ITF65' then 'Reggio Calabria'
        when 'ITFG' then 'Isole (aggregato ISTAT)'
        when 'ITG' then 'Isole'
        when 'ITG1' then 'Sicilia'
        when 'ITG11' then 'Trapani'
        when 'ITG12' then 'Palermo'
        when 'ITG13' then 'Messina'
        when 'ITG14' then 'Agrigento'
        when 'ITG15' then 'Caltanissetta'
        when 'ITG16' then 'Enna'
        when 'ITG17' then 'Catania'
        when 'ITG18' then 'Ragusa'
        when 'ITG19' then 'Siracusa'
        when 'ITG2' then 'Sardegna'
        when 'ITG25' then 'Sassari'
        when 'ITG26' then 'Nuoro'
        when 'ITG27' then 'Cagliari'
        when 'ITG28' then 'Oristano'
        when 'ITZ' then 'Extra-Regio'
        else normalize_string(r.REF_AREA)
    end as territorio_nome,
    case
        when normalize_string(r.REF_AREA) = 'IT' then 'nazionale'
        when length(normalize_string(r.REF_AREA)) = 3 then 'macro_area'
        when length(normalize_string(r.REF_AREA)) = 4
             and normalize_string(r.REF_AREA) not similar to 'IT[A-Z]{2,}' then 'regione'
        when length(normalize_string(r.REF_AREA)) = 4 then 'macro_area'
        when length(normalize_string(r.REF_AREA)) = 5
             and normalize_string(r.REF_AREA) not similar to 'IT[A-Z]{2,}' then 'provincia'
        else 'altro'
    end as livello,
    normalize_string(r.DATA_TYPE_AGGR) as tipo_dato_codice,
    case normalize_string(r.DATA_TYPE_AGGR)
        when 'B1GQ_B_W2_S1' then 'PIL'
        when 'B1G_B_W2_S1' then 'VA'
        when 'D21X31_C_W2_S1' then 'Imposte nette prodotti'
        else normalize_string(r.DATA_TYPE_AGGR)
    end as tipo_dato,
    normalize_string(r.VALUATION) as valutazione_codice,
    'prezzi correnti' as valutazione,
    cast_int(r.TIME_PERIOD) as anno,
    cast_double(r.OBS_VALUE) as valore_mln_eu
from raw_input r
join edizione_max e
  on normalize_string(r.REF_AREA) = e.REF_AREA
 and normalize_string(r.DATA_TYPE_AGGR) = e.DATA_TYPE_AGGR
 and normalize_string(r.EDITION) = e.max_ed
where normalize_string(r.VALUATION) = 'V'
  and normalize_string(r.ADJUSTMENT) = 'N'
  and anno is not null
  and cast_double(OBS_VALUE) is not null
