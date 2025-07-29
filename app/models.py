from . import db

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100))
    precio = db.Column(db.Float)
    descripcion = db.Column(db.String(200))
    
    def __init__(self, nombre: str, precio: float, descripcion: str):
        self.nombre = nombre
        self.precio = precio
        self.descripcion = descripcion

class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cliente = db.Column(db.String(100))
    fecha = db.Column(db.String(100))
    productos = db.relationship('PedidoProductos', backref='pedido')

    def __init__(self, cliente: str, fecha: str):
        self.cliente = cliente
        self.fecha = fecha

    @property
    def total(self):
        # Calcula el total sumando precio * cantidad de cada producto asociado
        return sum(pp.producto.precio * pp.cantidad for pp in self.productos)

    def agregar_producto(self, producto: Producto, cantidad: int):
        self.productos.append(PedidoProductos(self, producto, cantidad))

class PedidoProductos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'))
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'))
    cantidad = db.Column(db.Integer)
    producto = db.relationship('Producto')

    def __init__(self, pedido: Pedido, producto: Producto, cantidad: int):
        self.pedido = pedido
        self.producto = producto
        self.cantidad = cantidad