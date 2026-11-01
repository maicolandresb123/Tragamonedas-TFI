"""Pruebas de las reglas originales sin requerir Flask."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from adaptador import juego, DATOS

assert juego.APUESTA == 10
assert juego.simbolos == ['🍒', '🍋', '🔔', '⭐', '7']
assert len(juego.girar()) == 3
assert juego.calcular_premio(['7', '7', '7']) == 100
assert juego.calcular_premio(['7', '🍒', '7']) == 10
assert juego.calcular_premio(['7', '🍋', '🔔']) == 0

archivo_original = juego.ARCHIVO
try:
    juego.ARCHIVO = str(DATOS / '_saldo_prueba.txt')
    juego.guardar_saldo(120)
    assert juego.cargar_saldo() == 120
    historial = DATOS / '_historial_prueba.txt'
    juego.guardar_historial(str(historial), ['🍒', '🍋', '7'], 0, 110)
    assert 'Premio: 0 | Saldo: 110' in historial.read_text(encoding='utf-8')
finally:
    juego.ARCHIVO = archivo_original
    (DATOS / '_saldo_prueba.txt').unlink(missing_ok=True)
    (DATOS / '_historial_prueba.txt').unlink(missing_ok=True)
print('OK: funciones originales, premios, saldo e historial.')
