from flask import Flask, request, render_template, redirect, url_for
from models import db
from flask_cors import CORS
from api import api
import datetime
import requests
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///controlFinanciero.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'claveSecreta'
db.init_app(app)
api.init_app(app)
CORS(app)

@app.route('/')
def index():
    """ Cargar datos de la api con requests """
    
    return render_template('index.html')

@app.route('/gastos-Dashboard/')
def gastos():
    """ Cargar datos de la api con requests """
    response = requests.get('http://localhost:3000/finanzas/gastos')
    return render_template('dashboard-gastos.html', gastos=response.json())

@app.route('/ingresos-Dashboard/')
def ingresos():
    """ Cargar datos de la api con requests """
    response = requests.get('http://localhost:3000/finanzas/ingresos')
    return render_template('dashboard-ingresos.html', ingresos=response.json())

@app.route('/deudas-Dashboard/')
def deudas():
    """ Cargar datos de la api con requests """
    response = requests.get('http://localhost:3000/finanzas/deudas')
    return render_template('dashboard-deudas.html', deudas=response.json())

@app.route('/deudas-Dashboard/add_deuda', methods=['GET', 'POST'])
def add_deuda():
    """ default form """
    if request.method == 'POST':
        deudor = request.form['deudor']
        cantidad = request.form['cantidad']
        desde_cuando = request.form['desde_cuando']
        comentarios = request.form['comentarios']
        resuelto = request.form.get('resuelto')
        print(resuelto)
        if resuelto is None:
            resuelto = False
        elif resuelto.lower() == 'on':
            resuelto = True
        else:
            resuelto = False

        response = requests.post('http://localhost:3000/finanzas/Deudas/', json={"deudor": deudor, "cantidad": cantidad, "desde_cuando": desde_cuando, "comentarios": comentarios, "resuelto": resuelto})
        if response.status_code == 201:
            return redirect(url_for('deudas'))
        else:
            return redirect(url_for('add_deuda'))
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    return render_template('add-deuda.html', today=today)

@app.route( '/gastos-Dashboard/add_gasto', methods=['GET', 'POST'])
def add_gasto():
    """ default form """
    if request.method == 'POST':
        fecha = request.form['fecha']
        concepto = request.form['concepto']
        cantidad = request.form['cantidad']
        descripcion = request.form['descripcion']
        response = requests.post('http://localhost:3000/finanzas/Gastos/', json={"fecha": fecha, "concepto": concepto, "cantidad": cantidad, "descripcion": descripcion})
        if response.status_code == 201:
            return redirect(url_for('gastos'))
        else:
            return redirect(url_for('add_gasto'))
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    return render_template('add-gasto.html', today=today)

@app.route('/ingresos-Dashboard/add_ingreso', methods=['GET', 'POST'])
def add_ingreso():
    """ default form """
    if request.method == 'POST':
        fecha = request.form['fecha']
        concepto = request.form['concepto']
        cantidad = request.form['cantidad']
        descripcion = request.form['descripcion']
        response = requests.post('http://localhost:3000/finanzas/Ingresos/', json={"fecha": fecha, "concepto": concepto, "cantidad": cantidad, "descripcion": descripcion})
        if response.status_code == 201:
            return redirect(url_for('ingresos'))
        else:
            return redirect(url_for('add_ingreso'))
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    return render_template('add-ingreso.html', today=today)

@app.route('/delete_deuda/<int:id>')
def delete_deuda(id):
    requests.delete(f'http://localhost:3000/finanzas/Deudas/{id}')
    return redirect(url_for('deudas'))

@app.route('/delete_gasto/<int:id>')
def delete_gasto(id):
    requests.delete(f'http://localhost:3000/finanzas/Gastos/{id}')
    return redirect(url_for('gastos'))

@app.route('/delete_ingreso/<int:id>')
def delete_ingreso(id):
    requests.delete(f'http://localhost:3000/finanzas/Ingresos/{id}')
    return redirect(url_for('ingresos'))

@app.route('/editar_deuda/<int:id>', methods=['GET', 'POST'])
def editar_deuda(id):
    id = int(id)
    response = requests.get(f'http://localhost:3000/finanzas/deudas/{int(id)}')
    print(response.json())
    if request.method == 'POST':
        deudor = request.form['deudor']
        cantidad = request.form['cantidad']
        desde_cuando = request.form['desde_cuando']
        comentarios = request.form['comentarios']
        resuelto = request.form.get('resuelto', 'false')
        resuelto = True if resuelto == 'true' else False

        response = requests.put(f'http://localhost:3000/finanzas/Deudas/{int(id)}', json={"deudor": deudor, "cantidad": cantidad, "desde_cuando": desde_cuando, "comentarios": comentarios, "resuelto": resuelto})
        if response.status_code == 200:
            return redirect(url_for('deudas'))
        else:
            return redirect(url_for('editar-deuda.html', id=id))
    return render_template('editar-deuda.html', deuda=response.json(), id=id)

@app.route('/editar_gasto/<int:id>', methods=['GET', 'POST'])
def editar_gasto(id):
    id = int(id)
    response = requests.get(f'http://localhost:3000/finanzas/gastos/{int(id)}')
    if request.method == 'POST':
        fecha = request.form['fecha']
        concepto = request.form['concepto']
        cantidad = request.form['cantidad']
        descripcion = request.form['descripcion']
        response = requests.put(f'http://localhost:3000/finanzas/Gastos/{int(id)}', json={"fecha": fecha, "concepto": concepto, "cantidad": cantidad, "descripcion": descripcion})
        if response.status_code == 200:
            return redirect(url_for('gastos'))
        else:
            return redirect(url_for('editar-gasto.html', id=id))
    return render_template('editar-gasto.html', gasto=response.json(), id=id)

@app.route('/editar_ingreso/<int:id>', methods=['GET', 'POST'])
def editar_ingreso(id):
    id = int(id)
    response = requests.get(f'http://localhost:3000/finanzas/ingresos/{int(id)}')
    if request.method == 'POST':
        fecha = request.form['fecha']
        concepto = request.form['concepto']
        cantidad = request.form['cantidad']
        descripcion = request.form['descripcion']
        response = requests.put(f'http://localhost:3000/finanzas/Ingresos/{int(id)}', json={"fecha": fecha, "concepto": concepto, "cantidad": cantidad, "descripcion": descripcion})
        if response.status_code == 200:
            return redirect(url_for('ingresos'))
        else:
            return redirect(url_for('editar-ingresos.html', id=id))
    return render_template('editar-ingresos.html', ingreso=response.json(), id=id)

@app.route('/graficas/')
def graficas():
    return render_template('grafica.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True , port=3000)