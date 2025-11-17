#Creación Base de Datos

# colores
rojo = '\033[91m'
amarillo = '\033[93m'
turquesa = '\033[38;5;44m'
reset = '\033[0m'

import sqlite3

DB_NAME = 'proyecto_datos.db'

def crear_base_datos():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # Crear tabla de PERIODOS 
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tbl_periodo (
            id_periodo INTEGER PRIMARY KEY AUTOINCREMENT,
            anio INTEGER NOT NULL,
            mes INTEGER,
            fecha_iso TEXT NOT NULL UNIQUE
        );
        """)
        print(f"\n{turquesa}Tabla{reset} {amarillo}'tbl_periodo'{reset}{turquesa} creada o ya existente.{reset}")

        # Crear tabla de IPC 
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tbl_ipc (
            id_periodo INTEGER PRIMARY KEY,
            variacion_anual_general REAL,
            FOREIGN KEY (id_periodo) REFERENCES tbl_periodo(id_periodo)
        );
        """)
        print(f"{turquesa}Tabla {reset}{amarillo}'tbl_ipc'{reset}{turquesa} creada o ya existente.{reset}")

        # Crear tabla de TASA DE PARO
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tbl_paro (
            id_periodo INTEGER,
            sexo TEXT,
            tasa_paro REAL,
            PRIMARY KEY (id_periodo, sexo),
            FOREIGN KEY (id_periodo) REFERENCES tbl_periodo(id_periodo)
        );
        """)
        print(f"{turquesa}Tabla{reset}{amarillo} 'tbl_paro'{reset}{turquesa} creada o ya existente.{reset}")
        
        # Crear tabla de SALARIO MEDIO 
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tbl_salario (
            id_periodo INTEGER,
            decil INTEGER,
            salario_bruto REAL,
            PRIMARY KEY (id_periodo, decil),
            FOREIGN KEY (id_periodo) REFERENCES tbl_periodo(id_periodo)
        );
        """)
        print(f"{turquesa}Tabla{reset}{amarillo} 'tbl_salario'{reset}{turquesa} creada o ya existente.{reset}")
        
        # Crear tabla de PIB 
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tbl_pib (
            id_periodo INTEGER PRIMARY KEY,
            variacion_anual REAL,
            FOREIGN KEY (id_periodo) REFERENCES tbl_periodo(id_periodo)
        );
        """)
        print(f"{turquesa}Tabla{reset}{amarillo}'tbl_pib'{reset}{turquesa} creada o ya existente.{reset}")
        print()
        


        # Confirmar los cambios
        conn.commit()

    except sqlite3.Error as e:
        print(f"{rojo}Error al crear la base de datos {e}{reset}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    crear_base_datos()