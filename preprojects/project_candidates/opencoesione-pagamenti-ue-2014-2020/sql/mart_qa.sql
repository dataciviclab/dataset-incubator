select
  regione,
  tema_sintetico as tema,
  count(*) as n_progetti,
  sum(finanz_ue) as finanz_ue_tot,
  sum(tot_pagamenti) as tot_pagamenti_tot,
  case
    when sum(finanz_ue) > 0 then sum(tot_pagamenti) / sum(finanz_ue)
    else null
  end as ratio_spesa
from clean_input
group by 1, 2
having
  case
    when sum(finanz_ue) > 0 then sum(tot_pagamenti) / sum(finanz_ue)
    else null
  end < 0.05
order by ratio_spesa asc nulls last, finanz_ue_tot desc
