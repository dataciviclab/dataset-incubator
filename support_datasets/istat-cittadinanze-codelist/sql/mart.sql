-- mart_cittadinanze: codice -> nome + tipo (paese/aggregato), per join nei candidate.
select codice, nome, tipo
from clean_input
order by tipo, codice
