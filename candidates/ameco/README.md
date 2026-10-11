# ameco

Previsioni macro-economiche della Commissione UE (AMECO, Spring 2026) per l'Italia e i grandi paesi europei.

**Fonte**: [AMECO database](https://economy-finance.ec.europa.eu/economic-research-and-databases/economic-databases/ameco-database_en) — DG ECFIN
**File raw**: `ameco0_csv.zip` (18 CSV wide, 35k serie totali)
**Release**: Spring 2026 Economic Forecast (file datati 2026-06-02)
**Licenza**: CC BY 4.0

## Domanda civica

Secondo le previsioni della Commissione UE, il debito e il saldo primario italiano convergono o divergono rispetto ai grandi paesi europei?

## Perché vale la pena

Il Lab ha già i dati osservati via Eurostat (`pil-intelligence`, `eurostat-debito-pil`). AMECO aggiunge ciò che Eurostat non copre:

1. **Previsioni ECFIN** 2025-2027 integrate nelle serie (Spring Forecast)
2. **Aggiustamento ciclico** del saldo di bilancio (`UBLGAP` — cyclically adjusted balance)
3. **Snowball effect** sul debito (`ADGGI` — decomposizione interesse-crescita)
4. **Peer set armonizzato** (61 paesi/aggregati nel full DB; 6 qui nel perimetro v0)

## Perimetro v0 (lean)

Duplicazione volontariamente evitata: solo le serie dove AMECO porta informazione nuova.

| Serie | Significato | Unità |
|---|---|---|
| `ZUTN` | Tasso di disoccupazione | % popolazione attiva |
| `UVGD` | PIL nominale | Mrd ECU/EUR |
| `UBLG` | Saldo netto amministrazioni pubbliche | % PIL (EDP) |
| `UDGG` | Debito consolidato amministrazioni pubbliche | % PIL (EDP) |
| `UBLGAP` | Saldo ciclicamente aggiustato | % PIL potenziale |
| `ADGGI` | Snowball effect sul debito | % PIL EDP |

Paesi: IT, DE, FR, ES + aggregati EU27, EA20.
Anni: 1960-2027 (wide→long nel clean); 2025+ = previsioni ECFIN.

## Output

| Mart | Grano | Contenuto |
|---|---|---|
| `mart_sintesi_paese` | paese × serie | Ultimo osservato + previsioni 2025-2027 |

## Criterio di promozione

- `readiness: ready` su `toolkit run`
- Valori Italia 2025 plausibili (disoccupazione ~6%, debito ~135% PIL — ordini di grandezza Spring 2026)
- Confronto IT vs DE/FR/ES sul debito coerente con Eurostat EDP per gli anni osservati

## Stato / prossimo passo

- v0: candidate lean in incubation
- Follow-up: eventuale estensione peer set, join con open-politica, overlay previsioni su dashboard esistenti
