-- mart.sql: mef-irpef-regionale
-- Aggregato per regione × anno: distribuzione reddito e contribuenti
-- Fonte: REG_tipo_reddito

WITH base AS (
  SELECT
    anno_di_imposta,
    regione,
    classe_reddito,
    numero_contribuenti
  FROM clean_input
),
rank_classi AS (
  -- Ordine sintetico delle classi di reddito per analisi di vulnerabilita
  SELECT
    anno_di_imposta,
    regione,
    classe_reddito,
    numero_contribuenti,
    CASE classe_reddito
      -- fascia inferiore: negativo/zero/basso (ordinali 1-3)
      WHEN 'minore di -1.000'          THEN 1
      WHEN 'da -1.000 a 0'             THEN 2
      WHEN 'zero'                       THEN 3
      -- fascia media-bassa (ordinali 4-16)
      WHEN 'da 0 a 1.000'               THEN 4
      WHEN 'da 1.000 a 1.500'           THEN 5
      WHEN 'da 1.500 a 2.000'           THEN 6
      WHEN 'da 2.000 a 2.500'           THEN 7
      WHEN 'da 2.500 a 3.000'           THEN 8
      WHEN 'da 3.000 a 3.500'           THEN 9
      WHEN 'da 3.500 a 4.000'           THEN 10
      WHEN 'da 4.000 a 5.000'           THEN 11
      WHEN 'da 5.000 a 6.000'           THEN 12
      WHEN 'da 6.000 a 7.000'           THEN 13
      WHEN 'da 7.000 a 8.000'           THEN 14
      WHEN 'da 8.000 a 9.000'           THEN 15
      WHEN 'da 9.000 a 10.000'          THEN 16
      -- fascia superiore: >= 10.000 euro/anno (ordinali 17-21)
      WHEN 'da 10.000 a 15.000'         THEN 17
      WHEN 'da 15.000 a 20.000'         THEN 18
      WHEN 'da 20.000 a 25.000'         THEN 19
      WHEN 'da 25.000 a 30.000'         THEN 20
      WHEN 'maggiore di 30.000'         THEN 21
      ELSE 99
    END AS classe_ordinale
  FROM base
)
SELECT
  anno_di_imposta,
  regione,
  SUM(numero_contribuenti)                          AS totale_contribuenti,
  -- fascia inferiore: classi con reddito <= 0 o 0-1.000 euro/anno (ordinale 1-3)
  SUM(CASE WHEN classe_ordinale <= 3  THEN numero_contribuenti ELSE 0 END)  AS contribuenti_fascia_inferiore,
  -- fascia superiore: classi con reddito >= 10.000 euro/anno (ordinale 17-21)
  SUM(CASE WHEN classe_ordinale >= 17 THEN numero_contribuenti ELSE 0 END)  AS contribuenti_fascia_superiore,
  ROUND(
    SUM(CASE WHEN classe_ordinale <= 3 THEN numero_contribuenti ELSE 0 END)::DOUBLE
    / NULLIF(SUM(numero_contribuenti), 0) * 100,
    2
  )                                                 AS pct_fascia_inferiore,
  ROUND(
    SUM(CASE WHEN classe_ordinale >= 17 THEN numero_contribuenti ELSE 0 END)::DOUBLE
    / NULLIF(SUM(numero_contribuenti), 0) * 100,
    2
  )                                                 AS pct_fascia_superiore,
  COUNT(DISTINCT classe_reddito)                    AS num_classi_presente
FROM rank_classi
GROUP BY anno_di_imposta, regione
ORDER BY anno_di_imposta, regione