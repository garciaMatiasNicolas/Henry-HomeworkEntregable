from abc import ABC, abstractmethod
from datetime import datetime
import pandas as pd

class ReportStrategy(ABC):
    @abstractmethod
    def generate(self, data: pd.DataFrame) -> dict:
        pass


class StatusSalaReportStrategy(ReportStrategy):
    def generate(self, data: pd.DataFrame) -> dict:
        resume = data.groupby("sala").agg({
            "temperatura": "mean",
            "humedad": "mean",
            "co2": "mean"
        }).reset_index()
        
        return {"type": "status_sala", "resume": resume.to_dict(orient="records")}


class CriticalAlertsReportStrategy(ReportStrategy):
    def generate(self, data: pd.DataFrame) -> dict:
        alerts = data[
            (data["co2"] > 1000) | (data["temperatura"] > 30) | (data["humedad"] < 20)
        ]
        return {"type": "critic_alerts", "alerts": alerts.to_dict(orient="records")}

class ReportFactory:
    _strategies = {
        "status_sala": StatusSalaReportStrategy,
        "critic_alerts": CriticalAlertsReportStrategy
    }

    @staticmethod
    def get_report(strategy_name: str) -> ReportStrategy:
        strategy_cls = ReportFactory._strategies.get(strategy_name)
        
        if not strategy_cls:
            raise ValueError(f"ERROR: Unknow report: {strategy_name}")
        
        return strategy_cls()
