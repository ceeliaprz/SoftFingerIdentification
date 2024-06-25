#INTENTO DE CORRECION DE DATOS
#solo se corrigen las comlumnas de las rotaciones XYZ, las posiciones no se corrigen al fin y al cabo no creo que las use! 
#pero para luego hacer los cambios de bases, tener en cuenta que las posiciones no estan corregidas, 
#tendre que meter en el datset_corregido las posiciones sin corregir
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# # Cargar el dataset y solo seleccionar la columna 'V'
# df = pd.read_excel('~/Documentos/cuartaprueba(midiendo)/test1.5.xlsx', usecols="V:AA", skiprows=7)

# # Asignar el nombre de la columna manualmente
# df.columns = ['RotationZ', 'RotationX', 'RotationY', 'PositionX', 'PositionY', 'PositionZ']

# #SOLO CORRIJO LAS ROTACIONES
# # Exploratory Data Analysis (EDA)
# # Funciones de análisis y corrección de datos
# def plot_columns(data, title):
#     fig, axs = plt.subplots(3, 1, figsize=(15, 15))
#     columns = ['RotationZ', 'RotationX', 'RotationY']
#     for i, col in enumerate(columns):
#         if col in data.columns:
#             axs[i].plot(data[col], label=col)
#             axs[i].set_title(f'{col} - {title}')
#             axs[i].legend()
#     plt.tight_layout()
#     plt.show()

# # Detectar gaps (valores faltantes) y devolver los índices de las filas donde se encuentran
# def detect_gaps(data):
#     gaps = data.isnull().any()
#     gap_indices = []
#     if gaps.any():
#         gap_indices = data.index[data.isnull()].tolist()
#     return gaps, gap_indices

# # Suavizar los datos usando un filtro de media exponencial
# def smooth_data(data, span=5):
#     return data.ewm(span=span, adjust=False).mean()

# # Detección de outliers usando el rango intercuartílico (IQR)
# def detect_outliers_iqr(data):
#     Q1 = data.quantile(0.25)
#     Q3 = data.quantile(0.75)
#     IQR = Q3 - Q1
#     outliers = ((data < (Q1 - 1.5 * IQR)) | (data > (Q3 + 1.5 * IQR)))
#     outlier_indices = data.index[outliers].tolist()
#     return outliers, outlier_indices

# # Función para detectar segmentos estables en los datos suavizados
# def detect_stable_segments(data, threshold=0.25, threshold2=100):
#     segments = []
#     start = 0
#     for i in range(1, len(data)):
#         if not np.isnan(data[i]) and abs(data[i] - data[start]) > threshold and abs(data[i] - data[start]) < threshold2:
#             segments.append((start, i))
#             start = i
#     segments.append((start, len(data)))
#     return segments

# # Función para corregir gaps y outliers
# def correct_data(data):
#     corrected_data = data.copy()
    
#     # Detectar gaps y outliers
#     gaps, gap_indices = detect_gaps(data)
#     outliers, outlier_indices = detect_outliers_iqr(data)

#     # Corregir gaps mediante interpolación
#     if gap_indices:
#         corrected_data.loc[gap_indices] = data.interpolate().loc[gap_indices]

#     # Corregir outliers mediante interpolación
#     if outlier_indices:
#         corrected_data.loc[outlier_indices] = np.nan
#         corrected_data = corrected_data.interpolate()
    
#     return corrected_data, gap_indices, outlier_indices, gaps, outliers

# #plot_columns(df, 'Original Data')

# # Procesar cada columna de rotación
# corrected_data_dict = {}
# for col in ['RotationZ', 'RotationX', 'RotationY']:

#     if(col == 'RotationZ' or col == 'RotationX'):
#         # Suavizar los datos
#         smoothed_data = smooth_data(df[col])
#         # Detectar segmentos estables en los datos suavizados
#         segments = detect_stable_segments(smoothed_data, threshold=0.25)
#     else:
#         segments = [(0, len(df))]

#     # Lista para almacenar los segmentos corregidos
#     corrected_segments = []
#     fig3, ax3 = plt.subplots(figsize=(15, 7))
#     fig4, ax4 = plt.subplots(figsize=(15, 7))

#     # # Crear una gráfica para los datos originales
#     # fig1, ax1 = plt.subplots(figsize=(15, 7))
#     # ax1.plot(df['RotationZ'], label='Data')
#     # ax1.set_title('Original Data')
#     # ax1.legend()
#     # plt.tight_layout()

