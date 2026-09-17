"""
This module creates simple SQLite database with fake orders which agent will be able to query with tool-calling
"""

import sqlite3
import os

DB_Path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "orders.db")

def create_orders_db():
    connection = sqlite3.connect(DB_Path)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id TEXT PRIMARY KEY,
            customer_name TEXT NOT NULL,
            product_name TEXT NOT NULL,
            status TEXT NOT NULL,
            order_date TEXT NOT NULL
        )
    """)

    fake_orders = [
        ("ORD-1001", "Jan Novák", "Sluchátka SoundMax Pro X200", "expedováno", "2026-09-10"),
        ("ORD-1002", "Petra Svobodová", "Notebook ProBook 15 R7", "zpracovává se", "2026-09-13"),
        ("ORD-1003", "Jan Novák", "Chytré hodinky FitPulse 4", "doručeno", "2026-09-05"),
        ("ORD-1004", "Tomáš Dvořák", "Notebook ProBook 15 R7", "zrušeno", "2026-09-08"),
    ]

    cursor.executemany(
        "INSERT OR REPLACE INTO orders VALUES (?, ?, ?, ?, ?)",
        fake_orders
    )

    connection.commit()
    connection.close()

    print(f"Database created: {DB_Path}")
    print("Fake orders inserted into the database.")
    print(f"Number of orders inserted: {len(fake_orders)}")

if __name__ == "__main__":
    create_orders_db()