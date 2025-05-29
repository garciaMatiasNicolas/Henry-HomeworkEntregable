import mysql.connector as mysql
from dotenv import load_dotenv
from ..model.Logs import Logs
from typing import List
import os
load_dotenv()


class MYSQLDataBase:
    CONN = mysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_DATABASE"),
        port=os.getenv('DB_PORT')
    )
    CURSOR = CONN.cursor()
    CREATE_TABLE_QUERY="""
        CREATE TABLE IF NOT EXISTS templogs (
            log_id INT PRIMARY KEY AUTO_INCREMENT,
            timestamp DATETIME NOT NULL,
            sala VARCHAR(100) NOT NULL,
            estado VARCHAR(100) NOT NULL,
            humedad FLOAT NOT NULL,
            co2 INT NOT NULL,
            temperatura FLOAT NOT NULL,
            mensaje VARCHAR(400) NOT NULL
        );
    """

    def create_tables(self):
        self.CURSOR.execute(self.CREATE_TABLE_QUERY)
        self.CONN.commit()
    
    def insert_logs(self, logs: List[Logs]):
        query = """
            INSERT INTO templogs (timestamp, sala, estado, humedad, co2, temperatura, mensaje)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        values = [
            (
                log.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                log.sala,
                log.status,
                log.humedity,
                log.co2,
                log.temperature,
                log.message
            )
            for log in logs
        ]

        self.CURSOR.executemany(query, values)
        self.CONN.commit()

    
