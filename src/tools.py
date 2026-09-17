"""

"""

import sqlite3
import os

from src.order_db import DB_Path

def find_order_status(order_id: str) -> dict:
    connection = sqlite3.connect(DB_Path)
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id, customer_name, product_name, status, order_date FROM orders WHERE id = ?",
        (order_id,)
    )

    row = cursor.fetchone()
    connection.close()

    if row is None:
        return {
            "found": False,
            "message": f"Order with ID '{order_id}' was not found."
        }

    return {
        "found": True,
        "order_id": row[0],
        "customer_name": row[1],
        "product_name": row[2],
        "status": row[3],
        "order_date": row[4]
    }

Tools = [
    {
        "type": "function",
        "function": {
            "name": "find_order_status",
            "description": (
                "Zjistí aktuální stav konkrétní objednávky podle jejího ID."
                "Použij tento nástroj vždy, když se zákazník ptá na stav,"
                "doručení nebo detaily své objednávky a zmíní ID objednávky."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "ID objednávky, např. 'ORD-1001'."
                    }
                },
                "required": ["order_id"]
            }
        }
    }
]

Available_Tools = {
    "find_order_status": find_order_status,
}