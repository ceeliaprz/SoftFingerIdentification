# CORRECCION DE DATOS, por si no se han corregido todos los gaps mediante Motive (programa del MOCAP)
#solo se corrigen las columnas de las rotaciones XYZ, las posiciones no se corrigen al fin y al cabo no creo que las use! 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

#CREACION DE DATASET de datos brutos SOLO CON ROTACIONES CORREGIDAS################################################################################################
#df = pd.read_excel('~/Documentos/cuartaprueba(midiendo)/test1.6.xlsx', usecols="V:AA", skiprows=7)
df = pd.read_excel('~/Documentos/ROB. BLANDA/SoftFingerIdentification/Data_prueba_celia(MOCAP)/validacion MOCAP/model7elucleaned.xlsx', usecols="V:AA", skiprows=7)

# Asignar el nombre de la columna manualmente
df.columns = ['RotationZ', 'RotationX', 'RotationY', 'PositionX', 'PositionY', 'PositionZ']


# Exploratory Data Analysis (EDA)
# Funciones de análisis y corrección de datos
def plot_columns(data, title):
    fig, axs = plt.subplots(3, 1, figsize=(15, 15))
    columns = ['RotationZ', 'RotationX', 'RotationY']
    for i, col in enumerate(columns):
        if col in data.columns:
            axs[i].plot(data[col], label=col)
            axs[i].set_title(f'{col} - {title}')
            axs[i].legend()
    plt.tight_layout()
    plt.show()

# Detectar gaps (valores faltantes) y devolver los índices de las filas donde se encuentran
def detect_gaps(data):
    gaps = data.isnull().any()
    gap_indices = []
    if gaps.any():
        gap_indices = data.index[data.isnull()].tolist()
    return gaps, gap_indices

# Detección de outliers negativos en RotationY
def detect_negative_outliers(data, threshold=-100):
    outliers = data < threshold
    outlier_indices = data.index[outliers].tolist()
    return outliers, outlier_indices

# Función para corregir gaps y outliers
def correct_data(data):
    corrected_data = data.copy()
    
    # Detectar gaps y outliers
    gaps, gap_indices = detect_gaps(data)
    outliers, outlier_indices = detect_negative_outliers(data)

    # Corregir gaps mediante interpolación
    if gap_indices:
        corrected_data.loc[gap_indices] = data.interpolate().loc[gap_indices]

    # Corregir outliers mediante interpolación
    if outlier_indices:
        corrected_data.loc[outlier_indices] = np.nan
        corrected_data = corrected_data.interpolate()
    
    return corrected_data, gap_indices, outlier_indices, gaps, outliers

# Procesar cada columna de rotación
corrected_data_dict = {}
for col in ['RotationZ', 'RotationX', 'RotationY', 'PositionX', 'PositionY', 'PositionZ']:

    if(col == 'RotationY'): # se corrigen gaps y outliers
        # Detectar outliers y gaps
        corrected_data, gap_indices, outliers_indices, gaps, outliers = correct_data(df[col])
    else: #solo gaps
        corrected_data = df[col].copy()
        gaps, gap_indices = detect_gaps(df[col])
        # Corregir gaps mediante interpolación
        if gap_indices:
            corrected_data.loc[gap_indices] = df[col].interpolate().loc[gap_indices]

    corrected_data_dict[col] = corrected_data
    fig1, ax1 = plt.subplots(figsize=(15, 7))
    fig2, ax2 = plt.subplots(figsize=(15, 7))

    # Graficar datos sin corregir pero marcando gaps y outliers
    ax1.plot(df[col].index, df[col], label='Original Data')
    if gap_indices:
        print('Indices de gap:', gap_indices)
        for gap_index in gap_indices:
            ax1.plot(gap_index, 0, 'go', label='Gaps')
    if col == 'RotationY':
        ax1.plot(df[col].index[outliers], df[col][outliers], 'ro', label='Outliers')
    ax1.set_title(f'{col} - Original Data with Outliers and Gaps')
    ax1.legend()
    y_limits = ax1.get_ylim()  # Guardar los límites de los ejes Y
    ax1.set_ylim(y_limits)
    plt.tight_layout()
    

    # Graficar datos corregidos
    ax2.plot(corrected_data.index, corrected_data, label='Corrected Data')
    ax2.set_title(f'{col} - Corrected Data')
    ax2.set_ylim(y_limits)  # Mantener los límites de los ejes Y
    ax2.legend()
    plt.tight_layout()
    plt.show()

# Crear un nuevo DataFrame con las rotaciones y posiciones corregidas
corrected_df = pd.DataFrame(corrected_data_dict)

# Guardar los datos corregidos en un archivo Excel
corrected_df.to_excel('~/Documentos/ROB. BLANDA/SoftFingerIdentification/Data_prueba_celia(MOCAP)/validacion MOCAP/model7elucleaned_brutos.xlsx', index=False)