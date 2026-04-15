import duckdb
import os

input_file = 'out/data/raw/istat-delitti-denunciati/2024/temp/delitti_raw.txt'
output_folder = 'out/data/clean/istat-delitti-denunciati/2024'
output_file = os.path.join(output_folder, 'clean.parquet')

os.makedirs(output_folder, exist_ok=True)

try:
    conn = duckdb.connect()
    # Leggiamo il file come un unico blob e lo convertiamo in VARCHAR
    sql = f"""
    COPY (
        SELECT CAST(content AS VARCHAR) AS linea 
        FROM read_blob('{input_file}')
    ) TO '{output_file}' (FORMAT PARQUET);
    """
    conn.execute(sql)
    print(f"--- SUCCESS: {output_file} creato ---")
    
    # Verifichiamo la lunghezza della stringa caricata
    size = conn.execute(f"SELECT length(linea) FROM '{output_file}'").fetchone()[0]
    print(f"Caratteri caricati: {size} (circa {round(size/1024/1024, 2)} MB)")
except Exception as e:
    print(f"--- ERRORE: {e} ---")
