# inpa-comunicazioni

**Comunicazioni di procedura dei concorsi inPA** — il ciclo di vita dei bandi pubblici.

Ogni concorso pubblicato su inPA genera comunicazioni di procedura: calendari prove,
commissioni esaminatrici, proroghe, pubblicazione graduatorie finali. Questo dataset
traccia quell'evoluzione, collegata al bando via `concorso_id`.

- **Fonte**: API pubblica non documentata `https://portale.inpa.gov.it/concorsi-smart/api/communication/user/public-area/search`
- **Licenza**: dati pubblici PA (D.Lgs. 33/2013)
- **Copertura**: archivio vivo, ~4.244 comunicazioni (2025-2026)
- **Granularità**: singola comunicazione con categoria (tipo di esito) e data

## Domanda civica

I concorsi pubblici arrivano davvero a una graduatoria finale? Quanto tempo passa dal
bando all'esito? Quali enti pubblicano esiti trasparenti e quali restano fermi?

## Shape

- ~4.244 comunicazioni (snapshot 2026-08), archivio 2025-2026
- Campi: id, concorso_id, concorso_title, subject, body, categoria, data_pubblicazione, ente
- Categorie: Pubblicazione Graduatoria finale, Commissione esaminatrice, Calendario prove
  orali/scritte/preselettive, Proroga termini, Altro
- Join: `concorso_id` ↔ `inpa-bandi.id` per il ciclo bando→esito

## Perché vale la pena

- Terzo lato del triangolo: bandi (inPA) × personale (conto annuale) × esiti (qui)
- Risponde a "il reclutamento PA funziona?" — dai dati, non dalle percezioni
- Incrociabile con `inpa-bandi` per i tempi bando→graduatoria

## Output minimo atteso

- Dataset clean con comunicazioni per categoria, ente, periodo
- Mart esiti per rispondere a domande su trasparenza e tempistiche del reclutamento

## Stato / prossimo passo

- [ ] Snapshot nel tempo per calcolare i tempi bando→graduatoria (serve storico)
- [ ] Join con `inpa-bandi` per il ciclo completo
