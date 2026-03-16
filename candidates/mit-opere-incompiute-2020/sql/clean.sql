with base as (
    select
        trim("Graduatoria_pubblicata_da") as graduatoria_pubblicata_da,
        cast("Anno_di_riferimento" as integer) as anno_di_riferimento,
        nullif(trim("Codice_CUP"), '') as codice_cup,
        trim("Ambito_soggettivo") as ambito_soggettivo,
        trim("Denominazione_Stazione_appaltante") as stazione_appaltante,
        nullif(trim("Codice_fiscale"), '') as codice_fiscale,
        trim("Stato_opera(d.m. 42/2013, art. 1, c. 2)") as stato_opera,
        nullif(trim("Localizzazione_codice_ISTAT"), '') as localizzazione_codice_istat,
        nullif(trim("Localizzazione_codice_NUTS"), '') as localizzazione_codice_nuts,
        trim("Ambito_oggettivo") as ambito_oggettivo,
        trim("Titolo_opera_incompiuta") as titolo_opera_incompiuta,
        trim("Descrizione_intervento") as descrizione_intervento,
        cast(replace(replace(nullif(trim("Importo_complessivo_aggiornato_ultimo_quadro_economico"), ''), '.', ''), ',', '.') as double) as importo_complessivo_qe,
        cast(replace(replace(nullif(trim("Importo_lavori_ultimo_q.e._approvato"), ''), '.', ''), ',', '.') as double) as importo_lavori_qe,
        cast(replace(replace(nullif(trim("Importo_complessivo_lavori_ultimo SAL"), ''), '.', ''), ',', '.') as double) as importo_lavori_sal,
        cast(replace(replace(nullif(trim("Importo_oneri_ultimazione"), ''), '.', ''), ',', '.') as double) as importo_oneri_ultimazione,
        cast("Perc_avanzamento_lavori" as double) as perc_avanzamento_lavori,
        trim("Mancanza_fondi") as mancanza_fondi,
        trim("Cause_tecniche") as cause_tecniche,
        trim("Soprav_norme_tec./disp.legge") as sopravvenienza_norme,
        trim("Fallim_liquid_conc_prev") as fallimento_liquidazione,
        trim("Mancato_interesse_compl") as mancato_interesse,
        trim("opera_fruibile_collettività") as opera_fruibile_collettivita,
        trim("uso ridimensionato_opera") as uso_ridimensionato_opera,
        trim("infrastruttura_rete") as infrastruttura_rete,
        trim("Incompletezza_costituisce discontinuità_rete") as discontinuita_rete,
        trim("Livello_sviluppo(d.m. 42/2013, art. 4)") as livello_sviluppo
    from raw_input
),
filtered as (
    select *
    from base
    where codice_cup is not null
      and codice_cup <> 'TOT'
),
dedup as (
    select *,
        row_number() over (
            partition by codice_cup
            order by titolo_opera_incompiuta, stazione_appaltante
        ) as rn
    from filtered
)
select
    graduatoria_pubblicata_da,
    anno_di_riferimento,
    codice_cup,
    ambito_soggettivo,
    stazione_appaltante,
    codice_fiscale,
    stato_opera,
    localizzazione_codice_istat,
    localizzazione_codice_nuts,
    ambito_oggettivo,
    titolo_opera_incompiuta,
    descrizione_intervento,
    importo_complessivo_qe,
    importo_lavori_qe,
    importo_lavori_sal,
    importo_oneri_ultimazione,
    perc_avanzamento_lavori,
    mancanza_fondi,
    cause_tecniche,
    sopravvenienza_norme,
    fallimento_liquidazione,
    mancato_interesse,
    opera_fruibile_collettivita,
    uso_ridimensionato_opera,
    infrastruttura_rete,
    discontinuita_rete,
    livello_sviluppo
from dedup
where rn = 1
