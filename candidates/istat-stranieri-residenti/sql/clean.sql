-- clean.sql: stranieri residenti al 1 gennaio per provincia x cittadinanza
-- (ISTAT 29_317_DF_DCIS_POPSTRCIT1_1 via DBnomics)
--
-- `aggregato` = la riga non e' una "foglia": territorio non-standard
-- (livello='aggregato') OPPURE cittadinanza non-paese.
-- Nomi e classificazione da support condivisi.

select
    cast_int(r.TIME_PERIOD) as anno,
    normalize_string(r.REF_AREA) as territorio_codice,
    t.nome as territorio,
    t.livello as livello,
    normalize_string(r.CITIZENSHIP) as cittadinanza_codice,
    c.nome as cittadinanza,
    (t.livello = 'aggregato' or c.tipo = 'aggregato') as aggregato,
    cast_int(r.OBS_VALUE) as residenti
from raw_input r
left join read_csv('{support.territori.path}', auto_detect=true, header=true) t
    on t.ref_area = normalize_string(r.REF_AREA)
left join read_csv('{support.cittadinanze.path}', auto_detect=true, header=true) c
    on c.codice = normalize_string(r.CITIZENSHIP)
where cast_int(r.OBS_VALUE) is not null
