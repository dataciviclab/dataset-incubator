-- Mart: bdap_anagrafe_enti
-- Support dataset: pass-through, nessuna aggregazione

SELECT
  *
FROM clean_input
WHERE id_ente IS NOT NULL
;
