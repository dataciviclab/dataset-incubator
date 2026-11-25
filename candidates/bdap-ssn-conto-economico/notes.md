# notes.md — bdap-ssn-conto-economico

## Source-check (2026-11-07)

Famiglia OpenBDAP: *"Modello di rilevazione del Conto Economico degli enti del SSN
a livello Regionale"* — 13 package, 2012-2024, ~1,3-1,5 MB per anno.

| verifica | esito |
|---|---|
| schema stabile 2012-2024 | ✅ stesse 7 colonne, stesso delimitatore `;`, `cp1252` |
| chiave (anno, regione, codice voce) | ✅ nessun duplicato nel 2012 e nel 2024 |
| identità `ZZ9999 = AZ − BZ + CZ + DZ + EZ − YZ` | ✅ scarto 0,00 € su 21/21 territori |
| `AZ9999` = somma voci `A.N` primo livello | ✅ 21/21 territori |
| somma regionale 2024 = file nazionale 2024 | ✅ 150,05 / 149,20 / −0,85 mld € |
| copertura territoriale | ⚠️ Calabria (`180`) assente nel 2021 |

Accesso: `https://bdap-opendata.rgs.mef.gov.it/SpodCkanApi/api/3/datastore/dump/<uuid>.csv`.
Il catalogo espone anche `/export/csv/{anno}---<Titolo>.csv`, ma il nome è fragile:
gli UUID sono preferiti.

## Scelte di mapping

1. **Perché il mart è costruito sui codici, non sulla numerazione**
   La numerazione delle voci cambia tra anni (nel 2012 le voci di costo arrivano a
   `B.16`, nel 2024 a `B.14`, e `A.3` esiste solo dal 2015 circa). I codici delle
   voci principali (`AA0010`, `BA2090`, `BZ9999`, ...) sono invece stabili su tutto
   il periodo. Le aggregazioni usano i codici; la gerarchia testuale serve solo a
   `livello`/`voce_livello1`.

2. **Perché `riga_sintesi` esiste**
   Le righe `*Z9999` sono totali di sezione pubblicati dalla fonte: sommarle alle
   voci di dettaglio produrrebbe un double-counting silenzioso. Meglio esplicitarle.

3. **Perché `altri_costi` non c'è**
   Ammortamenti e accantonamenti cambiano numerazione e composizione nel tempo.
   Il mart espone le voci stabili e lascia `totale_costi` come aggregato; chi vuole
   il residuo lo calcola come differenza.

4. **Perché `columns` è dichiarato nel `clean.read`**
   La fonte esporta tutto come testo, ma il riconoscimento automatico della data
   (`dd/mm/yyyy`) è ambiguo e il toolkit la inferiva come `DATE` in modo non
   deterministico. Dichiarando `VARCHAR` e facendo `strptime('%d/%m/%Y')` il
   parsing è esplicito. Serve anche a ignorare la colonna vuota in coda al CSV
   (ogni riga finisce con `;`).

## Note tecniche

- `readiness: ready (8/8)` su 13/13 anni, con `min_rows: 5000` sul clean e
  `min_rows: 20` sul mart.
- Righe clean per anno: 7.086 (2012) → 8.144 (2024), 436→481 voci distinte.
- Il 2019 segna un cambio di piano dei conti (428→485 voci): non è un drift di
  parsing ma nuove voci pubblicate dalla fonte.
- `P. A. Bolzano` / `P. A. Trento` hanno codici ISTAT `041`/`042`; le altre regioni
  seguono la numerazione ISTAT standard.

## Aperto

- Estendere a Conto Economico nazionale e Stato Patrimoniale (stessa struttura,
  famiglie sorelle già mappate in `_local/generated/openbdap_catalog_map.csv`).
- Pro-capite: richiede popolazione per regione e anno da dataset esterno.
- Se la fonte pubblica il 2025, aggiungere l'anno a `url_suffix_by_year` e a `years`.
