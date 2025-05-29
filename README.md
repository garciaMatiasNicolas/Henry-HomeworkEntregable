# Henry-HomeworkEntregable

El siguiente proyecto consiste en una API REST construida con FastAPI que permite:

- Cargar logs ambientales desde un archivo CSV a una base de datos MySQL.
- Generar reportes agrupados por salas en un rango de fechas específico.
- Obtener reportes de alertas críticas.
- Guardar en un CACHE contruido aquellos logs cuyo timestamp sea menor a 5 minutos de la hora en la que se consulta el log

## 📁 Estructura del Proyecto

```css
Henry-HomeworkEntregable/
├── data/
│   └── logs_ambientales_ecowatch.csv
├── src/
│   ├── app/
│   │   ├── controllers.py
│   │   └── router.py  
│   ├── model/
│   │   └──  Logs.py
│   ├── services/
│   │   ├── Cache.py
│   │   ├── Dataloader.py
│   │   ├── Database.py
│   │   └── Reports.py
│   ├── main.py
│
├── requirements.txt
└── README.md
```

## 🚀 Instalación y Ejecución

### 1. Clonar el repositorio
```bash
git clone https://github.com/garciaMatiasNicolas/Henry-HomeworkEntregable.git
cd Henry-HomeworkEntregable
```

### 2. Crear y activar un entorno virtual (opcional pero recomendado)
```bash
python -m venv .venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
Crear un archivo .env en la raíz del proyecto con la siguiente estructura:
```ini
DB_HOST=localhost
DB_PORT=3306
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_NAME=nombre_de_tu_base_de_datos
```
Asegúrate de que los valores coincidan con tu configuración local de MySQL.

### 5. Ejecutar la aplicación
```bash
uvicorn src.app.main:app --reload # podemos pasarle un puerto especifico por parametros --port 8080 (por defecto corre en el 8000)
```
La API estará disponible en http://127.0.0.1:8000.

## 📚 Documentación de la API
FastAPI genera automáticamente documentación interactiva. Puedes acceder a ella en:

Swagger UI: http://127.0.0.1:8000/docs

ReDoc: http://127.0.0.1:8000/redoc

## 📌 Endpoints Disponibles
### 1. Cargar Logs desde CSV
Endpoint: *POST /logs/load*

Descripción: Carga los logs ambientales desde el archivo CSV ubicado en data/logs_ambientales_ecowatch.csv a la base de datos.

Respuesta exitosa:
```json
{
  "message": "Logs insertados correctamente"
}
```

### 2. Reporte Agrupado por Salas
Endpoint: *GET /reports/sala*

Parámetros de consulta:

start: Fecha y hora de inicio en formato YYYY-MM-DD HH:MM.

end: Fecha y hora de fin en formato YYYY-MM-DD HH:MM.

Descripción: Genera un reporte de los logs agrupados por salas en el rango de fechas especificado.

Ejemplo de solicitud:
```bash
GET /reports/sala?start=2025-05-01%2000:00&end=2025-05-25%2000:00
```

### 3. Reporte de Alertas Críticas
Endpoint: *GET /reports/alerts*

Descripción: Obtiene un reporte de las alertas críticas registradas en los logs en el rango de fechas especificado.

Ejemplo de solicitud:
```bash
GET /reports/alerts?start=2025-05-01%2000:00&end=2025-05-25%2000:00
```

## 🛠️ Consideraciones Técnicas
* Framework: FastAPI
* Base de Datos: MySQL
* Cache: Implementación personalizada en Cache.py
* Ejecución de Reportes: Patrón Strategy implementado en Reports.py

