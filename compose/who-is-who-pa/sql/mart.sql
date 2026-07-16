-- Mart: who-is-who-pa — pass-through
-- Serve come tabella dimensionale completa per navigazione ente→ufficio→responsabile

SELECT * FROM clean_input
ORDER BY denominazione_ente, descrizione_uo
