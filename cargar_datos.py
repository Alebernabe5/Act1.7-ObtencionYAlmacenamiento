import requests
import pandas as pd
from datetime import datetime, timezone 

r = requests.get("https://servicios.ine.es/wstempus/jsCache/ES/DATOS_TABLA/69553").json()

#print(r) #Con esto aparece entera para comprobar si funciona
#print(r[0].keys()) #Aparece la cabecera

# Esto te mostrará los indicadores disponibles: IPC, PIB, Paro, Salarios, etc.
#for indicador in r:
 #   print(indicador['Nombre'])

tbl_periodo = [] 
tbl_ipc = []
tbl_pib = []
tbl_paro = []
tbl_salario = []


# --- FILTRADO POR INDICADOR ---
for serie in r:
    nombre = serie["Nombre"]

    for dato in serie["Data"]:
        anyo = dato["Anyo"]
        valor = dato["Valor"]

        # Periodo trimestral (igual que en tu primer script)
        if dato["FK_Periodo"] == 19:
            periodo = 1
        elif dato["FK_Periodo"] == 20:
            periodo = 2
        elif dato["FK_Periodo"] == 21:
            periodo = 3
        elif dato["FK_Periodo"] == 22:
            periodo = 4
        else:
            periodo = None

        # --- Clasificación por indicador ---
        if "IPC" in nombre:
            tbl_ipc.append([nombre, anyo, periodo, valor])
        elif "PIB" in nombre:
            tbl_pib.append([nombre, anyo, periodo, valor])
        elif "Paro" in nombre:
            tbl_paro.append([nombre, anyo, periodo, valor])
        elif "Salario" in nombre:
            tbl_salario.append([nombre, anyo, periodo, valor])

        # Tabla general con todos los indicadores
        tbl_periodo.append([nombre, anyo, periodo, valor])

# --- CREAR DATAFRAMES ---
df_general = pd.DataFrame(tbl_periodo, columns=["Indicador", "Año", "Periodo", "Valor"])
df_ipc = pd.DataFrame(tbl_ipc, columns=["Indicador", "Año", "Periodo", "Valor"])
df_pib = pd.DataFrame(tbl_pib, columns=["Indicador", "Año", "Periodo", "Valor"])
df_paro = pd.DataFrame(tbl_paro, columns=["Indicador", "Año", "Periodo", "Valor"])
df_salario = pd.DataFrame(tbl_salario, columns=["Indicador", "Año", "Periodo", "Valor"])

# --- GUARDADO LOCAL ---
fechaYhora = int(datetime.now(timezone.utc).timestamp())

df_general.to_csv(f"Indicadores_{fechaYhora}.csv", index=False, encoding="utf-8")
df_ipc.to_csv(f"IPC_{fechaYhora}.csv", index=False, encoding="utf-8")
df_pib.to_csv(f"PIB_{fechaYhora}.csv", index=False, encoding="utf-8")
df_paro.to_csv(f"Paro_{fechaYhora}.csv", index=False, encoding="utf-8")
df_salario.to_csv(f"Salario_{fechaYhora}.csv", index=False, encoding="utf-8")

print("Archivos guardados correctamente.")
