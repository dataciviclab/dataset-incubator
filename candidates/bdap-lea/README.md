# bdap-lea

Fonte: OpenBDAP - Modello LEA degli enti del SSN.

Discussion pubblica di riferimento:
- `dataciviclab` Datasets #179

Issue intake:
- `dataset-incubator` #113

## Domanda guida

Quanto pesa la prevenzione collettiva nel consuntivo 2024 delle ASL italiane, e quanto varia questo peso tra enti e territori quando si escludono le aggregazioni regionali?

## Perimetro v0

- solo annualita `2024`
- soli enti operativi (`Codice Ente SSN != '000'`)
- granularita per ente SSN e regione
- nessun confronto storico completo nel primo ciclo

## Dataset

- fonte: Ragioneria Generale dello Stato / OpenBDAP
- formato: CSV
- delimitatore: `;`
- encoding atteso: `cp1252` / `latin-1`
- accesso: usare il dump HTTPS del datastore CKAN

## Perche vale la pena testarlo

- fonte civicamente forte su spesa sanitaria di consuntivo
- buon test reale del plugin CKAN su un caso non banale ma stretto
- consente un v0 leggibile senza partire subito dalla serie 2012-2024

## Output minimo atteso

- `clean` con colonne guida normalizzate sul 2024
- `mart` minimo per enti operativi
- notebook v0 di lettura prudente sulla prevenzione collettiva

## Criterio di promozione

- run reale riuscito
- mart leggibile e coerente col perimetro v0
- gestione esplicita di HTTPS, encoding e aggregazioni regionali

## Stato

- intake

## Prossimo passo

- verificare `effective_root`
- eseguire un primo `run all`
- classificare il candidate come `runnable` o `scaffolded_with_blocker`
