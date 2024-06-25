#PARA COMBINAR DATASETS DE MOCAP CON DATASET DE ENCODER
#PRIMERO uno los datasets de los encoders en 1 por cada test y cambio la frecuencia de muestreo de 100 a 120 Hz
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# # Cargar los tres datasets
# df1 = pd.read_csv('~/Documentos/ROB. BLANDA/SOFIA_Python/data/Data_prueba_celia/cuarta_prueba/data_test2.0midiendo.csv', usecols=[1, 2, 3, 4, 5, 6, 7, 8])
# df2 = pd.read_csv('~/Documentos/ROB. BLANDA/SOFIA_Python/data/Data_prueba_celia/cuarta_prueba/data_test2.1midiendo.csv', usecols=[1, 2, 3, 4, 5, 6, 7, 8])
# df3 = pd.read_csv('~/Documentos/ROB. BLANDA/SOFIA_Python/data/Data_prueba_celia/cuarta_prueba/data_test2.2midiendo.csv', usecols=[1, 2, 3, 4, 5, 6, 7, 8])

# # Asignar nombres de columnas
# columns = ['inclination_ref', 'orientation_ref', 'pitch_ref_rad', 'yaw_ref_rad', 'pitch_ref_deg', 'yaw_pitch_deg','MOTOR7','MOTOR8']
# df1.columns = columns
# df2.columns = columns
# df3.columns = columns

# # Calcular la media de los tres datasets
# df_mean = (df1 + df2 + df3) / 3

# # Guardar el nuevo dataset con la media
# df_mean.to_excel('~/Documentos/ROB. BLANDA/SOFIA_Python/data/Data_prueba_celia/cuarta_prueba/data_test2_ENCODER.xlsx', index=False)

# CABIAMOS FRECUENCIA DE MUESTREO DE ENCODER DE 100 A 120 HZ
# df = pd.read_excel('~/Documentos/ROB. BLANDA/SOFIA_Python/data/Data_prueba_celia/cuarta_prueba/data_test2_ENCODER.xlsx')
# # Asumimos que la frecuencia de muestreo original es de 100 Hz
# frecuencia_original = 100  # Hz
# frecuencia_nueva = 120  # Hz

# # Crear el índice de tiempo original y nuevo
# time_100hz = np.arange(0, len(df) / frecuencia_original, 1 / frecuencia_original)
# time_120hz = np.arange(0, time_100hz[-1], 1 / frecuencia_nueva)

# # Interpolar los datos originales a los nuevos tiempos
# df_resampled = pd.DataFrame()

# # Resamplear 
# for column in df.columns:
#     df_resampled[column] = np.interp(time_120hz, time_100hz, df[column])

# # Graficar el dataset original y el resampleado
# plt.figure(figsize=(14, 7))

# # Seleccionamos una columna para el ejemplo, puedes seleccionar la que prefieras
# column_to_plot_100 = df.columns[7]
# column_to_plot_120 = df_resampled.columns[7]

# plt.plot(time_100hz, df[column_to_plot_100], label=f'Original 100 Hz - {column_to_plot_100}', marker='o', linestyle='-', markersize=3)
# plt.plot(time_120hz, df_resampled[column_to_plot_120], label=f'Resampleado 120 Hz - {column_to_plot_120}', marker='x', linestyle='--', markersize=2)

# plt.title(f'Comparación del dataset original y resampleado ({column_to_plot_100})')
# plt.xlabel('Tiempo (s)')
# plt.ylabel('Valor')
# plt.legend()
# plt.grid(True)
# plt.show()

# # Guardar el DataFrame resampleado en un nuevo archivo Excel
# output_path = '~/Documentos/ROB. BLANDA/SOFIA_Python/data/Data_prueba_celia/cuarta_prueba/data_test2_ENCODER_120hz.xlsx'
# df_resampled.to_excel(output_path, index=False)




#SEGUNDO MOCAP############################################################################################################################################################################
## PRIMERO: poner los 3 datasets del mocap con el mismo numero de filas, vamos a quitar las filas que sobran al principio con el temporizador
# mocap1_6_df = pd.read_excel('~/Documentos/cuartaprueba(midiendo)/test1.6_brutos_quitandofilas2.xlsx')
# # # Parámetros proporcionados
# # # tiempo_a_quitar = 3.26  # en segundos
# # # frecuencia_muestreo = 120  # en Hz

# # # # Calcular el número de filas a eliminar
# # #filas_a_eliminar = 148
# # # print(f"Filas a eliminar: {filas_a_eliminar}")

# # # # Cargar el archivo Excel
# # # file_path = '~/Documentos/cuartaprueba(midiendo)/test2.2_brutos_transformada_encoder_dedos_ajust.xlsx'
# # # df = pd.read_excel(file_path)

