import os
import random
from datetime import datetime

# =====================================================
#  🎰 TRAGAMONEDAS - ¡CÓDIGO DAÑADO!
# =====================================================
#  Un error borró partes IMPORTANTES del programa.
#  Tu misión: restaurarlo siguiendo los comentarios TODO.
#
#  1. Leé todo el código antes de tocar nada.
#  2. Resolvé los TODO en orden (del 1 al 15).
#  3. Ejecutá después de cada uno para ver qué cambia.
#  4. Usá el tutorial paso a paso si te trabás.
#
#  Cuando termines: tiene que poder jugar con Enter, cargar
#  fichas y recordar tu saldo al cerrar y volver a abrir.
# =====================================================


# ---------- DATOS DEL JUEGO ----------

# TODO 1: armar la lista con los 5 símbolos: "🍒", "🍋", "🔔", "⭐", "7"
simbolos = ["🍒", "🍋", "🔔", "⭐", "7"]

# TODO 2: definir la apuesta de cada tirada: 10 fichas
APUESTA = 10

# TODO 3: definir el nombre del archivo donde se guarda el saldo: "saldo.txt"
ARCHIVO = "saldo.txt"


# ---------- FUNCIONES ----------

def cargar_saldo():
    """Lee el saldo guardado en el archivo. Si no existe, empieza con 100."""
    if os.path.exists(ARCHIVO):
        archivo = open(ARCHIVO, "r")
        # TODO 4: leer el contenido con archivo.read(), convertirlo a
        #         número entero con int() y guardarlo en la variable saldo
        saldo = int(archivo.read())
        archivo.close()
        print("Saldo anterior cargado.")
    else:
        saldo = 100
        print("Primera vez: empezás con 100 fichas.")
    return saldo


def guardar_saldo(saldo):
    """Escribe el saldo en el archivo (borra lo anterior)."""
    archivo = open(ARCHIVO, "w")  
    # TODO 5: escribir el saldo en el archivo con archivo.write()
    #         (write solo acepta texto: convertí el saldo con str())
    archivo.write(str(saldo))
    archivo.close()


def girar():
    """Devuelve una lista con 3 símbolos al azar."""
    rodillos = []
    # TODO 6: armar un bucle for que se repita 3 veces (range(3)).
    #         En cada vuelta: elegir un símbolo con random.choice(simbolos)
    #         y agregarlo a la lista rodillos con append().
    for i in range(3):
        rodillos.append(random.choice(simbolos))
    return rodillos


def calcular_premio(rodillos):
    """Tres iguales: x10. Dos iguales: recupera la apuesta. Sino: 0."""
    # TODO 7: completá la condición "los 3 rodillos son iguales"
    #         (usá == y el operador and)
    if rodillos[0] == rodillos[1] and rodillos[1] == rodillos[2]:
        # TODO 8: devolver el premio: la APUESTA multiplicada por 10
        return APUESTA * 10
    elif rodillos[0] == rodillos[1] or rodillos[1] == rodillos[2] or rodillos[0] == rodillos[2]:
        return APUESTA
    else:
        return 0


# ---------- BONUS TRACK: HISTORIAL DE LA PARTIDA ----------

def guardar_historial(archivo_historial, rodillos, premio, saldo):
    """Agrega los símbolos, el premio y el saldo final de una tirada."""
    archivo = open(archivo_historial, "a", encoding="utf-8")
    archivo.write(f"{' | '.join(rodillos)} | Premio: {premio} | Saldo: {saldo}\n")
    archivo.close()


# ---------- PROGRAMA PRINCIPAL ----------
print("=== 🎰 TRAGAMONEDAS (fichas virtuales) 🎰 ===")

# TODO 9: llamar a cargar_saldo() y guardar lo que devuelve en la variable saldo
saldo = cargar_saldo()

# BONUS TRACK: un archivo de historial por cada inicio del programa.
fecha_inicio = datetime.now().strftime("%Y-%m-%d_%H-%M")
archivo_historial = f"historial_partida_{fecha_inicio}.txt"

while True:
    print(f"\nSaldo: {saldo} fichas | Cada tirada cuesta {APUESTA}")
    orden = input("[Enter] palanca | [+] cargar fichas | [s] salir: ")

    if orden == "":
        if saldo >= APUESTA:
            # TODO 10: restarle la APUESTA al saldo
            saldo = saldo - APUESTA

            # TODO 11: llamar a la función girar() y guardar lo que
            #          devuelve en la variable rodillos
            rodillos = girar()
            print("\n  [", " | ".join(rodillos), "]")

            # TODO 12: llamar a calcular_premio(rodillos) y guardar lo que
            #          devuelve en la variable premio
            premio = calcular_premio(rodillos)

            # TODO 13: sumarle el premio al saldo
            saldo = saldo + premio

            if premio > APUESTA:
                print(f"¡GANASTE {premio} fichas!")
            elif premio == APUESTA:
                print("Dos iguales: recuperás tu apuesta.")
            else:
                print("Perdiste. ¡Probá de nuevo!")

            # TODO 14: llamar a guardar_saldo() pasándole el saldo
            guardar_saldo(saldo)

            # BONUS TRACK: registrar esta tirada en el historial.
            guardar_historial(archivo_historial, rodillos, premio, saldo)
        else:
            print("No tenés fichas. Cargá más con +")
    elif orden == "+":
        cantidad = int(input("¿Cuántas fichas querés cargar? "))
        saldo = saldo + cantidad
        guardar_saldo(saldo)
    elif orden == "s":
        guardar_saldo(saldo)
        print("Saldo guardado. ¡Hasta la próxima!")
        # TODO 15: salir del bucle while (¿qué instrucción corta un while?)
        break
    else:
        print("Opción inválida.")
