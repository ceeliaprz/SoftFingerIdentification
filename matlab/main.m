datamocap = readmatrix("testdata/nuevomov2.1_celia_brutos_trans_encoder_dedos_ajust.xlsx");%INCLUIR EL TIEMPO
dataencoder = readmatrix("testdata/data_nuevomov2.1_ENCODER.xlsx"); 

mocap_data = [datamocap(:,7) datamocap(:,1:6)]; %primero tiempo, luego columnas XYZ
encoder_data = dataencoder(:,1:8); % Todas las columnas de encoder data

%encoder_data = [dataencoder(:,7)]; % guardamos los datos encoder del motor 7
% vector = data(:,4);
% encoder_data = vector(~isnan(vector));
% Leer el archivo CSV y almacenarlo en una tabla
% tablaDatosencoder = readtable("data_test1.5midiendo.csv");
% encoder_data = table2array([tablaDatosencoder(:,8)]);

long = length(encoder_data(:,1));
encoder_time = (0:0.01:(long-1)*0.01)';%creamos columna tiempo que vaya de saltos de 0.01 
encoder_data = [encoder_time encoder_data];%primero tiempo luego columnas datos

offset_time = 17.75;%modificar segun veamos en la grafica para que empiecen a la vez
[mocap_time,mocap_data,encoder_time,encoder_data]=test(mocap_data,offset_time,encoder_data);% los tiempos del ecoder y mocap son los mismos al estar resampleados a 0.01
%% 
% Definir los puntos de referencia
%ALARGAR BAJO TIEMPO
%ACORTAR AUMENTO TIEMPO
%TEST 1.5
% encoder_refs = [0,0; 26.4, 0.00548;  28.31,-0.1416;34.4,-0.0012943;38.04,0.04967; 54.04,0.283456; 64.32,0.07086;70.04,0.2136 ;82.03,0.42543; 100.28,0.434617;110.04,0.567125; 114.35,-0.242768;120.35,0.1183;128.34,0.540078]; % Tiempo y valor en el encoder
% mocap_refs = [0,0; 23.06, -0.0280631; 25.8,0.001324 ;30.95,0.0911425;34.2,0.07485; 47.5, -0.05; 57.78,0.11435;62, 0.053735;73.2,-0.07268; 89,-0.014327; 97.8,-0.0999;101.5,0.290713 ;106.3,0.2;114,-0.0109125] % Tiempo y valor en el mocap

%TEST2.0
% encoder_refs = [0,0;2,-0.071415;6.02,-0.2128;10.56,0;14.04,-0.04864;16.04,-0.09710;20,-0.19397;22.49,0;26.13,-0.04929;28.04,-0.049;30.15,-0.0982174;34.03,-0.12299;40.01,-0.2458;42.02,-0.36934;46.78,-0.001512;50,-0.108;58.02,-0.5412;68.01,-0.364965;74,-0.07099;82.02,-0.35366;86,-0.048517;92.05,0.364949;94.67,0.004378;102.35,0.431389;106.77,0.00428;124.04,0.266811;130.09,0.65592;134.05,0.1405;152.04,0.5675]; % Tiempo y valor en el encoder
% mocap_refs = [0,0;2.1,0.04619;5.86,0.1614;9.89,0.02535;13.25,0.04502;14.89,0.09764;18.55,0.22145;20.60,0.0314;24.5,-0.04929;26.0,0.09216;27.5,0.207877;31.4,0.267;36.7,0.08128;38.0,0.12984;43.2,0.0031;46.0,0.02458;53.1,019588;62.2,0.114392;67.5,0.012268;75.33,0.097988;78.6,-0.002153;84.6,0.171632;86.65,0.018929;93.85,0.188179;97.6,0.0268;113.3,0.0968869;119.0,0.2743;122.5,0.045883;139.0,0.21978]; % Tiempo y valor en el mocap

