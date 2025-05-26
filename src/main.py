from services.Database import MYSQLDataBase
from services.Cache import Cache
from services.Reports import ReportFactory
from app.api import ReportExecutor, LoggerExecute
from datetime import datetime
import os

database = MYSQLDataBase()
database.create_tables()
cache = Cache()


def main_menu():
    while True:
        print("\n🔸 MENÚ PRINCIPAL 🔸")
        print("1. Cargar logs")
        print("2. Ver reporte agrupado por salas")
        print("3. Ver reporte de Alertas")
        print("4. Ver Logs entre un rango de fechas")
        print("5. Salir")
    
        option = input("Elegí una opción (1-4): ").strip()

        if option == "1":
            actual_dir = os.path.dirname(os.path.abspath(__file__))
            csv_route = os.path.join(actual_dir, "..", "data", "logs_ambientales_ecowatch.csv")
            csv_route = os.path.normpath(csv_route)

            insert_logs = LoggerExecute(
                database=database,
                cache=cache,
                data_filepath=csv_route,
                source='csv'
            )

            insert_logs.insert_data()

        elif option == "2":
            print("\n🔸 Rango de fechas para obtener logs 🔸")
            start_input = input("Ingresá la fecha de inicio (YYYY-MM-DD HH:MM): ")
            end_input = input("Ingresá la fecha de fin (YYYY-MM-DD HH:MM): ")

            start_date = datetime.strptime(start_input, "%Y-%m-%d %H:%M")
            end_date = datetime.strptime(end_input, "%Y-%m-%d %H:%M")
            
            strategy = ReportFactory.get_report("status_sala")
            executor = ReportExecutor(
                strategy=strategy,
                cache=cache,
                database=database,
                start_date=start_date,
                end_date=end_date
            )
            data = executor.execute()

            print(data)
        
        elif option == "3":
            print("\n🔸 Rango de fechas para obtener logs 🔸")
            start_input = input("Ingresá la fecha de inicio (YYYY-MM-DD HH:MM): ")
            end_input = input("Ingresá la fecha de fin (YYYY-MM-DD HH:MM): ")

            strategy = ReportFactory.get_report("critic_alerts")
            executor = ReportExecutor(
                strategy=strategy,
                cache=cache,
                database=database,
                start_date=None,
                end_date=None
            )
            data = executor.execute()

            print(data)

        elif option == "4":
            pass

        elif option == "5":
            print("Hasta luego.")
            break

        else:
            print("Ingrese una opcion valida.")


if __name__ == "__main__":
    main_menu()