select
  anno_riferimento,
  codice_regione,
  descrizione_regione,
  codice_ente_ssn,
  codice_ente_bdap,
  descrizione_ente,
  codice_voce_contabile,
  descrizione_voce_contabile,
  consumi_sanitari,
  consumi_non_sanitari,
  prestazioni_sanitarie,
  servizi_sanitari,
  servizi_non_sanitari,
  personale_sanitario,
  personale_professionale,
  personale_tecnico,
  personale_amministrativo,
  ammortamenti,
  sopravvenienze_e_insussistenze,
  altri_costi,
  importo_totale
from clean_input
where codice_ente_ssn <> '000'
