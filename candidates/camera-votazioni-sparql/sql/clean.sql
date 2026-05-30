-- Votazioni Camera: pulizia tipi e parsing date
SELECT
  TRY_CAST(favorevoli AS INTEGER) AS favorevoli,
  TRY_CAST(contrari AS INTEGER) AS contrari,
  TRY_CAST(astenuti AS INTEGER) AS astenuti,
  TRY_CAST(votanti AS INTEGER) AS votanti,
  TRY_CAST(presenti AS INTEGER) AS presenti,
  TRY_CAST(approvato AS BOOLEAN) AS approvato,
  TRY_CAST(votazioneFinale AS BOOLEAN) AS votazione_finale,
  TRY_CAST(votazioneSegreta AS BOOLEAN) AS votazione_segreta,
  TRY_CAST(richiestaFiducia AS BOOLEAN) AS richiesta_fiducia,
  titolo,
  maggioranza,
  -- data in formato AAAAMMGG (es. 20260527), arriva come BIGINT
  TRY_STRPTIME(data::VARCHAR, '%Y%m%d')::DATE AS data,
  legislatura,
  seduta,
  attoCamera AS atto_camera
FROM raw_input
