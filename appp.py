import sqlite3

conn = sqlite3.connect('almacen.db')
conn.execute('''CREATE TABLE producto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    descripcion TEXT NOT NULL,
    cantidad INTEGER NOT NULL,
    precio REAL NOT NULL
)''')
conn.close()
print("Base de datos y tabla creadas correctamente.")
