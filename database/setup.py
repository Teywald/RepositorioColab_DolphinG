# Hola guapos, esta es la parte donde se crea la base de datos en SQLite3, basicamente con solo ejecutarlo ya queda creada la base de datos

import sqlite3 #la libreria que usamos, sirve para manejar y crear bases de datos

conn = sqlite3.connect("dolphin_green.db")
cursor = conn.cursor()

# Crearmos las tablas para almacenar información
cursor.execute("""
CREATE TABLE IF NOT EXISTS Reserva(
    Id INTEGER PRIMARY KEY,
    NombreCliente TEXT,
    Documento INTEGER,
    NumeroContacto TEXT,
    Correo TEXT,
    Direccion TEXT,
    NumeroPersonas INTEGER,
    FechaLlegada TEXT,
    FechaSalida TEXT,
    Estado INTEGER DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS ParametrosCotizacion(
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    ValorNocheCabanaTempAlta INTEGER,
    ValorNocheCabanaTempBaja INTEGER,
    ValorCocinera INTEGER,
    ValorAuxCocina INTEGER,
    Deposito INTEGER
)
""")

cursor.execute("""
CREATE TABLE Temporada(
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Nombre VARCHAR,
    FechaInicio TEXT,
    FechaFin TEXT
)         
""")

cursor.execute("""
    INSERT INTO ParametrosCotizacion
    (Id, ValorNocheCabanaTempAlta, ValorNocheCabanaTempBaja, ValorCocinera, ValorAuxCocina, Deposito)
    VALUES (?, ?, ?, ?, ?, ?)
""", (1, 1800000, 1200000, 60000, 50000, 400000))

conn.commit()
conn.close()