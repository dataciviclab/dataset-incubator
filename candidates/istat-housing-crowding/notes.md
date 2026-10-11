# Note tecniche - istat-housing-crowding

## Canale (2026-10-11)

- toolkit `type: sdmx` · `IT1/33_179` v1.0 su esploradati (default dal fix toolkit #444)
- Raw senza pinning delle breakdown dimensioni (key vuota = all) → ~990 righe
  con breakdown completi; richiede toolkit con fix key completa (toolkit PR #501)
- Il mirror dbnomics esponeva solo i totali (44 righe, sola TENURE_STATUS) —
  issue #873; il canale SDMX diretto è la recovery

## Correzione mapping TENURE_STATUS

Le label ISTAT dicono `1=rent`, `2=property`. Il clean pre-recovery (#870,
canale dbnomics) mappava `1→Proprietà`, `2→Affitto` (inverted, scritto senza
riferimento alle label). Ora: `1→Affitto`, `2→Proprietà`. Le due serie del
mart si scambiano di etichetta rispetto alla versione precedente.

## Perimetro

- `REF_AREA=IT`, `DATA_TYPE=ABITAZ_AFFOLL_MED`, `MEASURE=10`
- Dato ISTAT: le breakdown esistono SOLO sul totale famiglie (TENURE=99);
  rent/property (1/2) esistono solo come righe di totale breakdown
- Clean porta tutto: tenure 1/2 (totali) + righe di totale con breakdown
  (componenti nucleo, tipologia, figli, anziani, quintile reddito,
  sesso/età/istruzione/condizione percettore), 990 righe
- Mart = righe di totale su tutte le breakdown, tenure 1/2 (44 righe:
  serie storica rent vs property)

## Run

```bash
cd candidates/istat-housing-crowding
python -m toolkit.cli.app run raw   -c dataset.yml -y 2024 --root ../../out
python -m toolkit.cli.app run clean -c dataset.yml -y 2024 --root ../../out
python -m toolkit.cli.app run mart  -c dataset.yml -y 2024 --root ../../out
```
