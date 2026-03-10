-- mart.sql — malasanita_struttura_mortalita — mart_regioni
-- Eseguito da: sources/a_strutture_asl/dataset.yml (sezione mart)
-- Input:
--   clean_input → malasanita_a_strutture_asl (granularità ASL)
--   read_parquet → malasanita_c_strutture_ricovero (granularità struttura)
--   read_parquet → malasanita_d_mortalita_istat (granularità regione×causa×sesso×età×titolo)
-- Output: una riga per regione (21 righe attese: 19 regioni + 2 PA)
--
-- Opzione 1 — mart flat regionale per preanalysis
-- Risponde a: "Le regioni con meno personale sanitario hanno tassi di mortalità più alti?"
--
-- Opzione 3 (Power BI / approfondimento futuro):
--   Separare mart_strutture (A+C aggregato per regione) e mart_mortalita (D per regione×causa)
--   senza join nel mart. Il join viene fatto in Power BI o nel notebook, dove si può:
--   - filtrare per causa specifica (es. mortalità evitabile secondo metodologia Euro-2013)
--   - espandere per disciplina da fonte B (reparti) → correlazione per specialità
--   - drill-down per ASL invece che per regione
--
-- Nota tecnica: i path read_parquet sono relativi alla CWD del processo toolkit.
--   Eseguire sempre da dataset-incubator/ (come da CLAUDE.md e README).
--
-- Chiave di join A+C → D: nome regione normalizzato (UPPER TRIM + eccezioni CASE).
--   ⚠️ Verificare dopo primo run che tutte le 21 righe abbiano join_d_ok = true.
--   Se alcune righe hanno join_d_ok = false, aggiornare il CASE WHEN nel CTE lookup_d.

WITH

-- ─── Fonte A: personale MMG/pediatri per ASL → aggregato per regione ──────────
asl AS (
    SELECT
        anno,
        codice_regione,
        regione,
        SUM(totale_medici)    AS medici_mmg,
        SUM(totale_pediatri)  AS pediatri,
        SUM(totale_residenti) AS pop_residente
    FROM clean_input
    GROUP BY anno, codice_regione, regione
),

-- ─── Fonte C: strutture ricovero → personale e posti letto per regione ────────
strutture_raw AS (
    SELECT * FROM read_parquet(
        'out/data/clean/malasanita_c_strutture_ricovero/{year}/malasanita_c_strutture_ricovero_{year}_clean.parquet'
    )
),
strutture AS (
    SELECT
        anno,
        codice_regione,
        SUM(totale_personale)       AS personale_ospedaliero,
        SUM(medici)                 AS medici_ospedalieri,
        SUM(infermieri)             AS infermieri,
        SUM(posti_letto_previsti)   AS posti_letto_previsti,
        SUM(posti_letto_utilizzati) AS posti_letto_utilizzati
    FROM strutture_raw
    GROUP BY anno, codice_regione
),

-- ─── Fonte D: mortalità ISTAT → totale decessi per regione ───────────────────
-- Aggregazione su tutte le cause × sessi × classi età × titoli studio.
-- Assumiamo righe non sovrapponibili (ogni decesso in una sola cella).
-- ⚠️ Se la fonte D contiene righe di subtotale "Totale" per sesso/età/titolo,
--    aggiungere filtri WHERE per escluderle (es. cod_sesso NOT IN (0,9)).
mortalita_raw AS (
    SELECT * FROM read_parquet(
        'out/data/clean/malasanita_d_mortalita_istat/{year}/malasanita_d_mortalita_istat_{year}_clean.parquet'
    )
),
mortalita AS (
    SELECT
        anno,
        cod_territorio,
        territorio,
        SUM(decessi) AS decessi_totali
    FROM mortalita_raw
    GROUP BY anno, cod_territorio, territorio
),

-- ─── Lookup: nome regione A (MinSalute) → nome territorio D (ISTAT) ──────────
-- Nomi verificati su dati reali dopo primo run (2026-03-09):
--   A usa backtick in "VALLE D`AOSTA", D usa apostrofo "VALLE D'AOSTA"
--   A ha "PROV. AUTON. BOLZANO/TRENTO", D ha solo "Bolzano"/"Trento" (Title Case)
--   A ha "FRIULI VENEZIA GIULIA", D ha "FRIULI V.G." (abbreviato)
lookup_d AS (
    SELECT
        a.codice_regione,
        UPPER(TRIM(
            CASE UPPER(TRIM(a.regione))
                WHEN 'VALLE D`AOSTA'            THEN 'VALLE D''AOSTA'
                WHEN 'PROV. AUTON. BOLZANO'     THEN 'BOLZANO'
                WHEN 'PROV. AUTON. TRENTO'      THEN 'TRENTO'
                WHEN 'FRIULI VENEZIA GIULIA'    THEN 'FRIULI V.G.'
                ELSE UPPER(TRIM(a.regione))
            END
        )) AS territorio_norm
    FROM asl a
)

-- ─── Join finale ──────────────────────────────────────────────────────────────
SELECT
    a.anno,
    a.codice_regione,
    a.regione,

    -- Personale territoriale (fonte A)
    a.medici_mmg,
    a.pediatri,
    a.pop_residente,

    -- Personale e dotazione ospedaliera (fonte C)
    c.personale_ospedaliero,
    c.medici_ospedalieri,
    c.infermieri,
    c.posti_letto_previsti,
    c.posti_letto_utilizzati,

    -- Mortalità (fonte D)
    d.decessi_totali,

    -- Tassi per 100.000 residenti (denominatore: pop_residente da fonte A)
    ROUND(a.medici_mmg * 100000.0        / NULLIF(a.pop_residente, 0), 2) AS medici_mmg_per_100k,
    ROUND(c.medici_ospedalieri * 100000.0 / NULLIF(a.pop_residente, 0), 2) AS medici_osp_per_100k,
    ROUND(c.infermieri * 100000.0         / NULLIF(a.pop_residente, 0), 2) AS infermieri_per_100k,
    ROUND(d.decessi_totali * 100000.0     / NULLIF(a.pop_residente, 0), 2) AS tasso_mortalita_per_100k,

    -- Flag diagnostico: true = join con D riuscito, false = territorio non trovato
    CASE WHEN d.territorio IS NOT NULL THEN true ELSE false END AS join_d_ok

FROM asl a
LEFT JOIN strutture c
    ON  a.codice_regione = c.codice_regione
    AND a.anno = c.anno
LEFT JOIN lookup_d l
    ON  a.codice_regione = l.codice_regione
LEFT JOIN mortalita d
    ON  UPPER(TRIM(d.territorio)) = l.territorio_norm
    AND d.anno = a.anno

ORDER BY a.codice_regione
