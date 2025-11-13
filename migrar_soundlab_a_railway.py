import mysql.connector

# --- Configuración de conexiones ---
# Base local (origen)
source = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="123456",
    database="soundlab",
    port=3306  # cambiá si tu MySQL usa otro puerto (por ej. 3307)
)


# Base Railway (destino)
target = mysql.connector.connect(
    host="shinkansen.proxy.rlwy.net",          # ejemplo: containers-us-west-xx.railway.app
    user="root",
    password="QsMudtIzMdpTWMoEFlLbylvgmIUGmJmG",
    database="railway",
    port=19227                        # o el puerto que te da Railway
)

src_cursor = source.cursor(dictionary=True)
tgt_cursor = target.cursor()

# --- Copiar tablas ---
src_cursor.execute("SHOW TABLES")
tables = [row['Tables_in_soundlab'] for row in src_cursor.fetchall()]

for table_name in tables:
    print(f"📦 Copiando tabla: {table_name}...")
    src_cursor.execute(f"SELECT * FROM {table_name}")
    rows = src_cursor.fetchall()

    if not rows:
        print(f"  (sin datos)")
        continue

    cols = ", ".join(rows[0].keys())
    placeholders = ", ".join(["%s"] * len(rows[0]))
    insert_query = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})"

    for row in rows:
        try:
            tgt_cursor.execute(insert_query, tuple(row.values()))
        except Exception as e:
            print(f"  ⚠️ Error copiando fila: {e}")

    target.commit()
    print(f"  ✅ {len(rows)} filas copiadas.")

src_cursor.close()
tgt_cursor.close()
source.close()
target.close()
print("\n✅ Migración completada con éxito.")
