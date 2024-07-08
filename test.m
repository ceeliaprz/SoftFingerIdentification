function [mocap_time,mocap_data,encoder_time,encoder_data] =test(mocap_data,offset_time,encoder_data)

%Separamos datos del mocap
position_mocap=mocap_data(:,4);
time_mocap=mocap_data(:,1);

%Igualar tiempos
t_test=time_mocap;
iniVal = find(t_test<offset_time);%Encuentro en el tiempo del mocap, el valor justo por debajo del offset
t_ini=t_test(1:length(iniVal));
t_test=t_test(length(iniVal):length(t_test));
t_test=t_test-t_ini(length(t_ini));

r_test=position_mocap(length(iniVal):length(position_mocap));

time_enc=encoder_data(:,1); %Cogemos el tiempo del encoder
% iniVal = find(time_mech<offset_time);
% t_ini=time_mech(1:length(iniVal));
% time_mech=time_mech(length(iniVal):length(time_mech));
% time_mech=time_mech-t_ini(length(t_ini));
motor=encoder_data(:,8); %8 MOTOR7/ 9 MOTOR8


%% times
ts1=timeseries(r_test,t_test); %Mocap
ts1out = resample(ts1,0:0.01:t_test(length(t_test))); %resampleamos el mocap a la frecuencia del encoder
ts1out.Data = fillmissing(ts1out.Data,'next');
% figure
% plot(ts1out.Time,ts1out.Data,'LineWidth',1,'Color',[0.85,0.33,0.10])
% title('resistance')
% ylabel('\DeltaR/R0')
% xlabel('Time, s')


ts3=timeseries(motor,time_enc); %Encoder
ts3out = resample(ts3,0:0.01:time_enc(length(time_enc))); 
ts3out.Data = fillmissing(ts3out.Data,'next');
% figure
% plot(ts3out.Time,ts3out.Data)
% title('strain')
% xlabel('Time, s')
% ylabel('Strain, abs')


encoder_time=ts3out.Time;
encoder_data=ts3out.Data;

mocap_time=ts1out.Time;
mocap_data=deg2rad(ts1out.Data);% Los grados del mocap a radianes para ver mejor la grafica


%% plot GF Deltas
figure
plot(encoder_time, encoder_data, 'DisplayName', 'Encoder Data') % Agregar leyenda al primer plot
hold on
plot(mocap_time, mocap_data, 'DisplayName', 'Mocap Data') % Agregar leyenda al segundo plot

% Agregar leyenda al gráfico
legend('show')

% Títulos y etiquetas de los ejes (opcional, para mayor claridad)
title('Sin alinear')
xlabel('Time')
ylabel('Data')

% Mostrar la figura
hold off

end