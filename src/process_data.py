import pandas as pd
import glob
import os
from tqdm import tqdm
# ---------------------------------------------------------------
# CONFIGURACIÓN INICIAL
# ---------------------------------------------------------------
ruta_raw = "../data/raw"
ruta_output = "../data/clean"
os.makedirs(ruta_output, exist_ok=True)

# Buscar todos los CSV
archivos = sorted(glob.glob(os.path.join(ruta_raw, "*.csv")))
print(f"Archivos encontrados: {len(archivos)}\n")

# ---------------------------------------------------------------
# FUNCIÓN DE LIMPIEZA POR ARCHIVO
# ---------------------------------------------------------------
def cargar_y_limpiar(path):
    df = pd.read_csv(path, sep=';', encoding='utf-8', dayfirst=True, on_bad_lines='skip', low_memory=False)
    
    # Normalizar nombres de columnas
    df.columns = (
        df.columns.str.strip()
        .str.replace(" ", "_")
        .str.replace("-", "_")
        .str.lower()
    )

    # Asegurar existencia de columnas clave
    expected_cols = ['fecha','provincia','canton','cod_parroquia','parroquia','servicio','subtipo']
    for col in expected_cols:
        if col not in df.columns:
            df[col] = None

    # Estandarizar texto (mayúsculas -> minúsculas -> formato título)
    text_cols = ['provincia','canton','parroquia','servicio','subtipo']
    for c in text_cols:
        df[c] = (
            df[c].astype(str)
            .str.strip()
            .str.title()
            .replace('Nan', pd.NA)
        )

    # Convertir cod_parroquia a texto
    df['cod_parroquia'] = df['cod_parroquia'].astype(str).str.replace('.0','', regex=False)

    # Convertir fecha a datetime
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce', dayfirst=True)

    # Eliminar filas con datos faltantes críticos
    df = df.dropna(subset=['fecha','provincia','servicio'])

    # Quitar registros de "Zona No Delimitada"
    df = df[df['provincia'] != 'Zona No Delimitada']
    df = df[df['provincia'] != '0']
    cols_group = ['fecha','provincia','canton','cod_parroquia','parroquia','servicio','subtipo']
    df_grouped = (
        df.groupby(cols_group)
          .size()
          .reset_index(name='cantidad_eventos')
    )
    
    return df_grouped

dfs = []
for archivo in tqdm(archivos, desc="Procesando archivos ECU911", ncols=80):
    df_clean = cargar_y_limpiar(archivo)
    dfs.append(df_clean)

data = pd.concat(dfs, ignore_index=True)
print("Total de filas después de limpieza básica:", len(data))
path_out = os.path.join(ruta_output, "ecu911_emergencias_2021_2025.parquet")
data.to_parquet(path_out, index=False)
print(f"Archivo limpio guardado en: {path_out}")