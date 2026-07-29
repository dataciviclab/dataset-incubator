# elezioni-voto (compose)

**Dataset**: `elezioni_voto`
**Tipo**: compose — unisce 3 dataset elettorali in uno schema normalizzato

## Cos'è

Vista unificata del voto in Italia per elezioni **comunali**, **europee** e **regionali**.
Ogni riga = comune × lista × tornata. Schema comune con `tipo_elezione` come dimensione.

**Volume**: 1.35M righe, 23 tornate (1979-2024), ~9.200 comuni.

## Copertura

| Dataset | Tornate | Periodo | Righe |
|---|---|---|---|
| `elezioni_comunali` | 7 | 2016–2024 | 43K |
| `elezioni_europee` | 10 | 1979–2024 | 1.19M |
| `elezioni_regionali` | 6 | 2018–2024 | 118K |

## Schema clean (16 colonne)

| Dimensione | Colonne |
|---|---|
| 🔑 Chiave | `data_elezione`, `tipo_elezione` |
| 📍 Territorio | `regione`, `provincia`, `comune`, `circoscrizione` |
| 👥 Affluenza | `elettori`, `votanti`, `schede_bianche`, `affluenza_pct` |
| 🗳️ Voto | `lista`, `voti_lista`, `candidato`, `voti_candidato`, `turno`, `seggi_lista` |

## Mart analitici

| Mart | Granularità | Cosa produce |
|---|---|---|
| `mart_sintesi` | comune × tornata × tipo | Affluenza %, gap vs media provinciale/regionale/nazionale, fascia |
| `mart_trend` | comune × tipo_elezione | CAGR affluenza, variazione assoluta, prima/ultima tornata |
| `mart_liste` | provincia × lista × anno | % voti per lista, rank, HHI concentrazione, gap primo/secondo |

## Fonti

| Dataset | Periodo | Provenienza |
|---|---|---|
| `elezioni_comunali` | 2016–2024 | Eligendo — DAIT Ministero dell'Interno |
| `elezioni_europee` | 1979–2024 | Eligendo — DAIT Ministero dell'Interno |
| `elezioni_regionali` | 2018–2024 | Eligendo — DAIT Ministero dell'Interno |

Tutti i dataset sorgente sono pubblicati su GCS come `dataciviclab-clean/{slug}/{year}/...`.

## Join model

```
elezioni_voto (1.35M righe)
 ├── elezioni_comunali (2016-2024) — comune × candidato × lista × turno
 ├── elezioni_europee  (1979-2024) — comune × lista
 └── elezioni_regionali (2018-2024) — comune × candidato × lista
```

I 3 dataset sono uniti via `UNION ALL BY NAME` con aggiunta della colonna `tipo_elezione`.
Le colonne specifiche di ogni tipo (`candidato`, `turno`, `seggi_lista`, `circoscrizione`) sono NULL per i tipi che non le hanno.

## Domande che risponde

| Mart | Esempi |
|---|---|
| `mart_sintesi` | "La mia città vota più o meno della media regionale?" "Quali comuni hanno l'affluenza più alta?" |
| `mart_trend` | "L'affluenza cala più al Nord o al Sud?" "Quali comuni sono cresciuti di più?" |
| `mart_liste` | "Quale lista domina in ogni provincia?" "Quanto è concentrato il voto?" |

## Run

```bash
toolkit run full --config compose/elezioni-voto/dataset.yml --years 2026
```

## Limiti noti

Vedi `notes.md` per:
- Anomalie nei dati Eligendo pre-2000 (affluenza > 100%)
- Minerbe (VR) 2024 — votanti non riportato
- Schema `elezioni_referendum` e `elezioni_politiche` non inclusi (hanno struttura diversa — vedi design docs)