#     # # Crear una gráfica para los datos suavizados
#     # fig2, ax2 = plt.subplots(figsize=(15, 7))
#     # ax2.plot(smoothed_data, label='Smoothed Data', linestyle='--')
#     # ax2.set_title('Smoothed Data')
#     # ax2.legend()
#     # plt.tight_layout()

#     # # Crear una tercera figura para mostrar los datos con outliers destacados
#     # fig3, ax3 = plt.subplots(figsize=(15, 7))
#     # ax3.plot(df['RotationZ'], label='Original Data with Outliers and Gaps') 

#     # # Crear una cuarta figura para mostrar los datos interpolados y corregidos
#     # fig4, ax4 = plt.subplots(figsize=(15, 7))


#     # Graficar segmentos estables
#     for start, end in segments:
#         segment_data = df[col].iloc[start:end]

#         # Detectar outliers y gaps
#         segment_data_interpolated, gap_indices, outliers_indices, gaps, outliers = correct_data(segment_data)

#         # Agregar el segmento corregido a la lista
#         corrected_segments.append(segment_data_interpolated)

#         # Verificar si hay gaps y graficarlos
#         if gap_indices:
#             print('Indices de gap:', gap_indices)
#             #print("Indices de segment_data:", segment_data.index)
#             for gap_index in gap_indices:
#                 ax3.plot(gap_index, 0, 'go', label='Gaps' if start == 0 else "")
#                 ax4.plot(gap_index, segment_data_interpolated.loc[gap_index], 'go', label='Gaps' if start == 0 else "")

#         # Graficar outliers y gaps en los segmentos corregidos
#         ax4.plot(segment_data_interpolated.index, segment_data_interpolated, label=f'Segment {start}-{end}')
#         ax4.plot(outliers_indices, segment_data_interpolated.loc[outliers_indices], 'ro', label='Corrected Outliers' if start == 0 else "")

#         # Graficar datos sin corregir pero marcando outliers en los segmentos
#         ax3.plot(segment_data.index, segment_data, label=f'Segment {start}-{end}')
#         ax3.plot(segment_data.index[outliers], segment_data[outliers], 'ro', label='Outliers' if start == 0 else "")

#     # Unir los segmentos corregidos en una sola serie de datos e interpolar
#     corrected_data = pd.concat(corrected_segments).sort_index().interpolate()
#     corrected_data_dict[col] = corrected_data

#     ax3.set_title(f'{col} - Original Data with Outliers and Gaps')
#     ax3.legend()
#     y_limits = ax3.get_ylim()  # Guardar los límites de los ejes Y
#     ax3.set_ylim(y_limits)
#     plt.tight_layout()
    

#     ax4.set_title(f'{col} - Interpolated and Corrected Data')
#     ax4.set_ylim(y_limits)  # Mantener los límites de los ejes Y
#     ax4.legend()
#     plt.tight_layout()
    

#     # Graficar los datos corregidos completos
#     fig5, ax5 = plt.subplots(figsize=(15, 7))
#     ax5.plot(corrected_data_dict[col], label='Fully Corrected Data')
#     ax5.set_title('Fully Corrected Data')
#     ax5.set_ylim(y_limits)  # Mantener los límites de los ejes Y
#     ax5.legend()
#     plt.tight_layout()
#     plt.show()
    
# #plot_columns(pd.DataFrame(corrected_data_dict), 'Corrected Data')

# # Crear un nuevo DataFrame con las rotaciones corregidas y posiciones originales
# corrected_df = pd.DataFrame(corrected_data_dict)
# for col in ['PositionX', 'PositionY', 'PositionZ']:
#     corrected_df[col] = df[col]

# # Guardar los datos corregidos en un archivo Excel
# corrected_df.to_excel('~/Documentos/cuartaprueba(midiendo)/test1.5_corrected.xlsx', index=False)

#CREACION DE DATASET de datos brutos SOLO CON ROTACION Y CORREGIDA y X Y Z CON GAPS################################################################################################

# Cargar el dataset y solo seleccionar la columna 'V'
df = pd.read_excel('~/Documentos/cuartaprueba(midiendo)/test1.6.xlsx', usecols="V:AA", skiprows=7)

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
#corrected_df.to_excel('~/Documentos/cuartaprueba(midiendo)/test2.2_brutos.xlsx', index=False)