import requests
import pandas as pd
from datetime import datetime, timezone

# --- DESCARGA ---
url = "https://servicios.ine.es/wstempus/jsCache/ES/DATOS_TABLA/69553"
r = requests.get(url).json()

# --- ACUMULADORES ---
rows = []  # tabla general
por_territorio = {}  # dict de listas por región

for serie in r:
    nombre = serie["Nombre"].strip()  # ej: "Tasa de paro... Andalucia. 16 y más años."
    # Extraer territorio: está entre el texto y el tramo de "16 y más años."
    # Estrategia simple: coger la última frase antes de "16 y más años."
    # También puedes dividir por puntos y quedarte con el penúltimo token.
    partes = [p.strip() for p in nombre.split(".") if p.strip()]
    print(partes)
    # Penúltimo token suele ser el territorio (ej: "Andalucía", "Total Nacional", etc.)
    territorio = partes[-2] if len(partes) >= 2 else partes[-1]

    for dato in serie["Data"]:
        anyo = dato["Anyo"]
        valor = dato["Valor"]
        fk_periodo = dato["FK_Periodo"]  # aquí es 28 (anual)
        periodo = "Anual" if fk_periodo == 28 else fk_periodo  # por si cambia futuro

        rows.append([territorio, anyo, periodo, valor])
        por_territorio.setdefault(territorio, []).append([territorio, anyo, periodo, valor])

# --- DATAFRAMES ---
df_general = pd.DataFrame(rows, columns=["Territorio", "Año", "Periodo", "TasaParo"])

# Crear un dict de DataFrames por territorio
dfs_territorio = {t: pd.DataFrame(v, columns=["Territorio", "Año", "Periodo", "TasaParo"])
                  for t, v in por_territorio.items()}

# --- GUARDADO ---
ts = int(datetime.now(timezone.utc).timestamp())
df_general.to_csv(f"TasaParo_Todos_{ts}.csv", index=False, encoding="utf-8")


print("CSV general y CSVs por territorio guardados correctamente.")
