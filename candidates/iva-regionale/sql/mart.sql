-- mart.sql — iva_regionale
SELECT
    anno, regione, cod_regione, contribuenti,
    volume_affari_eur, acquisti_eur, va_fiscale_eur,
    imposta_dovuta_eur, imposta_credito_eur
FROM clean_input
