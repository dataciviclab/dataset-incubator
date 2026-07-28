-- mart_comuni — OpenCivitas: arricchimento + benchmark in un unico mart
--
-- Unisce i vecchi mart_indicatori (join comuni_master) + mart_benchmark.
-- Stessa cardinalità del clean (~2,6M righe/anno).
-- Ogni riga = (comune, anno, ambito, indicatore, valore) con:
--   • codice_istat via comuni_master
--   • benchmark: media nazionale/regionale, percentile, fascia, distanza %

with comuni as (
  select codice_istat, denominazione, codice_catastale, provincia as provincia_nome,
         substr(codice_istat, 1, 3) as prov_cod, regione, flag_capoluogo,
         ripartizione
  from read_parquet('{support.comuni_master.mart}')
),
base as (
  select
    c.username,
    c.anno,
    c.ambito,
    c.indicatore,
    c.descrizione_indicatore,
    c.tipo_indicatore,
    c.valore_num,
    c.denominazione,
    cm.codice_istat,
    cm.codice_catastale,
    c.regione as regione_clean,
    cm.regione as regione,
    cm.flag_capoluogo,
    cm.ripartizione
  from clean_input c
  left join comuni cm
    on upper(cm.denominazione) = upper(c.denominazione)
    and cm.prov_cod = c.provincia
  where c.valore_num is not null
    and c.tipo_indicatore in ('IND', 'DET')
)
select
  *,
  -- Benchmark nazionale
  round(avg(valore_num) over (partition by anno, ambito, indicatore), 6)        as media_nazionale,
  round(avg(valore_num) over (partition by anno, ambito, indicatore, regione), 6) as media_regionale,
  round(stddev(valore_num) over (partition by anno, ambito, indicatore), 6)      as std_nazionale,
  count(*) over (partition by anno, ambito, indicatore)                          as n_comuni_nazionali,
  -- Percentile
  round(percent_rank() over (partition by anno, ambito, indicatore order by valore_num), 4) as percentile_nazionale,
  -- Distanza %
  case
    when avg(valore_num) over (partition by anno, ambito, indicatore) <> 0
    then round((valore_num - avg(valore_num) over (partition by anno, ambito, indicatore))
         / abs(avg(valore_num) over (partition by anno, ambito, indicatore)) * 100, 2)
  end as distanza_media_nazionale_pct,
  case
    when avg(valore_num) over (partition by anno, ambito, indicatore, regione) <> 0
    then round((valore_num - avg(valore_num) over (partition by anno, ambito, indicatore, regione))
         / abs(avg(valore_num) over (partition by anno, ambito, indicatore, regione)) * 100, 2)
  end as distanza_media_regionale_pct,
  -- Fascia
  case
    when percent_rank() over (partition by anno, ambito, indicatore order by valore_num) >= 0.8 then 'ELEVATO'
    when percent_rank() over (partition by anno, ambito, indicatore order by valore_num) >= 0.6 then 'SOPRA_MEDIA'
    when percent_rank() over (partition by anno, ambito, indicatore order by valore_num) >= 0.4 then 'MEDIA'
    when percent_rank() over (partition by anno, ambito, indicatore order by valore_num) >= 0.2 then 'SOTTO_MEDIA'
    else 'BASSO'
  end as fascia_valore
from base
where codice_istat is not null
order by codice_istat, anno, ambito, indicatore;
