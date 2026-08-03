-- mart_top_mandati — Persone con più legislature (carriere lunghe)
--
-- 1 riga = 1 persona (persona_id): numero di legislature in cui è stata
-- eletta. Nota: un deputato URI è per-legislatura (d10000_0, d10000_1...),
-- quindi l'aggregazione è per persona_id (id numerico dall'URI).
-- Risponde: chi ha avuto la carriera parlamentare più lunga?
-- (es. Meloni = 5 legislature: 15,16,17,18,19)
--
-- PK: (persona_id)

SELECT
    persona_id,
    count(DISTINCT legislatura)              AS n_legislature,
    count(DISTINCT deputato)                 AS n_mandati,
    -- nome del mandato più recente (per identificare la persona)
    ANY_VALUE(cognome)                       AS cognome,
    ANY_VALUE(nome)                          AS nome
FROM clean_input
WHERE persona_id IS NOT NULL
GROUP BY persona_id
ORDER BY n_legislature DESC, persona_id
