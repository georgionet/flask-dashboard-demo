#!/usr/bin/env python3
"""Crea la base de datos SQLite de demo con datos de ventas."""
import sqlite3
import random
from datetime import date, timedelta

PRODUCTOS = {
    "Notebook Dell": ("Electronica", 850000),
    "Monitor LG 27": ("Electronica", 320000),
    "Mouse Logitech": ("Electronica", 35000),
    "Teclado Mecanico": ("Electronica", 89000),
    "Camiseta Polo": ("Ropa", 25000),
    "Zapatillas Nike": ("Ropa", 89000),
    "Chaqueta Cuero": ("Ropa", 155000),
    "Jeans Levis": ("Ropa", 55000),
    "Aceite de Oliva": ("Alimentos", 12000),
    "Cafe Premium": ("Alimentos", 18000),
    "Chocolate Artesanal": ("Alimentos", 8500),
    "Vino Reserva": ("Alimentos", 22000),
    "Lampara LED": ("Hogar", 35000),
    "Silla Oficina": ("Hogar", 189000),
    "Set Toallas": ("Hogar", 28000),
    "Organizador Escritorio": ("Hogar", 15000),
}

CLIENTES = [
    "Empresa Alpha", "Beta Corp", "Gamma SpA",
    "Delta Ltda", "Epsilon SA", "Zeta Comercial",
    "Eta Servicios", "Theta Industries", "Iota Tech",
]

CIUDADES = ["Santiago", "Valparaiso", "Concepcion", "Antofagasta"]

VENDEDORES = ["Carlos Munoz", "Maria Lopez", "Pedro Soto", "Ana Rivera"]


def seed(db_path="demo.db", num_rows=60):
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    cur.execute("DROP TABLE IF EXISTS ventas")
    cur.execute("""
        CREATE TABLE ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            producto TEXT NOT NULL,
            categoria TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            precio_unitario REAL NOT NULL,
            total REAL NOT NULL,
            cliente TEXT NOT NULL,
            ciudad TEXT NOT NULL,
            vendedor TEXT NOT NULL
        )
    """)

    start = date(2026, 1, 1)
    for i in range(1, num_rows + 1):
        producto = random.choice(list(PRODUCTOS.keys()))
        categoria, precio = PRODUCTOS[producto]
        cantidad = random.randint(1, 20)
        fecha = start + timedelta(days=random.randint(0, 105))
        cliente = random.choice(CLIENTES)
        ciudad = random.choice(CIUDADES)
        vendedor = random.choice(VENDEDORES)

        cur.execute(
            "INSERT INTO ventas (fecha, producto, categoria, cantidad, precio_unitario, total, cliente, ciudad, vendedor) VALUES (?,?,?,?,?,?,?,?,?)",
            (fecha.isoformat(), producto, categoria, cantidad, precio, cantidad * precio, cliente, ciudad, vendedor),
        )

    con.commit()
    con.close()
    print(f"DB creada: {db_path} ({num_rows} registros)")


if __name__ == "__main__":
    seed()
