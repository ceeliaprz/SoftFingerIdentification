datamocap = readmatrix("test1.5_brutos_transformada_encoder_dedos_ajust.xlsx");%INCLUIR EL TIEMPO
dataencoder = readmatrix("data_test1_ENCODER.xlsx");

mocap_data = [datamocap(:,7) datamocap(:,1:6)]; %primero tiempo, luego columnas XYZ
encoder_data = dataencoder; % Todas las columnas de encoder data

%encoder_data = [dataencoder(:,7)]; % guardamos los datos encoder del motor 7
% vector = data(:,4);
% encoder_data = vector(~isnan(vector));
% Leer el archivo CSV y almacenarlo en una tabla
% tablaDatosencoder = readtable("data_test1.5midiendo.csv");
% encoder_data = table2array([tablaDatosencoder(:,8)]);

long = length(encoder_data(:,1));
encoder_time = (0:0.01:(long-1)*0.01)';%creamos columna tiempo que vaya de saltos de 0.01 
encoder_data = [encoder_time encoder_data];%primero tiempo luego columnas datos

offset_time = 10.37;%modificar segun veamos en la grafica para que empiecen a la vez
[mocap_time,mocap_data,encoder_time,encoder_data]=test(mocap_data,offset_time,encoder_data);% los tiempos del ecoder y mocap son los mismos al estar resampleados a 0.01
%% 
% Definir los puntos de referencia
encoder_refs = [0,0; 26.4, 0.00548;  28.31,-0.1416;34.4,-0.0012943;38.04,0.04967; 54.04,0.283456; 64.32,0.07086;70.04,0.2136 ;82.03,0.42543; 100.28,0.434617;110.04,0.567125; 114.35,-0.242768;120.35,0.1183;128.34,0.540078]; % Tiempo y valor en el encoder
mocap_refs = [0,0; 23.06, -0.0280631; 25.8,0.001324 ;30.95,0.0911425;34.2,0.07485; 47.5, -0.05; 57.78,0.11435;62, 0.053735;73.2,-0.07268; 89,-0.014327; 97.8,-0.0999;101.5,0.290713 ;106.3,0.2;114,-0.0109125] % Tiempo y valor en el mocap

% Calcular los desfases locales restando tiempo encoder-mocap
desfases = encoder_refs(:,1) - mocap_refs(:,1);

% Crear una función de desfase que varíe con el tiempo usando interpolación
%Para ajustar los tiempos del mocap a lo largo de todo el conjunto de datos, 
%interpolamos los desfases calculados en los puntos de referencia. 
% Esto permite obtener un desfase continuo para cualquier tiempo en los datos del mocap.
times = [encoder_refs(:,1)']; % Tiempos de los puntos de referencia del encoder
desfases_interp = interp1(times, desfases, mocap_time, 'linear', 'extrap');%ajustamos el mocap time según los desfases a los puntos ref

% Ajustar los tiempos del mocap con los desfases interpolados
mocap_time_ajustado = mocap_time + desfases_interp;

% Interpolación de mocap a tiempos del encoder para alinearlos
% encontrar los valores del mocap correspondientes a los tiempos del encoder.
mocap_data_interp = interp1(mocap_time_ajustado, mocap_data, encoder_time, 'linear');

% Plotear los datos ajustados
figure;
hold on;
plot(encoder_time, encoder_data, 'DisplayName', 'Encoder Data');
plot(encoder_time, mocap_data_interp, 'DisplayName', 'Interpolated Mocap Data');
xlabel('Time');
ylabel('Data');
title('Alineados con Desfase Variable');
legend;
grid on;
hold off;
% Añadir líneas de referencia
for i = 2:length(encoder_refs)
    xline(encoder_refs(i,1), '--', ['Reference Time ' num2str(encoder_refs(i,1))]);
end