%NUEVOMOV1.1
% encoder_refs = [0,0; 4.01,-0.18879;6.02,-0.1749;8.02,-0.155987;10.01,-0.1328;12.01,-0.105;22.16,0.093;24.01,0.09315;26.01,0;28.01,-0.337;30.01,-0.3236;34.01,-0.268;36.01,-0.2277;38.01,-0.18;40.01,-0.127;42,-0.07077;44.01,-0.0118;46.01,0.047;48.01,0.1053;52,0;56.03,-0.458;60.01,-0.3799;76.02,0.225;82.02,-0.5929;86.01,-0.4916;102,0.2929;107.93,-0.72827;112.03,-0.6011;116.01,-0.4057;128.09,0.3579]; % Tiempo y valor en el encoder
% mocap_refs = [0,0; 4.29,0.00181;6.13,0.0095;8.06,0.01721;9.75,0.0329;11.56,0.0428;21.06,0.0615;22.9,0.0584;25.14,0.0138;28.19,0.0036;30.17,0.00737;33.9,0.042;36.99,0.058;39.1,0.0838;41.29,0.0948;43.1,0.109;46.1,0.11;48.3,0.1143;50.7,0.115;55.6,0.0158;61.4,0.0116;66.9,0.0637;81.8,0.1816;87.5,0.0181;93,0.08468;107.9,0.244;113.4,0.0239;118.7,0.10975;122.6,0.21124;134,0.3052]; % Tiempo y valor en el mocap

%NUEVOMOV2.1
encoder_refs = [0,0; 2.03,-0.649561;4.01,-0.00234;6.02,-0.63;8.28,-0.59;10.02,-0.59;10.74,0;12.37,-0.53;14.02,-0.534;14.57,0;16.01,0;18.01,-0.46;18.64,0;20.45,-0.37;22,-0.374;22.42,0;24.01,0;24.32,-0.27;25.99,-0.37;28.22,-0.168;30,-0.16877;30.2,0;32.13,-0.0556;34.24,0;36.15,00569;40.21,0.1689;42.01,0.1687;44,0;44.26,0.2757;46.01,0.275;47.99,0;55,0;65,0]; % Tiempo y valor en el encoder
mocap_refs = [0,0; 2.8,0.328;4.87,0.00311;7,0.3196;11.2,0.2976;12.8,0.29;13.72,0.02;15.8,0.264;17.93,0.2624;18.2,0.0184;19.8,0.00259;22.3,0.213;22.99,0.0163;25.02,0.1633;27.0,0.1611;27.58,0.01;29.7,0;30.0,0.1137;31.5,0.111;34.7,0.234;37.2,-0.014;36.72,0.0482;39.5,0.252446;42.5,-0.0106;46.1,0.25612;51.92,0.253;54.4,0.25;57.98,0.0177;58.2,0.26;60.45,-0.125;63.4,0.0234;71.7,0;83.59,0]; % Tiempo y valor en el mocap

% Calcular los desfases locales restando tiempo encoder-mocap
desfases = encoder_refs(:,1) - mocap_refs(:,1);

