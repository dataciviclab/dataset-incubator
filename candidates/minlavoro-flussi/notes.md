# Notes — minlavoro-flussi

## Quirk della fonte

- **API OData instabile sotto richiamo ripetuto**: il catalogo risponde 403 senza User-Agent; chiamate ripetute in serie possono perdere package. L'extract.py usa retry (3 tentativi con backoff). La cache locale in `data/` (gitignored) è il modo affidabile per i run di sviluppo.
- **Colonne con nomi troncati/hash**: alcune tabelle RA usano suffissi tipo `_98F4D271` per colonne età/settore. L'extract li normalizza via `_norm_col`.
- **`Ripartizione_geografica` contiene a volte codici regione**: nelle tabelle RA 03.x e 05.x la colonna si chiama ripartizione ma contiene valori `01-PIEMONTE`. L'extract distingue via prefisso numerico.
- **Genere `Totale`**: la NOTA include righe di subtotale con `Genere=Totale`. Il clean le marca con `is_totale_genere=TRUE` per escluderle dai mart senza perderle.
- **Indicatori multipli**: le tabelle RA contengono sia valori assoluti che variazioni percentuali. I mart filtrano per indicatori di conteggio.

## Decisioni metodologiche

- **Fusione NOTA+RA**: le due pubblicazioni sono lo stesso fenomeno (comunicazioni obbligatorie). I totali nazionali coincidono esattamente sugli anni sovrapposti (2021-2023). La fusione in un'unica tabella long evita ambiguità su quale fonte usare.
- **Schema long**: 16 colonne con dimensioni nullable. Ogni riga traccia la tabella di origine via `tabella_id` per traceability completa.
- **primary_key deroga (clean)**: non dichiarata — schema long fuso con indicatori multipli e tabelle fonte sovrapposte. L'unicità reale è (tabella_id, indicatore, dimensioni). Le PK sono dichiarate nei mart.

## Rischi noti

- La fonte è un portale CKAN government con WAF: rate-limit possibile in CI.
- I CSV in `data/` sono cache locale del fetch OData (gitignored). In CI l'extract fa fetch diretto.
- La copertura 2024+ dipende dalla pubblicazione del prossimo Rapporto Annuale.

## Confronto con open-inps

- `open-inps/inps-rapporti-lavoro` copre lo stesso fenomeno via Osservatorio INPS con granularità provinciale e serie 2014-2026.
- MinLavoro aggiunge: trasformazioni, tirocini, somministrazione, qualifica professionale, motivo dettagliato.
- Il join analitico si fa su (anno, regione, genere) — non duplicare i flussi base.
