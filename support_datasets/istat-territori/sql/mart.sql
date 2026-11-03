-- mart_territori: ref_area -> nome + livello, per join nei candidate.
select ref_area, nome, livello
from clean_input
order by livello, ref_area
