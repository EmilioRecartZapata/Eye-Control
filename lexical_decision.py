from psychopy import visual, event, core
import random

# Configuración de la ventana
win = visual.Window(size=(800, 600), color='grey', units='pix')

# Fase de presentación del proyecto
mensaje_presentacion = visual.TextStim(win, text="Bienvenido a la tarea de decisión léxica", color='black', height=30)
mensaje_presentacion.draw()
win.flip()
event.waitKeys()

# Generar lista de palabras y no palabras para los trials
palabras = ["casa", "perro", "sol", "árbol", "manzana", "extraterrestre", 'telescopio', 'planeta', 'cohete', 'girafa']
no_palabras = ["fueco", "barol", "pentiente", "chono", "dalor", "antitud", "hucho", "midre", "balzana"]
todos_los_estimulos = palabras + no_palabras

# Generar 30 trials aleatorios
random.shuffle(todos_los_estimulos)
trials = todos_los_estimulos[:30]

# Crear cuadrados gigantes para las opciones
cuadro_izquierda = visual.Rect(win, width=400, height=400, lineColor='black', pos=(-200, 0))
cuadro_derecha = visual.Rect(win, width=400, height=400, lineColor='black', pos=(200, 0))

# Crear las opciones para cada trial
opcion_izquierda = visual.TextStim(win, text="", color='black', height=30, pos=(-200, 0))
opcion_derecha = visual.TextStim(win, text="", color='black', height=30, pos=(200, 0))

# Inicializar variables para contar los resultados
verdadero_positivo = 0
verdadero_negativo = 0
falso_positivo = 0
falso_negativo = 0

# Realizar los 30 trials
for estimulo in trials:
    # Obtener la categoría de la palabra actual
    categoria_actual = "palabra" if estimulo in palabras else "no_palabra"

    # Seleccionar aleatoriamente una palabra de la otra categoría
    palabra_opuesta = random.choice(palabras) if categoria_actual == "no_palabra" else random.choice(no_palabras)

    opciones = [opcion_izquierda, opcion_derecha]
    # Aleatorizar la posición de las palabras y las no palabras
    random.shuffle(opciones)

    # Asignar la palabra actual a una posición aleatoria
    opciones[0].setText(estimulo)
    # Asignar la palabra de la categoría opuesta a la otra posición
    opciones[1].setText(palabra_opuesta)

    cuadro_izquierda.draw()
    cuadro_derecha.draw()

    for opcion in opciones:
        opcion.draw()
    win.flip()

    mouse = event.Mouse(visible=True)
    mouse.clickReset()
    mouse_pressed = False
    cursor_positions = []
    while True:
        if mouse.getPressed()[0] == 1:
            mouse_pressed = True
            cursor_positions.append(mouse.getPos())
        elif mouse_pressed and mouse.getPressed()[0] == 0:
            break

    # Analizar respuesta
    respuesta_correcta = estimulo in palabras
    seleccion_izquierda = cursor_positions[-1][0] < 0

    if respuesta_correcta and seleccion_izquierda:
        verdadero_positivo += 1
    elif not respuesta_correcta and not seleccion_izquierda:
        verdadero_negativo += 1
    elif respuesta_correcta and not seleccion_izquierda:
        falso_negativo += 1
    elif not respuesta_correcta and seleccion_izquierda:
        falso_positivo += 1

# Mostrar resultados de los trials
print("Verdaderos Positivos:", verdadero_positivo)
print("Verdaderos Negativos:", verdadero_negativo)
print("Falsos Positivos:", falso_positivo)
print("Falsos Negativos:", falso_negativo)

# Tarea de reconocimiento
mensaje_reconocimiento = visual.TextStim(win, text="Tarea de reconocimiento", color='black', height=30)
mensaje_reconocimiento.draw()
win.flip()
event.waitKeys()

# Seleccionar 5 palabras y 5 no palabras para el test de atención
palabras_test_atencion = random.sample(palabras, 5) + random.sample(no_palabras, 5)

# Reiniciar variables para contar los resultados del test de atención
verdadero_positivo_atencion = 0
verdadero_negativo_atencion = 0
falso_positivo_atencion = 0
falso_negativo_atencion = 0

# Realizar el test de atención
for estimulo in palabras_test_atencion:
    opciones_test_atencion = random.sample([opcion_izquierda, opcion_derecha], 2)
    opciones_test_atencion[0].setText(estimulo)
    opciones_test_atencion[1].setText(random.choice(todos_los_estimulos))

    cuadro_izquierda.draw()
    cuadro_derecha.draw()

    for opcion in opciones_test_atencion:
        opcion.draw()
    win.flip()

    mouse.clickReset()
    mouse_pressed = False
    cursor_positions = []
    while True:
        if mouse.getPressed()[0] == 1:
            mouse_pressed = True
            cursor_positions.append(mouse.getPos())
        elif mouse_pressed and mouse.getPressed()[0] == 0:
            break

    # Analizar respuesta del test de atención
    respuesta_correcta_atencion = estimulo in palabras
    seleccion_izquierda_atencion = cursor_positions[-1][0] < 0

    if respuesta_correcta_atencion and seleccion_izquierda_atencion:
        verdadero_positivo_atencion += 1
    elif not respuesta_correcta_atencion and not seleccion_izquierda_atencion:
        verdadero_negativo_atencion += 1
    elif respuesta_correcta_atencion and not seleccion_izquierda_atencion:
        falso_negativo_atencion += 1
    elif not respuesta_correcta_atencion and seleccion_izquierda_atencion:
        falso_positivo_atencion += 1

# Mostrar resultados del test de atención
print("\nResultados del Test de Atención:")
print("Verdaderos Positivos:", verdadero_positivo_atencion)
print("Verdaderos Negativos:", verdadero_negativo_atencion)
print("Falsos Positivos:", falso_positivo_atencion)
print("Falsos Negativos:", falso_negativo_atencion)

# Cierre de la ventana al finalizar
win.close()
core.quit()
