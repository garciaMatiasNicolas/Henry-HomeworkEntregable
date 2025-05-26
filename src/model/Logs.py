import pandas as pd
from datetime import datetime

class Logs:

    def __init__(
        self, 
        status: str,
        message: str,
        sala: str,
        humedity: float,
        temperature: float,
        co2: int,
        timestamp: datetime,
    ):
        self.status: str = status
        self.message: str = message
        self.sala: str = sala
        self.humedity: float = humedity
        self.co2: int = co2
        self.temperature: float = temperature
        self.timestamp: datetime = timestamp
 
    @staticmethod
    def from_db_row(row: tuple) -> 'Logs':
        return Logs(
            timestamp=row[0],
            sala=row[1],
            status=row[2],
            humedity=row[3],
            co2=row[4],
            temperature=row[5],
            message=row[6]
        )

    @staticmethod
    def from_row(row) -> "Logs":
        return Logs(
            timestamp=pd.to_datetime(row["timestamp"]),
            sala=row["sala"],
            status=row["estado"],
            temperature=float(row["temperatura"]),
            humedity=float(row["humedad"]),
            co2=float(row["co2"]),
            message=row["mensaje"]
        )
    
    def __repr__(self):
        return f"Logs(sala={self.sala}, timestamp={self.timestamp}, status={self.status})"
