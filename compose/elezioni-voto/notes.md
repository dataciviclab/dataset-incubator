# Note tecniche — elezioni-voto

## Schema di normalizzazione

Il compose unisce 3 dataset con schemi diversi aggiungendo `tipo_elezione` e allineando i nomi delle colonne. DuckDB `UNION ALL BY NAME` allinea automaticamente le colonne mancanti a NULL.

### Mapping colonne fonte → compose

| Colonna compose | comunali | europee | regionali |
|---|---|---|---|
| `data_elezione` | ✅ | ✅ | ✅ |
| `tipo_elezione` | 'comunali' | 'europee' | 'regionali' |
| `regione` | ✅ | ✅ | ✅ |
| `provincia` | ✅ | ✅ | ✅ |
| `comune` | ✅ | ✅ | ✅ |
| `circoscrizione` | ❌ (NULL) | ✅ | ✅ |
| `elettori` | ✅ | ✅ | ✅ |
| `votanti` | ✅ | ✅ | ✅ |
| `schede_bianche` | ✅ | ✅ | ✅ |
| `affluenza_pct` | calcolata | calcolata | calcolata |
| `lista` | ✅ | ✅ | ✅ |
| `voti_lista` | ✅ | ✅ | ✅ |
| `candidato` | ✅ | ❌ (NULL) | ✅ |
| `voti_candidato` | ✅ | ❌ (NULL) | ✅ |
| `turno` | ✅ | ❌ (NULL) | ❌ (NULL) |
| `seggi_lista` | ✅ | ❌ (NULL) | ❌ (NULL) |

**Non passate nel compose** (presenti in alcuni sorgenti ma non normalizzate):
- `elettori_maschi`, `votanti_maschi` (solo comunali)
- `elettori_uomini`, `votanti_uomini` (solo referendum)
- `seggi_lista` (solo comunali)

Se servono, vanno aggiunte come colonne opzionali nel clean.sql.

## Dataset non inclusi

Due dataset elettorali hanno struttura troppo diversa per essere uniti senza forzare troppi NULL:

| Dataset | Perché escluso |
|---|---|
| `elezioni_politiche` | Camera/Senato, candidati uninominali, collegi, dati anagrafici candidati, 1948-2022. Schema molto più ricco e diverso. Merita compose autonomo. |
| `elezioni_referendum` | Voti SI/NO, nessuna lista, nessun candidato, granularità provinciale pre-2011. Struttura non compatibile. |

## Qualità dati

### Run 2026-07-28

| Metrica | Valore |
|---|---|
| Righe clean | 1.351.089 |
| Colonne clean | 16 |
| Tornate coperte | 23 (3 tipi) |
| Comuni distinti (europee) | ~9.200 |
| Readiness | needs-review (7/8) |

### Anomalie note nei dati sorgente

**1. Affluenza > 100% in tornate pre-2000 (dato Eligendo)**

In alcune tornate storiche (1979-2014), il dato `elettori` risulta sottostimato per un numero limitato di comuni, producendo un'affluenza calcolata > 100%.

- **Causa**: errore nei dati originali Eligendo, non nel compose
- **Impatto**: ~100 comuni su 1.35M righe (0.007%)
- **Distribuzione**: 37 nel 1979, 30 nel 1984, 16 nel 1989, 4 nel 1994, 3 nel 1999, 5 nel 2004, 2 nel 2009, 1 nel 2014
- **Dal 2019: zero anomalie** — dato pulito
- **Esempio**: Rosà (VI) 1999 — 552 elettori, 7.456 votanti (1.350%). La somma voti liste (7.019) conferma che l'errore è sugli elettori, non sui votanti.
- **Mitigazione**: per analisi che richiedono precisione assoluta sull'affluenza, escludere tornate pre-2019 o filtrare `WHERE affluenza_pct <= 100`

**2. Minerbe (VR) — votanti = 0 (europee 2024)**

Eligendo riporta 3.794 elettori e 0 votanti, ma le 12 liste totalizzano 1.663 voti. Il campo `votanti` non è stato popolato.
- **Impatto**: affluenza = 0% per questo comune (calcolata su votanti=0)
- **Mitigazione**: escludere dalla media se si calcola l'affluenza; per analisi sui voti alle liste è utilizzabile

**3. Comuni con < 100 elettori**

~50 comuni, prevalentemente frazioni alpine (CN, TO, IM), hanno meno di 100 elettori. L'affluenza in questi comuni è molto alta (82-94%) ma statisticamente rumorosa. È un fenomeno reale (comunità piccole = partecipazione alta) non un errore.

## Performance

| Macchina | Tempo |
|---|---|
| Locale (7.5GB RAM) | ~8s (raw+clean+mart) |
| CI (GitHub Actions 7GB) | ~5s stimato |

Il compose è leggero perché non esegue preprocess — legge direttamente parquet già puliti su GCS. L'unione di 23 tornate è gestita da DuckDB in memoria.

## Manutenzione

Quando esce una nuova tornata elettorale per uno dei 3 tipi:
1. Aggiungere l'URL GCS del nuovo anno in `sql/clean.sql` nella CTE corrispondente
2. Eseguire `toolkit run full --years 2026`
3. Pushato su GCS dal post-merge CI

Esempio — nuova europea 2029:
```sql
-- Aggiungere in cima alla lista europee:
'https://storage.googleapis.com/dataciviclab-clean/elezioni_europee/2029/elezioni_europee_2029_clean.parquet',
```
