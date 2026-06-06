-- clean.sql: mef-irpef-regionale
-- Fonte: MEF Finanze — REG_tipo_reddito_{year}.csv
-- Struttura: riga header skip + 441 righe dati (21 classi × 21 regioni)
-- Normalizzazione: tutte le colonne a VARCHAR → cast esplicito

SELECT
  -- il year viene iniettato dal template renderer del toolkit
  {year}::INTEGER                                           AS anno_di_imposta,

  -- column00: classe di reddito (es. "minore di -1.000", "da 0 a 1.000")
  NULLIF(column00, '')::VARCHAR                   AS classe_reddito,

  -- column01: regione
  NULLIF(column01, '')::VARCHAR                   AS regione,

  -- column02: numero contribuenti
  NULLIF(regexp_replace(column02, '[.]', '', 'g'), '')::DOUBLE AS numero_contribuenti,

  -- reddito dominicale (dot = thousand sep in Italian CSV)
  NULLIF(regexp_replace(column03, '[.]', '', 'g'), '')::DOUBLE  AS reddito_dominicale_freq,
  NULLIF(regexp_replace(column04, '[.]', '', 'g'), '')::DOUBLE  AS reddito_dominicale_eur,

  -- reddito agrario
  NULLIF(regexp_replace(column05, '[.]', '', 'g'), '')::DOUBLE  AS reddito_agrario_freq,
  NULLIF(regexp_replace(column06, '[.]', '', 'g'), '')::DOUBLE AS reddito_agrario_eur,

  -- reddito allevamento
  NULLIF(regexp_replace(column07, '[.]', '', 'g'), '')::DOUBLE AS reddito_allevamento_freq,
  NULLIF(regexp_replace(column08, '[.]', '', 'g'), '')::DOUBLE AS reddito_allevamento_eur,

  -- reddito da fabbricati
  NULLIF(regexp_replace(column09, '[.]', '', 'g'), '')::DOUBLE AS reddito_fabbricati_freq,
  NULLIF(regexp_replace(column10, '[.]', '', 'g'), '')::DOUBLE AS reddito_fabbricati_eur,

  -- reddito da lavoro dipendente
  NULLIF(regexp_replace(column11, '[.]', '', 'g'), '')::DOUBLE AS reddito_lavoro_dipendente_freq,
  NULLIF(regexp_replace(column12, '[.]', '', 'g'), '')::DOUBLE AS reddito_lavoro_dipendente_eur,

  -- reddito da pensione
  NULLIF(regexp_replace(column13, '[.]', '', 'g'), '')::DOUBLE AS reddito_pensione_freq,
  NULLIF(regexp_replace(column14, '[.]', '', 'g'), '')::DOUBLE AS reddito_pensione_eur,

  -- altri redditi assimilati lavoro dipendente
  NULLIF(regexp_replace(column15, '[.]', '', 'g'), '')::DOUBLE AS altri_assimilati_ld_freq,
  NULLIF(regexp_replace(column16, '[.]', '', 'g'), '')::DOUBLE AS altri_assimilati_ld_eur,

  -- reddito da lavoro autonomo
  NULLIF(regexp_replace(column17, '[.]', '', 'g'), '')::DOUBLE AS reddito_lavoro_autonomo_freq,
  NULLIF(regexp_replace(column18, '[.]', '', 'g'), '')::DOUBLE AS reddito_lavoro_autonomo_eur,

  -- perdita da lavoro autonomo
  NULLIF(regexp_replace(column19, '[.]', '', 'g'), '')::DOUBLE AS perdita_lavoro_autonomo_freq,
  NULLIF(regexp_replace(column20, '[.]', '', 'g'), '')::DOUBLE AS perdita_lavoro_autonomo_eur,

  -- altri redditi da lavoro autonomo provvigioni
  NULLIF(regexp_replace(column21, '[.]', '', 'g'), '')::DOUBLE AS provvigioni_770_freq,
  NULLIF(regexp_replace(column22, '[.]', '', 'g'), '')::DOUBLE AS provvigioni_770_eur,

  -- reddito imprenditore contabilita ordinaria
  NULLIF(regexp_replace(column23, '[.]', '', 'g'), '')::DOUBLE AS reddito_cont_ordinaria_freq,
  NULLIF(regexp_replace(column24, '[.]', '', 'g'), '')::DOUBLE AS reddito_cont_ordinaria_eur,

  -- reddito imprenditore contabilita semplificata
  NULLIF(regexp_replace(column25, '[.]', '', 'g'), '')::DOUBLE AS reddito_cont_semplificata_freq,
  NULLIF(regexp_replace(column26, '[.]', '', 'g'), '')::DOUBLE AS reddito_cont_semplificata_eur,

  -- reddito da partecipazione
  NULLIF(regexp_replace(column27, '[.]', '', 'g'), '')::DOUBLE AS reddito_partecipazione_freq,
  NULLIF(regexp_replace(column28, '[.]', '', 'g'), '')::DOUBLE AS reddito_partecipazione_eur,

  -- perdita da partecipazione
  NULLIF(regexp_replace(column29, '[.]', '', 'g'), '')::DOUBLE AS perdita_partecipazione_freq,
  NULLIF(regexp_replace(column30, '[.]', '', 'g'), '')::DOUBLE AS perdita_partecipazione_eur,

  -- plusvalenze finanziarie
  NULLIF(regexp_replace(column31, '[.]', '', 'g'), '')::DOUBLE AS plusvalenze_freq,
  NULLIF(regexp_replace(column32, '[.]', '', 'g'), '')::DOUBLE AS plusvalenze_eur,

  -- reddito di capitale
  NULLIF(regexp_replace(column33, '[.]', '', 'g'), '')::DOUBLE AS reddito_capitale_freq,
  NULLIF(regexp_replace(column34, '[.]', '', 'g'), '')::DOUBLE AS reddito_capitale_eur,

  -- redditi diversi
  NULLIF(regexp_replace(column35, '[.]', '', 'g'), '')::DOUBLE AS redditi_diversi_freq,
  NULLIF(regexp_replace(column36, '[.]', '', 'g'), '')::DOUBLE AS redditi_diversi_eur,

  -- altri redditi da lavoro autonomo e start-up
  NULLIF(regexp_replace(column37, '[.]', '', 'g'), '')::DOUBLE AS altri_la_startup_freq,
  NULLIF(regexp_replace(column38, '[.]', '', 'g'), '')::DOUBLE AS altri_la_startup_eur,

  -- tassazione separata
  NULLIF(regexp_replace(column39, '[.]', '', 'g'), '')::DOUBLE AS tassazione_separata_freq,
  NULLIF(regexp_replace(column40, '[.]', '', 'g'), '')::DOUBLE AS tassazione_separata_eur

FROM raw_input
WHERE
  column00 IS NOT NULL
  AND column00 != ''
  AND column01 IS NOT NULL
  AND column01 != ''
  -- skip header-like rows and regioni non valide
  AND column00 != 'Classi di reddito complessivo in euro'
  AND column01 != 'Regione'
  AND column01 != 'Mancante/errata'