# # # # Eliminar las filas iniciales
# # #mocap1_7_df = mocap1_7_df.iloc[filas_a_eliminar:].reset_index(drop=True) #Eliminamos las filas iniciales utilizando iloc para seleccionar 
# # # #las filas desde filas_a_eliminar hasta el final del DataFrame y luego reiniciamos los índices con reset_index(drop=True).
# start_row = 16702
# end_row = start_row + 432

# # # # # Eliminar filas específicas
# mocap1_6_df = mocap1_6_df.drop(mocap1_6_df.index[start_row:end_row]).reset_index(drop=True)

# # # # # # Guardar el DataFrame modificado en un nuevo archivo
# output_path = '~/Documentos/cuartaprueba(midiendo)/test1.6_brutos_quitandofilas2.xlsx'
# mocap1_6_df.to_excel(output_path, index=False)


#ALINEAR los 3 DATASETS de MOCAP############################################################################################################################################################################
# Cargar los datos
mocap1_5_df = pd.read_excel('~/Documentos/cuartaprueba(midiendo)/test1.5_brutos_quitandofilas2.xlsx')
mocap1_6_df = pd.read_excel('~/Documentos/cuartaprueba(midiendo)/test1.6_brutos_quitandofilas2.xlsx')
mocap1_7_df = pd.read_excel('~/Documentos/cuartaprueba(midiendo)/test1.7_brutos_quitandofilas2.xlsx')

def detect_keypoints(df, column, threshold):
    diffs = df[column].diff().abs()
    keypoints = df[diffs > threshold].index
    return keypoints

# Detectar puntos clave en los tres datasets
mocap1_5_keypoints = detect_keypoints(mocap1_5_df, 'Resultant Rotation Z', threshold=0.5)
mocap1_6_keypoints = detect_keypoints(mocap1_6_df, 'Resultant Rotation Z', threshold=0.5)
mocap1_7_keypoints = detect_keypoints(mocap1_7_df, 'Resultant Rotation Z', threshold=0.5)


# Alinear los puntos clave entre los tres datasets
def align_multiple_keypoints(*keypoints_lists):
    min_len = min(map(len, keypoints_lists))
    aligned_keypoints = [keypoints[:min_len] for keypoints in keypoints_lists]
    return aligned_keypoints

aligned_keypoints = align_multiple_keypoints(mocap1_5_keypoints, mocap1_6_keypoints, mocap1_7_keypoints)
aligned_mocap1_5_keypoints, aligned_mocap1_6_keypoints, aligned_mocap1_7_keypoints = aligned_keypoints


# Sincronizar los datasets utilizando interpolación
def synchronize_data(reference_df, target_df, reference_keypoints, target_keypoints):
    reference_index = reference_df.loc[reference_keypoints].index
    target_index = target_df.loc[target_keypoints].index
    
    interp_func = interp1d(target_index, reference_index, kind='linear', fill_value='extrapolate')
    synchronized_index = interp_func(target_df.index)
    
    target_df['synchronized_index'] = synchronized_index
    synchronized_target_df = target_df.set_index('synchronized_index').reindex(reference_df.index).interpolate().reset_index()
    
    return synchronized_target_df

synchronized_mocap1_6_df = synchronize_data(mocap1_5_df, mocap1_6_df, aligned_mocap1_5_keypoints, aligned_mocap1_6_keypoints)
synchronized_mocap1_7_df = synchronize_data(mocap1_5_df, mocap1_7_df, aligned_mocap1_5_keypoints, aligned_mocap1_7_keypoints)

plt.figure(figsize=(14, 7))

# Plot original data for reference
plt.plot(mocap1_5_df.index, mocap1_5_df['Resultant Rotation Z'], label='Mocap 1.5')
plt.plot(mocap1_6_df.index, mocap1_6_df['Resultant Rotation Z'], label='Mocap 1.6')
plt.plot(mocap1_7_df.index, mocap1_7_df['Resultant Rotation Z'], label='Mocap 1.7')

# Plot keypoints
plt.scatter(mocap1_5_df.loc[aligned_mocap1_5_keypoints].index, mocap1_5_df.loc[aligned_mocap1_5_keypoints, 'Resultant Rotation Z'], color='red', label='Mocap 1.5 Key Points')
plt.scatter(mocap1_6_df.loc[aligned_mocap1_6_keypoints].index, mocap1_6_df.loc[aligned_mocap1_6_keypoints, 'Resultant Rotation Z'], color='green', label='Mocap 1.6 Key Points')
plt.scatter(mocap1_7_df.loc[aligned_mocap1_7_keypoints].index, mocap1_7_df.loc[aligned_mocap1_7_keypoints, 'Resultant Rotation Z'], color='blue', label='Mocap 1.7 Key Points')

plt.xlabel('Index')
plt.ylabel('Rotation Z')
plt.legend()
plt.title('Synchronization of Mocap Data with Key Points')
plt.show()

#ALINEAR DATASET MOCAP CON ENCODER############################################################################################################################################################################


