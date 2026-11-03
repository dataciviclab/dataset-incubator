-- Mart: riepilogo CER per regione
-- Risponde a: dove nascono le comunità energetiche e con che potenza?
SELECT
    regione,
    count(*) AS n_cer,
    round(sum(potenza_kw), 2) AS potenza_kw_totale,
    sum(n_impianti) AS n_impianti_totale,
    sum(n_utenze) AS n_utenze_totale,
    round(avg(potenza_kw), 2) AS potenza_kw_media,
    round(avg(n_utenze), 1) AS n_utenze_medio
FROM clean_input
GROUP BY regione
ORDER BY n_cer DESC
