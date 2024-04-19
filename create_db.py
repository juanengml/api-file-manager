import sqlite3


def createDB():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Criar tabela para armazenar as configurações dos dispositivos
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS devices
                    (id TEXT PRIMARY KEY, config TEXT)"""
    )

    # Criar tabela para armazenar os logs dos dispositivos
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS logs
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, id_device TEXT, log_data TEXT)"""
    )

    conn.commit()
    conn.close()
