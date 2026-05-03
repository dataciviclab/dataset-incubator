select
    anno,
    prestazione,
    settore,
    settore_specifiche,
    case
        when "Ore_autorizzate_agli_Operai" = '.' then null
        else try_cast("Ore_autorizzate_agli_Operai" as double)
    end as ore_operai,
    case
        when "Ore_autorizzate_agli_Impiegati" = '.' then null
        else try_cast("Ore_autorizzate_agli_Impiegati" as double)
    end as ore_impiegati,
    case
        when "Totale_ore_autorizzate" = '.' then null
        else try_cast("Totale_ore_autorizzate" as double)
    end as totale_ore
from raw_input
where
    -- escludi righe di solo totale (sono aggregati di riga, non dati atomici)
    settore_specifiche not ilike '%totale%'
    and trim(settore_specifiche) != ''
    and settore_specifiche is not null
