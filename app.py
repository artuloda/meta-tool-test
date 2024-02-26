# app.py
from flask import Flask, render_template

import main

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/clientes')
def clientes():
    return render_template('clientes.html', data=nodes_df)

@app.route('/vehiculos')
def vehiculos():
    return render_template('vehiculos.html', vehicle_data=fleet_df)

@app.route('/mapa')
def mapa():
    return render_template('map.html')

if __name__ == '__main__':
    nodes_df, fleet_df, result_df = main.main()

    #app.run(debug=True)
    app.run()

