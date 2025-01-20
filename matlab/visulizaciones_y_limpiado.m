%% VISUALIZATION OF DATA
% ML
data1 = readmatrix("validationdata/transformadas/model1elu_brutos_trans_encoder_dedos_ajust.xlsx");
data2 = readmatrix("validationdata/encoder/data_model1elu_ENCODER.xlsx");

% cinematica inversa
data3 = readmatrix("traindata/test1.5_brutos_transformada_encoder_dedos_ajust.xlsx");
data4 = readmatrix("traindata/data_test1_ENCODER.xlsx");

figure;

subplot(2,1,1); %para ML
hold on;
plot(data1(:,1), 'DisplayName', 'Rot X- yaw ');
plot(data1(:,3), 'DisplayName', 'Rot Z- pitch');
plot(data2(:,5), 'DisplayName', 'pitch grados');
plot(data2(:,6), 'DisplayName', 'yaw grados');
xlabel('Units');
ylabel('degrees ');
title('comparation ref and real (ML)');
legend;

subplot(2,1,2); %para c.inversa
hold on;
plot(data3(:,1), 'DisplayName', 'Rot X- yaw ');
plot(data3(:,3), 'DisplayName', 'Rot Z- pitch');
plot(data4(:,5), 'DisplayName', 'pitch grados');
plot(data4(:,6), 'DisplayName', 'yaw grados');
xlabel('Units');
ylabel('degrees ');
title('comparation ref and real (c.inversa)');
legend;

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
% % Lee el archivo original como una tabla para conservar los nombres de las columnas
% data = readmatrix("testdata/TESTNUEVOMOV2.1_ALINEADOS_quitandoultimo_LIMPIO.xlsx");
% 
% % Extraer datos relevantes
% time = data(:,1);
% rotation_x = data(:,10);  % Amarillo X
% rotation_z = data(:,12);  % Morado Z
% 
% % --- Etapa 1: Visualización de los datos originales ---
% figure;
% hold on;
% plot(data(:,1), data(:,8:9), 'DisplayName', 'Motor Encoder Data in radians');
% plot(data(:,1), data(:,[10,12]), 'DisplayName', 'Interpolated Mocap Data Rotations in degrees');
% xlabel('Time');
% ylabel('Data motors (radians) and rotations (degrees)');
% title('Encoder motors values and real rotations X y Z with noise');
% legend;
% grid on;
% hold off;

