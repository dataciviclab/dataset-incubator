# Note — mortalita-istat-evitabile

## Metodologia

Tre mart con diversa granularità metodologica:

| Mart | Cosa misura | Uso |
|---|---|---|
| `v1` | Mortalità totale 30+ (`cod_causa=25`) | Baseline storica |
| `v2` | 12 cause Euro-2013, tasso grezzo 30+ | Proxy di supporto |
| `v3` | 12 cause Euro-2013, broad age-standardization 30+ ⭐ | **Baseline raccomandata** |

## Rischi noti

- **Esclusione cod_territorio=4**: Trentino-Alto Adige aggregato escluso (doppio conteggio con PA Bolzano/Trento)
- **Filtri fissi**: `cod_sesso=3` (totale), `cod_classe_eta=9` (30+), `cod_titolo_studio=9` (totale)
- **v3**: age-standardization su 3 bande larghe (30-69, 70-84, 85+) — non sostituisce ESP2013 piena
- **Fonte ISTAT**: URL ZIP (`Tavole.zip`) potrebbe cambiare con le pubblicazioni annuali
- **Sheet name**: `d_base_2022` potrebbe variare negli anni successivi
