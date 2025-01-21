import PyKDL
import math
import pandas as pd
#PARA CALCULAR LA MATRIZ DE TRANS HOMOGENEA, SE MIDE DEL SISTEMA EN EL QUE QUIERO EL PUNTO AL SISTEMA DONDE ESTA EL PUNTO

#TRANSFORMADA BASE/ENCODER [FIJA PARA TODAS LAS DEMAS TOMAS DE DATOS]********************************************************************************************************************
 ##mido primero de base a encoder como si los quisiera en la base
rotacion_base_encoder = PyKDL.Rotation.RotY(math.radians(120))
traslacion_base_encoder = PyKDL.Vector(-0.03, 0.09458, 0)#en METROS
transformada_base_encoder = PyKDL.Frame(rotacion_base_encoder, traslacion_base_encoder)
 ##INVIERTO PARA OBTENER ENCODER A BASE
transformada_encoder_base = transformada_base_encoder.Inverse()
# print("Matriz de Transformación encoder base:")
# print(transformada_encoder_base)


#TRANSFORMADA GLOBAL/BASE [FIJA PERO CADA VEZ QUE SE TOMAN DATOS HABRÁ QUE CALCULARLA]********************************************************************************************************************
  # mido primero de global a base como si los quisiera en la global
rotacion_global_base = PyKDL.Rotation.RPY(math.radians(0.0075), math.radians(141.86), math.radians(0.02))
traslacion_global_base = PyKDL.Vector(0.09484565897, 0.2454492718, 0.00012274815) #en METROS pero ojo que en motive exportamos en cm
transformada_global_base = PyKDL.Frame(rotacion_global_base, traslacion_global_base)
roll, pitch, yaw = transformada_global_base.M.GetRPY()
roll_deg = math.degrees(roll) #x
pitch_deg = math.degrees(pitch) #y
yaw_deg = math.degrees(yaw) #z
print("angulos en grados:", roll_deg, pitch_deg, yaw_deg)

  ##INVIERTO PARA OBTENER BASE A GLOBAL
transformada_base_global = transformada_global_base.Inverse()
print("Matriz de Transformación base global:")
print(transformada_base_global)
roll_invertido, pitch_invertido, yaw_invertido = transformada_base_global.M.GetRPY()
pitch_invertido_deg = math.degrees(pitch_invertido)
print("Pitch invertido en grados:", pitch_invertido_deg)

#TRANSFORMADA GLOBAL/DEDOS[CALCULARLA PARA CADA FILA DEL DATASET Y CADA VEZ QUE TOMEMOS DATOS]********************************************************************************************************************
# Definir los nombres de las columnas
column_names = ['Rotation Z', 'Rotation X', 'Rotation Y', 'Position X', 'Position Y', 'Position Z']

# Leer el archivo Excel desde las filas y columnas especificadas
df = pd.read_excel('~/Documentos/ROB. BLANDA/SoftFingerIdentification/Data_prueba_celia(MOCAP)/validacion MOCAP/model7elucleaned_brutos.xlsx', usecols="A:F", skiprows=0, header=None)

# Eliminar la primera fila que contiene encabezados incorrectos
df = df.iloc[1:]

# Asignar los nombres de las columnas manualmente
df.columns = column_names

# Convertir todos los valores a cadenas y luego a floats, reemplazando comas por puntos
df = df.applymap(lambda x: float(str(x).replace(',', '.')))

# Imprimir los nombres de las columnas para verificar
print("Columnas leídas del archivo Excel:")
print(df.columns)

# Crear una lista para almacenar los transformada_base_dedos
lista_transformada_base_dedos = []
lista_transformada_encoder_dedos = []
lista_transformada_encoder_dedos_ajustada = []

# Definir la rotación adicional para alinear los ejes dedos con encoder ¡¡cuidado que para cada dataset varía!!
# El ángulo se saca una vez obtenido el dataset transformado encoder_dedos, viendo que al inicio del movimiento este debería estar en 0
# rotacion_ajuste_y = PyKDL.Rotation.RotY(math.radians(-81.87))
# rotacion_ajuste_x = PyKDL.Rotation.RotX(math.radians(-170.9))
# rotacion_ajuste_z = PyKDL.Rotation.RotZ(math.radians(-171.59))
# rotacion_ajuste_total = rotacion_ajuste_x * rotacion_ajuste_y * rotacion_ajuste_z

