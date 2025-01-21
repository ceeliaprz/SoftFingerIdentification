import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# # Cargar datasets
df1 = pd.read_csv('~/Documentos/ROB. BLANDA/SOFIA_Python/data/Data_prueba_celia/validacion/movpred_RandomForest.csv', usecols=[1, 2, 3, 4, 5, 6, 7, 8])
# df2 = pd.read_csv('~/Documentos/ROB. BLANDA/SOFIA_Python/data/Data_prueba_celia/cuarta_prueba/data_test2.1midiendo.csv', usecols=[1, 2, 3, 4, 5, 6, 7, 8])
# df3 = pd.read_csv('~/Documentos/ROB. BLANDA/SOFIA_Python/data/Data_prueba_celia/cuarta_prueba/data_test2.2midiendo.csv', usecols=[1, 2, 3, 4, 5, 6, 7, 8])

# # Asignar nombres de columnas
columns = ['inclination_ref', 'orientation_ref', 'pitch_ref_rad', 'yaw_ref_rad', 'pitch_ref_deg', 'yaw_ref_deg','MOTOR7_pred','MOTOR8_pred']
df1.columns = columns
# df2.columns = columns
# df3.columns = columns

# # Calcular la media de los tres datasets (esto se hizo para los primeros movimientos grabados, para obtener la media de los tres datasets que son el mismo movimiento)
# df_mean = (df1 + df2 + df3) / 3

# # Guardar el nuevo dataset con la media
# df_mean.to_excel('~/Documentos/ROB. BLANDA/SOFIA_Python/data/Data_prueba_celia/cuarta_prueba/data_test2_ENCODER.xlsx', index=False)

# # Guardar dataset de csv en archivo excel
df1.to_excel('~/Documentos/ROB. BLANDA/SOFIA_Python/data/Data_prueba_celia/validacion/data_RandomForest_ENCODER.xlsx', index=False)

