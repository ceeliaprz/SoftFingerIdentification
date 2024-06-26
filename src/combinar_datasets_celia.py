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
#mocap1_5_df = pd.read_excel('~/Documentos/cuartaprueba(midiendo)/test2.0_brutos_quitandofilas2.xlsx')
#mocap1_6_df = pd.read_excel('~/Documentos/cuartaprueba(midiendo)/test2.1_brutos_quitandofilas2.xlsx')
#mocap1_7_df = pd.read_excel('~/Documentos/cuartaprueba(midiendo)/test2.2_brutos_quitandofilas2.xlsx')

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


# Eliminar filas específicas para alinear entre si los 3 datasets
# start_row = 11072
# end_row = start_row + 30
#mocap1_5_df = mocap1_5_df.drop(mocap1_5_df.index[start_row:end_row]).reset_index(drop=True)
#mocap1_6_df = mocap1_6_df.drop(mocap1_6_df.index[start_row:end_row]).reset_index(drop=True)
#mocap1_7_df = mocap1_7_df.drop(mocap1_7_df.index[start_row:end_row]).reset_index(drop=True)

# # # # # # # Guardar el DataFrame modificado en un nuevo archivo
# output_path = '~/Documentos/cuartaprueba(midiendo)/test2.0_brutos_quitandofilas2.xlsx'
# mocap1_5_df.to_excel(output_path, index=False)

# output_path = '~/Documentos/cuartaprueba(midiendo)/test2.1_brutos_quitandofilas2.xlsx'
# mocap1_6_df.to_excel(output_path, index=False)

# output_path = '~/Documentos/cuartaprueba(midiendo)/test2.2_brutos_quitandofilas2.xlsx'
# mocap1_7_df.to_excel(output_path, index=False)

#ALINEAR los 3 DATASETS de MOCAP############################################################################################################################################################################
# Cargar los datos
# mocap1_5_df = pd.read_excel('~/Documentos/ROB. BLANDA/SoftClawIdentification/cuartaprueba(DATOSMOCAP)/test2.0_brutos_quitandofilas2.xlsx')
# mocap1_6_df = pd.read_excel('~/Documentos/ROB. BLANDA/SoftClawIdentification/cuartaprueba(DATOSMOCAP)/test2.1_brutos_quitandofilas2.xlsx')
# mocap1_7_df = pd.read_excel('~/Documentos/ROB. BLANDA/SoftClawIdentification/cuartaprueba(DATOSMOCAP)/test2.2_brutos_quitandofilas2.xlsx')


# # Crear la figura y los subplots
# fig, axs = plt.subplots(2, 1, figsize=(14, 14))

# # Sincronización de los datasets
# axs[0].plot(mocap1_5_df.index, mocap1_5_df['Resultant Rotation Z'], label='Mocap 2.0')
# axs[0].plot(mocap1_6_df.index, mocap1_6_df['Resultant Rotation Z'], label='Mocap 2.1')
# axs[0].plot(mocap1_7_df.index, mocap1_7_df['Resultant Rotation Z'], label='Mocap 2.2')
# axs[0].set_xlabel('Index')
# axs[0].set_ylabel('Rotation Z')
# axs[0].legend()
# axs[0].set_title('Synchronization of Mocap Data')


# ## MEDIA 3 DEL MOCAP
# # Asignar nombres de columnas
# columns = ['Resultant Rotation X', 'Resultant Rotation Y', 'Resultant Rotation Z', 'Resultant Position X', 'Resultant Position Y', 'Resultant Position Z']
# mocap1_5_df.columns = columns
# mocap1_6_df.columns = columns
# mocap1_7_df.columns = columns

# # Calcular la media de los tres datasets
# df_mean = (mocap1_5_df + mocap1_6_df + mocap1_7_df) / 3

# # Gráfica de la media
# axs[1].plot(df_mean.index, df_mean['Resultant Rotation Z'], label='Mean Mocap')
# axs[1].set_xlabel('Index')
# axs[1].set_ylabel('Rotation Z')
# axs[1].legend()
# axs[1].set_title('Mean Rotation Z of Mocap Data')

# # Mostrar la figura con los subplots
# plt.tight_layout()
# plt.show()

# # Guardar el nuevo dataset con la media
# df_mean.to_excel('~/Documentos/ROB. BLANDA/SoftClawIdentification/cuartaprueba(DATOSMOCAP)/data_test2_MOCAP.xlsx', index=False)

#ALINEAR DATASET MOCAP CON ENCODER############################################################################################################################################################################
# Cargar los datos
encoder_df = pd.read_excel('~/Documentos/ROB. BLANDA/SOFIA_Python/data/Data_prueba_celia/cuarta_prueba/data_test1_ENCODER_120hz.xlsx')
mocap_df = pd.read_excel('~/Documentos/ROB. BLANDA/SoftClawIdentification/cuartaprueba(DATOSMOCAP)/data_test1_MOCAP.xlsx')

