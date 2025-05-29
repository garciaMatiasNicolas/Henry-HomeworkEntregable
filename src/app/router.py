from fastapi import APIRouter, Query
from datetime import datetime
import os

from ..services.Database import MYSQLDataBase
from ..services.Cache import Cache
from ..services.Reports import ReportFactory
from .controllers import ReportExecutor, LoggerExecute  

router = APIRouter()

database = MYSQLDataBase()
database.create_tables()
cache = Cache()


@router.post("/logs/load")
def load_logs():
    """Carga los logs desde el CSV en la base de datos"""
    actual_dir = os.path.dirname(os.path.abspath(__file__))
    csv_route = os.path.normpath(os.path.join(actual_dir, "..", "..", "data", "logs_ambientales_ecowatch.csv"))

    insert_logs = LoggerExecute(
        database=database,
        cache=cache,
        data_filepath=csv_route,
        source='csv'
    )
    insert_logs.insert_data()
    return {"message": "Logs insertados correctamente"}


@router.get("/reports/sala")
def report_sala(start: str = Query(...), end: str = Query(...)):
    """Reporte agrupado por salas"""
    try:
        start_date = datetime.strptime(start, "%Y-%m-%d %H:%M")
        end_date = datetime.strptime(end, "%Y-%m-%d %H:%M")
    except ValueError:
        return {"error": "Formato de fecha inválido. Usa 'YYYY-MM-DD HH:MM'"}

    strategy = ReportFactory.get_report("status_sala")
    executor = ReportExecutor(
        strategy=strategy,
        cache=cache,
        database=database,
        start_date=start_date,
        end_date=end_date
    )
    data = executor.execute()
    return data


@router.get("/reports/alerts")
def report_alerts():
    """Reporte de alertas críticas"""
    strategy = ReportFactory.get_report("critic_alerts")
    executor = ReportExecutor(
        strategy=strategy,
        cache=cache,
        database=database,
        start_date=None,
        end_date=None
    )
    data = executor.execute()
    return data
