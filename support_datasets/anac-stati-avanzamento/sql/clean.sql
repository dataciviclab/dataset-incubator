-- Macro toolkit: cast_int, cast_double
SELECT
    normalize_string(cig) AS cig,
    normalize_string(denominazione_sal) AS denominazione_sal,
    normalize_string(flag_ritardo) AS flag_ritardo,
    TRY_CAST(data_emissione_sal AS DATE) AS data_emissione_sal,
    cast_double(importo_sal) AS importo_sal,
    cast_int(n_giorni_scostamento) AS n_giorni_scostamento,
    cast_int(progressivo_sal) AS progressivo_sal,
    cast_int(id_aggiudicazione) AS id_aggiudicazione,
    TRY_CAST(DATA_CERT_PAGAMENTO AS DATE) AS data_cert_pagamento,
    cast_double(IMPORTO_CERT_PAGAMENTO) AS importo_cert_pagamento,
    cast_double(GIORNI_PROROGA) AS giorni_proroga
FROM raw_input
WHERE cig IS NOT NULL AND TRIM(cig) != ''
