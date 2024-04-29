from models import db, GastosModal, IngresosModal, DeudasModal
from flask_restful import Resource, Api, reqparse

api = Api()

parseador = reqparse.RequestParser()
parseador.add_argument('fecha' , type=str)
parseador.add_argument('concepto' , type=str)
parseador.add_argument('cantidad' , type=float)
parseador.add_argument('descripcion' , type=str)
parseador.add_argument('deudor' , type=str)
parseador.add_argument('desde_cuando' , type=str)
parseador.add_argument('comentarios' , type=str)
parseador.add_argument('resuelto' , type=bool)


class Todo(Resource):
    #get,post, put,delete
    #get: obtener
    def get(self, base_datos=None, finanzas_id=None):
        if not base_datos and not finanzas_id:
            Gastos = GastosModal.query.all()
            Ingresos = IngresosModal.query.all()
            Deudas = DeudasModal.query.all()
            return {"Gastos": [(gasto.id,gasto.fecha,gasto.concepto,gasto.cantidad,gasto.descripcion) for gasto in Gastos] if Gastos else 'No hay gastos',
                    "Ingresos":[(ingreso.id,ingreso.fecha,ingreso.concepto,ingreso.cantidad,ingreso.descripcion) for ingreso in Ingresos] if Ingresos else 'No hay ingresos',
                    "Deudas": [(deuda.id,deuda.deudor,deuda.cantidad,deuda.desde_cuando,deuda.comentarios,deuda.resuelto) for deuda in Deudas] if Deudas else 'No hay deudas'}, 200
        elif base_datos == 'gastos':
            if finanzas_id:
                Gasto = GastosModal.query.filter_by(id=finanzas_id).first()
                return {"id": Gasto.id, "fecha": Gasto.fecha, "concepto": Gasto.concepto, "cantidad": Gasto.cantidad, "descripcion": Gasto.descripcion}, 200
            elif not finanzas_id:
                Gastos = GastosModal.query.all()
                json = {}
                for Gasto in Gastos:
                    json[Gasto.id] = {"fecha": Gasto.fecha, "concepto": Gasto.concepto, "cantidad": Gasto.cantidad, "descripcion": Gasto.descripcion}
                if json == {}:
                    return {"message": "No hay gastos"}, 404
                return json,200
        elif base_datos == 'ingresos':
            if finanzas_id:
                Ingreso = IngresosModal.query.filter_by(id=finanzas_id).first()
                return {"id": Ingreso.id, "fecha": Ingreso.fecha, "concepto": Ingreso.concepto, "cantidad": Ingreso.cantidad, "descripcion": Ingreso.descripcion},200
            else:
                Ingresos = IngresosModal.query.all()
                json = {}
                for Ingreso in Ingresos:
                    json[Ingreso.id] = {"fecha": Ingreso.fecha, "concepto": Ingreso.concepto, "cantidad": Ingreso.cantidad, "descripcion": Ingreso.descripcion}
                if json == {}:
                    return {"message": "No hay ingresos"}, 404
                return json,200
        elif base_datos == 'deudas':
            if finanzas_id:
                Deuda = DeudasModal.query.filter_by(id=finanzas_id).first()
                return {"id": Deuda.id, "deudor": Deuda.deudor, "cantidad": Deuda.cantidad, "desde_cuando": Deuda.desde_cuando, "comentarios": Deuda.comentarios, "resuelto": Deuda.resuelto},200
            else:
                Deudas = DeudasModal.query.all()
                json = {}
                for Deuda in Deudas:
                    json[Deuda.id] = {"deudor": Deuda.deudor, "cantidad": Deuda.cantidad, "desde_cuando": Deuda.desde_cuando, "comentarios": Deuda.comentarios, "resuelto": Deuda.resuelto}
                if json == {}:
                    return {"message": "No hay deudas"}, 404
                return json,200
        else:
            return {"message": "No se encontro la base de datos revisa la url"}, 404
     #post: crear
    def post(self, base_datos):
        if base_datos == 'Gastos':
            args = parseador.parse_args()
            Gasto = GastosModal(fecha=args['fecha'], concepto=args['concepto'], cantidad=args['cantidad'], descripcion=args['descripcion'])
            db.session.add(Gasto)
            db.session.commit()
            return {"id": Gasto.id, "fecha": Gasto.fecha, "concepto": Gasto.concepto, "cantidad": Gasto.cantidad, "descripcion": Gasto.descripcion},201
        elif base_datos == 'Ingresos':
            args = parseador.parse_args()
            Ingreso = IngresosModal(fecha=args['fecha'], concepto=args['concepto'], cantidad=args['cantidad'], descripcion=args['descripcion'])
            db.session.add(Ingreso)
            db.session.commit()
            return {"id": Ingreso.id, "fecha": Ingreso.fecha, "concepto": Ingreso.concepto, "cantidad": Ingreso.cantidad, "descripcion": Ingreso.descripcion},201
        elif base_datos == 'Deudas':
            args = parseador.parse_args()
            Deuda = DeudasModal(deudor=args['deudor'], cantidad=args['cantidad'], desde_cuando=args['desde_cuando'], comentarios=args['comentarios'], resuelto=args['resuelto'])
            db.session.add(Deuda)
            db.session.commit()
            return {"id": Deuda.id, "deudor": Deuda.deudor, "cantidad": Deuda.cantidad, "desde_cuando": Deuda.desde_cuando, "comentarios": Deuda.comentarios, "resuelto": Deuda.resuelto},201
    #put: actualizar
    def put(self, base_datos, finanzas_id):
        if base_datos == 'Gastos':
            args = parseador.parse_args()
            Gasto = GastosModal.query.filter_by(id=finanzas_id).first()
            Gasto.fecha = args['fecha']
            Gasto.concepto = args['concepto']
            Gasto.cantidad = args['cantidad']
            Gasto.descripcion = args['descripcion']
            db.session.commit()
            return {"id": Gasto.id, "fecha": Gasto.fecha, "concepto": Gasto.concepto, "cantidad": Gasto.cantidad, "descripcion": Gasto.descripcion}
        elif base_datos == 'Ingresos':
            args = parseador.parse_args()
            Ingreso = IngresosModal.query.filter_by(id=finanzas_id).first()
            Ingreso.fecha = args['fecha']
            Ingreso.concepto = args['concepto']
            Ingreso.cantidad = args['cantidad']
            Ingreso.descripcion = args['descripcion']
            db.session.commit()
            return {"id": Ingreso.id, "fecha": Ingreso.fecha, "concepto": Ingreso.concepto, "cantidad": Ingreso.cantidad, "descripcion": Ingreso.descripcion}
        elif base_datos == 'Deudas':
            args = parseador.parse_args()
            Deuda = DeudasModal.query.filter_by(id=finanzas_id).first()
            Deuda.deudor = args['deudor']
            Deuda.cantidad = args['cantidad']
            Deuda.desde_cuando = args['desde_cuando']
            Deuda.comentarios = args['comentarios']
            Deuda.resuelto = args['resuelto']
            db.session.commit()
            return {"id": Deuda.id, "deudor": Deuda.deudor, "cantidad": Deuda.cantidad, "desde_cuando": Deuda.desde_cuando, "comentarios": Deuda.comentarios, "resuelto": Deuda.resuelto}
    #delete: eliminar
    def delete(self, base_datos, finanzas_id):
        if base_datos == 'Gastos':
            Gasto = GastosModal.query.filter_by(id=finanzas_id).first()
            db.session.delete(Gasto)
            db.session.commit()
            return {"message": "Gasto eliminado"}
        elif base_datos == 'Ingresos':
            Ingreso = IngresosModal.query.filter_by(id=finanzas_id).first()
            db.session.delete(Ingreso)
            db.session.commit()
            return {"message": "Ingreso eliminado"}
        elif base_datos == 'Deudas':
            Deuda = DeudasModal.query.filter_by(id=finanzas_id).first()
            db.session.delete(Deuda)
            db.session.commit()
            return {"message": "Deuda eliminada"}

api.add_resource(Todo,'/finanzas/', '/finanzas/<string:base_datos>/', '/finanzas/<string:base_datos>/<int:finanzas_id>')