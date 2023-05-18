#!/usr/bin/env python3
import tensorflow as tf
import numpy as np

# Cargar el modelo desde el archivo .tflite
model_name_1 = 'command_model_2.tflite'
model_name_2 = 'command_model_3.tflite'
model_name_3 = 'command_model_4.tflite'


interpreter_1 = tf.lite.Interpreter(model_path=model_name_1)
interpreter_2 = tf.lite.Interpreter(model_path=model_name_2)
interpreter_3 = tf.lite.Interpreter(model_path=model_name_3)

# Asignar tensores a la entrada y salida del modelo
input_details_1 = interpreter_1.get_input_details()
output_details_1 = interpreter_1.get_output_details()
input_details_2 = interpreter_2.get_input_details()
output_details_2 = interpreter_2.get_output_details()
input_details_3 = interpreter_3.get_input_details()
output_details_3 = interpreter_3.get_output_details()


def prediction(input,input_details,interpreter,output_details):
    # Asignar los datos de entrada al tensor de entrada del modelo
    input_data = np.expand_dims(input.astype('float32'), axis=0)
    interpreter.allocate_tensors()
    commands = ['noise','go', 'take','bring','cancel','one','two','three','four','five','six','seven']
    # commands = ['now', 'take','fetch','noise','cancel','driver','pillow','slider','stick','stop','wrench','piston','crank']
    
    interpreter.set_tensor(input_details[0]['index'], input_data)

    # Ejecutar el modelo
    interpreter.invoke()

    # Obtener los resultados del modelo
    output_data = interpreter.get_tensor(output_details[0]['index'])
    threshold = 0.80
    true = np.argmax(output_data[0])
    if output_data[0][true] > threshold:
        print(commands[true], output_data[0][true])
    else:
        print('Not recognized') 
        #print(output_data)
    