from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "paas-practica-clave"

productos = [
    {"id": 1, "nombre": "Laptop Lenovo", "categoria": "Computación", "cantidad": 5, "precio": 3500.00},
    {"id": 2, "nombre": "Mouse inalámbrico", "categoria": "Accesorios", "cantidad": 12, "precio": 85.00},
    {"id": 3, "nombre": "Teclado mecánico", "categoria": "Accesorios", "cantidad": 8, "precio": 250.00},
]

@app.route("/")
def index():
    total_unidades = sum(p["cantidad"] for p in productos)
    valor_inventario = sum(p["cantidad"] * p["precio"] for p in productos)
    return render_template(
        "index.html",
        productos=productos,
        total_unidades=total_unidades,
        valor_inventario=valor_inventario
    )

@app.route("/agregar", methods=["POST"])
def agregar():
    nombre = request.form.get("nombre", "").strip()
    categoria = request.form.get("categoria", "").strip()
    cantidad = request.form.get("cantidad", "").strip()
    precio = request.form.get("precio", "").strip()

    if not nombre or not categoria or not cantidad or not precio:
        flash("Todos los campos son obligatorios.")
        return redirect(url_for("index"))

    try:
        cantidad = int(cantidad)
        precio = float(precio)
        if cantidad < 0 or precio < 0:
            raise ValueError
    except ValueError:
        flash("Cantidad y precio deben ser valores válidos y no negativos.")
        return redirect(url_for("index"))

    nuevo_id = max([p["id"] for p in productos], default=0) + 1
    productos.append({
        "id": nuevo_id,
        "nombre": nombre,
        "categoria": categoria,
        "cantidad": cantidad,
        "precio": precio
    })

    flash("Producto agregado correctamente.")
    return redirect(url_for("index"))

@app.route("/eliminar/<int:producto_id>", methods=["POST"])
def eliminar(producto_id):
    global productos
    productos = [p for p in productos if p["id"] != producto_id]
    flash("Producto eliminado.")
    return redirect(url_for("index"))

@app.route("/editar/<int:producto_id>", methods=["POST"])
def editar(producto_id):
    producto = next((p for p in productos if p["id"] == producto_id), None)

    if producto is None:
        flash("Producto no encontrado.")
        return redirect(url_for("index"))

    nombre = request.form.get("nombre", "").strip()
    categoria = request.form.get("categoria", "").strip()
    cantidad = request.form.get("cantidad", "").strip()
    precio = request.form.get("precio", "").strip()

    try:
        cantidad = int(cantidad)
        precio = float(precio)
        if not nombre or not categoria or cantidad < 0 or precio < 0:
            raise ValueError
    except ValueError:
        flash("Datos de edición no válidos.")
        return redirect(url_for("index"))

    producto.update({
        "nombre": nombre,
        "categoria": categoria,
        "cantidad": cantidad,
        "precio": precio
    })

    flash("Producto actualizado correctamente.")
    return redirect(url_for("index"))

@app.route("/health")
def health():
    return {"status": "ok", "application": "Inventario PaaS"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