% Crear una función de desfase que varíe con el tiempo usando interpolación
% Para ajustar los tiempos del mocap a lo largo de todo el conjunto de datos, 
% interpolamos los desfases calculados en los puntos de referencia. 
% Esto permite obtener un desfase continuo para cualquier tiempo en los datos del mocap.
times = [encoder_refs(:,1)']; % Tiempos de los puntos de referencia del encoder
desfases_interp = interp1(times, desfases, mocap_time, 'linear', 'extrap');%ajustamos el mocap time según los desfases a los puntos ref

% Ajustar los tiempos del mocap con los desfases interpolados
mocap_time_ajustado = mocap_time + desfases_interp;

% Interpolación de mocap a tiempos del encoder para alinearlos
% encontrar los valores del mocap correspondientes a los tiempos del encoder.
mocap_data_interp = interp1(mocap_time_ajustado, mocap_data, encoder_time, 'linear');

%PARA QUITAR ULTIMAS FILAS QUE NO ESTABAN BIEN ALINEADAS DEL MOVIMIENTO DE
%TEST2.1
% % % mocap_data_interp2 = mocap_data_interp(1:43.66/0.01, :);
% % % encoder_data2 = encoder_data(1:43.66/0.01,:);
% % % encoder_time2 = encoder_time(1:43.66/0.01,:);

% Plotear TODO alineado

encoder_labels = {'inclination deg', 'orientation deg', 'pitch ref rad', 'yaw ref rad', 'pitch ref deg', 'yaw ref deg', 'Motor 7', 'Motor 8'};
mocap_labels = {'mocap rotation X', 'mocap rotation Y', 'mocap rotation Z', 'mocap position X', 'mocap position Y', 'mocap position Z'};

 figure;
 hold on;
%Estos bucles de plot para asignar las labes a cada una de las columnas
%cuando ploteo todas al final
%Plot para Encoder Data (una serie por cada columna de encoder)
for i = 1:size(encoder_data, 2)
    plot(encoder_time, encoder_data(:, i), 'DisplayName', encoder_labels{i});
end

% Plot para los datos de Mocap interpolados (una serie por cada columna)
for i = 1:size(mocap_data_interp, 2)
    plot(encoder_time, mocap_data_interp(:, i), 'DisplayName', mocap_labels{i});
end

% %estos plots son para cuando voy alineando 2 columnas
% plot(encoder_time, encoder_data, 'DisplayName', 'columna 1 y 2 y 3 y 4encoder');
% plot(encoder_time, mocap_data_interp, 'DisplayName', 'Interpolated Mocap Data');
% xlabel('Time');
% ylabel('Data');
% title('TODAS COLUMNAS ALINEADAS');
% legend;
% grid on;
% hold off;
% % Añadir líneas de referencia
% for i = 2:length(encoder_refs)
%     xline(encoder_refs(i,1), '--', ['Reference Time ' num2str(encoder_refs(i,1))]);
% end

% Plotear solo la referencia pitch teorica EN GRADOS con la rotacion Z (pitch real GRADOS) y
% la yaw teorica GRADOS con la rotacion X GRADOS
% se ve lo que tendría que ser y lo que hace el verdadero movimiento del
% dedo
% figure;
% hold on;
% plot(encoder_time, encoder_data(:,5:6), 'DisplayName', 'Encoder Data');
% plot(encoder_time, mocap_data_interp(:,[1,3]), 'DisplayName', 'Interpolated Mocap Data');
% xlabel('Time');
% ylabel('Data');
% title('Pitch ref grados con ROT Z (pitch real GRADOS) y Yaw ref grados con ROT X ');
% legend;
% grid on;
% hold off;
% % Añadir líneas de referencia
% for i = 2:length(encoder_refs)
%     xline(encoder_refs(i,1), '--', ['Reference Time ' num2str(encoder_refs(i,1))]);
% end

% % Guardar los datos alineados con desfase variable en un nuevo archivo Excel
% aligned_data_with_shift = [encoder_time encoder_data mocap_data_interp]; % Combina los datos del encoder y del mocap
% % Definir nombres de las columnas (puedes personalizarlos según tus datos)
% column_names = [{'Time'}, {'Inclination_deg'},{'Orientation_deg'},{'Pitch_rad'},{'Yaw_rad'},{'Pitch_deg'},{'Yaw_deg'},{'Motor7_rad'},{'Motor8_rad'},{'RotationX_deg'},{'RotationY_deg'},{'RotationZ_deg'},{'PositionX_cm'},{'PositionY_cm'},{'PositionZ_cm'}];
% 
% % Convertir a tabla para facilitar la escritura en Excel
% data_table = array2table(aligned_data_with_shift, 'VariableNames', column_names);
% writetable(data_table, 'TESTNUEVOMOV2.1_ALINEADOS_quitandoultimo.xlsx'); % Guarda los datos en un archivo Excel
