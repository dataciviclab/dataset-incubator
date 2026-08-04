# Notes — senato-firmatari

## Fonte

- Endpoint SPARQL Senato: `https://dati.senato.it/sparql` (GET obbligatorio, POST 403)
- Namespace `osr:` (`http://dati.senato.it/osr/`), graph `http://dati.senato.it/ddl/19`
- **I firmatari NON sono un predicato diretto del ddl**: sono risorse
  `osr:iniziativa` collegate via `osr:iniziativa` dal ddl. La catena è:
  `ddl → iniziativa/INIZ-DDL-{n} → presentatore / primoFirmatario / tipoIniziativa / senatore`

## Quirk della fonte (verificati 2026-08-04)

- **`osr:presentatore` non esiste come predicato del ddl** — ho verificato che il
  graph ha 29 predicati per ddl e tra questi non c'è presentatore. Il predicato
  `osr:presentatore` esiste solo sulle risorse `iniziativa/*`.
- **⚠️ `osr:idDdl` ≠ URI `/ddl/N`**: sono due numerazioni diverse. Es. il ddl
  `/ddl/59716` ha `osr:idDdl = 55017`. La chiave di join con `senato-ddl` è
  `osr:idDdl` (che senato-ddl usa come `id_ddl`), NON l'id dall'URI.
- **⚠️ Un `idDdl` può avere più URI `/ddl/N`**: la stessa "pratica" è legata a
  più versioni del ddl (es. presentato alla Camera e al Senato). Per questo la
  PK del clean è `(ddl, iniziativa)`, non `(ddl_id, iniziativa)`.
- **`primoFirmatario`**: presente su ~16% delle iniziative (32/200 nel campione).
  Il resto dei firmatari è nel testo `descrIniziativa` ("ed altri") non espanso
  in risorse separate — limite della fonte, non del dataset.
- **`senatore`**: solo i firmatari senatori hanno URL `/senatore/N` (~34%).
  I presentatori "On." (deputati) e "Ministro" (governativi) non ce l'hanno.
- **`tipoIniziativa`**: presente al 100% — Parlamentare, Governativa, Regionale,
  CNEL, Popolare.
- **⚠️ WAF Senato tronca a ~10.000 righe/risposta**: la query firmatari produce
  ~38.000 righe → serve paginazione OFFSET (`pages: 4, step: 10000`). Con 3
  pagine il CSV si fermava a 30k (perdeva ~8.000 righe silenziosamente —
  scoperto confrontando col COUNT fonte: 34.761 iniziative vs 29.522 catturate).
- **`dataAggiuntaFirma`/`dataRitiroFirma`**: la fonte le fornisce in formato ISO
  (es. 2023-05-26), NON YYYYMMDD — il clean le casta direttamente a DATE.

## Volumi

- DDL con metadati (graph ddl/19): 5.124
- Iniziative/presentatori totali: **37.992** (4 pagine — completo)
- idDdl distinti: 4.659 — match 100% con `senato-ddl`
- Con `data_aggiunta_firma`: 6.731 · con `data_ritiro_firma`: 161
- Con `deputato_url` (link Camera): 21.755 · con `senatore_id`: 12.792
- Firma media: ~8.1 iniziative per idDdl

## Limiti dichiarati

- **NON risponde "tutti i firmatari"**: il graph espande i presentatori dichiarati
  (per idDdl), non l'elenco completo "ed altri" del testo `descrIniziativa`.
- Presentatori non-senatori (deputati, ministri) inclusi con `senatore_id = NULL`.
