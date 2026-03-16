select
  {year} as anno_riferimento,
  codice_comune,
  comune,
  popolazione_residente,
  totale_maschi as popolazione_maschile,
  totale_femmine as popolazione_femminile
from clean_input
where codice_comune is not null
  and comune is not null
  and eta = 999
