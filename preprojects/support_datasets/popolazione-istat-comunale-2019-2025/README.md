# Popolazione ISTAT comunale

## Domanda

Possiamo costruire una base comunale di popolazione residente ISTAT riusabile come join affidabile per altri dataset territoriali del Lab?

## Dataset

- fonte principale: demo ISTAT `POSAS`
- copertura target nel preproject: 2019-2025
- formato sorgente: ZIP annuale con CSV comunale
- pattern URL verificato: `https://demo.istat.it/data/posas/POSAS_{year}_it_Comuni.zip`

## Perche questo support dataset vale

Questo filone non vale solo come analisi sulla popolazione.

Vale soprattutto come base infrastrutturale per:

- join con dataset comunali come `IRPEF`
- controlli di copertura territoriale
- indicatori pro capite
- doppio check su variazioni territoriali o anomalie nei dataset comunali

Non entra in `preanalysis` per default: il suo ruolo iniziale e supportare altri filoni.

## Output minimo atteso

- tabella comunale per anno con `codice_comune`, `comune`, `popolazione_residente`
- tabella per anno e classe di eta
- nota breve sui rischi di join e sui cambi territoriali da monitorare

## Stato

- intake
- `2019`, `2020` e `2025` verificati con run riuscita
- finestra completa da rilanciare quando il lock locale su `out/data/_runs` non interferisce

## Criterio di uscita

Far uscire questo support dataset da `dataset-incubator` se:

- il run e2e multi-anno e stabile
- il `clean` conserva bene il dettaglio per eta e sesso
- il `mart` comunale e utilizzabile come base di join con altri filoni
- si chiarisce dove allocarlo in modo piu stabile nel workflow del Lab

## Prossimo passo

- verificare run multi-anno `2019-2025`
- controllare stabilita minima dello schema POSAS
- usare il `mart` comunale come base per un primo join di prova con `IRPEF`
