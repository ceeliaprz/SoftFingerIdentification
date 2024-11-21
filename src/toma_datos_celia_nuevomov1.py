
import math
import numpy as np
import pandas as pd
import time
import json as js
import os

from model.system_motors import SystemMotors
from datetime import datetime  # Importa la función datetime

# My function to calculate the inverse kinematics of the Finger
def FingerInverseKinematics(incl, orien):
    #Medidas en m
    a = 0.013 #‘a' es la longitud del centro del triángulo al cables y en este caso ‘a' y ‘b' son iguales
    Lo = 0.098 # Longitud dedo en reposo
    radio = 0.008 #Radio de la polea donde se enrrolla el cable 

    # ángulos en radianes
    theta=incl*math.pi/180 
    psi=orien*math.pi/180 

    # Vector que guardará las variaciones
    v_lengths = np.zeros(2)

    if (theta!=0):
        R=Lo/theta

        phi8= (math.pi/2)-psi 
        phi7= (7*math.pi/6)-psi 

        v_lengths[0]= theta * a * math.cos(phi8) 
        v_lengths[1]= theta * a * math.cos(phi7)
        

    else:
        v_lengths[0]=0
        v_lengths[1]=0

    # Angulos en radianes de los motores
    posan8 = v_lengths[0]/radio #motor8
    posan7 = v_lengths[1]/radio #motor7

    return posan8, posan7


def main():
    # Motors
    id_fingers=[7,8]
    motors = SystemMotors(2)  # instantiate SystemMotors class >> number of motors
    motors.loadMotors(id_fingers, "SoftGripperMotorConfig.json")  # motor's ids
    motors.startMotors()  # start motors
    
    # Parameters of the DataFrame
    # Initial positions
    orientation = 0
    inclination = 0
    motors.setPositions([0,0])
    print("Vamos a cero")
    time.sleep(3)

    # Parameters of the DataFrame
    cols = ['time','inclination_ref', 'orientation_ref','pitch_ref_rad', 'yaw_ref_rad','pitch_ref_deg','yaw_ref_deg','M7', 'M8']
    data = []
    motors.setupPositionsMode(5, 5)  # setting velocity and acceleration values

    # Inclination's repetition
    for inclination in range(7, 28, 5): #grados
        
        # Orientation's repetition
        for orientation in range(98, 209, 10): #grados
            # InverseKinematics 
            posan8, posan7 = FingerInverseKinematics(inclination, orientation)
            
            #ESTÁN AL REVES?-->ESTABAN BIEN, CAMBIAR ORDEN DE CASI TODOS(de la carpeta tercera prueba), he quitado - en pitch
            pitch = (inclination*math.pi/180) * math.sin(orientation*math.pi/180) #radianes
            yaw = (-inclination*math.pi/180) * math.cos(orientation*math.pi/180) #radianes
            pitch_deg = pitch * 180 / math.pi  # grados
            yaw_deg = yaw * 180 / math.pi # grados

            motors.setPositions([posan7, -posan8])  # setting the positions of the motors

            # Knowing the Inclination and Orientation of the sensor, with a previous motor position
            for i in np.arange(0, 2, 0.01):  # time sampling >> steps of 0.01

                #Adding the current time until microseconds
                current_time = datetime.now().strftime("%M:%S.%f")
                # Adding the values of incli, orient and encoders in "data"
                data.append([current_time, inclination, orientation, pitch, yaw, pitch_deg, yaw_deg, motors.motorsArray[0].getPosition(), 
                             motors.motorsArray[1].getPosition()])

        # Regresar a la posición inicial
        motors.setPositions([0, 0])
        for i in np.arange(0, 2, 0.01):  # time sampling >> steps of 0.01
                
                #Adding the current time until microseconds (minutos:segundos.microsegundos)
                current_time = datetime.now().strftime("%M:%S.%f")
                # Adding the values of incli, orient and encoders in "data"
                data.append([current_time, 0, 0, 0, 0, 0, 0, motors.motorsArray[0].getPosition(
                ), motors.motorsArray[1].getPosition()])

        # adding the data values (array type), to the data frame
        df = pd.DataFrame(data, columns=cols)
        # print(df)
        df.to_csv(
            '/home/celia/Documentos/ROB. BLANDA/SOFIA_Python/data/Data_prueba_celia/nuevomov/mov1.1.csv', index=False)
        df.info()

    print("Data Ready")
    motors.setPositions([0,0])
    time.sleep(3)

if __name__ == "__main__":
    main()