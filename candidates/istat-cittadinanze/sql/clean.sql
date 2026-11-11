-- clean.sql: acquisizioni di cittadinanza italiana (ISTAT 29_849 via SDMX)
--
-- Grano: anno x territorio (nazionale/ripartizione/regione/provincia) x
-- ex-cittadinanza x processo di acquisizione.
-- `aggregato` = la riga non e' una "foglia": territorio non-standard
-- (livello='aggregato': macro-aree ITCD/ITFG, ITDA, ...) OPPURE cittadinanza
-- non-paese (aree geopolitiche, WORLD, 999).
-- Nomi e classificazione da support condivisi (istat_territori, istat_cittadinanze).

select
    cast_int(r.TIME_PERIOD) as anno,
    normalize_string(r.REF_AREA) as territorio_codice,
    t.nome as territorio,
    t.livello as livello,
    normalize_string(r.MOSTREL_CCITENSHIP) as cittadinanza_codice,
    c.nome as cittadinanza,
    normalize_string(r.ACQUISITION_PROCESS) as processo_codice,
    case normalize_string(r.ACQUISITION_PROCESS)
        when 'ALL' then 'Totale'
        when 'MAT' then 'Matrimonio'
        when 'RS' then 'Residenza'
        when 'TRS' then 'Altro'
        else normalize_string(r.ACQUISITION_PROCESS)
    end as processo,
    (t.livello = 'aggregato' or c.tipo = 'aggregato') as aggregato,
    cast_int(r.value) as acquisizioni
from raw_input r
left join read_csv('{support.territori.path}', auto_detect=true, header=true) t
    on t.ref_area = normalize_string(r.REF_AREA)
left join read_csv('{support.cittadinanze.path}', auto_detect=true, header=true) c
    on c.codice = normalize_string(r.MOSTREL_CCITENSHIP)
where cast_int(r.value) is not null