# Iterar sobre las filas del DataFrame
for index, row in df.iterrows():
    # Leer la rotación y traslación desde el DataFrame
    rot_z = row['Rotation Z'] #grados
    rot_x = row['Rotation X']
    rot_y = row['Rotation Y']
    pos_x = row['Position X']/100 #necesito m y tenia cm
    pos_y = row['Position Y']/100
    pos_z = row['Position Z']/100
    
    # Crear la rotación y traslación en PyKDL
    rotacion_global_dedos = PyKDL.Rotation.RPY(math.radians(rot_x), math.radians(rot_y), math.radians(rot_z))
    traslacion_global_dedos = PyKDL.Vector(pos_x, pos_y, pos_z)
    
    # Crear la matriz de transformación
    transformada_global_dedos = PyKDL.Frame(rotacion_global_dedos, traslacion_global_dedos)
    #print("Matriz de Transformación global dedos:")
    #print(transformada_global_dedos)
    #rot_global_dedos= [math.degrees(angle) for angle in transformada_global_dedos.M.GetRPY()]
    #print(rot_global_dedos)


    # Multiplicar la transformación por la transformación fija
    transformada_base_dedos = transformada_base_global * transformada_global_dedos 
    # print("Matriz de Transformación base dedos:")
    # print(transformada_base_dedos)

    transformada_encoder_dedos = transformada_encoder_base * transformada_base_dedos

    # Aplicar la rotación de ajuste
    # transformada_encoder_dedos_ajustada = PyKDL.Frame(transformada_encoder_dedos.M*rotacion_ajuste_total, transformada_encoder_dedos.p) 

    ## Extraer la rotación y traslación en grados y centímetros para base a dedos
    rot_base_dedos = [math.degrees(angle) for angle in transformada_base_dedos.M.GetRPY()]
    pos_base_dedos = [transformada_base_dedos.p.x() * 100, transformada_base_dedos.p.y() * 100, transformada_base_dedos.p.z() * 100]

    # Guardar el resultado
    lista_transformada_base_dedos.append([rot_base_dedos[0], rot_base_dedos[1], rot_base_dedos[2],
                       pos_base_dedos[0], pos_base_dedos[1], pos_base_dedos[2]])

    # Extraer rotación y traslación en grados y centímetros para encoder a dedos
    rot_encoder_dedos = [math.degrees(angle) for angle in transformada_encoder_dedos.M.GetRPY()]
    pos_encoder_dedos = [transformada_encoder_dedos.p.x() * 100, transformada_encoder_dedos.p.y() * 100, transformada_encoder_dedos.p.z() * 100]
    
    # Guardar el resultado también para encoder a dedos
    lista_transformada_encoder_dedos.append([rot_encoder_dedos[0], rot_encoder_dedos[1], rot_encoder_dedos[2],
                       pos_encoder_dedos[0], pos_encoder_dedos[1], pos_encoder_dedos[2]])


    # rot_encoder_dedos_ajust = [math.degrees(angle) for angle in transformada_encoder_dedos_ajustada.M.GetRPY()]
    # pos_encoder_dedos_ajust = [transformada_encoder_dedos_ajustada.p.x() * 100, transformada_encoder_dedos_ajustada.p.y() * 100, transformada_encoder_dedos_ajustada.p.z() * 100]
    
    # # Guardar el resultado también para encoder a dedos
    # lista_transformada_encoder_dedos_ajustada.append([rot_encoder_dedos_ajust[0], rot_encoder_dedos_ajust[1], rot_encoder_dedos_ajust[2],
    #                    pos_encoder_dedos_ajust[0], pos_encoder_dedos_ajust[1], pos_encoder_dedos_ajust[2]])


# # Convertir los transformada_base_dedos a un DataFrame de pandas
resultados_df_base_dedos = pd.DataFrame(lista_transformada_base_dedos, columns=['Resultant Rotation X', 'Resultant Rotation Y', 'Resultant Rotation Z', 
                                                  'Resultant Position X', 'Resultant Position Y', 'Resultant Position Z'])

# # Guardar los transformada_base_dedos en un nuevo archivo Excel
resultados_df_base_dedos.to_excel('~/Documentos/ROB. BLANDA/SoftFingerIdentification/Data_prueba_celia(MOCAP)/validacion MOCAP/transformadas/model7elucleaned_brutos_trans_base_dedos.xlsx', index=False)

# #convertir los transformada_encoder_dedos a un DataFrame de pandas
resultados_df_encoder_dedos = pd.DataFrame(lista_transformada_encoder_dedos, columns=['Resultant Rotation X', 'Resultant Rotation Y', 'Resultant Rotation Z',
                                                  'Resultant Position X', 'Resultant Position Y', 'Resultant Position Z'])

# Guardar los transformada_encoder_dedos en un nuevo archivo Excel
resultados_df_encoder_dedos.to_excel('~/Documentos/ROB. BLANDA/SoftFingerIdentification/Data_prueba_celia(MOCAP)/validacion MOCAP/transformadas/model7elucleaned_brutos_trans_encoder_dedos.xlsx', index=False)

# # #convertir los transformada_encoder_dedos a un DataFrame de pandas
# resultados_df_encoder_dedos_ajustada = pd.DataFrame(lista_transformada_encoder_dedos_ajustada, columns=['Resultant Rotation X', 'Resultant Rotation Y', 'Resultant Rotation Z',
#                                                   'Resultant Position X', 'Resultant Position Y', 'Resultant Position Z'])

# # Guardar los transformada_encoder_dedos en un nuevo archivo Excel
# resultados_df_encoder_dedos_ajustada.to_excel('~/Documentos/ROB. BLANDA/SoftFingerIdentification/Data_prueba_celia(MOCAP)/validacion MOCAP/transformadas/AJUSTADAS/model7elucleaned_brutos_trans_encoder_dedos_ajust.xlsx', index=False)

