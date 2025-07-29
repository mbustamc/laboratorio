from app import db
from flask import current_app as app, render_template, jsonify, request, session
from app.models import Producto, Pedido, PedidoProductos

# Página principal
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/carrito", methods=["GET", "POST"])
def carrito():
    if request.method == "POST":
        session["carrito"] = request.get_json()
        return "", 204
    productos = session.get("carrito", [])
    return render_template("carrito.html", productos=productos)

@app.route("/productos/<int:id>")
def mostrar_producto(id):
    return render_template("producto.html", producto_id=id)

@app.route("/pedidos")
def mostrar_pedidos():
    pedidos = Pedido.query.all()
    return render_template("pedidos.html", pedidos=pedidos)

# API para ver todos los productos
@app.route("/api/productos", methods=["GET"])
def ver_productos():
    productos = Producto.query.all()
    return jsonify([{
        "id": p.id,
        "nombre": p.nombre,
        "precio": p.precio,
        "descripcion": p.descripcion
    } for p in productos])

# API para obtener un producto por ID
@app.route("/api/productos/<int:id>", methods=["GET"])
def obtener_producto(id):
    producto = Producto.query.get(id)
    if producto:
        return jsonify({
            "id": producto.id,
            "nombre": producto.nombre,
            "precio": producto.precio,
            "descripcion": producto.descripcion
        })
    else:
        return jsonify({"mensaje": "Producto no encontrado"}), 404

# API para procesar pedido
@app.route("/api/procesar_pedido", methods=["POST"])
def procesar_pedido():
    pedido_data = request.get_json()
    carrito = session.get("carrito", [])
    if carrito:
        nuevo_pedido = Pedido(cliente="Cliente temporal", fecha="2025-07-12")
        db.session.add(nuevo_pedido)
        db.session.commit()  # Para obtener el id del pedido

        for item in carrito:
            producto = Producto.query.get(item["id"])
            if producto:
                pedido_producto = PedidoProductos(
                    pedido=nuevo_pedido,
                    producto=producto,
                    cantidad=item["cantidad"]
                )
                db.session.add(pedido_producto)
        db.session.commit()
        session["ultimo_pedido"] = pedido_data
        return jsonify({"status": "ok", "mensaje": "Pedido procesado correctamente"})
    else:
        return jsonify({"status": "error", "mensaje": "Carrito vacío"}), 400

# API para ver todos los pedidos
@app.route("/api/pedidos", methods=["GET"])
def obtener_pedidos():
    pedidos = Pedido.query.all()
    def pedido_to_dict(pedido):
        return {
            "id": pedido.id,
            "cliente": pedido.cliente,
            "fecha": pedido.fecha,
            "productos": [
                {
                    "id": pp.producto.id,
                    "nombre": pp.producto.nombre,
                    "precio": pp.producto.precio,
                    "cantidad": pp.cantidad
                }
                for pp in pedido.productos
            ]
        }
    return jsonify([pedido_to_dict(p) for p in pedidos])