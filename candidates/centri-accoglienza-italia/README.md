# centri-accoglienza-italia

Centri di accoglienza per migranti in Italia: CAS, CPA e Hotspot.

**Fonte**: Centri d'Italia (ActionAid Italia + Fondazione Openpolis)
**Licenza**: CC-BY 4.0

## Domanda

Quante persone immigrate vengono accolte in Italia, dove, a che costo, e in che tipo di struttura? Esiste uno squilibrio territoriale tra posti disponibili e arrivi?

## Dataset

Singolo centro di accoglienza con data di rilevazione. Il file CSV contiene tutti gli anni 2018-2024.

- **Copertura**: 2018–2024 (7 anni)
- **Granularità**: singolo centro (centro_id), con geografia completa (comune, provincia, regione con codici ISTAT)
- **Record**: ~47.400
- **Metriche**: capienza, presenze_giornaliere, costo_giornaliero_per_ospite (€/giorno)
- **Tipologie**: CAS ADULTI, CAS MINORI, CPA, HOTSPOT
- **Info gestionali**: ente_gestore, procedura_affidamento, operativita, date convenzione

## Output minimo atteso

- Mart aggregato per anno × regione × tipologia centro (capienza totale, presenze, costo medio, tasso occupazione)
- Notebook v0 che confronta capacità accoglienza regionale con arrivi (da onData sbarchi)

## Criterio di promozione

- Mart con dati consistenti su tutti gli anni
- Join validato con comuni_master via comune_codice_istat

## Stato

- intake (#595)

## Prossimo passo

- Arricchire con dati SAI (progetti e strutture) come mart aggiuntivo
- Notebook di analisi territoriale
