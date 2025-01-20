function [mocap_time,mocap_data_resampled,encoder_time,encoder_data_resampled] =test(mocap_data,offset_time,encoder_data)
% % PARA IR ALINEANDO DOS COLUMNAS POCO A POCO
% %Separamos datos del mocap
% position_mocap=mocap_data(:,4);%columna 4 rotacion Z, columna 2 rotacion X
% time_mocap=mocap_data(:,1);
% 
% %Igualar tiempos
% t_test=time_mocap;
% iniVal = find(t_test<offset_time);%Encuentro en el tiempo del mocap, el valor justo por debajo del offset
% t_ini=t_test(1:length(iniVal));
% t_test=t_test(length(iniVal):length(t_test));
% t_test=t_test-t_ini(length(t_ini));%t_test sale de quitar a t_test el numero de filas de t_ini
% 
% r_test=position_mocap(length(iniVal):length(position_mocap),:);%son los valores de positino mocap quitando las filas de t_ini
% 
% time_enc=encoder_data(:,1); %Cogemos el tiempo del encoder
% % iniVal = find(time_mech<offset_time);
% % t_ini=time_mech(1:length(iniVal));
% % time_mech=time_mech(length(iniVal):length(time_mech));
% % time_mech=time_mech-t_ini(length(t_ini));
% motor=encoder_data(:,9); % 8 MOTOR7/ 9 MOTOR8
% 
% % times 2 colum poco a poco
% ts1=timeseries(r_test,t_test); %Mocap
% ts1out = resample(ts1,0:0.01:t_test(length(t_test))); %resampleamos el mocap a la frecuencia del encoder
% ts1out.Data = fillmissing(ts1out.Data,'next');
% mocap_time = ts1out.Time;
% mocap_data_resampled=deg2rad(ts1out.Data);% Los grados del mocap a radianes para ver mejor la grafica
% 
% ts3=timeseries(motor,time_enc); %Encoder
% ts3out = resample(ts3,0:0.01:time_enc(length(time_enc))); 
% ts3out.Data = fillmissing(ts3out.Data,'next');
% encoder_time=ts3out.Time;
% encoder_data_resampled=ts3out.Data;

% **************************************************************************************************************************************
% DESCOMENTAR LOS SIGUIENTE CUANDO YA SE VAYA A GUARDAR EN UN DATASET TODAS LAS COLUMNAS ALINEADAS, NO SE APLICARÁ EL CAMBIO DE GRADOS A RADIANES.
% %Separamos datos del mocap
position_mocap=mocap_data(:,2:7);%de la 2 a la 7 son las columnas de datos rotacion y posicion que queremos alinear
time_mocap=mocap_data(:,1);

%Igualar tiempos
t_test=time_mocap;
iniVal = find(t_test<offset_time);%Encuentro en el tiempo del mocap, el valor justo por debajo del offset
t_ini=t_test(1:length(iniVal));
t_test=t_test(length(iniVal):length(t_test));
t_test=t_test-t_ini(length(t_ini));

r_test=position_mocap(length(iniVal):length(position_mocap),:);

time_enc=encoder_data(:,1); %Cogemos el tiempo del encoder
% iniVal = find(time_mech<offset_time);
% t_ini=time_mech(1:length(iniVal));
% time_mech=time_mech(length(iniVal):length(time_mech));
% time_mech=time_mech-t_ini(length(t_ini));
motor=encoder_data(:,2:9); %cogemos todas las columnas del encoder
% times TODAS COLUMNAS  
encoder_data_resampled = zeros(length(time_enc), size(motor, 2));
for i = 1:size(motor,2)
        % Procesar cada columna de datos del encoder
        ts3 = timeseries(motor(:,i), time_enc); % Encoder
        ts3out = resample(ts3, 0:0.01:time_enc(length(time_enc))); 
        ts3out.Data = fillmissing(ts3out.Data, 'next');

        % Guardar los datos alineados en la matriz de resultados
        encoder_data_resampled(:, i) = ts3out.Data;
end
encoder_time=ts3out.Time;

 % Resample mocap data previo para ver longitud que va a quedar para crear
 % matriz 
ts1 = timeseries(r_test(:, 1), t_test); % Mocap
ts1out = resample(ts1, 0:0.01:t_test(length(t_test))); % Resampleamos el mocap a la frecuencia del encoder
ts1out.Data = fillmissing(ts1out.Data, 'next');
mocap_time = ts1out.Time; % Usamos la longitud de esta serie temporal para inicializar la matriz de resultados

 % Inicializamos mocap_data_aligned
 mocap_data_resampled = zeros(length(mocap_time), size(position_mocap, 2));%ponemos el 2 para obtener num de columnas de positio_mocap
 for i = 1:size(position_mocap,2)
        % Procesar cada columna de datos del mocap
        ts1 = timeseries(r_test(:, i), t_test); % Mocap
        ts1out = resample(ts1, 0:0.01:t_test(length(t_test))); % Resampleamos el mocap a la frecuencia del encoder
        ts1out.Data = fillmissing(ts1out.Data, 'next');

        % Guardar los datos alineados en la matriz de resultados
        mocap_data_resampled(:, i) = ts1out.Data;
 end
% PASAR A RADIANES A LA HORA DE ESTAR ALINEANDO PARA VER MEJOR PERO LUEGO
% GUARDAR LOS DATOS EN GRADOS
%mocap_data_resampled = deg2rad(mocap_data_resampled); % Los grados del mocap a radianes para ver mejor la gráfica


%% plot GF Deltas

figure
hold on

for i=1:size(encoder_data_resampled,2)
    plot(encoder_time, encoder_data_resampled(:,i), 'DisplayName', ['Encoder Data' num2str(i)]) % Agregar leyenda al primer plot
end

for i=1:size(mocap_data_resampled,2)
    plot(mocap_time, mocap_data_resampled(:,i), 'DisplayName', ['Mocap Data' num2str(i)]) % Agregar leyenda al segundo plot
end 

% Agregar leyenda al gráfico
legend('show')

% Títulos y etiquetas de los ejes (opcional, para mayor claridad)
title('Sin alinear pero quitando tiempo inicial')
xlabel('Time')
ylabel('Data')

% Mostrar la figura
hold off

end