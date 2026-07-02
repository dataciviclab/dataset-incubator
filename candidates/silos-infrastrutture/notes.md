## Tecnico

- Granularità: singolo intervento con CUP, denominazione, localizzazione (luogo_lavori)
- Formato: CSV in ZIP (estratto con `unzip_first_csv`)
- Encoding: UTF-8 con BOM, delim `;`, decimali `,` (formato italiano)
- Anni CSV disponibili su dati.camera.it: 2016, 2018, 2019, 2020, 2021, 2022, 2024
- Schema drift significativo tra anni: nomi colonna cambiano, colonne aggiunte/rimosse, 2018 senza CUP
- `read_mode: strict` con colonne VARCHAR esplicite + parsing manuale dei numeri in clean.sql

## Cautele

- **2023 non disponibile** come CSV — solo PDF del rapporto
- **Serie storica cross-anno non omogenea**: colonne cambiano nome e struttura ogni anno (Costi al 31/08/2024 vs Costi al 31 maggio 2018 (b), ecc.)
- **Stato di attuazione non sempre popolato**: ~742 righe su 3.527 hanno stato null (sono nodi aggregati di livello superiore)
- **Costi nulli** sui lotti costruttivi di dettaglio (livello 6) — i valori sono aggregati al livello superiore
- **Join con `mit_opere_incompiute_2020`**: possibile via CUP, ma verificare overlap (SILOS ha opere strategiche/prioritarie, MIT ha opere incompiute)
- **Non tutti gli interventi hanno CUP**: ~40% mancante
