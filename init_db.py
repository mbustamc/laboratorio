from app import create_app, db


app = create_app()

with app.app_context():
    db.create_all()
    print("Tablas creadas correctamente.")

    
from app.models import Producto, Pedido, PedidoProductos

with app.app_context():
    db.create_all()
    db.session.add(Producto(nombre="Producto 1", precio=10.0, descripcion="Descripción del producto 1"))
    db.session.add(Producto(nombre="Producto 2", precio=20.0, descripcion="Descripción del producto 2"))
    db.session.add((Producto(nombre="Producto 3", precio=30.0, descripcion="Descripción del producto 3")))   
    db.session.add((Producto(nombre="Producto 4", precio=40.0, descripcion="Descripción del producto 4")))
    db.session.add((Producto(nombre="Producto 5", precio=50.0, descripcion="Descripción del producto 5")))
    db.session.commit()
    db.session.add(Pedido(cliente="Cliente 1", fecha="2025-07-12"))
    db.session.add(Pedido(cliente="Cliente 2", fecha="2025-07-13"))
    db.session.add(Pedido(cliente="Cliente 3", fecha="2025-07-14"))
    db.session.add(Pedido(cliente="Cliente 4", fecha="2025-07-15"))
    db.session.add(Pedido(cliente="Cliente 5", fecha="2025-07-16"))
    db.session.commit()

    pedido = Pedido.query.get(1)
    producto = Producto.query.get(1)
    pp = PedidoProductos(pedido, producto, 2)
    db.session.add(pp)
    db.session.commit()

    # Agregar más productos a otros pedidos
    pedido = Pedido.query.get(2)
    producto = Producto.query.get(3)
    pp = PedidoProductos(pedido, producto, 1)
    db.session.add(pp)
    db.session.commit()

    pedido = Pedido.query.get(3)
    producto = Producto.query.get(5)
    pp = PedidoProductos(pedido, producto, 2)
    db.session.add(pp)
    db.session.commit()