from services.Database import MYSQLDataBase
from services.Cache import Cache
from services.Dataloader import DataLoaderFactory
from services.Reports import ReportStrategy
from model.Logs import Logs
from datetime import datetime, timedelta
import pandas as pd


class LoggerExecute:
    def __init__(self, database: MYSQLDataBase, cache: Cache, data_filepath: str, source: str):
        self.database: MYSQLDataBase = database
        self.cache: Cache = cache
        self.validated_data: pd.DataFrame = self.validate(data_filepath=data_filepath, source=source)
        
    @staticmethod
    def validate(data_filepath: str, source: str) -> pd.DataFrame:
        validated_data = DataLoaderFactory(source=source, filepath=data_filepath).validate()
        return validated_data

    def sync_old_logs_to_db(self):
        old_logs = self.cache._clean_old_logs()
        
        if old_logs:
            print(f"Insertando {len(old_logs)} logs a la base de datos...")
            self.database.insert_logs(old_logs)
        else:
            print("No hay logs en cache para insertar a la base de datos.")

    def insert_data(self):
        self.sync_old_logs_to_db()

        now = datetime.now()
        five_minutes_ago = now - timedelta(minutes=5)
        self.validated_data["timestamp"] = pd.to_datetime(self.validated_data["timestamp"])

        recent_logs_df = self.validated_data[self.validated_data["timestamp"] > five_minutes_ago]
        old_logs_df = self.validated_data[self.validated_data["timestamp"] <= five_minutes_ago]

        recent_logs = [Logs.from_row(row) for _, row in recent_logs_df.iterrows()]
        old_logs = [Logs.from_row(row) for _, row in old_logs_df.iterrows()]

        if old_logs:
            print(f"Insertando {len(old_logs)} logs antiguos a la base de datos...")
            self.database.insert_logs(old_logs)
        else:
            print("No hay logs antiguos para insertar en base de datos.")

        if recent_logs:
            print(f"Agregando {len(recent_logs)} logs recientes al cache...")
            for log in recent_logs:
                self.cache.add_log(log)
        else:
            print("No hay logs recientes para agregar al cache.")


class ReportExecutor:
    def __init__(self, strategy: ReportStrategy, start_date: datetime, end_date: datetime, cache: Cache, database: MYSQLDataBase):
        self.strategy: ReportStrategy = strategy
        self.start_date: datetime = start_date
        self.end_date: datetime = end_date
        self.cache: Cache = cache
        self.database: MYSQLDataBase = database

    def get_log_data(self) -> pd.DataFrame:
        now = datetime.now()
        five_minutes_ago = now - timedelta(minutes=5)

        if self.start_date >= five_minutes_ago:
            all_logs = list(self.cache.logs)
        else:
            query = """
                SELECT timestamp, sala, estado, humedad, co2, temperatura, mensaje
                FROM templogs
                WHERE timestamp BETWEEN %s AND %s;
            """
            self.database.CURSOR.execute(query, (self.start_date, self.end_date))
            rows = self.database.CURSOR.fetchall()
            all_logs = [Logs.from_db_row(row) for row in rows]

        # Filtrar por rango
        filtered_logs = [
            log for log in all_logs
            if self.start_date <= log.timestamp <= self.end_date
        ]

        # Convertir a DataFrame
        return pd.DataFrame([{
            "timestamp": log.timestamp,
            "sala": log.sala,
            "estado": log.status,
            "mensaje": log.message,
            "humedad": log.humedity,
            "temperatura": log.temperature,
            "co2": log.co2
        } for log in filtered_logs])
    
    def execute(self) -> dict:
        data = self.get_log_data()
        return self.strategy.generate(data)

