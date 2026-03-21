# Compose

Questa cartella documenta il layer `compose/` del filone.

Obiettivo:

- leggere i mart dei due source dataset
- aggiungere il mapping anagrafico degli enti al FSC 2025
- ottenere un primo mart leggibile per comune, ancora molto stretto

Campi minimi attesi nel mart finale:

- `username`
- `comune`
- `provincia`
- `regione`
- `popolazione`
- `capacita_fiscale`
- `fondo_perequativo`
- `dotazione_finale_fsc`
- `capacita_fiscale_procapite`
- `fondo_perequativo_procapite`
- `dotazione_finale_fsc_procapite`

Scelta adottata:

- il file SQL del compose vive anche in `compose/sql/` come riferimento architetturale
- l'esecuzione resta agganciata a `sources/a_fsc_2025/dataset.yml`, per un vincolo del toolkit sul layer `mart`
- in `sources/a_fsc_2025/sql/` resta quindi una copia eseguibile del compose

Esecuzione:

```powershell
py -m toolkit.cli.app run mart --config candidates/opencivitas-fsc-rso/sources/a_fsc_2025/dataset.yml
```
