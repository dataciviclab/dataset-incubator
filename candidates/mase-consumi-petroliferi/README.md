# mase_consumi_petroliferi

Consumi petroliferi in Italia **per prodotto**, mensile.

**Fonte**: MASE — Statistiche energetiche e minerarie (SISEN)
→ [sisen.mase.gov.it/dgsaie/consumi-petroliferi](https://sisen.mase.gov.it/dgsaie/consumi-petroliferi)
(source_id: `mase_dgsaie`)

**Domanda civica**: quanto petrolio consumiamo e come cambia il mix tra benzina,
gasolio, GPL e bitumi? La transizione si vede nei consumi?
([Discussion #462](https://github.com/orgs/dataciviclab/discussions/462))

## Perimetro v0

- **Anno**: 2025 (primo taglio; la fonte copre 2002-2025)
- **Unità**: prodotto × mese (nazionale)
- **Metrica**: `consumo_kt` — migliaia di tonnellate (,000 tonn.)
- **Prodotti**: benzina, carboturbo, gasolio, olio combustibile, lubrificanti, GPL,
  bitumi + `totale prodotti principali`

## Output

- `clean` — `anno, mese, prodotto, consumo_kt`
- `mart_consumi_mensili` — come clean + `quota_pct` sul totale mensile

## Come girare

```bash
toolkit run -c candidates/mase-consumi-petroliferi/dataset.yml --year 2025
toolkit inspect -c candidates/mase-consumi-petroliferi/dataset.yml -y 2025
```

## Incroci disponibili in Lab

- `mase_prezzi_carburanti_mensili` / `_settimanali` — prezzi vs volumi (stesso publisher)
- `aci_parco_comune` / `aci_prime_iscrizioni_autovetture` — parco veicoli per alimentazione
- `ispra_emissioni_ghg` — emissioni del settore trasporti
- `mase_gas_consumi` — confronto gas vs petrolio per settore

## Limiti noti

- v0 = **un solo anno** (2025): un file per anno, ID non deterministico → multi-anno
  richiede enumerazione CMIS (vedi `notes.md`).
- Estratti solo i **prodotti principali**; le voci "di cui" (reti, extrarète,
  autotrazione, ecc.) sono nel foglio ma non nel v0.
- Layout a blocchi affiancati (I°/II° semestre): le colonne cumulative sono ignorate.
- Licenza MASE non dichiarata sul portale → da chiarire prima della pubblicazione.
