# mase_consumi_petroliferi

Consumi petroliferi in Italia **per prodotto**, serie storica mensile.

**Fonte**: MASE — Statistiche energetiche e minerarie (SISEN), *Consumi petroliferi*
→ [sisen.mase.gov.it/dgsaie/consumi-petroliferi](https://sisen.mase.gov.it/dgsaie/consumi-petroliferi)
(source_id: `mase_dgsaie`)

**Domanda civica**: quanto petrolio consumiamo e come cambia il mix tra benzina,
gasolio, GPL e bitumi? La transizione si vede nei consumi?
([Discussion #462](https://github.com/orgs/dataciviclab/discussions/462))

## Perimetro

- **Periodo**: **2002-2025**
- **Unità**: prodotto × mese (nazionale)
- **Metrica**: `consumo_kt` — migliaia di tonnellate (,000 tonn.)
- **Prodotti**: benzina, carboturbo, gasolio, olio combustibile, lubrificanti, GPL,
  bitumi + `totale prodotti principali`

## Output

- `clean` — `anno, mese, prodotto, consumo_kt`
- `mart_consumi_mensili` — come clean + `quota_pct` sul totale mensile
- `mart_consumi_annuali` — aggregato annuo + `quota_pct`

## Come girare

```bash
TOOLKIT_ALLOW_SCRIPT_SOURCE=1 toolkit run -c candidates/mase-consumi-petroliferi/dataset.yml --year 2025
toolkit inspect -c candidates/mase-consumi-petroliferi/dataset.yml -y 2025
```

`preprocess.py` scarica i 24 file annuali (2002-2025) e li normalizza. `2025` è
**nominale** (rilascio più recente), non un filtro.

## Cosa dice la serie (kt/anno)

| | 2002 | 2007 | 2013 | 2020 | 2025 |
|---|---|---|---|---|---|
| benzina | 16.070 | 11.892 | 8.025 | 5.785 | **8.937** |
| gasolio | 26.717 | 30.684 | 25.915 | 23.073 | 25.799 |
| GPL | 3.719 | 3.140 | 3.282 | 2.934 | 3.226 |
| **totale** | 68.303 | 58.957 | 44.241 | 36.214 | **45.511** |

La benzina si è **quasi dimezzata** dal 2002 al 2013, poi si è stabilizzata e dal
2020 **risale** (+54% sul minimo COVID). Il totale è sceso del 33% in 20 anni.

## Incroci disponibili in Lab

- `mase_prezzi_carburanti_mensili` / `_settimanali` — prezzi vs volumi (stesso publisher)
- `aci_parco_comune` / `aci_prime_iscrizioni_autovetture` — parco veicoli per alimentazione
- `ispra_emissioni_ghg` — emissioni del settore trasporti
- `mase_gas_consumi` — confronto gas vs petrolio

## Limiti noti

- Estratti i **prodotti di sintesi**; le ripartizioni "di cui" (rete/extrarète,
  autotrazione, termoelettrica) sono nel foglio ma non nel v0
- Alcuni file contengono **più anni in fogli diversi** (es. 2023 → 2021, 2022, 2023):
  il preprocess tiene solo l'anno del file, per non duplicare le serie
- Licenza MASE non dichiarata sul portale → da chiarire prima della pubblicazione
