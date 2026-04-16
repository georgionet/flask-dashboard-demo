from flask import Blueprint, render_template, request, url_for
from app.db import query_db
from app.filters import build_query, get_sort_clause
from app.export import export_excel, export_csv

bp = Blueprint("dashboard", __name__)

PER_PAGE = 15

FILTER_KEYS = ("fecha_desde", "fecha_hasta", "categoria", "ciudad", "cliente")


def _filter_args():
    return {k: v for k, v in request.args.items() if k in FILTER_KEYS and v}


@bp.route("/")
def index():
    where, params = build_query(request.args)
    sort = get_sort_clause(request.args)
    fargs = _filter_args()

    page = request.args.get("page", 1, type=int)
    offset = (page - 1) * PER_PAGE

    columns, rows = query_db(f"SELECT * FROM ventas{where}{sort} LIMIT ? OFFSET ?", (*params, PER_PAGE, offset))
    _, total_rows = query_db(f"SELECT COUNT(*) as cnt FROM ventas{where}", params)
    total = total_rows[0]["cnt"] if total_rows else 0

    _, sum_rows = query_db(f"SELECT COALESCE(SUM(total),0) as total_sum, COALESCE(SUM(cantidad),0) as qty_sum FROM ventas{where}", params)
    total_sum = sum_rows[0]["total_sum"] if sum_rows else 0
    qty_sum = sum_rows[0]["qty_sum"] if sum_rows else 0

    _, cat_data = query_db(f"SELECT categoria, SUM(total) as total FROM ventas{where} GROUP BY categoria ORDER BY total DESC", params)
    _, time_data = query_db(f"SELECT fecha, SUM(total) as total FROM ventas{where} GROUP BY fecha ORDER BY fecha", params)
    _, client_data = query_db(f"SELECT cliente, SUM(total) as total FROM ventas{where} GROUP BY cliente ORDER BY total DESC LIMIT 5", params)

    _, categories = query_db("SELECT DISTINCT categoria FROM ventas ORDER BY categoria")
    _, cities = query_db("SELECT DISTINCT ciudad FROM ventas ORDER BY ciudad")

    sort_col = request.args.get("sort", "fecha")
    sort_dir = request.args.get("dir", "desc")

    # Pre-build sort URLs per column
    sort_urls = {}
    for col in columns:
        if col == "id":
            continue
        next_dir = "asc" if sort_col == col and sort_dir == "desc" else "desc"
        sort_urls[col] = url_for("dashboard.index", **fargs, sort=col, dir=next_dir)

    total_pages = (total + PER_PAGE - 1) // PER_PAGE
    page_urls = {}
    for p in range(1, total_pages + 1):
        page_urls[p] = url_for("dashboard.index", **fargs, page=p, sort=sort_col, dir=sort_dir)

    return render_template("dashboard/index.html",
        rows=rows, columns=columns,
        page=page, total=total, per_page=PER_PAGE, total_pages=total_pages,
        total_sum=total_sum, qty_sum=qty_sum,
        cat_data=cat_data, time_data=time_data, client_data=client_data,
        categories=[c["categoria"] for c in categories],
        cities=[c["ciudad"] for c in cities],
        filters=request.args,
        sort_col=sort_col, sort_dir=sort_dir,
        sort_urls=sort_urls, page_urls=page_urls,
        export_xlsx_url=url_for("dashboard.export", **fargs, format="xlsx"),
        export_csv_url=url_for("dashboard.export", **fargs, format="csv"),
    )


@bp.route("/export")
def export():
    where, params = build_query(request.args)
    sort = get_sort_clause(request.args)
    fmt = request.args.get("format", "xlsx")

    columns, rows = query_db(f"SELECT * FROM ventas{where}{sort}", params)

    if fmt == "csv":
        return export_csv(columns, rows)
    return export_excel(columns, rows)
