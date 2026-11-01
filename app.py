"""Bonus gráfico del TFI: la lógica se toma del Python original sin modificarlo."""
from datetime import datetime
from threading import Lock
from flask import Flask, jsonify, render_template, request
from adaptador import juego, DATOS

app = Flask(__name__)
_candado = Lock()
_historial = []

def nuevo_historial():
    fecha = datetime.now().strftime('%Y-%m-%d_%H-%M')
    destino = DATOS / f'historial_partida_{fecha}.txt'
    numero = 2
    while destino.exists():
        destino = DATOS / f'historial_partida_{fecha}_{numero}.txt'
        numero += 1
    destino.touch()
    return destino

ARCHIVO_HISTORIAL = nuevo_historial()

def saldo_actual():
    return juego.cargar_saldo()

@app.get('/')
def inicio():
    return render_template('index.html')

@app.get('/api/estado')
def estado():
    with _candado:
        return jsonify(saldo=saldo_actual(), apuesta=juego.APUESTA, historial=_historial)

@app.post('/api/girar')
def girar():
    with _candado:
        saldo = saldo_actual()
        if saldo < juego.APUESTA:
            return jsonify(error='No tenés fichas suficientes. Cargá para continuar.', saldo=saldo), 400
        saldo -= juego.APUESTA
        rodillos = juego.girar()
        premio = juego.calcular_premio(rodillos)
        saldo += premio
        juego.guardar_saldo(saldo)
        juego.guardar_historial(str(ARCHIVO_HISTORIAL), rodillos, premio, saldo)
        jugada = {'rodillos': rodillos, 'premio': premio, 'saldo': saldo}
        _historial.insert(0, jugada)
        del _historial[12:]
        return jsonify(**jugada, historial=_historial)

@app.post('/api/cargar')
def cargar():
    datos = request.get_json(silent=True) or {}
    cantidad = datos.get('cantidad')
    if type(cantidad) is not int or cantidad <= 0 or cantidad > 100000:
        return jsonify(error='Ingresá una cantidad entera entre 1 y 100000.'), 400
    with _candado:
        saldo = saldo_actual() + cantidad
        juego.guardar_saldo(saldo)
        return jsonify(saldo=saldo)

if __name__ == '__main__':
    print('Interfaz: http://127.0.0.1:5000')
    app.run(host='127.0.0.1', port=5000, debug=False)
