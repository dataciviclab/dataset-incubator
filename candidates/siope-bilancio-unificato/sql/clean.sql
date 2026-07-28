-- clean: UNION ALL di entrate e uscite SIOPE
-- La colonna `lato` viene iniettata automaticamente dal raw tramite inject_column.
-- Le colonne divergenti (macro_categoria_v2 in entrate, macro_area/macro_categoria in uscite)
-- vengono allineate da read_parquet(union_by_name=true).

select * from raw_input;
