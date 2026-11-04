-- mart_merci_per_direttrice.sql: lettura analitica del trasporto merci su strada.
-- Nota sui dati: le coppie regione->regione NON esistono; i flussi sono
-- regione->Italia (uscita) e Italia->regione (entrata). Quindi il mart misura
-- quanto ogni regione SPEDE e RICEVE rispetto al resto d'Italia, non una matrice.

with base as (
    select anno, regione_carico, regione_scarico, valore
    from clean_input
    where unita = 'GC_TKM'
      and regione_carico  like 'IT%'
      and regione_scarico like 'IT%'
),
flussi as (
    select anno,
           case when regione_carico <> 'IT' then regione_carico else regione_scarico end as regione,
           case when regione_carico <> 'IT' then 'uscita' else 'entrata' end as verso,
           valore
    from base
    where (regione_carico = 'IT') <> (regione_scarico = 'IT')  -- esclude i totali IT->IT
),
per_regione as (
    select anno, regione,
           sum(case when verso = 'uscita'  then valore else 0 end) as tkm_uscita,
           sum(case when verso = 'entrata' then valore else 0 end) as tkm_entrata
    from flussi group by 1, 2
),
totale as (select anno, sum(valore) as tkm_totali from base group by 1)
select
    p.anno,
    p.regione,
    p.tkm_uscita,
    p.tkm_entrata,
    p.tkm_uscita + p.tkm_entrata                                        as tkm_movimentati,
    p.tkm_uscita - p.tkm_entrata                                        as saldo_uscita_entrata,
    round(100.0 * (p.tkm_uscita + p.tkm_entrata) / nullif(t.tkm_totali, 0), 2) as quota_pct
from per_regione p
join totale t on t.anno = p.anno
order by p.anno, tkm_movimentati desc
