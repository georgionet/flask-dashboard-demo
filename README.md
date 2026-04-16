# flask-dashboard-demo

Dashboard web en Flask con tabla interactiva, filtros dinamicos, graficos y exportacion a Excel/CSV.

## Que hace

- Muestra tabla de ventas paginada y ordenable por cualquier columna
- Filtros por fecha, categoria, ciudad y cliente
- Graficos interactivos (barras, linea, torta) con Chart.js
- Exportacion a Excel y CSV respetando los filtros activos
- KPIs en tiempo real (registros, unidades, monto total)

## Stack

- **Flask** — Application factory + Blueprints
- **SQLite** — Base de datos demo incluida
- **Tailwind CSS** — Via CDN, sin build step
- **Chart.js** — Graficos via CDN
- **openpyxl** — Export Excel

## Uso

```bash
# Instalar dependencias
pip install -r requirements.txt

# Crear base de datos demo
python seed.py

# Levantar servidor
python run.py
```

Abrir `http://localhost:5000` en el navegador.

## Funcionalidades

### Filtros
- Rango de fechas (desde / hasta)
- Dropdown de categoria
- Dropdown de ciudad
- Busqueda por nombre de cliente
- Boton limpiar filtros

### Tabla
- Paginacion (15 por pagina)
- Ordenar por cualquier columna (click en header)
- Formato de moneda automatico

### Graficos
- **Barras**: Ventas por categoria
- **Torta**: Top 5 clientes
- **Linea**: Ventas por fecha

### Exportacion
- Excel (`.xlsx`) con headers formateados
- CSV (`.csv`)
- Ambos respetan los filtros activos

## Estructura

```
app/
  __init__.py          # Application factory
  db.py                # SQLite helpers
  dashboard.py         # Blueprint con rutas
  filters.py           # Logica de filtrado
  export.py            # Export Excel/CSV
  templates/
    base.html          # Layout con Tailwind + Chart.js
    dashboard/
      index.html       # Dashboard principal
seed.py                # Genera DB demo
run.py                 # Entry point
```

## Datos demo

El script `seed.py` genera 60 registros de ventas con:
- 4 categorias: Electronica, Ropa, Alimentos, Hogar
- 9 clientes
- 4 ciudades: Santiago, Valparaiso, Concepcion, Antofagasta
- Fechas entre enero y abril 2026

## Licencia

MIT
