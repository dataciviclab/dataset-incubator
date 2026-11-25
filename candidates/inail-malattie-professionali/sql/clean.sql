-- INAIL malattie professionali — CLEAN
-- Fonte: CSV semestrale Italia (24 colonne, delimiter ;).
-- Microdati: ID lavoratore/caso NON inclusi nel clean (privacy).
-- Le date sono in formato gg/mm/aaaa.

SELECT
    TRY_CAST(DataRilevazione AS DATE) AS data_rilevazione,
    TRY_CAST(DataProtocollo AS DATE) AS data_protocollo,
    TRY_CAST(DataDefinizione AS DATE) AS data_definizione,
    TRY_CAST(DataMorte AS DATE) AS data_morte,
    normalize_string(SedeInailCompetente) AS sede_inail,
    normalize_string(Genere) AS genere,
    normalize_string(LuogoNascita) AS luogo_nascita,
    normalize_string(SettoreCorrelatoMalattia) AS settore_correlato,
    normalize_string(SubSettoreCorrelatoMalattia) AS sub_settore_correlato,
    normalize_string(ICD10denunciato) AS icd10_denunciato,
    normalize_string(ICD10accertato) AS icd10_accertato,
    normalize_string(AgenteCausale) AS agente_causale,
    normalize_string(QualificazioneLegge) AS qualificazione_legge,
    normalize_string(MalattiaAsbestoCorrelata) AS malattia_asbesto_correlata,
    normalize_string(DefinizioneAmministrativaCaso) AS definizione_caso,
    normalize_string(DefinizioneAmministrativaLavoratore) AS definizione_lavoratore,
    normalize_string(DefinizioneAmministrativaEsitoMortale) AS esito_mortale,
    normalize_string(Indennizzo) AS indennizzo,
    cast_int(GradoMenomazioneLavoratore) AS grado_menomazione_lavoratore,
    cast_int(GradoMenomazioneCaso) AS grado_menomazione_caso,
    cast_int(GiorniIndennizzati) AS giorni_indennizzati,
    normalize_string(Gestione) AS gestione
FROM raw_input
WHERE DataRilevazione IS NOT NULL
