-- Mart: PIL, Valore Aggiunto, Imposte nette per territorio e anno
-- Da clean_input

select
    territorio_codice,
    livello,
    anno,
    max(case when tipo_dato_codice = 'B1GQ_B_W2_S1' then valore_mln_eu end) as pil_mln_eu,
    max(case when tipo_dato_codice = 'B1G_B_W2_S1' then valore_mln_eu end) as va_mln_eu,
    max(case when tipo_dato_codice = 'D21X31_C_W2_S1' then valore_mln_eu end) as imposte_nette_mln_eu
from clean_input
where anno is not null
  and livello in ('nazionale', 'regione', 'provincia')
group by territorio_codice, livello, anno
order by territorio_codice, anno
