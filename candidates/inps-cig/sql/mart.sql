select
    anno,
    prestazione,
    settore,
    sum(ore_operai) as ore_operai,
    sum(ore_impiegati) as ore_impiegati,
    sum(totale_ore) as totale_ore
from clean_input
group by anno, prestazione, settore
