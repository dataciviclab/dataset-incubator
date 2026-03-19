# Notes - ispra-ru-costi-kg

## Stato tecnico

Branch di lavoro iniziale:

- `feat/ispra-ru-cross-intake`

Stato attuale:

- candidate attivo su issue `#33`
- `dataset.yml` definiti per `A/B/C`
- `clean` e `mart` minimi definiti per `A/B/C`
- notebook `v0` e `v1` disponibili
- Discussion pubblica già aggiornata: `#22`

## Architettura adottata

Pattern multi-fonte:

- `sources/a_ru_base`
- `sources/b_kg_per_abitante`
- `sources/c_costo_per_abitante`
- `compose/` finale per il cross

Scelta adottata:

- i tre `source dataset` sono stati formalizzati con anni `2020-2024`
- `A` RU base eseguito con successo su `2020-2024`
- `B` kg per abitante eseguito con successo su `2020-2024`
- `C` costo per abitante eseguito con successo su `2020-2024`
- per `B/C` il parser robusto è stato reso esplicito nel `dataset.yml` per gestire le note testuali in coda ai CSV
- `mart_cross_comuni.sql` spostato in `compose/sql/`
- il `compose/` non è eseguibile da solo: il `run mart` resta agganciato a `sources/a_ru_base/dataset.yml`
- il toolkit non consente di eseguire un SQL `mart` fuori dalla `base_dir` del dataset, quindi in `sources/a_ru_base/sql/` resta una copia eseguibile del cross
- il gate vero resta la verifica di:
  - chiavi di join
  - overlap temporale
  - qualità comparativa delle metriche

## Provenienza

Contesto legacy utile:

- `dataciviclab/projects/progetto-pilota.md`

Asset da recuperare o ricontrollare:

- parsing del dataset RU base già emerso nel pilota
- cluster demografico e logica quadranti dal `progetto-pilota`
- anni effettivamente disponibili nel cross mart locale
- livello territoriale reale e stabilità delle chiavi

## Rischi noti

- mismatch di granularità o nomenclatura territoriale
- overlap temporale troppo corto tra le tabelle
- `costo per abitante` non direttamente confrontabile senza caveat ulteriori
- il `cluster_demografico` del `v2` dipende dalla colonna `popolazione` presente in `mart_cross_comuni`: va sempre verificata la copertura effettiva prima del notebook
- possibile valore diverso dei due dataset aggiuntivi:
  - vero asse analitico del filone
  - oppure solo support dataset

## Stato reale del cross mart

Il cross mart locale è oggi disponibile per:

- `2020`
- `2023`
- `2024`

Mancano sul clone corrente:

- `2021` per la sorgente `C`
- `2022` per la sorgente `B`

Nota operativa:

- il gap è dovuto a run incompleti/lock OneDrive, non a un limite concettuale del filone

## Esito del primo step

Primo gate chiuso:

- i tre endpoint ISPRA reggono davvero su `2020-2024`
- i tre `source dataset` producono `raw`, `clean` e `mart`
- il filone ha un primo `compose` minimo eseguibile su `codice_comune_istat x anno`

Copertura join del primo compose:

- `2020`: `4397` comuni con join pieno `A + B + C` su `7628`
- `2023`: `6250` comuni con join pieno `A + B + C` su `7669`
- `2024`: `6477` comuni con join pieno `A + B + C` su `7671`

Interpretazione iniziale:

- il cross regge tecnicamente
- la copertura dei dataset costi non è ancora totale sul perimetro RU base
- il primo notebook dovrà distinguere bene:
  - perimetro completo RU
  - perimetro ridotto con join `A + B + C`

## Esito dei notebook

Notebook creati:

- `notebooks/ispra_ru_costi_kg_v0.ipynb`
- `notebooks/ispra_ru_costi_kg_v1.ipynb`

Scelte metodologiche già fissate:

- lettura pubblica limitata al perimetro con `join_b_ok` e `join_c_ok`
- focus principale sul `2024`
- contesto temporale usato nel `v1`: `2020`, `2023`, `2024`
- Discussion pubblica di riferimento: `#22`

Prime evidenze da verificare meglio:

- la copertura del join cresce in modo netto tra `2020` e `2024`
- nel perimetro joinato `2024` la relazione tra `kg RU per abitante` e `costo per abitante` è positiva
- la relazione tra `% RD` e `costo per abitante` è più debole e va letta con cautela

## Contratto minimo del v2

La v2 unisce due logiche:

- profondità metodologica del `progetto-pilota`
- asse costi del candidate `ispra-ru-costi-kg`

Perimetro approvato:

- base principale: `2024`
- contesto evolutivo: `2020`, `2023`, `2024`
- ponte con il pilota: confronto `2020 -> 2023`

Decisione metodologica già fissata in `#33`:

- il `quadrante_costo` si calcola su **livello 2024**
- le soglie sono le **mediane 2024** del campione joinato `A + B + C`
- il delta `2020 -> 2024` resta narrativa di contesto, non base della classificazione

Verifiche tecniche già chiuse:

- `codice_comune_istat` nel cross mart locale è `VARCHAR` a 6 cifre (`2020`, `2023`, `2024`)
- la colonna `popolazione` è presente in `mart_cross_comuni`
- il `cluster_demografico` prodotto dal lookup `2024` non restituisce solo `N/D`

Prossimi passi reali del `v2`:

- verificare chiave di join tra `codice_comune_istat` del cross mart e `istat_comune_6` del pilota
- tenere ISTAT popolazione come join di robustezza successivo, non come prerequisito
- completare gli anni mancanti del cross mart locale
- rieseguire `mart_compose_v2` anche sugli anni mancanti quando `B 2022` e `C 2021` saranno disponibili
- costruire il notebook `v2`

## Stato implementazione v2

Primo layer `v2` già materializzato:

- `mart_compose_v2` aggiunto al `dataset.yml` di `sources/a_ru_base`
- SQL duplicato in:
  - `sources/a_ru_base/sql/mart_compose_v2.sql`
  - `compose/sql/mart_compose_v2.sql`
- run `mart` verificato localmente su `2020`, `2023`, `2024`

Scelte implementate:

- `regione_macro` derivata da lookup fissa
- `cluster_demografico` derivato da lookup `2024` del cross mart
- `quadrante_costo` valorizzato solo per `2024`
- soglie `2024` calcolate come mediane del campione joinato `A + B + C`
- dipendenza operativa esplicita: il `2024` va materializzato prima degli altri anni per il `mart_compose_v2`

Valori osservati nel run locale:

- `soglia_rd_2024 = 73.63`
- `soglia_costo_euro_ab_2024 = 170.065`

Distribuzione `quadrante_costo` nel `2024`:

- `Virtuoso costo-performance (RD alta, costo basso)`: `2018`
- `Criticità su entrambi gli assi (RD bassa, costo alto)`: `2017`
- `Buona performance ma costo alto (RD alta, costo alto)`: `1220`
- `Costo contenuto ma performance debole (RD bassa, costo basso)`: `1219`
- `Dati mancanti`: `1197`

Distribuzione `cluster_demografico` nel `2024`:

- `<5k`: `5327`
- `5k-20k`: `1841`
- `20k-100k`: `460`
- `>100k`: `43`

## Nota metodologica sul mart cross

- i costi da `B` sono espressi in `centesimi per chilogrammo`
- i costi da `C` sono espressi in `euro per abitante`
- i due assi non sono sommabili e servono a letture diverse:
  - `cent/kg` per ragionare sul costo unitario del servizio
  - `euro/abitante` per una lettura civica più immediata del carico economico sul territorio
