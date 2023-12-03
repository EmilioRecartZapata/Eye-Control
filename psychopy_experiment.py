from psychopy import visual, event, core
import random
import cv2
import mediapipe as mp
import pyautogui

win = visual.Window(size=(800, 600), color='grey', units='pix')

cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_w, screen_h = pyautogui.size()

mensaje_presentacion = visual.TextStim(win, text="Bienvenido a la tarea de decisión léxica", color='black', height=30)
mensaje_presentacion.draw()
win.flip()
event.waitKeys()

palabras = ["casa", "perro", "sol", "árbol", "manzana", "extraterrestre", 'telescopio', 'planeta', 'cohete', 'girafa']
no_palabras = ["fueco", "barol", "pentiente", "chono", "dalor", "antitud", "hucho", "midre", "balzana"]
todos_los_estimulos = palabras + no_palabras

random.shuffle(todos_los_estimulos)
trials = todos_los_estimulos[:30]

cuadro_izquierda = visual.Rect(win, width=400, height=400, lineColor='black', pos=(-200, 0))
cuadro_derecha = visual.Rect(win, width=400, height=400, lineColor='black', pos=(200, 0))

opcion_izquierda = visual.TextStim(win, text="", color='black', height=30, pos=(-200, 0))
opcion_derecha = visual.TextStim(win, text="", color='black', height=30, pos=(200, 0))

verdadero_positivo = 0
verdadero_negativo = 0
falso_positivo = 0
falso_negativo = 0

for estimulo in trials:
    categoria_actual = "palabra" if estimulo in palabras else "no_palabra"

    palabra_opuesta = random.choice(palabras) if categoria_actual == "no_palabra" else random.choice(no_palabras)

    opciones = [opcion_izquierda, opcion_derecha]
    random.shuffle(opciones)

    opciones[0].setText(estimulo)
    opciones[1].setText(palabra_opuesta)

    cuadro_izquierda.draw()
    cuadro_derecha.draw()

    for opcion in opciones:
        opcion.draw()
    win.flip()

    # Control ocular
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks
    frame_h, frame_w, _ = frame.shape

    if landmark_points:
        landmarks = landmark_points[0].landmark
        for id, landmark in enumerate(landmarks[1:4]):
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 0))
            if id == 1:
                amplification_factor = 1  # Valores menores a 1 desplaza Up Left y valores mayores Down Right
                screen_x = screen_w * landmark.x * amplification_factor
                screen_y = screen_h * landmark.y * amplification_factor
                pyautogui.moveTo(screen_x, screen_y)

        left = [landmarks[145], landmarks[159]]
        right = [landmarks[374], landmarks[386]]

        # Contar el número de pestañeos
        num_blinks = 0
        for eye in [left, right]:
            if (eye[0].y - eye[1].y) < 0.004:
                num_blinks += 1

        if num_blinks == 1:
            respuesta = "izquierda"
        elif num_blinks == 2:
            respuesta = "derecha"
        else:
            respuesta = "ninguna"

        print("Respuesta:", respuesta)

    keys = event.waitKeys(keyList=['left', 'right'])
    
    respuesta_correcta = estimulo in palabras
    seleccion_izquierda = keys[0] == 'left'

    if respuesta_correcta and seleccion_izquierda:
        verdadero_positivo += 1
    elif not respuesta_correcta and not seleccion_izquierda:
        verdadero_negativo += 1
    elif respuesta_correcta and not seleccion_izquierda:
        falso_negativo += 1
    elif not respuesta_correcta and seleccion_izquierda:
        falso_positivo += 1

print("Verdaderos Positivos:", verdadero_positivo)
print("Verdaderos Negativos:", verdadero_negativo)
print("Falsos Positivos:", falso_positivo)
print("Falsos Negativos:", falso_negativo)

mensaje_reconocimiento = visual.TextStim(win, text="Tarea de reconocimiento", color='black', height=30)
mensaje_reconocimiento.draw()
win.flip()
event.waitKeys()

palabras_test_atencion = random.sample(palabras, 5) + random.sample(no_palabras, 5)

verdadero_positivo_atencion = 0
verdadero_negativo_atencion = 0
falso_positivo_atencion = 0
falso_negativo_atencion = 0

for estimulo in palabras_test_atencion:
    opciones_test_atencion = random.sample([opcion_izquierda, opcion_derecha], 2)
    opciones_test_atencion[0].setText(estimulo)
    opciones_test_atencion[1].setText(random.choice(todos_los_estimulos))

    cuadro_izquierda.draw()
    cuadro_derecha.draw()

    for opcion in opciones_test_atencion:
        opcion.draw()
    win.flip()

    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks
    frame_h, frame_w, _ = frame.shape

    if landmark_points:
        landmarks = landmark_points[0].landmark
        for id, landmark in enumerate(landmarks[1:4]):
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 0))
            if id == 1:
                amplification_factor = 1  # Valores menores a 1 desplaza Up Left y valores mayores Down Right
                screen_x = screen_w * landmark.x * amplification_factor
                screen_y = screen_h * landmark.y * amplification_factor
                pyautogui.moveTo(screen_x, screen_y)

        left = [landmarks[145], landmarks[159]]
        right = [landmarks[374], landmarks[386]]

        num_blinks = 0
        for eye in [left, right]:
            if (eye[0].y - eye[1].y) < 0.004:
                num_blinks += 1

        if num_blinks == 1:
            respuesta = "izquierda"
        elif num_blinks == 2:
            respuesta = "derecha"
        else:
            respuesta = "ninguna"

        print("Respuesta:", respuesta)

    keys = event.waitKeys(keyList=['left', 'right'])

    respuesta_correcta_atencion = estimulo in palabras
    seleccion_izquierda_atencion = keys[0] == 'left'

    if respuesta_correcta_atencion and seleccion_izquierda_atencion:
        verdadero_positivo_atencion += 1
    elif not respuesta_correcta_atencion and not seleccion_izquierda_atencion:
        verdadero_negativo_atencion += 1
    elif respuesta_correcta_atencion and not seleccion_izquierda_atencion:
        falso_negativo_atencion += 1
    elif not respuesta_correcta_atencion and seleccion_izquierda_atencion:
        falso_positivo_atencion += 1

print("\nResultados del Test de Atención:")
print("Verdaderos Positivos:", verdadero_positivo_atencion)
print("Verdaderos Negativos:", verdadero_negativo_atencion)
print("Falsos Positivos:", falso_positivo_atencion)
print("Falsos Negativos:", falso_negativo_atencion)

win.close()
core.quit()