% % Define el rango donde quieres aplicar el filtro de mediana (limpieza de picos)
% test2.0
% ranges_x = {2179:2253, 3396:3450, 12975:12992};  % Rangos
% umbral_superior_x = [0.87, 1.711, 15.3669];         % Umbrales superiores para cada rango
% umbral_inferior_x = [0.2, 0.296, 15.2372];       % Umbrales inferiores para cada rango
% ranges_z = {9401:9449, 10587:10650};  % Rangos
% umbral_superior_z = [2.566, 0.1980];         % Umbrales superiores para cada rango
% umbral_inferior_z = [0.1209, -1.097];       % Umbrales inferiores para cada rango
% test nuevomov1.1
% ranges_x = {122/0.01:122.333/0.01};  % Rangos
% umbral_superior_x = [17.21];         % Umbrales superiores para cada rango
% umbral_inferior_x = [16.7];       % Umbrales inferiores para cada rango
% test nuevomov2.1
% ranges_x = {225:247, 609:646, 1000:1032};  % Rangos
% umbral_superior_x = [1.085, 1.189, 2.722];         % Umbrales superiores para cada rango
% umbral_inferior_x = [0.45, 0.63, 2.12];       % Umbrales inferiores para cada rango
% ranges_z = {2808:2826, 3191:3217, 3394:3426};  % Rangos
% umbral_superior_z = [3.1, 0.209,-0.569];         % Umbrales superiores para cada rango
% umbral_inferior_z = [2.79, -0.53,-1.176];
% % % Copiar las señales originales para editar solo la sección deseada
% rotation_x_cleaned = rotation_x;
% rotation_z_cleaned = rotation_z;
% 
% % Iterar sobre los rangos y aplicar la limpieza a la rotación X
% for i = 1:length(ranges_x)
%     range = ranges_x{i};
%     upper_threshold_x = umbral_superior_x(i);
%     lower_threshold_x = umbral_inferior_x(i);
% 
%     % Limpieza en el rango actual de rotación X
%     section_x = rotation_x_cleaned(range);
%     section_x(section_x > upper_threshold_x | section_x < lower_threshold_x) = NaN;
%     rotation_x_cleaned(range) = fillmissing(section_x, 'movmedian', 30);
% end
% 
% % Iterar sobre los rangos y aplicar la limpieza a la rotación Z
% for i = 1:length(ranges_z)
%     range = ranges_z{i};
%     upper_threshold_z = umbral_superior_z(i);
%     lower_threshold_z = umbral_inferior_z(i);
% 
%     % Limpieza en el rango actual de rotación Z
%     section_z = rotation_z_cleaned(range);
%     section_z(section_z > upper_threshold_z | section_z < lower_threshold_z) = NaN;
%     rotation_z_cleaned(range) = fillmissing(section_z, 'movmedian', 30);
% end
% 
% % --- Etapa 2: Visualización después de limpiar los picos ---
% figure;
% hold on;
% plot(time, rotation_x_cleaned, 'r', 'DisplayName', 'Without Peaks X');
% plot(time, rotation_z_cleaned, 'b', 'DisplayName', 'Without Peaks Z');
% xlabel('Time');
% ylabel('Rotaciones (Grados)');
% title('Despues de eliminar picos');
% legend;
% grid on;
% hold off;
% 
% % Aplicar filtro Savitzky-Golay después de limpiar los picos
% window_size = 19; % Tamaño de ventana (debe ser impar)
% polynomial_order = 3; % Orden del polinomio
% 
% rotation_x_smooth = sgolayfilt(rotation_x_cleaned, polynomial_order, window_size);
% rotation_z_smooth = sgolayfilt(rotation_z_cleaned, polynomial_order, window_size);
% 
% % --- Etapa 3: Visualización después del suavizado ---
% figure;
% hold on;
% plot(time, rotation_x_smooth, 'g', 'DisplayName', 'Cleaned X');
% plot(time, rotation_z_smooth, 'c', 'DisplayName', 'Cleaned Z');
% plot(data(:,1), data(:,8:9), 'DisplayName', 'Motor Encoder Data in radians');
% xlabel('Time');
% ylabel('Rotations (Degrees)');
% title('Cleaned Data');
% legend;
% grid on;
% hold off;
% 
% % Reemplazar las columnas de rotación X y Z con las limpias
% data(:,10) = rotation_x_smooth;  % Reemplaza la columna de rotación X
% data(:,12) = rotation_z_smooth;  % Reemplaza la columna de rotación Z
% 
% column_names = [{'Time'}, {'Inclination_deg'},{'Orientation_deg'},{'Pitch_rad'},{'Yaw_rad'},{'Pitch_deg'},{'Yaw_deg'},{'Motor7_rad'},{'Motor8_rad'},{'RotationX_deg'},{'RotationY_deg'},{'RotationZ_deg'},{'PositionX_cm'},{'PositionY_cm'},{'PositionZ_cm'}];
% 
% % Convertir a tabla para facilitar la escritura en Excel
% data_table = array2table(data, 'VariableNames', column_names);
% writetable(data_table, 'testdata/TESTNUEVOMOV2.1_ALINEADOS_quitandoultimo_LIMPIO.xlsx'); % Guarda los datos en un archivo Excel


% FILTRO MEDIANA MOVIL PARA PICO
% data_section_x = rotation_x_smooth(startIdx:endIdx);
% data_section_z = rotation_z_smooth(startIdx:endIdx);
% % Aplica el filtro de mediana móvil a esa sección
% windowSize = 30;  % Tamaño de la ventana del filtro de mediana
% data_section_x_filtered = movmean(data_section_x, windowSize);
% data_section_z_filtered = movmean(data_section_z, windowSize);
% 
% % Reemplaza la sección original con la sección filtrada
% rotation_x_smooth(startIdx:endIdx) = data_section_x_filtered;
% rotation_z_smooth(startIdx:endIdx) = data_section_z_filtered;
% 
% % Visualizar resultados después del filtrado
% figure;
% hold on;
% plot(time, rotation_x_smooth, 'r', 'DisplayName', 'Rotación X Filtrada (Amarillo)');
% plot(time, rotation_z_smooth, 'b', 'DisplayName', 'Rotación Z Filtrada (Morado)');
% legend;
% xlabel('Tiempo');
% ylabel('Rotaciones (grados)');
% title('Datos Suavizados y Filtrados con Mediana Móvil');
% grid on;
% hold off;

%% VISUALIZATION OF DATA TO LOAD IN THE NEURONAL NETWORK OR ML MODEL
% data = readmatrix("testdata/TESTNUEVOMOV2.1_ALINEADOS.xlsx");
% 
% figure;
% hold on;
% plot(data(:,1), data(:,8:9), 'DisplayName', 'Motor Encoder Data in radians');
% plot(data(:,1), data(:,[10,12]), 'DisplayName', 'Interpolated Mocap Data Rotations in degrees');
% xlabel('Time');
% ylabel('Data motors (radians) and rotations (degrees)');
% title('Encoder motors values and real rotations X y Z');
% legend;
% grid on;
% hold off;
% % % Añadir líneas de referencia
% % for i = 2:length(encoder_refs)
% %     xline(encoder_refs(i,1), '--', ['Reference Time ' num2str(encoder_refs(i,1))]);
% % end
