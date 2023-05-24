#!/usr/bin/env python3
import tensorflow as tf
import numpy as np

# model_names = ['command_model.tflite', 'command_model_1.tflite', 'command_model_2.tflite', 'command_model_3.tflite', 'command_model_4.tflite']
# interpreters = [tf.lite.Interpreter(model_path=model_name) for model_name in model_names]
# input_details = [interpreter.get_input_details() for interpreter in interpreters]
# output_details = [interpreter.get_output_details() for interpreter in interpreters]
model_name = 'numbers_model.tflite'
interpreter = tf.lite.Interpreter(model_path=model_name)
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
commands = ['noise','bring','cancel','go', 'take']
commands = ['noise','cancel','one','two','three','four','five','six','seven']

threshold = 0.90

def prediction_multi(input, input_details, interpreter, output_details):
    input_data = np.expand_dims(input.astype('float32'), axis=0)
    interpreter.allocate_tensors()
    
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    
    output_data = interpreter.get_tensor(output_details[0]['index'])
    
    true = np.argmax(output_data)
    if output_data[0][true] > threshold:
        return commands[true]
    else:
        return 'Not recognized'

def prediction(input,input_details,interpreter,output_details):
    # Asignar los datos de entrada al tensor de entrada del modelo
    input_data = np.expand_dims(input.astype('float32'), axis=0)
    interpreter.allocate_tensors()
    
    interpreter.set_tensor(input_details[0]['index'], input_data)

    # Ejecutar el modelo
    interpreter.invoke()

    # Obtener los resultados del modelo
    output_data = interpreter.get_tensor(output_details[0]['index'])
    threshold = 0.90
    true = np.argmax(output_data[0])
    if output_data[0][true] > threshold:
        return(commands[true])
    else:
        return('Not recognized') 
        #print(output_data)