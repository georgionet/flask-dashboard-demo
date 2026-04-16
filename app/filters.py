def build_query(args):
    conditions = []
    params = []

    fecha_desde = args.get("fecha_desde", "").strip()
    fecha_hasta = args.get("fecha_hasta", "").strip()
    categoria = args.get("categoria", "").strip()
    ciudad = args.get("ciudad", "").strip()
    cliente = args.get("cliente", "").strip()

    if fecha_desde:
        conditions.append("fecha >= ?")
        params.append(fecha_desde)
    if fecha_hasta:
        conditions.append("fecha <= ?")
        params.append(fecha_hasta)
    if categoria:
        conditions.append("categoria = ?")
        params.append(categoria)
    if ciudad:
        conditions.append("ciudad = ?")
        params.append(ciudad)
    if cliente:
        conditions.append("cliente LIKE ?")
        params.append(f"%{cliente}%")

    where = f" WHERE {' AND '.join(conditions)}" if conditions else ""
    return where, params


def get_sort_clause(args):
    sort_col = args.get("sort", "fecha")
    sort_dir = args.get("dir", "desc")

    allowed_cols = {"fecha", "producto", "categoria", "cantidad", "precio_unitario", "total", "cliente", "ciudad", "vendedor"}
    if sort_col not in allowed_cols:
        sort_col = "fecha"
    if sort_dir not in ("asc", "desc"):
        sort_dir = "desc"

    return f" ORDER BY {sort_col} {sort_dir.upper()}"
