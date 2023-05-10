#!/usr/bin/env python3
import tensorflow as tf
import numpy as np



# Cargar el modelo desde el archivo .tflite
model_name = 'command_model.tflite'
interpreter = tf.lite.Interpreter(model_path=model_name)

# Asignar tensores a la entrada y salida del modelo
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()


def prediction(input,input_details,interpreter,output_details):
    # Asignar los datos de entrada al tensor de entrada del modelo
    input_data = np.expand_dims(input.astype('float32'), axis=0)
    interpreter.allocate_tensors()
    # commands = ['now', 'take','fetch','noise','cancel']
    commands = ['take', 'wrench','fetch','noise','now','cancel']
    interpreter.set_tensor(input_details[0]['index'], input_data)

    # Ejecutar el modelo
    interpreter.invoke()

    # Obtener los resultados del modelo
    output_data = interpreter.get_tensor(output_details[0]['index'])
    threshold = 0.9
    true = np.argmax(output_data[0])
    if output_data[0][true] > threshold:
        print(commands[true])
    print(output_data)