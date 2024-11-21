%% VISUALIZATION OF THE BESTS DATASET TO ALIGN IN MAIN (para elegir cual cojo para alinear)
% data1 = readmatrix("test2.0_brutos_transformada_encoder_dedos_ajust.xlsx");
% data2 = readmatrix("test2.1_brutos_transformada_encoder_dedos_ajust.xlsx");
% data3 =readmatrix("test2.2_brutos_transformada_encoder_dedos_ajust.xlsx");
% 
% figure;
% hold on;
% plot(data1(:,3), 'DisplayName', 'Rotation z test2.0');
% plot(data2(:,3), 'DisplayName', 'Rotation z test2.1');
% plot(data3(:,3), 'DisplayName', 'Rotation z test2.2');
% 
% xlabel('Units');
% ylabel('diferents Rotation X ');
% title('comparation of the different tests');
% legend;

%% COMPARACION DE MOVIMIENTO ENCODERS
% grid on;
% hold off;
% data1 = readmatrix("testdata/data_nuevomov1_ENCODER.xlsx");
% data2 = readmatrix("testdata/data_nuevomov1.1_ENCODER.xlsx");
% 
% figure;
% hold on;
% plot(data1(:,8), 'DisplayName', 'encodermov1');
% plot(data2(:,8), 'DisplayName', 'encodermov1.1');
% 
% xlabel('Units');
% ylabel('diferents Rotation X ');
% title('comparation of the different tests');
% legend;
% grid on;
% hold off;

%% LIMPIADO
% Suponiendo que tus datos están en el vector `data`
% Lee el archivo original como una tabla para conservar los nombres de las columnas
% data = readtable("testdata/data_nuevomov1.1_ENCODER.xlsx");
% 
% % Define el rango donde quieres aplicar el filtro de mediana
% startIdx = 12636;  % Índice aproximado de inicio de la zona con ruido
% endIdx = 12810;  % Índice de fin de la zona con ruido
% 
% % Extrae la sección ruidosa de la columna 8
% data_section = data{startIdx:endIdx, 8};  % Usamos llaves {} para acceder a los datos numéricos
% 
% % Aplica el filtro de mediana móvil a esa sección
% windowSize = 25;  % Tamaño de la ventana del filtro de mediana
% data_section_filtered = movmean(data_section, windowSize);
% 
% % Reemplaza la sección original con la sección filtrada
% data_filtered = data;  % Copia la tabla original
% data_filtered{startIdx:endIdx, 8} = data_section_filtered;  % Sustituye solo en la columna 8
% 
% % Grafica los datos antes y después del filtrado
% figure;
% plot(data{:,8}, 'b', 'DisplayName', 'Datos Originales'); hold on;  % Acceder a la columna 8 de data
% plot(data_filtered{:,8}, 'r', 'DisplayName', 'Datos Filtrados');  % Acceder a la columna 8 de data_filtered
% legend;
% title('Aplicación de Filtro de Mediana Móvil en Zona Ruidosa');
% xlabel('Índice');
% ylabel('Valor');
% grid on;
% 
% % Guarda el nuevo dataset en un archivo Excel con los nombres de las columnas originales
% writetable(data_filtered, 'testdata/data_nuevomov1.1_ENCODER_filtered.xlsx', 'WriteRowNames', true);

%% VISUALIZATION OF DATA TO LOAD IN THE NEURONAL NETWORK OR ML MODEL
data = readmatrix("testdata/TESTNUEVOMOV2.1_ALINEADOS.xlsx");

figure;
hold on;
plot(data(:,1), data(:,8:9), 'DisplayName', 'Motor Encoder Data in radians');
plot(data(:,1), data(:,[10,12]), 'DisplayName', 'Interpolated Mocap Data Rotations in degrees');
xlabel('Time');
ylabel('Data motors (radians) and rotations (degrees)');
title('Encoder motors values and real rotations X y Z');
legend;
grid on;
hold off;
% % Añadir líneas de referencia
% for i = 2:length(encoder_refs)
%     xline(encoder_refs(i,1), '--', ['Reference Time ' num2str(encoder_refs(i,1))]);
% end
