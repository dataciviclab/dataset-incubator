-- mart_fasce — IRPEF Comunale: distribuzione contribuenti per fascia di reddito
--
-- Rimpiazza il vecchio mart_fasce_reddito.
-- Output: 1 riga = 1 provincia × anno.
-- Distribuzione dei contribuenti per fascia di reddito complessivo,
-- con quote percentuali e indicatore di ricchezza (quota oltre 55k).

select
    c.anno_di_imposta as anno,
    c.regione,
    c.sigla_provincia as provincia,
    count(*) as comuni,
    sum(c.numero_contribuenti) as contribuenti_totale,
    -- Contribuenti per fascia (valori assoluti)
    round(sum(c.reddito_complessivo_minore_o_uguale_a_zero_euro_freq), 0) as fascia_zero,
    round(sum(c.reddito_complessivo_da_0_a_10000_euro_freq), 0) as fascia_0_10k,
    round(sum(c.reddito_complessivo_da_10000_a_15000_euro_freq), 0) as fascia_10_15k,
    round(sum(c.reddito_complessivo_da_15000_a_26000_euro_freq), 0) as fascia_15_26k,
    round(sum(c.reddito_complessivo_da_26000_a_55000_euro_freq), 0) as fascia_26_55k,
    round(sum(c.reddito_complessivo_da_55000_a_75000_euro_freq), 0) as fascia_55_75k,
    round(sum(c.reddito_complessivo_da_75000_a_120000_euro_freq), 0) as fascia_75_120k,
    round(sum(c.reddito_complessivo_oltre_120000_euro_freq), 0) as fascia_oltre_120k,
    -- Quote percentuali
    round(sum(c.reddito_complessivo_da_0_a_10000_euro_freq) * 100.0
        / nullif(sum(c.numero_contribuenti), 0), 2) as quota_0_10k_pct,
    round(
        (sum(c.reddito_complessivo_da_55000_a_75000_euro_freq)
         + sum(c.reddito_complessivo_da_75000_a_120000_euro_freq)
         + sum(c.reddito_complessivo_oltre_120000_euro_freq))
        * 100.0 / nullif(sum(c.numero_contribuenti), 0)
    , 2) as quota_oltre_55k_pct,
    -- Indicatore sintetico: rapporto tra fascia alta (>55k) e bassa (<15k)
    round(
        (sum(c.reddito_complessivo_da_55000_a_75000_euro_freq)
         + sum(c.reddito_complessivo_da_75000_a_120000_euro_freq)
         + sum(c.reddito_complessivo_oltre_120000_euro_freq))
        * 1.0 / nullif(
            sum(c.reddito_complessivo_da_0_a_10000_euro_freq)
            + sum(c.reddito_complessivo_da_10000_a_15000_euro_freq)
        , 0)
    , 2) as rapporto_alta_bassa
from clean_input c
where c.regione is not null
  and c.sigla_provincia is not null
group by c.anno_di_imposta, c.regione, c.sigla_provincia
order by c.anno_di_imposta desc, contribuenti_totale desc;
