"""Carga únicamente las funciones del ejercicio original sin ejecutar su menú.

El archivo del profesor se mantiene intacto. Los datos del bonus se guardan
exclusivamente en Tragamonedas_Web/datos.
"""
import ast
import os
import random
from pathlib import Path
from types import ModuleType

BASE = Path(__file__).resolve().parent
FUENTE = BASE / 'referencia' / 'Tragamonedas corregido.py'
DATOS = BASE / 'datos'
DATOS.mkdir(exist_ok=True)


def cargar_funciones():
    codigo = FUENTE.read_text(encoding='utf-8-sig')
    arbol = ast.parse(codigo, filename=str(FUENTE))
    funciones = [n for n in arbol.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
    constantes = {
        n.targets[0].id: ast.literal_eval(n.value)
        for n in arbol.body if isinstance(n, ast.Assign) and len(n.targets) == 1
        and isinstance(n.targets[0], ast.Name)
        and n.targets[0].id in {'simbolos', 'APUESTA'}
    }
    if not {'simbolos', 'APUESTA'}.issubset(constantes):
        raise RuntimeError('El archivo de referencia no contiene los datos del juego.')
    nombres = {n.name for n in funciones}
    requeridas = {'cargar_saldo', 'guardar_saldo', 'girar', 'calcular_premio', 'guardar_historial'}
    if not requeridas.issubset(nombres):
        raise RuntimeError(f'Faltan funciones en el archivo original: {requeridas - nombres}')
    modulo = ModuleType('logica_del_profesor')
    modulo.__dict__.update(os=os, random=random, ARCHIVO=str(DATOS / 'saldo.txt'), **constantes)
    solo_funciones = ast.Module(body=funciones, type_ignores=[])
    ast.fix_missing_locations(solo_funciones)
    exec(compile(solo_funciones, str(FUENTE), 'exec'), modulo.__dict__)
    return modulo


juego = cargar_funciones()
